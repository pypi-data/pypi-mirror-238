from typing import Any

from .managed_cursor import ManagedCursor


class ConnectionBase(object):
    def __init__(self, connection_string: str):
        self.connection_string: str = connection_string
        self.database: str = ""
        self.connection: Any = None
        self.provider_name: str = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def commit(self):
        pass

    def rollback(self):
        pass

    def execute(self, query: str, params: {}) -> ManagedCursor:
        pass

    def execute_lastrowid(self, query: str, params: {}):
        pass

    def close(self):
        pass
