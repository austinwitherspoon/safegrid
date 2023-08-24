from typing import List
import pydantic


class Entity(pydantic.BaseModel):
    type: pydantic.types.ClassVar[str]
    id: int
