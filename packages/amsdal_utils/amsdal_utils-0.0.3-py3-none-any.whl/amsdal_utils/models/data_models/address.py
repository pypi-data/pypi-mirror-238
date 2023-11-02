from typing import TypeVar

from pydantic import BaseModel
from pydantic import field_validator

from amsdal_utils.models.enums import Versions

RESOURCE_DELIMITER = '#'
ADDRESS_PARTS_DELIMITER = ':'

AddressType = TypeVar('AddressType', bound='Address')


class Address(BaseModel):
    resource: str
    class_name: str
    class_version: Versions | str
    object_id: str
    object_version: Versions | str

    @property
    def is_full(self) -> bool:
        return all(
            element and not isinstance(element, Versions)
            for element in [
                self.class_name,
                self.class_version,
                self.object_id,
                self.object_version,
            ]
        )

    @classmethod
    def from_string(cls: type[AddressType], address: str) -> AddressType:
        if RESOURCE_DELIMITER not in address:
            msg = 'Resource name is not specified for this address.'
            raise ValueError(msg)

        resource, components = address.split(RESOURCE_DELIMITER, 1)

        components_dict = dict(enumerate(components.split(ADDRESS_PARTS_DELIMITER)))

        return cls(
            resource=resource,
            class_name=components_dict.get(0, ''),
            class_version=components_dict.get(1, ''),
            object_id=components_dict.get(2, ''),
            object_version=components_dict.get(3, ''),
        )

    @field_validator('class_version', 'object_version', mode='before')
    @classmethod
    def set_version(cls, version_id: str | Versions) -> str | Versions:
        if isinstance(version_id, str):
            try:
                return Versions(version_id)
            except ValueError:
                pass

        return version_id

    def to_string(self) -> str:
        parts = [
            str(item)
            for item in [
                self.class_name,
                self.class_version,
                self.object_id,
                self.object_version,
            ]
        ]
        keys_part = ADDRESS_PARTS_DELIMITER.join(parts)

        return f'{self.resource}{RESOURCE_DELIMITER}{keys_part}'

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string()

    def __hash__(self) -> int:
        return hash(self.to_string())

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Address):
            return False

        return self.to_string() == __value.to_string()
