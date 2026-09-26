"""Canonical v4 Project facade; historical APIs live in compatibility.v3.project.

Only protocol metadata selects a workspace. Host instruction files, role seats
and session governance are not inputs to this facade.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Any

from fcop.errors import _V4Code
from fcop.v4.creation import _Creation
from fcop.v4.encoding import fail, parse_json, safe_path


class Project:
    """Bind a canonical filesystem workspace and delegate all semantics to Core."""

    def __init__(self, path: Path | str, *, trusted_profiles: Mapping[str, Callable] | None = None,
                 strict: bool = True, workspace_dir: Path | str | None = None):
        self._path = Path(path).resolve()
        self._trusted_profiles = MappingProxyType(dict(trusted_profiles or {}))
        if workspace_dir is not None and (self._path / workspace_dir).resolve() != self._path / "fcop":
            raise fail(_V4Code.UNSUPPORTED_ENCODING, "Canonical workspaces use fcop/")
        self._v4_creation = None
        manifest = safe_path(self._path, "fcop/fcop.json")
        if manifest.exists():
            declaration = parse_json(manifest.read_bytes(), classification=True)
            if declaration.get("protocol_version") != "4.0":
                raise fail(_V4Code.UNSUPPORTED_WORKSPACE_VERSION,
                           "Use fcop.compatibility.v3.project.Project for historical workspaces")
            self._v4_creation = _Creation.open_if_declared(self._path, trusted_profiles=self._trusted_profiles)

    @property
    def path(self) -> Path:
        return self._path

    @property
    def config_path(self) -> Path:
        return self._path / "fcop/fcop.json"

    @property
    def workspace_dir(self) -> Path:
        return self._path / "fcop"

    @property
    def topology(self) -> str:
        return "v4" if self.is_initialized() else "empty"

    @property
    def workspace_layout(self) -> str:
        return "canonical"

    def is_initialized(self) -> bool:
        return self._v4_creation is not None

    def create_workspace(self, *, protocol_version: str = "4.0",
                         encoding: str = "fcop-filesystem/4.0", profiles: Sequence[str] = ()) -> dict:
        self._v4_creation = _Creation.create(self._path, protocol_version=protocol_version,
            encoding=encoding, profiles=profiles, trusted_profiles=self._trusted_profiles)
        return dict(self._v4_creation.manifest)

    def _invoke(self, name: str, *args: Any, **kwargs: Any) -> Any:
        creation = self._v4_creation
        if creation is None:
            raise fail(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Initialize a canonical 4.0 workspace first", operation=name)
        try:
            return creation.handler(name)(*args, **kwargs)
        except Exception as exc:
            from fcop.errors import V4ProtocolError
            if isinstance(exc, V4ProtocolError):
                if exc.operation_ref is None:
                    exc.operation_ref = kwargs.get("operation_id") or name
                if exc.subject_ref is None:
                    exc.subject_ref = kwargs.get("subject_ref") or kwargs.get("task_id") or creation.manifest.get("workspace_id")
            raise


def _delegate(name):
    def call(self, *args, **kwargs):
        return self._invoke(name, *args, **kwargs)
    call.__name__ = name
    call.__doc__ = f"Delegate {name} to the existing v4 Core implementation."
    return call


# Core API includes operations beyond the MCP surface. No legacy dispatcher.
for _name in ("create_task", "derive_workspace", "read_task", "write_report", "write_issue",
              "write_review", "mark_human_approved", "list_reports", "read_report", "inspect_state",
              "transition", "family_digest", "inspect_family", "merge_branches", "rule_distribution",
              "recover_operation", "inject_fault", "export_archive"):
    setattr(Project, _name, _delegate(_name))
