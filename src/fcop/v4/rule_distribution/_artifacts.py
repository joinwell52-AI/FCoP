"""Bounded, deterministic offline data archives; never a release/build service."""

from __future__ import annotations

import base64
import csv
import gzip
import hashlib
import io
import os
import re
import stat
import tarfile
import zipfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._errors import reject
from ._files import ARTIFACT, OWNERSHIP, external_file
from ._loader import sha
from ._read import package_read, request_shape

_ACTION = "build_artifacts"
_SELECTION = "RULE_SELECTION_INVALID"
_PREFIX = "fcop/rules/_data/v4/"


def local_path(value: Any, code: str, action: str, *, absent_leaf: bool = False) -> Path:
    """An explicit ordinary local path, without following indirect components."""
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        reject(code, action, "Explicit local path required")
    path = Path(value)
    if (not path.is_absolute() or value.startswith(("\\\\", "//"))
            or ".." in path.parts or "\x7f" in value
            or any(p.endswith((".", " ")) or re.fullmatch(r"(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?", p)
                   for p in path.parts[1:])):
        reject(code, action, "Unsafe local path")
    try:
        for part in (path, *path.parents):
            try:
                info = part.lstat()
            except FileNotFoundError:
                if absent_leaf and part == path:
                    continue
                raise
            if stat.S_ISLNK(info.st_mode) or (
                getattr(info, "st_file_attributes", 0) & 0x400
            ):
                reject(code, action, "Indirect local path")
            if part != path and not stat.S_ISDIR(info.st_mode):
                reject(code, action, "Non-directory ancestor")
        return path
    except (OSError, ValueError):
        reject(code, action, "Unavailable local path")


def _destination(root: Path, source: Path, value: Any) -> Path:
    path = local_path(value, OWNERSHIP, _ACTION, absent_leaf=True)
    try:
        resolved = path.resolve()
        for boundary in (root.resolve(), source.parent.resolve()):
            if resolved.is_relative_to(boundary) or boundary.is_relative_to(resolved):
                reject(OWNERSHIP, _ACTION, "Output overlaps an input or workspace boundary")
        if path.exists() and (not path.is_dir() or any(path.iterdir())):
            reject(OWNERSHIP, _ACTION, "Output must be an empty ordinary directory")
        return path
    except (OSError, ValueError, RuntimeError):
        reject(OWNERSHIP, _ACTION, "Output boundary unavailable")


def _wheel(members: dict[str, bytes], identity: str, metadata: bytes) -> bytes:
    payload = dict(members)
    info = f"{identity}.dist-info"
    payload[f"{info}/METADATA"] = metadata
    payload[f"{info}/WHEEL"] = (
        b"Wheel-Version: 1.0\nGenerator: fcop-offline-rule-export\n"
        b"Root-Is-Purelib: true\nTag: py3-none-any\n"
    )
    record = io.StringIO(newline="")
    writer = csv.writer(record, lineterminator="\n")
    for name, raw in sorted(payload.items()):
        digest = base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b"=").decode()
        writer.writerow((name, "sha256=" + digest, len(raw)))
    writer.writerow((f"{info}/RECORD", "", ""))
    payload[f"{info}/RECORD"] = record.getvalue().encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, raw in sorted(payload.items()):
            member = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            archive.writestr(member, raw)
    return output.getvalue()


def _sdist(members: dict[str, bytes], identity: str, version: str, metadata: bytes) -> bytes:
    payload = {**members, "PKG-INFO": metadata}
    # Owned static carrier metadata, not caller/user configuration. No backend
    # is imported or executed by this export action.
    payload["pyproject.toml"] = (
        '[build-system]\nrequires = ["hatchling>=1.21"]\nbuild-backend = "hatchling.build"\n'
        f'[project]\nname = "fcop-rule-data"\nversion = "{version}"\n'
        '[tool.hatch.build.targets.wheel]\npackages = ["fcop"]\n'
    ).encode()
    output = io.BytesIO()
    with (
        gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=0) as compressed,
        tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive,
    ):
        for name, raw in sorted(payload.items()):
            member = tarfile.TarInfo(f"{identity}/{name}")
            member.size, member.mode, member.mtime = len(raw), 0o644, 0
            member.uid = member.gid = 0
            member.uname = member.gname = ""
            archive.addfile(member, io.BytesIO(raw))
    return output.getvalue()


def build_artifacts(root: Path, request: Mapping[str, Any]) -> dict[str, Any]:
    request_shape(request, {"output_directory", "formats", "offline", "build_isolation"}, _ACTION)
    formats = request.get("formats")
    if (not isinstance(formats, list) or not formats
            or any(not isinstance(f, str) or f not in {"wheel", "sdist"} for f in formats)
            or len(set(formats)) != len(formats)
            or request.get("offline") is not True or request.get("build_isolation") is not False):
        reject(_SELECTION, _ACTION, "Explicit offline non-isolated formats required")
    package = package_read(request, _ACTION)
    source = Path(request.get("manifest_path") or (
        Path(__file__).resolve().parents[2] / "rules/_data/v4/manifest.json"
    ))
    manifest_raw = external_file(str(source), ARTIFACT, _ACTION)
    if sha(manifest_raw) != package.manifest_sha256:
        reject(ARTIFACT, _ACTION, "Manifest changed before export")
    output = _destination(root, source, request.get("output_directory"))
    members = {_PREFIX + "manifest.json": manifest_raw}
    members.update({
        _PREFIX + a["source_path"]: package.raw[a["module_id"], a["language"]]
        for a in package.artifacts
    })
    # This is a content-addressed data carrier, not the fcop runtime package or
    # a new project release version. The raw Manifest retains its own identity.
    version = "0+" + package.manifest_sha256
    identity = "fcop_rule_data-" + version
    metadata = (
        f"Metadata-Version: 2.1\nName: fcop-rule-data\nVersion: {version}\n"
        "Summary: Offline canonical rule data export; no adoption or runtime claim\n\n"
    ).encode()
    archives = {}
    if "wheel" in formats:
        archives["wheel"] = (identity + "-py3-none-any.whl", _wheel(members, identity, metadata))
    if "sdist" in formats:
        archives["sdist"] = (identity + ".tar.gz", _sdist(members, identity, version, metadata))
    # Recheck all sources and destination after in-memory archive construction.
    if package_read(request, _ACTION) != package:
        reject(ARTIFACT, _ACTION, "Package changed during export construction")
    _destination(root, source, str(output))
    try:
        if not output.exists():
            output.mkdir()
        for name, raw in archives.values():
            local_path(str(output), OWNERSHIP, _ACTION)
            with (output / name).open("xb") as target:
                target.write(raw)
                target.flush()
                os.fsync(target.fileno())
            if external_file(str(output / name), ARTIFACT, _ACTION) != raw:
                reject(ARTIFACT, _ACTION, "Export byte verification failed")
    except OSError:
        reject(OWNERSHIP, _ACTION, "Export I/O failed; inspect the explicit output directory")
    return {
        "artifacts": {kind: str(output / name) for kind, (name, _) in archives.items()},
        "member_count": len(members), "manifest_sha256": package.manifest_sha256, "offline": True,
    }
