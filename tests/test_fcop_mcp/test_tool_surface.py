"""MCP tool / resource surface snapshot tests.

Governing policy: :file:`adr/ADR-0003-stability-charter.md`, Commitment #2
("MCP tool contract locked"). Any change to the external contract —
tool names, parameter names, required-ness, resource URIs, resource
mime types — must be:

1. **Additive only** within a minor version (0.6.x); and
2. Accompanied by an intentional snapshot update:

       pytest tests/test_fcop_mcp/test_tool_surface.py --snapshot-update

   and a matching ``### Added — fcop-mcp`` entry in
   ``CHANGELOG.md``'s ``[Unreleased]`` section.

Renaming, deleting, or changing the required-ness of a tool parameter
is **forbidden** inside 0.6.x and requires a deprecation cycle landing
in 0.7.0 at the earliest — see ADR-0003 §"Deprecation Cycle".

The snapshot file :file:`snapshots/tool_surface.json` is tracked in
git. CI (the ``surface-check`` job in
``.github/workflows/test-fcop.yml``) greps the diff and fails any PR
that changes the snapshot without announcing the change in the
CHANGELOG.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import TypedDict

import pytest
from fcop_mcp.server import mcp

SNAPSHOT_PATH = Path(__file__).parent / "snapshots" / "tool_surface.json"


class _ParamSpec(TypedDict):
    """Structured view of a single tool parameter."""

    name: str
    type: str | None
    required: bool


class _ToolSpec(TypedDict):
    """Structured view of a single registered MCP tool."""

    name: str
    params: list[_ParamSpec]


def _collect_tools() -> list[_ToolSpec]:
    """Describe every registered MCP tool in a stable, diffable form.

    Reads the JSON-schema that FastMCP derives from each tool's
    Python signature (via ``FunctionTool.parameters``). Only the
    *public* contract is captured — name, param name, JSON type,
    and required-ness. Deliberately excludes docstring text so
    wording improvements don't churn the snapshot.
    """
    tools = asyncio.run(mcp.list_tools())
    out: list[_ToolSpec] = []
    for t in sorted(tools, key=lambda x: x.name):
        schema = t.parameters or {}
        properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
        required = set(schema.get("required", []) if isinstance(schema, dict) else [])
        params: list[_ParamSpec] = []
        for pname in sorted(properties):
            pspec = properties[pname]
            ptype = pspec.get("type") if isinstance(pspec, dict) else None
            params.append(
                _ParamSpec(name=pname, type=ptype, required=pname in required)
            )
        out.append(_ToolSpec(name=t.name, params=params))
    return out


def _collect_resources() -> dict[str, list[dict[str, str | None]]]:
    """Describe every MCP resource (static + templated)."""
    static = asyncio.run(mcp.list_resources())
    templated = asyncio.run(mcp.list_resource_templates())
    static_rows: list[dict[str, str | None]] = [
        {"uri": str(r.uri), "mime_type": r.mime_type} for r in static
    ]
    template_rows: list[dict[str, str | None]] = [
        {"uri_template": r.uri_template, "mime_type": r.mime_type}
        for r in templated
    ]
    static_rows.sort(key=lambda d: d["uri"] or "")
    template_rows.sort(key=lambda d: d["uri_template"] or "")
    return {"static": static_rows, "templates": template_rows}


def _collect_surface() -> dict[str, object]:
    return {
        "version": "1",
        "tools": _collect_tools(),
        "resources": _collect_resources(),
    }


def test_tool_surface_matches_snapshot(pytestconfig: pytest.Config) -> None:
    """Fail if any tool / resource drifted from the locked snapshot."""
    observed = _collect_surface()

    if pytestconfig.getoption("--snapshot-update", default=False):
        SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT_PATH.write_text(
            json.dumps(observed, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        pytest.skip("Snapshot updated; rerun without --snapshot-update to verify.")

    assert SNAPSHOT_PATH.exists(), (
        f"Snapshot missing: {SNAPSHOT_PATH}. "
        "Run `pytest --snapshot-update` to create it."
    )
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    if observed != expected:
        import difflib

        observed_text = json.dumps(observed, indent=2, sort_keys=True)
        expected_text = json.dumps(expected, indent=2, sort_keys=True)
        diff = "\n".join(
            difflib.unified_diff(
                expected_text.splitlines(),
                observed_text.splitlines(),
                fromfile="snapshot (expected)",
                tofile="observed (current)",
                lineterm="",
            )
        )
        pytest.fail(
            "MCP tool / resource surface drifted from snapshot.\n\n"
            "Per ADR-0003 (Pre-1.0 Stability Charter, Commitment #2):\n"
            "  * Additive changes (new tool / new optional param / new\n"
            "    resource URI): regenerate with\n"
            "    `pytest tests/test_fcop_mcp/test_tool_surface.py "
            "--snapshot-update`\n"
            "    and announce in CHANGELOG.md under [Unreleased].\n"
            "  * Rename / delete / required-ness change: NOT ALLOWED\n"
            "    in 0.6.x. Introduce a new tool, keep the old one as\n"
            "    a thin alias, and plan removal for the next minor.\n\n"
            f"Diff:\n{diff}"
        )


def test_tool_names_are_a_superset_of_snapshot() -> None:
    """Targeted regression: a tool disappearing should fail loudly.

    This is redundant with :func:`test_tool_surface_matches_snapshot` but
    gives a cleaner error for the single most common regression.
    """
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    expected_names = {t["name"] for t in expected["tools"]}
    observed_names = {t["name"] for t in _collect_tools()}
    missing = expected_names - observed_names
    assert not missing, (
        f"The following MCP tools disappeared: {sorted(missing)}. "
        "Tool removal is forbidden in 0.6.x per ADR-0003."
    )


def test_required_params_are_not_tightened() -> None:
    """Adding a new required parameter is a breaking change.

    The contract allows adding **optional** params, but promoting an
    existing param to required, or introducing a new required param,
    breaks every client that was calling the tool with the previous
    argument shape.
    """
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    expected_req: dict[str, set[str]] = {
        t["name"]: {p["name"] for p in t["params"] if p["required"]}
        for t in expected["tools"]
    }
    observed_req: dict[str, set[str]] = {
        t["name"]: {p["name"] for p in t["params"] if p["required"]}
        for t in _collect_tools()
    }
    regressions: dict[str, set[str]] = {}
    for name, req in observed_req.items():
        added_required = req - expected_req.get(name, set())
        if added_required:
            regressions[name] = added_required
    assert not regressions, (
        "New required parameters added to existing tools (breaking): "
        f"{regressions}. Per ADR-0003 this is forbidden in 0.6.x. "
        "Make them optional (with a default), or introduce a new tool."
    )


def test_resource_uris_are_not_removed() -> None:
    """Resource URIs are part of the public contract, just like tools."""
    if not SNAPSHOT_PATH.exists():
        pytest.skip("Snapshot not yet initialized")
    expected = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    observed = _collect_resources()
    expected_static = {r["uri"] for r in expected["resources"]["static"]}
    observed_static = {r["uri"] for r in observed["static"]}
    missing_static = expected_static - observed_static
    expected_templates = {
        r["uri_template"] for r in expected["resources"]["templates"]
    }
    observed_templates = {r["uri_template"] for r in observed["templates"]}
    missing_templates = expected_templates - observed_templates
    assert not (missing_static or missing_templates), (
        f"MCP resources disappeared — static: {sorted(missing_static)}, "
        f"templates: {sorted(missing_templates)}. Forbidden in 0.6.x."
    )
