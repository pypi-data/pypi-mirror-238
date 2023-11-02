from pydantic import BaseModel
from pydantic import Field


class RepositoryConfig(BaseModel):
    default: str
    models: dict[str, str] = Field(default_factory=dict)
