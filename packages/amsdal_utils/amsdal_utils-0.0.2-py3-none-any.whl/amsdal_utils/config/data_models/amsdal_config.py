from pydantic import BaseModel
from pydantic import field_validator

from amsdal_utils.config.data_models.connection_config import ConnectionConfig
from amsdal_utils.config.data_models.resources_config import ResourcesConfig


class AmsdalConfig(BaseModel):
    application_name: str
    connections: dict[str, ConnectionConfig]
    resources_config: ResourcesConfig

    @field_validator('connections', mode='before')
    @classmethod
    def set_connections(
        cls,
        values: dict[str, ConnectionConfig] | list[ConnectionConfig],
    ) -> dict[str, ConnectionConfig]:
        if isinstance(values, list):
            return {connection.name: connection for connection in values}

        return values
