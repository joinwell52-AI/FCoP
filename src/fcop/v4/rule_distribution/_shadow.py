"""Bounded, explicitly authorized downstream reads; no product execution."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

from ._errors import reject
from ._files import ADOPTION, external_file, hexadecimal
from ._loader import parse, sha
from ._read import request_shape

_FIELDS = {
    "authorization_kind",
    "scope",
    "downstream_kind",
    "downstream_root",
    "allowed_relative_paths",
    "expected_sha256",
}


def _root(value: Any) -> str:
    # Lexical only. In particular do not resolve/stat the downstream root.
    if (
        not isinstance(value, str)
        or not value
        or any(ord(c) < 32 for c in value)
        or value.startswith(("\\\\", "//"))
    ):
        reject(ADOPTION, "shadow", "Explicit local normalized root required")
    path = Path(value)
    if not path.is_absolute() or str(path) != os.path.normpath(value) or ".." in path.parts:
        reject(ADOPTION, "shadow", "Root must be normalized and absolute")
    return str(path)


def _relative(value: Any) -> str:
    if (
        not isinstance(value, str)
        or not value
        or PurePosixPath(value).is_absolute()
        or any(c in value for c in '\\:*?<>|"')
        or any(ord(c) < 32 for c in value)
        or any(
            p in {"", ".", ".."}
            or p.endswith((".", " "))
            or re.fullmatch(r"(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", p)
            for p in value.split("/")
        )
    ):
        reject(ADOPTION, "shadow", "Only exact ordinary relative file paths are allowed")
    return value


def _pins(raw: bytes) -> list[str]:
    # Return only literal semver pins, never arbitrary matching text or bodies.
    text = raw.decode("utf-8", errors="replace")
    found = {
        f"{name}=={version}"
        for name, version in re.findall(r"\b(fcop(?:-mcp)?)==([0-9]+\.[0-9]+\.[0-9]+)\b", text)
    }
    for name, version in re.findall(
        r'\b(FCOP(?:_MCP)?_ADOPTED_VERSION)\s*=\s*"([0-9]+\.[0-9]+\.[0-9]+)"', text
    ):
        found.add(f"{'fcop-mcp' if '_MCP_' in name else 'fcop'}=={version}")
    return sorted(found)


def shadow(request: Mapping[str, Any]) -> dict[str, Any]:
    action = "shadow"
    ref = request.get("shadow_authorization_ref")
    if (
        request.get("deploy") is not False
        or not isinstance(ref, dict)
        or set(ref) != {"path", "sha256"}
        or not hexadecimal(ref.get("sha256"))
    ):
        reject(
            ADOPTION, action, "Explicit read-only authorization required before downstream access"
        )
    target = _root(request.get("downstream_path"))
    auth_path = _root(ref.get("path"))
    if Path(auth_path).is_relative_to(Path(target)):
        reject(ADOPTION, action, "Authorization must be outside the downstream target")
    auth_raw = external_file(auth_path, ADOPTION, action)
    if sha(auth_raw) != ref["sha256"]:
        reject(ADOPTION, action, "Authorization digest mismatch")
    auth = parse(auth_raw, ADOPTION, action)
    if (
        set(auth) != _FIELDS
        or auth.get("authorization_kind") != "fcop-rule-distribution-shadow"
        or auth.get("scope") != "read-only"
        or auth.get("downstream_kind") != "fcop-consumer"
        or auth.get("downstream_root") != target
    ):
        reject(ADOPTION, action, "Read authorization scope or target mismatch")
    paths, expected = auth.get("allowed_relative_paths"), auth.get("expected_sha256")
    if not isinstance(paths, list) or not 1 <= len(paths) <= 16 or not isinstance(expected, dict):
        reject(ADOPTION, action, "Bounded exact allowlist required")
    paths = [_relative(p) for p in paths]
    if (
        len(set(paths)) != len(paths)
        or set(expected) != set(paths)
        or not all(hexadecimal(d) for d in expected.values())
    ):
        reject(ADOPTION, action, "Allowlist identity mismatch")
    request_shape(request, {"downstream_path", "shadow_authorization_ref", "deploy"}, action)
    if external_file(auth_path, ADOPTION, action) != auth_raw:
        reject(ADOPTION, action, "Authorization changed before downstream access")
    # Admission is complete. No directory enumeration, subprocess or writes.
    bodies = {p: external_file(str(Path(target) / p), ADOPTION, action) for p in paths}
    if any(sha(raw) != expected[p] for p, raw in bodies.items()):
        reject(ADOPTION, action, "Allowlisted downstream bytes differ from authorization")
    for p, raw in bodies.items():
        if external_file(str(Path(target) / p), ADOPTION, action) != raw:
            reject(ADOPTION, action, "Downstream evidence changed during read")
    if external_file(auth_path, ADOPTION, action) != auth_raw:
        reject(ADOPTION, action, "Authorization changed during read")
    return {
        "scope": "read-only",
        "deployed": False,
        "files": [
            {
                "path": p,
                "size_bytes": len(bodies[p]),
                "sha256": expected[p],
                "detected_pins": _pins(bodies[p]),
            }
            for p in paths
        ],
        "runtime_consumption_verified": None,
    }
