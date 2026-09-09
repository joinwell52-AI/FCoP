"""Build the same fixed commit twice; publish nothing. Ubuntu/Python 3.12 only."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import platform
import subprocess
import sys
import tarfile
import zipfile
from datetime import datetime, timezone
from email.parser import BytesParser
from importlib.metadata import version
from pathlib import Path

TARGET = "4.0.0rc1"
NAMES = ["fcop-4.0.0rc1-py3-none-any.whl", "fcop-4.0.0rc1.tar.gz",
         "fcop_mcp-4.0.0rc1-py3-none-any.whl", "fcop_mcp-4.0.0rc1.tar.gz"]
BASE = "167c5fd4ca4c9603c392bae3a4a055963e7b7ed6"
EPOCH = "1788940367"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(command, **kwargs):
    subprocess.run(command, check=True, **kwargs)


def export(repo, commit, target):
    raw = subprocess.check_output(["git", "-C", str(repo), "archive", "--format=tar", commit])
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
        # Repository-owned fixed Git blobs; still reject traversal and links.
        for member in archive.getmembers():
            assert not member.name.startswith("/") and ".." not in Path(member.name).parts
            assert member.isdir() or member.isfile()
        archive.extractall(target, filter="data")


def inspect_archive(path, canonical):
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            assert len(archive.namelist()) == len(set(archive.namelist()))
            members = {n: archive.read(n) for n in archive.namelist() if not n.endswith("/")}
        metadata = [raw for name, raw in members.items() if name.endswith(".dist-info/METADATA")]
    else:
        with tarfile.open(path) as archive:
            entries = archive.getmembers()
            assert len(entries) == len({m.name for m in entries})
            assert all(m.isdir() or m.isfile() for m in entries)
            members = {m.name: archive.extractfile(m).read() for m in entries if m.isfile()}
        metadata = [raw for name, raw in members.items() if name.count("/") == 1 and name.endswith("/PKG-INFO")]
    assert len(metadata) == 1
    meta = BytesParser().parsebytes(metadata[0])
    assert meta["Version"] == TARGET
    distribution = meta["Name"].replace("_", "-")
    assert distribution in {"fcop", "fcop-mcp"}
    assert "Development Status :: 4 - Beta" in meta.get_all("Classifier", [])
    if distribution == "fcop-mcp":
        from packaging.requirements import Requirement
        from packaging.specifiers import SpecifierSet
        core = [Requirement(r) for r in meta.get_all("Requires-Dist", []) if Requirement(r).name == "fcop"]
        assert len(core) == 1 and core[0].specifier == SpecifierSet(">=4.0.0rc1,<4.1.0")
    for name in members:
        assert not name.startswith(("/", "\\")) and ".." not in Path(name).parts
        assert not any(part in {".env", "__pycache__", ".pytest_cache", ".git", ".venv", "build"}
                       for part in name.split("/"))
        assert not name.endswith((".pyc", ".pyo"))
    embedded = {}
    for name, raw in members.items():
        assert str(path.parent.parent).encode() not in raw, name
        prefix = "fcop/rules/_data/v4/"
        if prefix in name:
            embedded[name.split(prefix, 1)[1]] = sha(raw)
    if distribution == "fcop":
        assert embedded == canonical and len(embedded) == 19
    return dict(distribution=distribution, version=meta["Version"], members=len(members),
                canonical_sha256=embedded, requirements=meta.get_all("Requires-Dist", []))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    repo = Path.cwd()
    output = args.output.resolve()
    assert not output.exists() and not output.is_relative_to(repo)
    assert platform.system() == "Linux" and sys.version_info[:2] == (3, 12)
    output.mkdir(parents=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    assert not subprocess.check_output(["git", "status", "--porcelain"])
    canonical = {}
    names = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", BASE,
                                      "src/fcop/rules/_data/v4"], text=True).splitlines()
    assert len(names) == 19
    for name in [*names, "spec/fcop-4.0-spec.md", "spec/fcop-4.0-spec.zh.md"]:
        raw = subprocess.check_output(["git", "show", BASE + ":" + name])
        current = subprocess.check_output(["git", "show", commit + ":" + name])
        assert raw == current
        if name in names:
            canonical[Path(name).name] = sha(raw)
    started = datetime.now(timezone.utc).isoformat()
    env = {**os.environ, "SOURCE_DATE_EPOCH": EPOCH, "PYTHONDONTWRITEBYTECODE": "1"}
    env.pop("PYTHONPATH", None)
    sets = []
    for index in (1, 2):
        source, artifacts = output / f"source-{index}", output / f"artifacts-{index}"
        export(repo, commit, source)
        artifacts.mkdir()
        for package in (source, source / "mcp"):
            run([sys.executable, "-m", "build", "--no-isolation", "--wheel", "--sdist",
                 "--outdir", str(artifacts), str(package)], env=env)
        assert sorted(p.name for p in artifacts.iterdir()) == sorted(NAMES)
        run([sys.executable, "-m", "twine", "check", *[str(artifacts / n) for n in NAMES]])
        records = []
        for name in NAMES:
            path = artifacts / name
            records.append(dict(filename=name, bytes=path.stat().st_size, sha256=sha(path.read_bytes()),
                                **inspect_archive(path, canonical)))
        sets.append(records)
    assert sets[0] == sets[1], "Non-reproducible candidate; do not mix sets"
    document = dict(schema="wp4d-candidates/v1", repository="joinwell52-AI/FCoP",
                    commit=commit, python=platform.python_version(),
                    tools={n: version(n) for n in ("build", "hatchling", "setuptools", "wheel", "twine")},
                    source_date_epoch=int(EPOCH), started=started,
                    finished=datetime.now(timezone.utc).isoformat(), run_id=os.getenv("GITHUB_RUN_ID"),
                    raw_reproducibility="4/4", files=sets[0])
    # The consumer receives only the first set plus this explicit hash manifest.
    manifest = output / "artifacts-1" / "candidate-manifest.json"
    manifest.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_manifest_sha256": sha(manifest.read_bytes()), "artifacts": sets[0]}))


if __name__ == "__main__":
    main()
