from collections.abc import Callable
from typing import Generic
from typing import TypeVar

TLazyObject = TypeVar('TLazyObject')


class LazyObject(Generic[TLazyObject]):
    def __init__(self, resolver: Callable[[], TLazyObject]) -> None:
        self._value: TLazyObject | None = None
        self._resolver: Callable[[], TLazyObject] = resolver

    @property
    def value(self) -> TLazyObject:
        if self._value is None:
            self._value = self._resolver()

        return self._value
