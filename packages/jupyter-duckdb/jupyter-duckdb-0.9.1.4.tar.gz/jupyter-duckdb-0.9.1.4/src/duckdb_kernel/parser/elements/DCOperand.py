from typing import Tuple

from .LogicOperand import LogicOperand
from ..tokenizer import Token


class DCOperand(LogicOperand):
    def __new__(cls, relation: Token, columns: Tuple[Token], skip_comma: bool = False):
        if not skip_comma and not all(t == ',' for i, t in enumerate(columns) if i % 2 == 1):
            raise AssertionError('arguments must be separated by commas')

        return tuple.__new__(
            cls,
            (relation, *(
                token if not token.endswith(',') else token[:-1]
                for token in columns
                if token != ','
            ))
        )

    @property
    def relation(self) -> Token:
        return self[0]

    @property
    def names(self) -> Tuple[Token]:
        return self[1:]

    def __str__(self) -> str:
        columns = ', '.join(self.names)
        return f'{self.relation}({columns})'
