"""WP4E read-only scope and authoritative-byte audit; no downstream access."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

BASE = "64a24295d6c1fa53a182a819d39b295c2ba8d2d0"
EXACT = {
    "README.md", "README.zh.md", "docs/index.html", "docs/mcp-tools.md", "mcp/README.md",
    ".github/workflows/release.yml", ".github/workflows/rc-candidate.yml",
    ".github/workflows/test-fcop.yml", ".github/workflows/test-fcop-mcp.yml",
    "scripts/wp4d_build.py", "scripts/wp4d_consume.py", "scripts/wp4d_candidate_ref.py",
    "examples/v4/third-party/mcp-only/client.py",
}


def git(*args):
    return subprocess.check_output(["git", *args])


def allowed(name):
    return name in EXACT or name.startswith((
        "taskbooks/fcop-4.0/WP4E/", "reports/FCOP-4.0-WP4E-", "reviews/fcop-4.0/wp4e/",
        "scripts/wp4e_", "tests/test_fcop/test_wp4e_", "tests/rc/evidence/wp4e/",
        "docs/fcop-4.0/rc-candidate-",
    ))


def main():
    root = Path.cwd()
    names = git("diff", "--name-only", BASE, "HEAD").decode().splitlines()
    assert all(allowed(n) for n in names), [n for n in names if not allowed(n)]
    protected = ("src", "mcp/src", "spec", "tests/conformance")
    for name in protected:
        assert git("rev-parse", BASE + ":" + name) == git("rev-parse", "HEAD:" + name), name
        assert not git("diff", "HEAD", "--", name), name
    canonical = git("ls-tree", "-r", "--name-only", BASE, "src/fcop/rules/_data/v4").decode().splitlines()
    assert len(canonical) == 19
    identities = {}
    for name in [*canonical, "spec/fcop-4.0-spec.md", "spec/fcop-4.0-spec.zh.md"]:
        raw = git("show", BASE + ":" + name)
        assert raw == (root / name).read_bytes(), name
        identities[name] = hashlib.sha256(raw).hexdigest()
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], check=True)
    print(json.dumps(dict(base=BASE, head=git("rev-parse", "HEAD").decode().strip(),
                          changed=names, canonical=19, authoritative=21, sha256=identities,
                          production_and_conformance_unchanged=True), sort_keys=True))


if __name__ == "__main__":
    main()
