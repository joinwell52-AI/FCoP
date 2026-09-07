"""Strict offline raw-byte loading, without caches or implicit dependencies."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from ._contract import ARTIFACT_FIELDS, DEPS, MODULES, OWNED
from ._errors import reject

_MANIFEST = "RULE_MANIFEST_INVALID"
_ARTIFACT = "RULE_ARTIFACT_MISMATCH"
_HEX = re.compile(r"[0-9a-f]{64}")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def text_bytes(raw: bytes, code: str, action: str) -> str:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        reject(code, action, "Invalid UTF-8")
    if (
        "\ufeff" in text or "\r" in text or "\x7f" in text
        or any(ord(c) < 32 and c not in "\t\n" for c in text)
        or not text.endswith("\n") or text.endswith("\n\n")
    ):
        reject(code, action, "Invalid raw Encoding")
    return text


def read_file(path: Path, code: str, action: str) -> bytes:
    try:
        if not path.is_file():
            reject(code, action, "Required regular file unavailable")
        return path.read_bytes()
    except (OSError, ValueError):
        reject(code, action, "Required file unreadable")


def parse(raw: bytes, code: str, action: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                reject(code, action, "Duplicate JSON key")
            result[key] = value
        return result

    def nonfinite(value: str) -> Any:
        reject(code, action, "Non-finite JSON value")

    try:
        value = json.loads(text_bytes(raw, code, action), object_pairs_hook=pairs,
                           parse_constant=nonfinite)
    except (ValueError, RecursionError):
        reject(code, action, "Invalid JSON")
    if not isinstance(value, dict):
        reject(code, action, "Expected JSON object")
    return value


def contained(root: Path, relative: Any, code: str, action: str) -> Path:
    if (
        not isinstance(relative, str) or not relative or "\\" in relative
        or ":" in relative or "\x00" in relative
        or any(part in {"", ".", ".."} for part in relative.split("/"))
        or PurePosixPath(relative).is_absolute()
    ):
        reject(code, action, "Invalid relative source path")
    try:
        resolved = (root / relative).resolve(strict=True)
        if not resolved.is_relative_to(root.resolve(strict=True)):
            reject(code, action, "Source escaped its declared boundary")
        return resolved
    except (OSError, ValueError, RuntimeError):
        reject(code, action, "Source path unavailable")


@dataclass(frozen=True)
class _Package:
    manifest: dict[str, Any]
    manifest_sha256: str
    artifacts: list[dict[str, Any]]
    raw: dict[tuple[str, str], bytes]

    def summary(self) -> dict[str, Any]:
        return {
            "protocol_version": "4.0",
            "package_version": self.manifest["package_version"],
            "manifest_sha256": self.manifest_sha256,
            "artifacts": self.artifacts,
            "clause_owners": {ref: module for module, refs in OWNED.items() for ref in refs},
        }


def load(manifest_path: Any, action: str) -> _Package:
    if manifest_path is None:
        path = Path(__file__).resolve().parents[2] / "rules/_data/v4/manifest.json"
    elif isinstance(manifest_path, str) and manifest_path and "\x00" not in manifest_path:
        path = Path(manifest_path)
        if not path.is_absolute():
            reject(_MANIFEST, action, "External Manifest must have an explicit absolute path")
    else:
        reject(_MANIFEST, action, "Invalid Manifest identity")
    raw = read_file(path, _MANIFEST, action)
    manifest = parse(raw, _MANIFEST, action)
    if (
        set(manifest) != {"manifest_schema", "protocol_version", "package_version", "artifacts"}
        or manifest["manifest_schema"] != "fcop-rule-distribution/v1"
        or manifest["protocol_version"] != "4.0"
        or not isinstance(manifest["package_version"], str)
        or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?", manifest["package_version"]) is None
    ):
        reject(_MANIFEST, action, "Manifest identity or field set invalid")
    artifacts = manifest["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 18:
        reject(_MANIFEST, action, "Expected eighteen artifact records")
    seen: set[tuple[str, str]] = set()
    bodies: dict[tuple[str, str], bytes] = {}
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != ARTIFACT_FIELDS:
            reject(_MANIFEST, action, "Invalid artifact field set")
        module, language = artifact["module_id"], artifact["language"]
        if not isinstance(module, str) or module not in MODULES or language not in ("en", "zh"):
            reject(_MANIFEST, action, "Unknown module or language")
        key = (module, language)
        if key in seen:
            reject(_MANIFEST, action, "Duplicate artifact identity")
        seen.add(key)
        if (
            artifact["normative_clause_refs"] != OWNED[module]
            or artifact["depends_on"] != DEPS[module]
            or type(artifact["load_order"]) is not int
            or artifact["load_order"] != (MODULES.index(module) + 1) * 10
            or artifact["audience"] != "business-agent"
            or artifact["required_when"] != ("branch-family" if module == "convergence" else "common")
            or artifact["conflicts_with"] != []
            or type(artifact["size_bytes"]) is not int or artifact["size_bytes"] < 0
            or not isinstance(artifact["sha256"], str) or not _HEX.fullmatch(artifact["sha256"])
        ):
            reject(_MANIFEST, action, "Invalid ownership, graph, parity or field type")
        source = contained(path.parent, artifact["source_path"], _ARTIFACT, action)
        if artifact["source_path"] != f"{module}.{language}.md":
            reject(_ARTIFACT, action, "Source path does not match canonical identity")
        body = read_file(source, _ARTIFACT, action)
        text = text_bytes(body, _ARTIFACT, action)
        if "<!-- fcop:" in text:
            reject(_ARTIFACT, action, "Reserved Host marker in source")
        if sha(body) != artifact["sha256"] or len(body) != artifact["size_bytes"]:
            reject(_ARTIFACT, action, "Raw artifact identity mismatch")
        bodies[key] = body
    if seen != {(module, lang) for module in MODULES for lang in ("en", "zh")}:
        reject(_MANIFEST, action, "Incomplete bilingual artifact set")
    ordered = sorted(artifacts, key=lambda a: (a["load_order"], a["module_id"], a["language"]))
    return _Package(manifest, sha(raw), ordered, bodies)
