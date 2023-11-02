from pydantic import BaseModel
from pydantic import ConfigDict

from amsdal_utils.query.enums import OrderDirection


class OrderBy(BaseModel):
    model_config = ConfigDict(frozen=True)

    field_name: str
    direction: OrderDirection = OrderDirection.ASC

    @classmethod
    def from_string(cls, value: str) -> 'OrderBy':
        if value.startswith('-'):
            return cls(field_name=value[1:], direction=OrderDirection.DESC)

        return cls(field_name=value, direction=OrderDirection.ASC)
