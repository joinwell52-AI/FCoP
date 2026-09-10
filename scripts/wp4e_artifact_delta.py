"""Attribute every archive member change to authorized public documentation."""
from __future__ import annotations

import argparse
import hashlib
import json
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path

BASELINE = {
    "fcop-4.0.0rc1-py3-none-any.whl": "b539fdd496d52ea608b5f42abd270c2ed04e8f011242d932ddedac48f8d7cee9",
    "fcop-4.0.0rc1.tar.gz": "43e4488af52bffac3e400c14f442136f955ee0477ddf0e94386481e6ec682bb4",
    "fcop_mcp-4.0.0rc1-py3-none-any.whl": "20167b314de1a90093b74cf42c7039edceddc1458e1b37ce3e9e6f31697c773a",
    "fcop_mcp-4.0.0rc1.tar.gz": "eefde60b6d156f5ef2184186f5f5a355837f0fc9e0244b3e2d8077dbed51000b",
}


def members(path):
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            return {n: archive.read(n) for n in archive.namelist() if not n.endswith("/")}
    with tarfile.open(path) as archive:
        return {n.name.split("/", 1)[1]: archive.extractfile(n).read()
                for n in archive.getmembers() if n.isfile()}


def compare(old, new):
    assert old.keys() == new.keys(), "Archive member set changed"
    changed = [n for n in old if old[n] != new[n]]
    for name in changed:
        if name in {"README.md", "README.zh.md"}:
            continue
        if name.endswith((".dist-info/METADATA", "/PKG-INFO")) or name == "PKG-INFO":
            before, after = [BytesParser().parsebytes(raw) for raw in (old[name], new[name])]
            assert list(before.items()) == list(after.items()), "Metadata headers changed"
            # Only the long description may change; it is exactly the authorized README.
            expected = Path("mcp/README.md").read_text(encoding="utf-8")
            assert str(after.get_payload()).strip() == expected.strip()
            continue
        if name.endswith(".dist-info/RECORD"):
            continue  # Every underlying non-RECORD member is independently compared.
        raise AssertionError("Unapproved artifact member changed: " + name)
    return changed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("baseline", type=Path)
    p.add_argument("candidate", type=Path)
    a = p.parse_args()
    rows = []
    for name, expected in BASELINE.items():
        old, new = a.baseline / name, a.candidate / name
        assert hashlib.sha256(old.read_bytes()).hexdigest() == expected
        changed = compare(members(old), members(new))
        rows.append(dict(filename=name, baseline_sha256=expected,
                         sha256=hashlib.sha256(new.read_bytes()).hexdigest(), changed_members=changed))
    print(json.dumps(dict(artifacts=rows, production_members_unchanged=True), sort_keys=True))


if __name__ == "__main__":
    main()
