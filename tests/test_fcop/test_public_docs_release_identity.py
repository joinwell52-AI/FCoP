"""Public release surfaces must not drift behind the installed package identity."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _version(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"([^"]+)"', text)
    assert match is not None
    return match.group(1)


def test_public_homepage_matches_current_core_and_mcp_release() -> None:
    core = _version("src/fcop/_version.py")
    mcp = _version("mcp/src/fcop_mcp/_version.py")
    assert core == mcp

    page = (ROOT / "docs/index.html").read_text(encoding="utf-8")
    for value in (
        f"FCoP {core}",
        f"releases/tag/v{core}",
        f"pypi.org/project/fcop/{core}/",
        f"pypi.org/project/fcop-mcp/{mcp}/",
        f'fcop=={core}',
        f'fcop-mcp=={mcp}',
        "<strong>49</strong> tools",
        "<strong>12</strong> resources",
        "<strong>4</strong> templates",
        "10.5281/zenodo.22701147",
    ):
        assert value in page

    for command in (
        "fcop init",
        "fcop status",
        "fcop inspect",
        "fcop validate",
        "fcop tools",
        "fcop doctor",
        "fcop version",
        "fcop spec",
        "fcop migrate",
    ):
        assert command in page

    for tool in ("create_branch", "inspect_family", "merge_branches"):
        assert tool in page

    current_package = re.findall(r"Current package: ([^ <]+)", page)
    assert current_package == [core]
