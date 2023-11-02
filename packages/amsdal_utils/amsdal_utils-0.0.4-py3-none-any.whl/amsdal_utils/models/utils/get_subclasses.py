from collections.abc import Iterator

from amsdal_utils.models.base import ModelBase
from amsdal_utils.models.enums import SchemaTypes


def get_subclasses(class_item: type[ModelBase] | None) -> Iterator[type[ModelBase]]:
    if class_item is None:
        return []

    for parent_class in class_item.mro():
        schema_type = getattr(parent_class, 'schema_type', None)

        if not schema_type or schema_type in (SchemaTypes.TYPE, SchemaTypes.CORE):
            break

        if parent_class.__name__ == class_item.__name__:
            continue

        yield parent_class
