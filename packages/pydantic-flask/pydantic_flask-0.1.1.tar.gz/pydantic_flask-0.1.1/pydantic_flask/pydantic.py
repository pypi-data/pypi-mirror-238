from __future__ import annotations

import functools
import json
from typing import Any
from typing import Callable
from typing import Dict
from typing import get_args
from typing import get_origin
from typing import get_type_hints
from typing import List
from typing import Type

from flask import current_app
from flask import request
from pydantic import validate_call
from pydantic import ValidationError
from werkzeug.datastructures import FileStorage

from pydantic_flask.types import Cookie
from pydantic_flask.types import FormSchema
from pydantic_flask.types import Header
from pydantic_flask.types import JsonSchema
from pydantic_flask.types import Schema


def parse_request(hints: Dict) -> Dict:
    result = {}
    for var, var_type in hints.items():
        if issubclass(var_type, JsonSchema):
            result[var] = var_type(**request.json)
        elif issubclass(var_type, FormSchema):
            result[var] = var_type(**request.form)
        elif issubclass(var_type, Header):
            result[var] = var_type(request.headers.get(var))
        elif issubclass(var_type, Cookie):
            result[var] = var_type(request.cookies.get(var))
        elif issubclass(var_type, FileStorage):
            result[var] = var_type(request.files.get(var))
        else:
            result[var] = request.args.get(var, type=var_type)
    return {k: v for k, v in result.items() if v}


def validate(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(**kwargs):
        try:
            params = parse_request(get_type_hints(func))
        except ValidationError as e:
            return {"error": json.loads(e.json())}, current_app.config.get("PYDANTIC_VALIDATION_ERROR_CODE", 400)

        for key in kwargs.keys():
            params.pop(key, None)

        try:
            return validate_call(config=dict(arbitrary_types_allowed=True))(func)(**kwargs, **params)
        except ValidationError as e:
            return {"error": json.loads(e.json())}, current_app.config.get("PYDANTIC_VALIDATION_ERROR_CODE", 400)

    return wrapper


def serialize(return_type: Any, from_attributes: bool = True):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(**kwargs):
            result = func(**kwargs)
            result = list(result) if isinstance(result, tuple) else [result, 200]

            try:
                type_origin = get_origin(return_type)
                type_args = get_args(return_type)
                if (
                    type_origin
                    and type_args
                    and issubclass(type_origin, List)
                    and issubclass(type_args[0], Schema)
                    and isinstance(result, list)
                ):
                    return_sub_type: Type[Schema] = type_args[0]
                    result[0] = return_sub_type.as_list(result[0], from_attributes)
                elif issubclass(return_type, Schema):
                    result[0] = return_type.as_dict(result[0], from_attributes)
                else:
                    raise TypeError("Invalid response schema.")
                return tuple(result)
            except ValidationError:
                raise ValueError("Serialize error.")

        return wrapper

    return decorator
