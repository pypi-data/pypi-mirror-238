from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

from amsdal_utils.models.data_models.address import Address


class TableSchema(BaseModel):
    address: Address
    columns: list['TableColumnSchema']
    indexed: list['TableIndexSchema'] = Field(default_factory=list)
    unique_columns: list[list[str]] = Field(default_factory=list)

    @field_validator('columns')
    @classmethod
    def validate_columns(cls, columns: list['TableColumnSchema']) -> list['TableColumnSchema']:
        if not columns:
            msg = 'columns must not be empty'
            raise ValueError(msg)
        return columns

    def __hash__(self) -> int:
        return hash(self.address.to_string())


class TableColumnSchema(BaseModel):
    name: str
    type: type  # noqa: A003
    default: Any
    nullable: bool = True


class TableIndexSchema(BaseModel):
    column_name: str
    index_type: str = ''
