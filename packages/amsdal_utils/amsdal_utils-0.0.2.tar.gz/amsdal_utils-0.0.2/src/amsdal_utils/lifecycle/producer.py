from collections import defaultdict
from typing import Any
from typing import ClassVar

from amsdal_utils.lifecycle.consumer import LifecycleConsumer
from amsdal_utils.lifecycle.enum import LifecycleEvent


class LifecycleProducer:
    __listeners: ClassVar[dict[LifecycleEvent, set[type[LifecycleConsumer]]]] = defaultdict(set)

    @classmethod
    def add_listener(cls, event: LifecycleEvent, listener: type[LifecycleConsumer]) -> None:
        cls.__listeners[event].add(listener)

    @classmethod
    def publish(cls, event: LifecycleEvent, *args: Any, **kwargs: Any) -> None:
        for listener_class in cls.__listeners[event]:
            listener_class(event).on_event(*args, **kwargs)
