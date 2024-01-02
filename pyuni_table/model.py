from uuid import UUID, uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class BaseModel(PydanticBaseModel):
    """
    An extension of Pydantic's BaseModel that adds an id field.
    """

    id: UUID = Field(default_factory=uuid4)
