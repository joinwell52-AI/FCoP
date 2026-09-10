"""Exact read-only byte evidence, sharing the accepted Host projection."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._artifacts import local_path
from ._errors import reject
from ._files import ARTIFACT, external_file, hexadecimal
from ._loader import sha
from ._profiles import inspect_profile
from ._projection import framed, new_entry
from ._read import package_read, request_shape
from ._selection import select

_ACTION = "measure_context"
_SELECTION = "RULE_SELECTION_INVALID"


def _identity(path: Path) -> tuple[int, int, int, int]:
    try:
        info = path.stat()
        return info.st_dev, info.st_ino, info.st_mtime_ns, info.st_size
    except OSError:
        reject(ARTIFACT, _ACTION, "Historical input unavailable during identity check")


def measure_context(root: Path, request: Mapping[str, Any]) -> dict[str, Any]:
    request_shape(request, {"historical_surfaces"}, _ACTION)
    package = package_read(request, _ACTION)
    host, profile_raw = inspect_profile(request, _ACTION, measurement_only=True)
    selected = select(root, package, request, _ACTION, validated_profile=host, measurement_only=True)
    if selected["assembly_id"] not in {"sequential", "parallel"}:
        reject(_SELECTION, _ACTION, "Explicit business assembly required")
    historical = request.get("historical_surfaces")
    if not isinstance(historical, list) or len(historical) != 6:
        reject(_SELECTION, _ACTION, "Exactly six historical surfaces required")
    paths: set[Path] = set()
    measured: list[dict[str, Any]] = []
    observed: list[tuple[Path, bytes, tuple[int, int, int, int]]] = []
    for ref in historical:
        if (not isinstance(ref, dict) or set(ref) != {"path", "sha256"}
                or not hexadecimal(ref["sha256"])):
            reject(_SELECTION, _ACTION, "Explicit path and raw hash required")
        path = local_path(ref["path"], ARTIFACT, _ACTION)
        canonical_path = path.resolve()
        if canonical_path in paths:
            reject(_SELECTION, _ACTION, "Duplicate historical surface")
        paths.add(canonical_path)
        stamp = _identity(path)
        raw = external_file(str(path), ARTIFACT, _ACTION)
        if sha(raw) != ref["sha256"]:
            reject(ARTIFACT, _ACTION, "Historical raw byte mismatch")
        observed.append((path, raw, stamp))
        measured.append({"path": ref["path"], "sha256": ref["sha256"], "size_bytes": len(raw)})
    target = host["target_paths"][0]
    projected = new_entry(host, framed(package, host, selected, target, _ACTION))
    if len(projected) > host["max_projection_bytes"]:
        reject("RULE_PROJECTION_LIMIT", _ACTION, "Full projection exceeds the static profile cap")
    if (external_file(request.get("host_profile_path"), ARTIFACT, _ACTION) != profile_raw
            or package_read(request, _ACTION) != package):
        reject(ARTIFACT, _ACTION, "Projection inputs changed during measurement")
    for path, raw, stamp in observed:
        if external_file(str(path), ARTIFACT, _ACTION) != raw:
            reject(ARTIFACT, _ACTION, "Historical input changed during measurement")
        if _identity(path) != stamp:
            reject(ARTIFACT, _ACTION, "Historical input identity changed")
    return {
        "projection_size_bytes": len(projected), "limit_unit": "utf8_bytes",
        "estimator": {"algorithm": "exact-utf8-byte-count", "version": "1"},
        "runtime_consumption_verified": None,
        "selected_modules": selected["selected_modules"],
        "selected_languages": selected["selected_languages"], "historical_surfaces": measured,
    }
