"""Stable promotion audit: version metadata only, no business behavior change."""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
from pathlib import Path

BASE = "5208d8a2b37c969b0b2067c01107966bf705293c"
EXACT = {
    "src/fcop/_version.py", "mcp/src/fcop_mcp/_version.py", "mcp/src/fcop_mcp/routing.py",
    "pyproject.toml", "mcp/pyproject.toml", "README.md", "README.zh.md", "fcop-README.pypi.md",
    "mcp/README.md", "CHANGELOG.md", "docs/releases/4.0.0.md",
    ".github/workflows/rc-candidate.yml", ".github/workflows/release.yml",
    "tests/test_fcop/test_wp4d_rc_identity.py", "tests/test_fcop/test_wp4e_release_readiness.py",
}


def git(*args):
    return subprocess.check_output(["git", *args])


def stripped(raw, assignment):
    tree = ast.parse(raw)
    tree.body = [n for n in tree.body if not (isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == assignment for t in n.targets))]
    return ast.dump(tree)


def main():
    names = set(git("diff", "--name-only", BASE, "HEAD").decode().splitlines())
    names.update(git("diff", "--name-only", "HEAD").decode().splitlines())
    names.update(git("ls-files", "--others", "--exclude-standard").decode().splitlines())
    assert all(n in EXACT or n.startswith(("scripts/wp4f_", "tests/stable/",
        "tests/test_fcop/test_wp4f_", "reports/FCOP-4.0-WP4F-",
        "taskbooks/fcop-4.0/WP4F/", "reviews/fcop-4.0/wp4f/")) for n in names), sorted(names)
    production = git("ls-tree", "-r", "--name-only", BASE, "src", "mcp/src").decode().splitlines()
    changed = {}
    for name in production:
        before, after = git("show", BASE + ":" + name), Path(name).read_bytes()
        if name.endswith("/_version.py"):
            assert stripped(before, "__version__") == stripped(after, "__version__")
            assert '__version__ = "4.0.0"' in after.decode()
        elif name == "mcp/src/fcop_mcp/routing.py":
            assert stripped(before, "PACKAGE_COMPATIBILITY") == stripped(after, "PACKAGE_COMPATIBILITY")
            tree = ast.parse(after)
            node = next(n for n in tree.body if isinstance(n, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "PACKAGE_COMPATIBILITY" for t in n.targets))
            assert ast.literal_eval(node.value.args[0]) == {
                ("3.2.5", "3.2.5"), ("4.0.0rc1", "4.0.0rc1"), ("4.0.0", "4.0.0")}
        else:
            # Git text checkout may materialize CRLF; immutable authority files
            # are byte-compared separately below. No source statements may differ.
            assert before.replace(b"\r\n", b"\n") == after.replace(b"\r\n", b"\n"), name
        if before.replace(b"\r\n", b"\n") != after.replace(b"\r\n", b"\n"):
            changed[name] = hashlib.sha256(after).hexdigest()
    for path in ("spec", "tests/conformance", "tests/test_fcop/snapshots",
                 "tests/test_fcop_mcp/snapshots", "mcp/server.json"):
        assert git("rev-parse", BASE + ":" + path) == git("rev-parse", "HEAD:" + path), path
        assert not git("diff", "HEAD", "--", path), path
    canonical = git("ls-tree", "-r", "--name-only", BASE, "src/fcop/rules/_data/v4").decode().splitlines()
    assert len(canonical) == 19
    for path in [*canonical, "spec/fcop-4.0-spec.md", "spec/fcop-4.0-spec.zh.md"]:
        assert Path(path).read_bytes() == git("show", BASE + ":" + path), path
    print(json.dumps(dict(status="PASS", base=BASE, authoritative_bytes="21/21",
                         version_metadata_only=changed, changed_files=sorted(names)), sort_keys=True))


if __name__ == "__main__":
    main()
