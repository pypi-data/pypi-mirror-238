from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel


class Header(str):
    pass


class Cookie(str):
    pass


class Schema(BaseModel):
    @classmethod
    def as_dict(cls, obj: Any, from_attributes=True) -> Dict[str, Any]:
        return cls.model_validate(obj, from_attributes=from_attributes).model_dump()

    @classmethod
    def as_list(cls, objs: List[Any], from_attributes=True) -> List[Dict[str, Any]]:
        return [cls.as_dict(obj, from_attributes) for obj in objs]


class JsonSchema(Schema):
    pass


class FormSchema(Schema):
    pass
