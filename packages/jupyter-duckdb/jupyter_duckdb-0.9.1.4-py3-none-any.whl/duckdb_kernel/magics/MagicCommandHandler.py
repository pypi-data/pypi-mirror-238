import re
from typing import Dict, Tuple, List

from . import MagicCommand, MagicCommandException, MagicCommandCallback


class MagicCommandHandler:
    def __init__(self):
        self._magics: Dict[str, MagicCommand] = {}

    def add(self, *command: MagicCommand):
        for cmd in command:
            for key in cmd.names:
                key = key.lower()
                self._magics[key] = cmd

    def __call__(self, silent: bool, code: str) -> Tuple[str, List[MagicCommandCallback], List[MagicCommandCallback]]:
        pre_query_callbacks = []
        post_query_callbacks = []

        while True:
            # ensure code starts with '%' or '%%' but not with '%%%'
            match = re.match(r'^%{1,2}([^% ]+?)($| .+?$)', code, re.MULTILINE | re.IGNORECASE)

            if match is None:
                break

            # remove magic command from code
            start, end = match.span()
            code = code[:start] + code[end + 1:]

            # extract command
            command = match.group(1).lower()

            if command not in self._magics:
                raise MagicCommandException(f'unknown magic command "{command}"')

            magic = self._magics[command]

            # extract parameters
            params = match.group(2)
            match = re.match(magic.parameters, params, re.IGNORECASE)

            if match is None:
                raise MagicCommandException(f'could not parse parameters for command "{command}"')

            # extract args
            args = [g for g, _ in zip(match.groups(), magic.args)]

            i = len(args) + 1

            # extract flags
            flags = {name: False for name, _ in magic.flags}

            offset = len(args) + 2 * len(magic.flags)
            while i < offset:
                name = match.group(i + 1)
                i += 2

                if name is not None:
                    flags[name.lower()] = True

            # extract optionals
            optionals = {name: default for name, default, _ in magic.optionals}

            offset = len(args) + 2 * len(magic.flags) + 3 * len(magic.optionals)
            while i < offset:
                name = match.group(i + 1)
                value = match.group(i + 2)
                i += 3

                if name is not None:
                    optionals[name.lower()] = value

            # add to callbacks
            callback = MagicCommandCallback(magic, silent, code, *args, **flags, **optionals)

            if not magic.requires_query_result:
                pre_query_callbacks.append(callback)
            else:
                post_query_callbacks.append(callback)

        # return callbacks
        return code, pre_query_callbacks, post_query_callbacks
