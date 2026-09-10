"""Exact accepted RC input for historical-only assertions, with a pinned hash."""
import hashlib
import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("accepted-rc-fixture.json")
SHA256 = "d6c868d8e92015c11905db31ec4987ee3ffb52eb2e9beab6cdd763ce85e63fd3"


def text(name):
    # Git may materialize this test-only JSON container with CRLF. Canonicalize
    # container line endings only; escaped source bytes inside JSON are unchanged.
    raw = FIXTURE.read_text(encoding="utf-8").encode("utf-8")
    assert hashlib.sha256(raw).hexdigest() == SHA256
    document = json.loads(raw)
    assert document["commit"] == "d5e851c3fa628167999a9f8b7b7b89290e7b8f06"
    return document["files"][name]


def identity_tree(directory):
    for name in ("src/fcop/_version.py", "mcp/src/fcop_mcp/_version.py",
                 "mcp/src/fcop_mcp/routing.py", "pyproject.toml", "mcp/pyproject.toml"):
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text(name), encoding="utf-8")
    return directory
