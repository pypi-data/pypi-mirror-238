import importlib.metadata
import typing as t
from abc import ABC

from flask import Blueprint
from flask import Flask

from pydantic_flask.pydantic import validate

flask_version = importlib.metadata.version("flask")
if flask_version[0] == "3":
    from flask.sansio.scaffold import T_route, Scaffold  # NOQA
else:
    from flask.scaffold import T_route, Scaffold  # NOQA


class PydanticScaffold(Scaffold, ABC):
    def route(self, rule: str, **options: t.Any) -> t.Callable[[T_route], T_route]:
        def decorator(f: T_route) -> T_route:
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, validate(f), **options)
            return f

        return decorator


class PydanticFlask(Flask, PydanticScaffold):
    pass


class PydanticBlueprint(Blueprint, PydanticScaffold):
    pass
