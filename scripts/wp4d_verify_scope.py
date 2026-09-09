"""Read-only WP4D write-set and frozen-byte verification against fixed authority."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "167c5fd4ca4c9603c392bae3a4a055963e7b7ed6"
ORIGINAL_TASKBOOK = "taskbooks/fcop-4.0/WP4D/01-Release-Candidate-and-Third-Party-Adoption-Proof-Taskbook-v1.0.zh.md"
TREES = {
    "tests/conformance/v4": "24ab264c6bca9a3183ee270becb552f22a4c4f9e",
    "tests/conformance/rule_distribution_v4": "4f99c7261b63b6db81c500604a231defaca9f14b",
}
EXACT = {
    "src/fcop/_version.py", "mcp/src/fcop_mcp/_version.py",
    "pyproject.toml", "mcp/pyproject.toml", "mcp/src/fcop_mcp/routing.py",
    "tests/test_fcop/test_pyproject_pins.py", "tests/test_fcop/test_audit.py",
    "scripts/fcop_rc_candidate_check.py", ".github/workflows/rc-candidate.yml",
    "CHANGELOG.md", "fcop-README.pypi.md", "mcp/README.md",
    "docs/releases/4.0.0rc1.md", "reviews/fcop-4.0/wp4d/MANIFEST.md",
    ORIGINAL_TASKBOOK,
}


def git(*args):
    return subprocess.check_output(["git", *args])


def blob(ref, name):
    return git("show", ref + ":" + name)


def allowed(name):
    return name in EXACT or name.startswith((
        "examples/v4/third-party/python-only/", "examples/v4/third-party/mcp-only/",
        "tests/rc/", "tests/test_fcop/test_wp4d_rc", "tests/test_fcop_mcp/test_wp4d_rc",
        "scripts/wp4d_", "docs/fcop-4.0/rc-candidate", "reports/FCOP-4.0-WP4D-",
    ))


def without_named_assignment(tree, name):
    tree.body = [node for node in tree.body
                 if not isinstance(node, ast.Assign)
                 or not any(isinstance(t, ast.Name) and t.id == name for t in node.targets)]
    return ast.dump(tree, include_attributes=False)


def main():
    root = Path.cwd()
    head = git("rev-parse", "HEAD").decode().strip()
    names = git("diff", "--name-only", BASE, head).decode().splitlines()
    assert all(allowed(name) for name in names), [n for n in names if not allowed(n)]
    assert blob(head, ORIGINAL_TASKBOOK) == blob("cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9", ORIGINAL_TASKBOOK)
    for path, expected in TREES.items():
        assert git("rev-parse", head + ":" + path).decode().strip() == expected
    canonical = git("ls-tree", "-r", "--name-only", BASE, "src/fcop/rules/_data/v4").decode().splitlines()
    assert len(canonical) == 19
    frozen = {}
    for name in [*canonical, "spec/fcop-4.0-spec.md", "spec/fcop-4.0-spec.zh.md"]:
        raw = blob(BASE, name)
        assert raw == blob(head, name) == (root / name).read_bytes(), name
        frozen[name] = hashlib.sha256(raw).hexdigest()
    for path, assignment in (
        ("mcp/src/fcop_mcp/routing.py", "PACKAGE_COMPATIBILITY"),
        ("src/fcop/_version.py", "__version__"),
        ("mcp/src/fcop_mcp/_version.py", "__version__"),
    ):
        old, new = (ast.parse(blob(ref, path)) for ref in (BASE, head))
        assert without_named_assignment(old, assignment) == without_named_assignment(new, assignment), path
    path = "tests/test_fcop/test_audit.py"
    old, new = (ast.parse(blob(ref, path)) for ref in (BASE, head))
    for tree in (old, new):
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                        and n.name == "test_scan_outdated_role_docs_far_behind")
        # Only the authorized old precondition (assignment and if) differs.
        del function.body[2:4]
    assert ast.dump(old, include_attributes=False) == ast.dump(new, include_attributes=False)
    print(json.dumps(dict(commit=head, changed_files=len(names), allowed_scope=True,
                          canonical_files=19, frozen_bytes=frozen, conformance_trees=TREES,
                          audit_test_id_fixture_assertion_preserved=True), sort_keys=True))


if __name__ == "__main__":
    main()
