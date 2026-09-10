"""Build separate historical fixture dependencies, never label them RC artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from wp4d_build import BASE, EPOCH, export


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    repo, out = Path.cwd(), args.output.resolve()
    assert not out.exists() and not out.is_relative_to(repo)
    out.mkdir(parents=True)
    source, wheels = out / "historical-source", out / "wheels"
    export(repo, BASE, source)
    wheels.mkdir()
    import os
    env = {**os.environ, "SOURCE_DATE_EPOCH": EPOCH, "PYTHONDONTWRITEBYTECODE": "1"}
    for package in (source, source / "mcp"):
        subprocess.run([sys.executable, "-m", "build", "--no-isolation", "--wheel",
                        "--outdir", str(wheels), str(package)], env=env, check=True)
    expected = ["fcop-3.2.5-py3-none-any.whl", "fcop_mcp-3.2.5-py3-none-any.whl"]
    assert sorted(p.name for p in wheels.iterdir()) == expected
    venv = out / "producer"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / "bin/python"  # This helper is invoked by the Ubuntu build job.
    subprocess.run([str(python), "-m", "pip", "install", str(wheels / expected[0])], check=True)
    artifact = out / "artifact"
    artifact.mkdir()
    import shutil
    for name in expected:
        shutil.copyfile(wheels / name, artifact / name)
    subprocess.run([str(python), "-I", "-B", str(repo / "tests/rc/legacy_fixture.py"),
                    "generate", str(out / "fixture-workspace"), str(artifact / "workspace.json")], check=True)
    files = [{ "filename": p.name, "bytes": p.stat().st_size,
               "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
             for p in sorted(artifact.iterdir())]
    (artifact / "historical-manifest.json").write_text(json.dumps(dict(
        purpose="historical fixtures, NOT RC candidates", commit=BASE, files=files,
    ), sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
