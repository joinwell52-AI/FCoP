"""Explicit source/archive/clean-install byte parity; run with python -I -B."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    import fcop

    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("archives", type=Path)
    parser.add_argument("--installed", action="store_true")
    args = parser.parse_args()
    if args.installed:
        assert Path(fcop.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    source = args.source / "src/fcop/rules/_data/v4"
    expected = {p.name: p.read_bytes() for p in source.iterdir() if p.is_file()}
    assert len(expected) == 19
    installed = Path(fcop.__file__).parent / "rules/_data/v4"
    assert {p.name: p.read_bytes() for p in installed.iterdir() if p.is_file()} == expected
    archives = [*args.archives.glob("fcop-*.whl"), *args.archives.glob("fcop-*.tar.gz")]
    assert len(archives) == 2
    observed = []
    for path in sorted(archives):
        if path.suffix == ".whl":
            with zipfile.ZipFile(path) as archive:
                members = {n: archive.read(n) for n in archive.namelist() if not n.endswith("/")}
        else:
            with tarfile.open(path) as archive:
                members = {m.name: archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}
        prefix = "fcop/rules/_data/v4/"
        canonical = {n.split(prefix, 1)[1]: raw for n, raw in members.items() if prefix in n}
        assert canonical == expected
        observed.append({"archive": path.name, "sha256": sha(path.read_bytes()), "canonical_members": 19})
    with tempfile.TemporaryDirectory(prefix="fcop-wp4c6-installed-") as sandbox:
        root = Path(sandbox) / "workspace"
        (root / "fcop").mkdir(parents=True)
        (root / "fcop/fcop.json").write_bytes((json.dumps({
            "protocol": "fcop", "protocol_version": "4.0",
            "workspace_id": "urn:uuid:00000000-0000-4000-8000-000000000006",
            "encoding": {"name": "fcop-filesystem", "version": "4.0"}, "profiles": [],
        }) + "\n").encode())
        result = fcop.Project(root).rule_distribution(action="build_artifacts", request={
            "formats": ["wheel", "sdist"], "output_directory": str(Path(sandbox) / "export"),
            "offline": True, "build_isolation": False,
        })
        assert result["member_count"] == 19 and result["manifest_sha256"] == sha(expected["manifest.json"])
        assert len(list(root.rglob("*"))) == 2
    print(json.dumps({
        "installed": args.installed, "import_path": fcop.__file__, "artifacts": observed,
        "canonical": [{"path": name, "size_bytes": len(raw), "sha256": sha(raw)}
                      for name, raw in sorted(expected.items())],
        "source_archive_install_raw_byte_parity": "PASS",
        "installed_public_export": "PASS",
    }, indent=2))


if __name__ == "__main__":
    main()
