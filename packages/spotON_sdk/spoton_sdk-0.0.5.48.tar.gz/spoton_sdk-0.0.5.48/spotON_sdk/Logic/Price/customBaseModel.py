from typing import Any
from pydantic import BaseModel

class CustomBaseModel(BaseModel):
    def to_dict(self) -> dict[str, Any]:
        return self.dict()