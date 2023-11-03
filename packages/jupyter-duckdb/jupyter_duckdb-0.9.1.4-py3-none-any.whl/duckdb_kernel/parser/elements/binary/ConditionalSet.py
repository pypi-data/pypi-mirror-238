import re
from typing import Tuple, Dict, List, Optional

from duckdb_kernel.db import Table
from .And import And
from .Equal import Equal
from ..DCOperand import DCOperand
from ..LogicElement import LogicElement
from ..LogicOperand import LogicOperand
from ..LogicOperator import LogicOperator
from ...tokenizer import Token
from ...util.RenamableColumnList import RenamableColumnList


class ConditionalSet:
    @staticmethod
    def symbols() -> Tuple[str, ...]:
        return '|',

    def __init__(self, projection: LogicOperand, condition: LogicElement):
        self.projection: LogicOperand = projection
        self.condition: LogicElement = condition

    @staticmethod
    def split_tree(le: LogicElement) -> Tuple[Optional[LogicElement], List[DCOperand]]:
        # DCOperands are the relations. They contain either custom attribute names ("AS") or constants.
        if isinstance(le, DCOperand):
            # First we look for constants to replace them with separate "AND" statements.
            for i in range(len(le.names)):
                if not le.names[i].is_constant:
                    continue

                # If a constant was found, we store the value and replace it with a random attribute name.
                constant = le.names[i]
                new_token = Token.random()
                new_operand = DCOperand(le.relation, le.names[:i] + (new_token,) + le.names[i + 1:], skip_comma=True)

                # We now need an equality comparison to ensure the introduced attribute is equal to the constant.
                equality = Equal(
                    LogicOperand(new_token),
                    LogicOperand(constant)
                )

                # The new operand might contain more constants. We make a recursive call to eliminate them too.
                new_le, dc_operands = ConditionalSet.split_tree(new_operand)

                # If the recursive call returns None as the new element, the DCOperand does not contain any more
                # constants, so we just return the equality operation together with the DCOperands.
                if new_le is None:
                    return equality, dc_operands

                # Otherwise we "chain" the current and the subsequent equality check using an "AND".
                else:
                    return And(equality, new_le), dc_operands

            # If no constants were found, return None and le as DCOperand.
            return None, [le]

        # LogicOperators are the usual operators like logical and, logical or, but also mathematical terms.
        if isinstance(le, LogicOperator):
            # First we create an empty list for the DCOperands.
            dc_operands = []

            # We replace the left and right operands using recursive calls. The resulting DCOperands are
            # added to the list we prepared above.
            le.left, d = ConditionalSet.split_tree(le.left)
            dc_operands += d

            le.right, d = ConditionalSet.split_tree(le.right)
            dc_operands += d

            # If the left operand is None, we return the right operand.
            # As we check if the return value is None outside the function,
            # it is fine if the right operand is also None.
            if le.left is None:
                return le.right, dc_operands

            # If the right operand is None, we return the left operand.
            # The left operand can not be None because of the previous if-clause.
            # However, it would not hurt if the left operand was also None.
            elif le.right is None:
                return le.left, dc_operands

            # If none of them is None, we do not need to replace the current LogicElement
            # and therefore return it unchanged.
            else:
                return le, dc_operands

        # LogicOperands stay as they are.
        # if isinstance(le, LogicOperand):
        #     print('LogicOperand:', le)

        # The default case is to return the LogicElement with not DCOperands.
        return le, []

    def to_sql(self, tables: Dict[str, Table]) -> str:
        # find and remove DCOperands from operator tree
        condition, dc_operands = self.split_tree(self.condition)

        # create RenamableColumnList with user defined names
        # and remove underscore references
        underscores = re.compile(r'_{1,}')

        rcls: List[RenamableColumnList] = []
        relations: List[str] = []

        for operand in dc_operands:
            source_columns = tables[operand.relation].columns

            # abort if relations have a different count of attributes
            # TODO useful message
            if len(source_columns) != len(operand.names):
                raise AssertionError(f'invalid number of attributes for relation {operand.relation}')

            # create column list
            rcl: RenamableColumnList = RenamableColumnList.from_iter(source_columns)
            for source, target in zip(source_columns, operand.names):
                rcl.rename(source.name, target)

            # remove underscore references
            i = 0
            while i < len(rcl):
                if underscores.fullmatch(rcl[i].name):
                    del rcl[i]
                else:
                    i += 1

            # store data
            rcls.append(rcl)
            relations.append(operand.relation)

        # construct select statements
        table_statements: List[str] = []

        for i, (relation, rcl) in enumerate(zip(relations, rcls)):
            columns = ', '.join(f'{r.current_name} AS {r.name}' for r in rcl)
            table_statements.append(f'(SELECT {columns} FROM {relation}) t{i}')

        # construct joins and column selection
        join_conditions: List[str] = []

        select_columns: Dict[str, str] = {}
        joined_columns: RenamableColumnList = RenamableColumnList()

        for i in range(len(rcls)):
            for k in range(i + 1, len(rcls)):
                intersection, other = rcls[i].intersect(rcls[k])

                for l, r in intersection:
                    join_conditions.append(f't{i}.{l.name} = t{k}.{r.name}')

                    l.current_name = f't{i}.{l.name}'
                    joined_columns.append(l)

                for o in other:
                    if o.name in self.projection:
                        if o in rcls[i]:
                            select_columns[o.name] = f't{i}.{o.name} AS {o.name}'
                        else:
                            select_columns[o.name] = f't{k}.{o.name} AS {o.name}'

        # return sql
        sql_select = ', '.join(select_columns[col] if col in select_columns else col
                               for col in self.projection)
        sql_tables = ', '.join(table_statements)
        sql_joins = ' AND '.join(join_conditions) if len(join_conditions) > 0 else 1
        sql_condition = condition.to_sql(joined_columns) if condition is not None else 1

        return f'SELECT DISTINCT {sql_select} FROM {sql_tables} WHERE {sql_joins} AND ({sql_condition})'
