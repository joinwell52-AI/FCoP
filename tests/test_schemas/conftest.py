"""tests/test_schemas/ 的共享 fixtures。

provide validators wired against the bundled-in-wheel schema copies so
the entire suite shares a single import-time registry build.
"""

from __future__ import annotations

from typing import Any

import pytest
from jsonschema import Draft202012Validator

from fcop.core.jsonschema_validator import (
    SCHEMA_NAMES,
    SCHEMA_REGISTRY,
    load_bundled_schema,
)


@pytest.fixture(scope="session")
def schemas() -> dict[str, dict[str, Any]]:
    """所有 7 份 schema，以文件名为 key。"""
    return {name: load_bundled_schema(name) for name in SCHEMA_NAMES}


@pytest.fixture(scope="session")
def validator_for(schemas: dict[str, dict[str, Any]]):
    """工厂：给一个 schema 文件名，返回绑好 registry 的 validator。"""

    def _make(schema_name: str) -> Draft202012Validator:
        if schema_name not in schemas:
            raise KeyError(schema_name)
        return Draft202012Validator(schemas[schema_name], registry=SCHEMA_REGISTRY)

    return _make
