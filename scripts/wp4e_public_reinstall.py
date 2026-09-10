"""Phase B only: read public PyPI bytes, verify accepted hashes, install anew."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    a = p.parse_args()
    manifest = json.loads(a.manifest.read_bytes())
    expected = {r["filename"]: r["sha256"] for r in manifest["files"]}
    assert len(expected) == 4
    work = Path(tempfile.mkdtemp(prefix="wp4e-public-reinstall-"))
    urls = {}
    for package in ("fcop", "fcop-mcp"):
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/4.0.0rc1/json", timeout=60) as response:
            data = json.load(response)
        assert data["info"]["version"] == "4.0.0rc1"
        for row in data["urls"]:
            if row["filename"] in expected:
                assert row["digests"]["sha256"] == expected[row["filename"]]
                assert row["url"].startswith("https://files.pythonhosted.org/")
                urls[row["filename"]] = row["url"]
    assert urls.keys() == expected.keys()
    for name, url in urls.items():
        with urllib.request.urlopen(url, timeout=120) as response:
            raw = response.read()
        assert hashlib.sha256(raw).hexdigest() == expected[name]
        (work / name).write_bytes(raw)
    venv = work / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
    python = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    subprocess.run([str(python), "-m", "pip", "install", "--no-cache-dir",
                    *[str(work / n) for n in sorted(expected) if n.endswith(".whl")]], check=True)
    probe = Path("tests/rc/installed_identity.py").resolve()
    subprocess.run([str(python), "-I", "-B", str(probe)], cwd=work, check=True)
    print(json.dumps(dict(public_pypi_hashes="4/4", clean_install=True, artifacts=expected)))


if __name__ == "__main__":
    main()
