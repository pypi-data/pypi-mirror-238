from .LogicParser import LogicParser
from .elements import *
from .tokenizer import *


# Instead of multiple nested loops, a tree with rotation can
# probably be used with less time complexity.

class RAParser:
    @staticmethod
    def parse_query(query: str) -> RAElement:
        initial_token = Token(query)
        return RAParser.parse_tokens(initial_token)

    @staticmethod
    def parse_tokens(*tokens: Token, target: RAOperator | RAOperand = None) -> RAElement:
        if len(tokens) == 1:
            tokens = tuple(Tokenizer.tokenize(tokens[0]))

        # binary operators
        for operator in RA_BINARY_OPERATORS:
            # iterate tokens and match symbol
            for i in range(1, len(tokens) + 1):
                if tokens[-i].lower() in operator.symbols():
                    # raise error if left or right operand missing
                    if i == 1:
                        raise AssertionError(f'right operand missing after {tokens[-i]}')
                    if i == len(tokens):
                        raise AssertionError(f'left operand missing before {tokens[-i]}')

                    # return the operator
                    # with left part of tokens and right part of tokens
                    return operator(
                        RAParser.parse_tokens(*tokens[:-i]),
                        RAParser.parse_tokens(*tokens[-i + 1:])
                    )

        # unary operators
        for i in range(1, len(tokens) + 1):
            # iterate operators and match token
            for operator in RA_UNARY_OPERATORS:
                if tokens[-i].lower() in operator.symbols():
                    # If no target from a previous step is handed over
                    # the last token is the operators target.
                    if target is None:
                        op = operator(
                            RAParser.parse_tokens(tokens[-1]),
                            LogicParser.parse_tokens(*tokens[-i + 1:-1])
                        )

                    # Otherwise the handed target is this operator's
                    # target.
                    else:
                        op = operator(
                            target,
                            LogicParser.parse_tokens(*tokens[-i + 1:])
                        )

                    # If there are any more tokens the operator is
                    # the target for the next step.
                    if i < len(tokens):
                        return RAParser.parse_tokens(
                            *tokens[:-i],
                            target=op
                        )

                    # Otherwise the operator is the return value.
                    else:
                        return op

        # return as name
        if len(tokens) > 1:
            raise AssertionError(f'{tokens=}')

        return RAOperand(tokens[0])
