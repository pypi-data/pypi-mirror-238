from .DatabaseError import DatabaseError
from .Column import Column
from .Constraint import Constraint
from .ForeignKey import ForeignKey
from .Table import Table

try:
    from .duckdb import Connection
    SQLITE_MODE = False
except ImportError:
    from .sqlite import Connection
    SQLITE_MODE = True
