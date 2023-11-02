from enum import Enum
from enum import auto


class LifecycleEvent(Enum):
    ON_AUTHENTICATE = auto()
    ON_PERMISSION_CHECK = auto()
    ON_MIGRATE = auto()
    ON_SERVER_STARTUP = auto()
