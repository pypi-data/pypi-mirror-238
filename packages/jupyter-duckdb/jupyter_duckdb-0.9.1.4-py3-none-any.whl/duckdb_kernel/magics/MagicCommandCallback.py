from typing import Optional, List

from . import MagicCommand


class MagicCommandCallback:
    def __init__(self, mc: MagicCommand, silent: bool, code: str, *args, **kwargs):
        self._mc: MagicCommand = mc
        self._silent: bool = silent
        self._code: str = code
        self._args = args
        self._kwargs = kwargs

    def __call__(self, columns: Optional[List[str]] = None, rows: Optional[List[List]] = None):
        if self._mc.requires_code:
            return self._mc(self._silent, self._code, *self._args, **self._kwargs)
        if self._mc.requires_query_result:
            return self._mc(self._silent, columns, rows, *self._args, **self._kwargs)
        else:
            return self._mc(self._silent, *self._args, **self._kwargs)
