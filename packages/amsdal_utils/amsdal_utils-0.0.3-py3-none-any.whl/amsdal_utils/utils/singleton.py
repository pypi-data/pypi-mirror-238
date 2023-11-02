from typing import Any
from typing import ClassVar


class Singleton(type):
    __instances: ClassVar[dict[type, Any]] = {}

    def __call__(cls, *args, **kwargs) -> Any:  # type: ignore[no-untyped-def]
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]

    def invalidate(cls) -> None:
        if cls is Singleton:
            cls.__instances.clear()
        elif cls in cls.__instances:
            del cls.__instances[cls]
