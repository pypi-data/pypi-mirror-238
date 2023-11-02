from typing import Any

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

DEFAULT_NAME = 'default'


class ConnectionConfig(BaseModel):
    name: str = DEFAULT_NAME
    backend: str = 'amsdal_data.connections.implementations.iceberg_history.IcebergHistoricalConnection'
    credentials: dict[str, Any] = Field(default_factory=dict)

    @field_validator('credentials', mode='before')
    @classmethod
    def set_credentials(cls, value: list[dict[str, Any]] | dict[str, Any]) -> dict[str, Any]:
        if isinstance(value, dict):
            return value

        credentials = {}

        for credential in value:
            credentials.update(credential)

        return credentials
