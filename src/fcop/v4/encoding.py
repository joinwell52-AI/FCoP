"""Private filesystem encoding primitives. No policy, scheduler, or registry."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
import time
import unicodedata
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Any, cast

import yaml

from fcop.errors import V4ProtocolError, _V4Code

STAGES = ("inbox", "active", "review", "done", "archive")
BUCKETS = {"REPORT": "reports", "ISSUE": "issues", "REVIEW": "reviews"}
ID_RE = re.compile(r"(?:TASK|REPORT|ISSUE|REVIEW)-[A-Za-z0-9][A-Za-z0-9._-]*\Z")
OP_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}\Z")


def fail(
    code: _V4Code, message: str, *, operation: str | None = None, subject: str | None = None
) -> V4ProtocolError:
    return V4ProtocolError(code, message, operation_ref=operation, subject_ref=subject)


def normalize(value: str) -> str:
    if not isinstance(value, str):
        raise fail(_V4Code.INVALID_ENVELOPE, "Expected a string")
    return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))


def canonical(value: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Request is not canonical UTF-8 JSON") from exc


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_text(data: bytes) -> str:
    try:
        value = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Invalid UTF-8") from exc
    if "\r" in value or value.startswith("\ufeff"):
        raise fail(_V4Code.INVALID_ENVELOPE, "Encoding requires UTF-8 without BOM and LF")
    return value


def _unique_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise fail(_V4Code.INVALID_ENVELOPE, "Duplicate JSON key")
        result[key] = value
    return result


def parse_json(data: bytes, *, classification: bool = False) -> dict[str, Any]:
    """Unique-key strict UTF-8 JSON; defer newline policy only for classification."""
    def invalid_constant(value: str) -> Any:
        raise ValueError(f"Non-JSON constant: {value}")

    try:
        result = json.loads(
            data.decode("utf-8") if classification else strict_text(data),
            object_pairs_hook=_unique_pairs,
            parse_constant=invalid_constant,
        )
        if not isinstance(result, dict):
            raise ValueError("Expected object")
        return result
    except ValueError as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Invalid JSON fact") from exc


def read_json(path: Path) -> dict[str, Any]:
    try:
        return parse_json(path.read_bytes())
    except OSError as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Unreadable JSON fact", subject=str(path)) from exc


class _UniqueLoader(yaml.SafeLoader):
    pass


def _mapping(loader: _UniqueLoader, node: yaml.MappingNode) -> dict[str, Any]:
    result: dict[str, Any] = {}
    construct = cast(Any, loader).construct_object
    for key_node, value_node in node.value:
        key = construct(key_node, deep=True)
        if not isinstance(key, str) or key in result:
            raise fail(_V4Code.INVALID_ENVELOPE, "Non-string or duplicate YAML key")
        result[key] = construct(value_node, deep=True)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def parse_envelope(path: Path) -> dict[str, Any]:
    try:
        text = strict_text(path.read_bytes())
        if not text.startswith("---\n") or "\n---\n" not in text[3:]:
            raise ValueError("Missing frontmatter delimiters")
        fields = yaml.load(text.split("---\n", 2)[1], Loader=_UniqueLoader)
        if not isinstance(fields, dict):
            raise ValueError("Expected YAML mapping")
        return fields
    except (OSError, ValueError, yaml.YAMLError) as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Invalid envelope", subject=str(path)) from exc


def envelope_bytes(fields: dict[str, Any], body: str) -> bytes:
    header = yaml.safe_dump(fields, allow_unicode=True, sort_keys=False)
    try:
        return ("---\n" + header + "---\n\n" + normalize(body).rstrip("\n") + "\n").encode("utf-8")
    except UnicodeEncodeError as exc:
        raise fail(_V4Code.INVALID_ENVELOPE, "Envelope is not valid UTF-8") from exc


def safe_path(root: Path, relative: str) -> Path:
    part = Path(relative)
    if part.is_absolute() or part.drive or ".." in part.parts or ":" in relative:
        raise fail(_V4Code.INVALID_ENVELOPE, "Unsafe workspace-relative path", subject=relative)
    candidate = root / part
    # Reject symlinks, including in-workspace redirects; no alternate namespace.
    for component in (candidate, *candidate.parents):
        if component == root.parent:
            break
        reparse = component.exists() and bool(
            getattr(component.lstat(), "st_file_attributes", 0)
            & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        )
        if component.is_symlink() or reparse:
            raise fail(
                _V4Code.INVALID_ENVELOPE, "Symlink/junction in workspace path", subject=relative
            )
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise fail(_V4Code.INVALID_ENVELOPE, "Path escapes workspace", subject=relative)
    return candidate


def sync_directory(path: Path) -> None:
    # Windows publication uses MoveFileEx WRITE_THROUGH below. POSIX persists
    # the directory entry explicitly; an unsupported operation fails closed.
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def supported_local(root: Path) -> None:
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes

        if str(root).startswith("\\\\"):
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "UNC/network paths are unsupported")
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        fs = ctypes.create_unicode_buffer(32)
        flags = wintypes.DWORD()
        get_volume = kernel.GetVolumeInformationW
        get_volume.argtypes = [
            wintypes.LPCWSTR,
            wintypes.LPWSTR,
            wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.POINTER(wintypes.DWORD),
            wintypes.LPWSTR,
            wintypes.DWORD,
        ]
        get_volume.restype = wintypes.BOOL
        if not get_volume(root.anchor, None, 0, None, None, ctypes.byref(flags), fs, 32):
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "Cannot establish filesystem capabilities")
        get_drive = kernel.GetDriveTypeW
        get_drive.argtypes = [wintypes.LPCWSTR]
        get_drive.restype = wintypes.UINT
        if get_drive(root.anchor) != 3 or fs.value != "NTFS":
            raise fail(
                _V4Code.UNSUPPORTED_FILESYSTEM, "Only local fixed NTFS volumes are supported"
            )
    elif sys.platform == "darwin":
        import ctypes

        # Darwin's public 64-bit statfs ABI and MNT_LOCAL:
        # https://github.com/apple-oss-distributions/xnu/blob/main/bsd/sys/mount.h
        class _MountInfo(ctypes.Structure):
            _fields_ = [
                ("sizes", ctypes.c_uint32 * 2),
                ("counts", ctypes.c_uint64 * 5),
                ("identity", ctypes.c_int32 * 2),
                ("owner", ctypes.c_uint32),
                ("kind", ctypes.c_uint32),
                ("flags", ctypes.c_uint32),
                ("subtype", ctypes.c_uint32),
                ("format", ctypes.c_char * 16),
                ("mounted_at", ctypes.c_char * 1024),
                ("source", ctypes.c_char * 1024),
                ("extension", ctypes.c_uint32 * 8),
            ]

        libc = ctypes.CDLL(None, use_errno=True)
        statfs = getattr(libc, "statfs$INODE64", libc.statfs)
        statfs.argtypes = [ctypes.c_char_p, ctypes.POINTER(_MountInfo)]
        statfs.restype = ctypes.c_int
        location = root
        while not location.exists() and location != location.parent:
            location = location.parent
        info = _MountInfo()
        if (
            statfs(os.fsencode(location), ctypes.byref(info))
            or not (info.flags & 0x1000)
            or info.format not in {b"apfs", b"hfs"}
        ):
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "Uncertified local macOS filesystem")
    elif os.name != "posix":
        raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "Unsupported filesystem platform")
    else:
        # On Linux, reject remote/unknown mounts rather than infer safety from
        # successful rename. Non-Linux/non-macOS POSIX hosts fail closed.
        mounts = Path("/proc/mounts")
        if not mounts.exists():
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "POSIX mount capabilities are unverified")
        matches = []
        for line in mounts.read_text(encoding="utf-8").splitlines():
            parts = line.split()
            mount = Path(parts[1].replace("\\040", " "))
            if root.is_relative_to(mount):
                matches.append((len(mount.parts), parts[2]))
        if not matches or max(matches)[1] not in {
            "ext4",
            "ext3",
            "xfs",
            "btrfs",
            "tmpfs",
            "overlay",
        }:
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "Uncertified local POSIX filesystem")


def publish(path: Path, data: bytes) -> None:
    """Fsync same-directory temporary, then publish without replacing a target.

    On errors the temporary is deliberately retained as recovery evidence.
    This is creation only, never lifecycle migration or automatic recovery.
    """
    fd, temporary = tempfile.mkstemp(
        prefix=f".fcop-create-{path.stem}-", suffix=".tmp", dir=path.parent
    )
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes

            move = ctypes.WinDLL("kernel32", use_last_error=True).MoveFileExW
            move.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD]
            move.restype = wintypes.BOOL
            # WRITE_THROUGH, deliberately no REPLACE_EXISTING.
            if not move(temporary, str(path), 0x8):
                raise ctypes.WinError(ctypes.get_last_error())
        else:
            os.link(temporary, path)
            sync_directory(path.parent)
            os.unlink(temporary)
            sync_directory(path.parent)
    except OSError as exc:
        code = (
            _V4Code.TARGET_ALREADY_EXISTS_DIFFERENT
            if path.exists()
            else _V4Code.UNSUPPORTED_FILESYSTEM
        )
        raise fail(
            code, "No-overwrite publication failed; temporary preserved", subject=str(path)
        ) from exc


def publish_directory(staging: Path, target: Path) -> None:
    """Publish a complete sibling directory with a kernel no-replace rename.

    No check-then-rename fallback: missing platform support fails closed.
    A failed staging remains evidence; this primitive never removes a tree.
    """
    if staging.parent != target.parent or staging.stat().st_dev != target.parent.stat().st_dev:
        raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "Initialization must stay on one filesystem")
    try:
        import ctypes

        if sys.platform == "win32":
            from ctypes import wintypes

            move = ctypes.WinDLL("kernel32", use_last_error=True).MoveFileExW
            move.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD]
            move.restype = wintypes.BOOL
            if not move(str(staging), str(target), 0x8):  # WRITE_THROUGH, no replace/copy
                raise ctypes.WinError(ctypes.get_last_error())
        elif sys.platform == "linux":
            libc = ctypes.CDLL(None, use_errno=True)
            rename = getattr(libc, "renameat2", None)
            if rename is None:
                raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "renameat2 is unavailable")
            rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p,
                               ctypes.c_uint]
            rename.restype = ctypes.c_int
            # AT_FDCWD = -100; RENAME_NOREPLACE = 1.
            if rename(-100, os.fsencode(staging), -100, os.fsencode(target), 1):
                number = ctypes.get_errno()
                raise OSError(number, os.strerror(number))
        elif sys.platform == "darwin":
            libc = ctypes.CDLL(None, use_errno=True)
            rename = getattr(libc, "renamex_np", None)
            if rename is None:
                raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "renamex_np is unavailable")
            rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
            rename.restype = ctypes.c_int
            if rename(os.fsencode(staging), os.fsencode(target), 0x4):  # RENAME_EXCL
                number = ctypes.get_errno()
                raise OSError(number, os.strerror(number))
        else:
            raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "No certified directory publication")
    except OSError as exc:
        raise fail(
            _V4Code.TARGET_ALREADY_EXISTS_DIFFERENT
            if target.exists() else _V4Code.RECOVERY_REQUIRED,
            "Directory publication failed; staging preserved",
            operation="create_workspace",
        ) from exc
    sync_directory(target.parent)


@contextmanager
def operation_lock(path: Path, *, timeout: float = 15) -> Iterator[None]:
    """A retained zero-byte lock inode plus a kernel lock, never an age lease."""
    # O_CREAT is harmless under races: nobody replaces or unlinks this inode.
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    acquired = False
    try:
        deadline = time.monotonic() + timeout
        while not acquired:
            try:
                if sys.platform == "win32":
                    import msvcrt

                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError as exc:
                if exc.errno not in {errno.EACCES, errno.EAGAIN, errno.EDEADLK}:
                    raise fail(_V4Code.UNSUPPORTED_FILESYSTEM, "OS locking unavailable") from exc
                if time.monotonic() >= deadline:
                    raise fail(
                        _V4Code.LOCK_RECOVERY_REQUIRED, "Operation lock remains unavailable"
                    ) from exc
                time.sleep(0.01)
        yield
    finally:
        if acquired:
            if sys.platform == "win32":
                import msvcrt

                os.lseek(fd, 0, os.SEEK_SET)
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
