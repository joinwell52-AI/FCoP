"""Private, deterministic package-data validation; never retrieves remote refs."""

from __future__ import annotations

import json
from datetime import datetime
from functools import lru_cache
from importlib.resources import files
from typing import Any

from jsonschema import (  # type: ignore[import-untyped]
    Draft202012Validator,
    FormatChecker,
    RefResolver,
)

from fcop.errors import _V4Code
from fcop.v4.encoding import fail


def _offline(uri: str) -> Any:
    raise ValueError(f"Schema reference is not bundled: {uri}")


@lru_cache(maxsize=1)
def _validators() -> dict[str, Any]:
    directory = files("fcop").joinpath("_data/schemas/v4")
    schemas = {
        path.name.removesuffix(".schema.json"): json.loads(path.read_bytes())
        for path in directory.iterdir() if path.name.endswith(".schema.json")
    }
    store = {schema["$id"]: schema for schema in schemas.values()}
    if len(store) != len(schemas) or not schemas:
        raise ValueError("Missing or duplicate bundled v4 schema IDs")
    def check_refs(value: Any) -> None:
        if isinstance(value, dict):
            if "$ref" in value and value["$ref"] not in store:
                _offline(value["$ref"])
            for child in value.values():
                check_refs(child)
        elif isinstance(value, list):
            for child in value:
                check_refs(child)
    check_refs(schemas)
    result = {}
    for name, schema in schemas.items():
        Draft202012Validator.check_schema(schema)
        resolver = RefResolver.from_schema(
            schema, store=store, handlers={"http": _offline, "https": _offline,
                                          "file": _offline, "ftp": _offline},
        )
        result[name] = Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker())
    return result


def _json_value(value: Any) -> Any:
    # SafeLoader represents YAML timestamps as datetime; their lexical ISO
    # representation has the same structural meaning. No Core projection.
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    return value


def _validate(name: str, value: dict[str, Any], *, code: _V4Code = _V4Code.INVALID_ENVELOPE) -> None:
    error = next(_validators()[name].iter_errors(_json_value(value)), None)
    if error is not None:
        location = "/".join(str(part) for part in error.absolute_path)
        raise fail(code, f"v4 {name} schema at {location or '/'}: {error.message}")
