"""Distribution-local path validation and immutable evidence I/O."""

from __future__ import annotations

import os
import re
import stat
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Any

from fcop.errors import V4ProtocolError
from fcop.v4.encoding import canonical, publish, safe_path

from ._errors import reject
from ._loader import parse, read_file, sha

INTERNAL = "fcop/internal/rule-distribution"
ADOPTION = "RULE_ADOPTION_REQUIRED"
RECOVERY = "RULE_DEPLOYMENT_RECOVERY_REQUIRED"
OWNERSHIP = "RULE_OWNERSHIP_CONFLICT"
ARTIFACT = "RULE_ARTIFACT_MISMATCH"


def hexadecimal(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def path_at(root: Path, relative: Any, code: str, action: str) -> Path:
    if (
        not isinstance(relative, str) or not relative
        or any(c in relative for c in "\\:< >\"|?*".replace(" ", ""))
        or any(ord(c) < 32 or ord(c) == 127 for c in relative)
        or any(p in {"", ".", ".."} or p.endswith((".", " "))
               or re.fullmatch(r"(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", p)
               for p in relative.split("/"))
    ):
        reject(code, action, "Unsafe distribution-relative path")
    try:
        return safe_path(root, relative)
    except (V4ProtocolError, OSError, ValueError):
        reject(code, action, "Unsafe distribution path component")


def external_file(value: Any, code: str, action: str) -> bytes:
    if not isinstance(value, str) or not value or "\x00" in value:
        reject(code, action, "Explicit local regular file required")
    path = Path(value)
    extended_local = os.name == "nt" and re.match(r"^\\\\\?\\[A-Za-z]:\\", str(path)) is not None
    if not path.is_absolute() or (str(path).startswith("\\\\") and not extended_local):
        reject(code, action, "Explicit local absolute input required")
    if os.name == "nt" and not extended_local:
        path = Path("\\\\?\\" + str(path))
    try:
        for part in (path, *path.parents):
            info = part.lstat()
            if stat.S_ISLNK(info.st_mode) or (
                getattr(info, "st_file_attributes", 0)
                & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
            ):
                reject(code, action, "Indirect local input is forbidden")
        return read_file(path, code, action)
    except (OSError, ValueError):
        reject(code, action, "Local input unavailable")


def reference_bytes(root: Path, ref: Any, kind: str, code: str, action: str) -> bytes:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or not hexadecimal(ref["sha256"]):
        reject(code, action, "Explicit complete byte identity required")
    if ref["path"] != f"{INTERNAL}/{kind}/{ref['sha256']}.json":
        reject(code, action, "Receipt filename identity mismatch")
    raw = read_file(path_at(root, ref["path"], code, action), code, action)
    if sha(raw) != ref["sha256"]:
        reject(code, action, "Receipt bytes do not match identity")
    return raw


def receipt(root: Path, ref: Any, kind: str, code: str, action: str) -> dict[str, Any]:
    return parse(reference_bytes(root, ref, kind, code, action), code, action)


def json_bytes(value: Mapping[str, Any]) -> bytes:
    return canonical(value) + b"\n"


def timestamp(value: Any, code: str, action: str) -> str:
    if not isinstance(value, str):
        reject(code, action, "Explicit timezone-aware timestamp required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None or "T" not in value:
            raise ValueError
    except ValueError:
        reject(code, action, "Invalid explicit timestamp")
    return value


def append_bytes(root: Path, relative: str, raw: bytes, action: str) -> None:
    path = path_at(root, relative, RECOVERY, action)
    if path.exists():
        if read_file(path, RECOVERY, action) != raw:
            reject(RECOVERY, action, "Immutable evidence conflict")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path_at(root, relative, RECOVERY, action)
    try:
        publish(path, raw)
    except V4ProtocolError:
        if not path.is_file() or path.read_bytes() != raw:
            reject(RECOVERY, action, "Evidence publication interrupted")


def append_receipt(root: Path, kind: str, value: dict[str, Any], action: str) -> dict[str, str]:
    raw = json_bytes(value)
    ref = {"path": f"{INTERNAL}/{kind}/{sha(raw)}.json", "sha256": sha(raw)}
    append_bytes(root, ref["path"], raw, action)
    return ref


def current_bytes(root: Path, relative: str, action: str) -> bytes | None:
    path = path_at(root, relative, OWNERSHIP, action)
    if not os.path.lexists(path):
        return None
    return read_file(path, OWNERSHIP, action)
