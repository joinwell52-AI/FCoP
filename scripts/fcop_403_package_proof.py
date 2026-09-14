"""Build a fixed local commit twice and verify four 4.0.3 archives; never publish."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import zipfile
from email.parser import BytesParser
from importlib.metadata import version
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

NAMES = {
    "fcop-4.0.3-py3-none-any.whl", "fcop-4.0.3.tar.gz",
    "fcop_mcp-4.0.3-py3-none-any.whl", "fcop_mcp-4.0.3.tar.gz",
}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(*args, **kwargs):
    return subprocess.check_output(list(args), **kwargs)


def members(path):
    if path.suffix == ".whl":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            assert len(names) == len(set(names))
            return {n: archive.read(n) for n in names if not n.endswith("/")}
    with tarfile.open(path) as archive:
        entries = archive.getmembers()
        assert all(m.isfile() or m.isdir() for m in entries)
        assert len(entries) == len({m.name for m in entries})
        return {m.name: archive.extractfile(m).read() for m in entries if m.isfile()}


def inspect(path, source):
    data = members(path)
    for name in data:
        assert not name.startswith(("/", "\\")) and ".." not in Path(name).parts
        assert Path(name).name not in {"AGENTS.md", "CLAUDE.md", "fcop-v4.mdc"}
        assert not name.endswith((".pyc", ".pyo"))
        assert not {".env", "__pycache__", ".git", ".venv"}.intersection(name.split("/"))
    metadata = [raw for n, raw in data.items() if n.endswith(".dist-info/METADATA")
                or (n.count("/") == 1 and n.endswith("/PKG-INFO"))]
    assert len(metadata) == 1
    meta = BytesParser().parsebytes(metadata[0])
    assert meta["Version"] == "4.0.3"
    assert "Development Status :: 5 - Production/Stable" in meta.get_all("Classifier", [])
    package = meta["Name"].replace("_", "-")
    readme = "mcp/README.md" if package == "fcop-mcp" else "fcop-README.pypi.md"
    description = metadata[0].split(b"\n\n", 1)[1]
    assert description == (source / readme).read_bytes()
    assert b"## CLI" in description and b"fcop tools merge_branches --json" in description
    prefix = "fcop/rules/_data/v4/"
    canonical = {n.split(prefix, 1)[1]: raw for n, raw in data.items() if prefix in n}
    if package == "fcop":
        expected = {p.name: p.read_bytes() for p in (source / "src/fcop/rules/_data/v4").iterdir() if p.is_file()}
        assert canonical == expected and len(canonical) == 19
        manifest = json.loads(canonical["manifest.json"])
        assert len(manifest["artifacts"]) == 18
        for row in manifest["artifacts"]:
            raw = canonical[row["source_path"]]
            assert sha(raw) == row["sha256"] and len(raw) == row["size_bytes"]
    else:
        assert package == "fcop-mcp" and not canonical
        reqs = [Requirement(r) for r in meta.get_all("Requires-Dist", [])]
        core = [r for r in reqs if r.name == "fcop"]
        assert len(core) == 1 and core[0].specifier == SpecifierSet(">=4.0.3,<4.1.0")
    return {"filename": path.name, "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size,
            "package": package, "version": "4.0.3", "description_sha256": sha(description),
            "canonical_members": len(canonical), "members": len(data), "host_targets": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    head = run("git", "rev-parse", args.commit, cwd=repo, text=True).strip()
    # Export canonical Git bytes, not this Windows user's CRLF checkout policy.
    raw = run("git", "-c", "core.autocrlf=false", "archive", "--format=tar", head, cwd=repo)
    epoch = run("git", "show", "-s", "--format=%ct", head, cwd=repo, text=True).strip()
    output = args.output.resolve()
    assert not output.exists(), "Use a fresh proof directory; preserve previous evidence"
    output.mkdir(parents=True)
    sets = []
    for number in (1, 2):
        source = output / f"source-{number}"
        source.mkdir()
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            entries = archive.getmembers()
            assert all(not m.name.startswith("/") and ".." not in Path(m.name).parts
                       and (m.isfile() or m.isdir()) for m in entries)
            archive.extractall(source, filter="data")
        artifacts = output / f"artifacts-{number}"
        env = dict(os.environ, SOURCE_DATE_EPOCH=epoch, PYTHONHASHSEED="0")
        for package in (source, source / "mcp"):
            result = run(sys.executable, "-m", "build", "--no-isolation", "--wheel", "--sdist",
                         "--outdir", str(artifacts), str(package), cwd=source, env=env,
                         stderr=subprocess.STDOUT)
            print(result.decode("utf-8", errors="replace"), flush=True)
        assert {p.name for p in artifacts.iterdir()} == NAMES
        rows = [inspect(p, source) for p in sorted(artifacts.iterdir())]
        result = run(sys.executable, "-m", "twine", "check", "--strict",
                     *[str(artifacts / name) for name in sorted(NAMES)], stderr=subprocess.STDOUT)
        print(result.decode("utf-8", errors="replace"), flush=True)
        sets.append(rows)
    assert sets[0] == sets[1], "Independent archive bytes differ"
    proof = dict(content_commit=head, source_date_epoch=epoch, reproducibility="4/4",
                 twine="8/8", files=sets[0], published=False,
                 tooling={n: version(n) for n in ("build", "hatchling", "twine", "packaging")})
    (output / "package-proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, indent=2))


if __name__ == "__main__":
    main()
