"""Static MCP/package/release obligations frozen by WP1.1."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT = ROOT / "tests" / "test_fcop_mcp" / "snapshots" / "tool_surface.json"
COMPAT = ROOT / "reports" / "FCOP-4.0-WP1-COMPATIBILITY-AND-MCP.md"
SPEC = ROOT / "spec" / "fcop-4.0-spec.md"


def test_mcp_surface_01() -> None:
    """MCP-SURFACE-01 · official surface remains exactly 45 + 11 + 3."""
    # Arrange/Act: decode the frozen canonical MCP snapshot.
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    # Assert: official counts and downstream drift exclusion.
    assert len(snapshot["tools"]) == 45
    assert len(snapshot["resources"]["static"]) == 11
    assert len(snapshot["resources"]["templates"]) == 3
    assert "close_issue" not in {item["name"] for item in snapshot["tools"]}


def test_mcp_package_01() -> None:
    """MCP-PACKAGE-01 · retained tools require explicit version dispatch."""
    # Arrange: frozen compatibility disposition.
    compat = COMPAT.read_text(encoding="utf-8")
    # Act: extract the numbered official tool rows.
    numbered_tools = re.findall(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`", compat, re.MULTILINE)
    # Assert: complete ordered mapping plus dispatch/Legacy/optional Relay rules.
    assert [int(number) for number, _ in numbered_tools[:45]] == list(range(1, 46))
    assert "v3/v4 分派" in compat
    assert "LEGACY_V3_ONLY" in compat
    assert "Relay" in compat and "optional" in compat


def test_release_gate_01() -> None:
    """RELEASE-GATE-01 · disagreement or absent gate blocks release."""
    # Arrange/Act: read the frozen release authority clauses.
    spec = SPEC.read_text(encoding="utf-8")
    # Assert: disagreement and absent authorization both block promotion.
    assert "Conflict among Schema, specification, and tests blocks release" in spec
    assert "does not authorize Schema, tests, implementation, migration, push, or release" in spec
