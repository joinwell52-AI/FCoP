"""Lockstep test: ``fcop-mcp`` MUST pin its ``fcop`` dependency to the
matching minor version.

The bug this test prevents is exactly ISSUE-20260427-006: ``fcop-mcp
0.7.0`` shipped to PyPI with ``fcop>=0.6,<0.7`` while its own code
imported APIs that only exist in ``fcop 0.7.0``. The result was a
broken release on PyPI for which the only fix was to yank and ship
``0.7.1``.

ADR-0002's stability charter says "fcop-mcp depends on fcop within
the same MINOR" — this test makes that contract executable instead
of leaving it as a doc the next maintainer might forget to read.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_version(version_file: Path) -> tuple[int, int]:
    text = _read_text(version_file)
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', text)
    assert match is not None, (
        f"Could not find __version__ in {version_file}: {text!r}"
    )
    return int(match.group(1)), int(match.group(2))


def _extract_fcop_pin(pyproject: Path) -> str:
    """Return the literal ``fcop>=...,<...`` line from ``mcp/pyproject.toml``.

    We deliberately parse with a small regex rather than ``tomllib``
    so the test still works when run from python <3.11 environments
    that some CI matrices keep around for compatibility.
    """
    text = _read_text(pyproject)
    match = re.search(r'"(fcop\s*>=[^"]+)"', text)
    assert match is not None, (
        f"Could not find 'fcop>=...' dependency string in {pyproject}"
    )
    return match.group(1).replace(" ", "")


def test_fcop_mcp_pin_matches_fcop_minor() -> None:
    """``fcop-mcp X.Y.Z`` must depend on ``fcop>=X.Y,<X.(Y+1)``.

    A mismatch is exactly the failure mode that caused the 0.7.0
    release blocker — fcop-mcp 0.7.0 shipped while its pin still said
    ``fcop>=0.6,<0.7``, so PyPI resolved to ``fcop 0.6.5`` which did
    not have the new ``RoleOccupancy`` API.
    """
    fcop_mcp_version_file = REPO_ROOT / "mcp" / "src" / "fcop_mcp" / "_version.py"
    fcop_mcp_pyproject = REPO_ROOT / "mcp" / "pyproject.toml"

    major, minor = _extract_version(fcop_mcp_version_file)
    pin = _extract_fcop_pin(fcop_mcp_pyproject)

    expected = f"fcop>={major}.{minor},<{major}.{minor + 1}"
    assert pin == expected, (
        f"fcop-mcp {major}.{minor}.x must depend on `{expected}`, "
        f"but pyproject.toml says `{pin}`. This is the ISSUE-20260427-006 "
        "lockstep bug — bump the dependency in mcp/pyproject.toml in "
        "the same commit that bumps mcp/src/fcop_mcp/_version.py."
    )


def test_fcop_and_fcop_mcp_versions_are_aligned() -> None:
    """The two packages release in lockstep at the minor level.

    This is a 0.x rule, not a 1.x+ rule — once we hit 1.0 the two
    packages are free to drift on minor. Until then, missing this
    alignment usually means somebody bumped only one ``_version.py``
    by accident.
    """
    fcop_version_file = REPO_ROOT / "src" / "fcop" / "_version.py"
    fcop_mcp_version_file = REPO_ROOT / "mcp" / "src" / "fcop_mcp" / "_version.py"

    fcop_major, fcop_minor = _extract_version(fcop_version_file)
    fcop_mcp_major, fcop_mcp_minor = _extract_version(fcop_mcp_version_file)

    assert (fcop_major, fcop_minor) == (fcop_mcp_major, fcop_mcp_minor), (
        f"fcop {fcop_major}.{fcop_minor}.x and fcop-mcp "
        f"{fcop_mcp_major}.{fcop_mcp_minor}.x are out of lockstep. Per "
        "ADR-0002 the two packages share a minor version while we are "
        "still pre-1.0."
    )
