from uuid import uuid4


class Token(str):
    def __new__(cls, value: str):
        in_quotes = False

        while True:
            # strip whitespaces
            value = value.strip()

            # return if too few characters are left
            if len(value) < 2:
                break

            # remove enclosing brackets
            for cs, ce in (
                    ('(', ')'),
                    ('[', ']'),
                    ('{', '}')
            ):
                if value[0] == cs and value[-1] == ce:
                    value = value[1:-1]
                    break
            else:
                break

        return super().__new__(cls, value)

    @staticmethod
    def random() -> 'Token':
        return Token('__' + str(uuid4()).replace('-', '_'))

    @property
    def empty(self) -> bool:
        return len(self) == 0

    @property
    def is_constant(self) -> bool:
        return ((self[0] == '"' and self[-1] == '"') or
                (self[0] == "'" and self[-1] == "'") or
                self.replace('.', '', 1).isnumeric())

    @property
    def single_quotes(self) -> str:
        # TODO Is this comparison useless because tokens are cleaned automatically?
        # TODO quotes are not automatically removed from now on
        if self[0] != '"' or self[-1] != '"':
            return self
        else:
            return f"'{self[1:-1]}'"

    def __getitem__(self, item) -> 'Token':
        return Token(super().__getitem__(item))
