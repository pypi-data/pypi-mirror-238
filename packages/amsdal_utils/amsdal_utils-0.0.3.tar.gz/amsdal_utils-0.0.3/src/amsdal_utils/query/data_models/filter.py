from typing import Any

from pydantic import BaseModel

from amsdal_utils.query.enums import Lookup


class Filter(BaseModel):
    field_name: str
    lookup: Lookup = Lookup.EQ
    value: Any

    @classmethod
    def build(cls, selector: str, value: Any) -> 'Filter':
        field_name, lookup = cls.parse_selector(selector)

        return cls(field_name=field_name, lookup=lookup, value=value)

    @classmethod
    def parse_selector(cls, selector: str) -> tuple[str, Lookup]:
        if '__' not in selector:
            return selector, Lookup.EQ

        field_name, lookup = selector.rsplit('__', 1)

        try:
            return field_name, Lookup(lookup)
        except ValueError:
            return selector, Lookup.EQ

    @property
    def is_nested_selection(self) -> bool:
        return '__' in self.field_name

    def __str__(self) -> str:
        return f'Filter(field_name={self.field_name}, lookup={self.lookup.value}, value={self.value})'

    def __repr__(self) -> str:
        return self.__str__()
