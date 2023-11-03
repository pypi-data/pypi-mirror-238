from typing import Dict, List, Tuple, Any

from . import Table


class Connection:
    def __init__(self, path: str):
        self.path: str = path

    def close(self):
        pass

    def execute(self, query: str) -> Tuple[List[str], List[List[Any]]]:
        raise NotImplementedError

    def analyze(self) -> Dict[str, Table]:
        raise NotImplementedError
