from .elements import *
from .tokenizer import *


class LogicParser:
    @staticmethod
    def parse_query(query: str) -> LogicElement:
        initial_token = Token(query)
        return LogicParser.parse_tokens(initial_token)

    @staticmethod
    def parse_tokens(*tokens: Token) -> LogicElement:
        if len(tokens) == 1:
            tokens = tuple(Tokenizer.tokenize(tokens[0]))

        # logic operators
        for operator in LOGIC_BINARY_OPERATORS:
            # iterate tokens and match symbol
            for i in range(1, len(tokens) + 1):
                if tokens[-i].lower() in operator.symbols():
                    # return the operator
                    # with left part of tokens and right part of tokens
                    return operator(
                        LogicParser.parse_tokens(*tokens[:-i]),
                        LogicParser.parse_tokens(*tokens[-i + 1:])
                    )

        # not
        if tokens[0] in LOGIC_NOT.symbols():
            return LOGIC_NOT(
                LogicParser.parse_tokens(*tokens[1:])
            )

        # ArgList
        return LogicOperand(*tokens)
