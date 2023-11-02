from abc import abstractmethod

from pydantic import BaseModel

from amsdal_utils.models.data_models.metadata import Metadata


class ModelBase(BaseModel):  # pragma: no cover
    @abstractmethod
    def get_metadata(self) -> Metadata:
        ...
