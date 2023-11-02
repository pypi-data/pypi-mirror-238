import time

from pydantic import BaseModel
from pydantic import Field
from pydantic import PrivateAttr

from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.models.utils.reference_builders import build_reference


class Metadata(BaseModel):
    _is_frozen: bool = PrivateAttr(False)

    address: Address
    class_schema_reference: Reference
    class_schema_type: SchemaTypes = SchemaTypes.USER
    is_deleted: bool = False
    next_version: str | None = None
    prior_version: str | None = None
    reference_to: list[Reference] = Field(default_factory=list)
    referenced_by: list[Reference] = Field(default_factory=list)
    created_at: float = Field(default_factory=lambda: round(time.time() * 1000))
    updated_at: float = Field(default_factory=lambda: round(time.time() * 1000))

    @property
    def is_latest(self) -> bool:
        return self.next_version is None

    @property
    def reference(self) -> Reference:
        reference_address = self.address

        if not self._is_frozen:
            reference_address = self.address.model_copy(update={'object_version': Versions.LATEST})

        return build_reference(
            resource=reference_address.resource,
            class_name=reference_address.class_name,
            object_id=reference_address.object_id,
            class_version=reference_address.class_version,
            object_version=reference_address.object_version,
        )
