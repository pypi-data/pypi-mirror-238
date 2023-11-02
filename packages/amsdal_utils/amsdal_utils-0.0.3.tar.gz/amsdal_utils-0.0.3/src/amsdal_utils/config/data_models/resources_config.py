from pydantic import BaseModel

from amsdal_utils.config.data_models.repository_config import RepositoryConfig


class ResourcesConfig(BaseModel):
    lakehouse: str
    lock: str
    repository: RepositoryConfig
