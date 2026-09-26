"""Read-only v4 rule resources backed by Core, without legacy routing."""

from __future__ import annotations

import json
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.exceptions import ResourceError
from fcop import Project
from fcop.errors import FcopError

URIS = (
    "fcop://rules",
    "fcop://protocol",
    "fcop://guidance/sequential/en",
    "fcop://guidance/sequential/zh",
    "fcop://guidance/parallel/en",
    "fcop://guidance/parallel/zh",
)


def _read(root: Path, uri: str) -> str:
    try:
        result = Project(root).rule_distribution(
            action="read_resource", request={"resource_uri": uri}
        )
    except FcopError as exc:
        raise ResourceError(json.dumps({
            "code": getattr(exc, "code", "toolkit:RULE_SELECTION_INVALID"),
            "resource": uri,
        })) from exc
    content = result["content"]
    if uri == "fcop://protocol":
        return "# FCoP specification identity\n\n" + "".join(
            f"- {key}: {content[key]}\n" for key in ("path", "revision", "sha256")
        )
    if uri == "fcop://rules":
        return "# FCoP rule package Manifest\n\n```json\n" + json.dumps(
            content, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False
        ) + "\n```\n"
    return str(content)


def _reader(root: Path, resource_uri: str):
    def read() -> str:
        return _read(root, resource_uri)
    return read


def register_resources(mcp: FastMCP, root: Path) -> None:
    for uri in URIS:
        read = _reader(root, uri)
        read.__name__ = "read_" + uri.removeprefix("fcop://").replace("/", "_")
        read.__doc__ = "Read package-owned FCoP 4.x rule facts through Core."
        mcp.resource(uri, mime_type="text/markdown")(read)
