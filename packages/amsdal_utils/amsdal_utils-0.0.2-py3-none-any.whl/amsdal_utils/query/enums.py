from enum import Enum
from enum import auto


class OrderDirection(Enum):
    ASC = auto()
    DESC = auto()


class Lookup(str, Enum):
    EQ = 'eq'
    NEQ = 'neq'
    GT = 'gt'
    GTE = 'gte'
    LT = 'lt'
    LTE = 'lte'
    IN = 'in'
    CONTAINS = 'contains'
    ICONTAINS = 'icontains'
    STARTSWITH = 'startswith'
    ISTARTSWITH = 'istartswith'
    ENDSWITH = 'endswith'
    IENDSWITH = 'iendswith'
    ISNULL = 'isnull'
    REGEX = 'regex'
    IREGEX = 'iregex'
