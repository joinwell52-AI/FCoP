"""Native read-only fixed CodeFlowMu shadow; no checkout, install or mutation there."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

FIXED = "b961b16dd0c8863ead6995d963fe0ca576a8abaa"
AUTH_SHA = "206129e8a68db7d5da1ef345d04c5e28348c1f392eef11aaa44e96f1fe6cdafa"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(repo, *args):
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
    )


def inventory(repo):
    tracked = git(repo, "ls-files", "-z").split(b"\0")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    records = {}
    for group, names in (("tracked", tracked), ("untracked", untracked)):
        group_files = {}
        for raw in names:
            if not raw:
                continue
            name = raw.decode("utf-8")
            path = repo / name
            assert path.resolve().is_relative_to(repo.resolve()), "Out-of-tree entry"
            if path.is_file():
                group_files[name] = sha(path.read_bytes())
            elif not path.exists():
                group_files[name] = "MISSING"
            else:
                raise AssertionError("Unsupported tracked/untracked entry: " + name)
        records[group] = group_files
    records["head"] = git(repo, "rev-parse", "HEAD").decode().strip()
    records["status_sha256"] = sha(git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all"))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("authorization", type=Path)
    parser.add_argument("product", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    import fcop
    from fcop import Project
    assert fcop.__version__ == "4.0.0rc1"
    assert Path(fcop.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    product = args.product.resolve()
    output = args.output.resolve()
    assert not output.is_relative_to(product)
    raw = args.authorization.read_bytes()
    assert sha(raw) == AUTH_SHA
    auth = json.loads(raw)
    downstream = Path(auth["downstream_root"])
    names = auth["allowed_relative_paths"]
    assert len(names) == len(set(names)) == 14
    observed = {name: (downstream / name).read_bytes() for name in names}
    for name, value in observed.items():
        assert sha(value) == auth["expected_sha256"][name]
        assert git(product, "show", f"{FIXED}:{name}") == value
    before = inventory(product)
    with tempfile.TemporaryDirectory(prefix="wp4d-shadow-caller-") as temporary:
        root = Path(temporary)
        p = Project(root)
        p.create_workspace(protocol_version="4.0", profiles=[])
        caller = {q.relative_to(root).as_posix(): q.read_bytes() if q.is_file() else None
                  for q in root.rglob("*")}
        result = p.rule_distribution(action="shadow", request={
            "downstream_path": str(downstream), "deploy": False,
            "shadow_authorization_ref": {"path": str(args.authorization.resolve()), "sha256": AUTH_SHA},
        })
        assert result["deployed"] is False and result["runtime_consumption_verified"] is None
        assert len(result["files"]) == 14
        pins = {p for record in result["files"] for p in record["detected_pins"]}
        assert {"fcop==3.2.5", "fcop-mcp==3.2.5"} <= pins
        assert {q.relative_to(root).as_posix(): q.read_bytes() if q.is_file() else None
                for q in root.rglob("*")} == caller
    after = inventory(product)
    assert before == after, "Product changed during read-only shadow; cannot claim zero drift"
    assert args.authorization.read_bytes() == raw
    assert {name: (downstream / name).read_bytes() for name in names} == observed
    evidence = dict(candidate=fcop.__version__, import_path=fcop.__file__, fixed_ref=FIXED,
                    shadow="14/14", codeflowmu_files_written=0, product=before,
                    tracked_untracked_byte_identity="MATCH", result=result)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(evidence, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"shadow": "14/14", "tracked": len(before["tracked"]),
                      "untracked": len(before["untracked"]), "inventory_sha256": sha(json.dumps(before, sort_keys=True).encode()),
                      "product_write_count": 0}))


if __name__ == "__main__":
    main()
