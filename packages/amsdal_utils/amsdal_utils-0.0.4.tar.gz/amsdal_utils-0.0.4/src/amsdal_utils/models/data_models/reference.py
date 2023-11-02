from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.enums import Versions


class ReferenceData(Address, validate_assignment=True):
    pass


class Reference(BaseModel, populate_by_name=True):
    ref: ReferenceData = Field(alias='$ref')

    @field_validator('ref', mode='before')
    @classmethod
    def set_address(cls, address: str | Address | dict[str, str]) -> ReferenceData:
        if isinstance(address, Address):
            ref = ReferenceData.from_string(address.to_string())
        elif isinstance(address, str):
            ref = ReferenceData.from_string(address)
        else:
            try:
                ref = ReferenceData(**address)
            except TypeError as exc:
                msg = 'Input should be a valid dictionary or instance of ReferenceData'
                raise ValueError(msg) from exc

        if not ref.class_version:
            msg = 'Class version is required.'
            raise ValueError(msg)

        if isinstance(ref.class_version, Versions) and ref.class_version == Versions.ALL:
            msg = 'Class version cannot be ALL.'
            raise ValueError(msg)

        if isinstance(ref.object_version, Versions) and ref.object_version == Versions.ALL:
            msg = 'Object version cannot be ALL.'
            raise ValueError(msg)

        if not ref.object_version:
            ref.object_version = Versions.LATEST

        if ref.object_version == Versions.LATEST:
            ref.class_version = Versions.LATEST

        return ref

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        # we always use Reference with aliased prop $ref
        data = dict(kwargs.items())
        data['by_alias'] = False
        return super().model_dump(**data)

    def __hash__(self) -> int:
        return hash(self.ref)
