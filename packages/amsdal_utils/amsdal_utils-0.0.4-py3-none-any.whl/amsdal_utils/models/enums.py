from enum import Enum


class Versions(str, Enum):
    ALL = 'ALL'
    LATEST = 'LATEST'

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class SchemaTypes(str, Enum):
    TYPE = 'type'
    CORE = 'core'
    USER = 'user'
    CONTRIB = 'contrib'
