"""Read-only unpublished RC identity and same-major.minor dependency guard."""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

TARGET = "4.0.0rc1"


def declared_version(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    values = [ast.literal_eval(node.value) for node in tree.body
              if isinstance(node, ast.Assign)
              and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets)]
    assert len(values) == 1 and isinstance(values[0], str)
    return values[0]


def validate_pin(pin, core_version, adapter_version):
    core, adapter = Version(core_version), Version(adapter_version)
    if core.release[:2] != adapter.release[:2]:
        raise ValueError("MCP_PIN_MAJOR_MINOR_MISMATCH")
    requirement = Requirement(pin)
    upper = f"{adapter.major}.{adapter.minor + 1}.0"
    expected = SpecifierSet(f">={core_version},<{upper}")
    if requirement.name != "fcop" or requirement.marker or requirement.extras:
        raise ValueError("MCP_PIN_NOT_UNCONDITIONAL_CORE")
    if requirement.specifier != expected:
        raise ValueError("MCP_PIN_NOT_SAME_MINOR_EXACT_LOWER")
    if not requirement.specifier.contains(core, prereleases=True):
        raise ValueError("MCP_PIN_REJECTS_CANDIDATE")
    return {"lower": str(core), "upper_exclusive": upper, "same_major_minor": True}


def read_pin(path):
    match = re.search(r'"(fcop\s*>=[^"]+)"', path.read_text(encoding="utf-8"))
    assert match is not None
    return match.group(1).replace(" ", "")


def check(repo):
    core = declared_version(repo / "src/fcop/_version.py")
    adapter = declared_version(repo / "mcp/src/fcop_mcp/_version.py")
    assert core == adapter == TARGET
    pin = read_pin(repo / "mcp/pyproject.toml")
    assert pin == "fcop>=4.0.0rc1,<4.1.0"
    validate_pin(pin, core, adapter)
    for name in ("pyproject.toml", "mcp/pyproject.toml"):
        text = (repo / name).read_text(encoding="utf-8")
        assert '"Development Status :: 4 - Beta"' in text
        assert '"Development Status :: 5 - Production/Stable"' not in text
    module = ast.parse((repo / "mcp/src/fcop_mcp/routing.py").read_text(encoding="utf-8"))
    assigned = next(n.value for n in module.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "PACKAGE_COMPATIBILITY" for t in n.targets))
    assert isinstance(assigned, ast.Call) and isinstance(assigned.func, ast.Name)
    assert assigned.func.id == "frozenset"
    pairs = ast.literal_eval(assigned.args[0])
    assert (TARGET, TARGET) in pairs and pairs <= {(TARGET, TARGET), ("3.2.5", "3.2.5")}
    return {"schema": "wp4d-identity/v1", "fcop": core, "fcop-mcp": adapter,
            "pin": pin, "candidate_pair": True, "stable_pair": False, "published": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    print(json.dumps(check(parser.parse_args().repo.resolve()), sort_keys=True))
