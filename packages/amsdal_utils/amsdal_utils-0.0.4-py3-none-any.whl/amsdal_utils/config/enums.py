from enum import Enum


class ResourceType(str, Enum):
    LAKEHOUSE = 'lakehouse'
    LOCK = 'lock'
    INTEGRATION = 'integration'
