"""Same-major.minor dependency contract, including the exact RC lower bound.

WP4D section 3.1 supersedes the historical major-wide allowance. Keep both
original test IDs and enforce the package pair and dependency together.
"""

from __future__ import annotations

from pathlib import Path

from packaging.version import Version
from scripts.fcop_rc_candidate_check import declared_version, read_pin, validate_pin

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_fcop_mcp_pin_matches_fcop_minor() -> None:
    core = declared_version(REPO_ROOT / "src/fcop/_version.py")
    adapter = declared_version(REPO_ROOT / "mcp/src/fcop_mcp/_version.py")
    pin = read_pin(REPO_ROOT / "mcp/pyproject.toml")
    result = validate_pin(pin, core, adapter)
    assert result["lower"] == core
    assert result["upper_exclusive"] == f"{Version(adapter).major}.{Version(adapter).minor + 1}.0"
    assert result["same_major_minor"] is True


def test_fcop_and_fcop_mcp_versions_are_aligned() -> None:
    core = Version(declared_version(REPO_ROOT / "src/fcop/_version.py"))
    adapter = Version(declared_version(REPO_ROOT / "mcp/src/fcop_mcp/_version.py"))
    assert core.release[:2] == adapter.release[:2], (
        f"fcop {core} and fcop-mcp {adapter} must share MAJOR.MINOR"
    )
