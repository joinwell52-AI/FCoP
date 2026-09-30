"""Canonical v4 Project facade; historical APIs live in compatibility.v3.project.

Only protocol metadata selects a workspace. Host instruction files, role seats
and session governance are not inputs to this facade.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

from fcop.errors import _V4Code
from fcop.v4.creation import _Creation
from fcop.v4.encoding import fail, parse_json, safe_path


class Project:
    """Bind a canonical filesystem workspace and delegate all semantics to Core."""

    def __init__(self, path: Path | str, *, trusted_profiles: Mapping[str, Callable[..., str]] | None = None,
                 strict: bool = True, workspace_dir: Path | str | None = None) -> None:
        self._path = Path(path).resolve()
        self._trusted_profiles = MappingProxyType(dict(trusted_profiles or {}))
        if workspace_dir is not None and (self._path / workspace_dir).resolve() != self._path / "fcop":
            raise fail(_V4Code.UNSUPPORTED_ENCODING, "Canonical workspaces use fcop/")
        self._v4_creation: _Creation | None = None
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
                         encoding: str = "fcop-filesystem/4.0", profiles: Sequence[str] = ()) -> dict[str, Any]:
        self._v4_creation = _Creation.create(self._path, protocol_version=protocol_version,
            encoding=encoding, profiles=profiles, trusted_profiles=self._trusted_profiles)
        return dict(self._v4_creation.manifest)

    def _invoke(self, name: str, *args: Any, **kwargs: Any) -> Any:
        creation = self._v4_creation
        if creation is None:
            raise fail(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Initialize a canonical 4.0 workspace first", operation=name)
        try:
            handler = creation.handler(name)
            if handler is None:
                raise fail(_V4Code.OPERATION_NOT_IMPLEMENTED, "Unknown Core operation", operation=name)
            return handler(*args, **kwargs)
        except Exception as exc:
            from fcop.errors import V4ProtocolError
            if isinstance(exc, V4ProtocolError):
                if exc.operation_ref is None:
                    exc.operation_ref = kwargs.get("operation_id") or name
                if exc.subject_ref is None:
                    exc.subject_ref = kwargs.get("subject_ref") or kwargs.get("task_id") or creation.manifest.get("workspace_id")
            raise

    def create_task(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate create_task to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("create_task", *args, **kwargs))

    def derive_workspace(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate derive_workspace to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("derive_workspace", *args, **kwargs))

    def read_task(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate read_task to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("read_task", *args, **kwargs))

    def write_report(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate write_report to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("write_report", *args, **kwargs))

    def write_issue(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate write_issue to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("write_issue", *args, **kwargs))

    def write_review(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate write_review to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("write_review", *args, **kwargs))

    def mark_human_approved(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate mark_human_approved to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("mark_human_approved", *args, **kwargs))

    def list_reports(self, *args: Any, **kwargs: Any) -> list[dict[str, Any]]:
        """Delegate list_reports to the existing v4 Core implementation."""
        return cast(list[dict[str, Any]], self._invoke("list_reports", *args, **kwargs))

    def read_report(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate read_report to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("read_report", *args, **kwargs))

    def inspect_state(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate inspect_state to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("inspect_state", *args, **kwargs))

    def transition(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate transition to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("transition", *args, **kwargs))

    def family_digest(self, *args: Any, **kwargs: Any) -> str:
        """Delegate family_digest to the existing v4 Core implementation."""
        return cast(str, self._invoke("family_digest", *args, **kwargs))

    def inspect_family(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate inspect_family to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("inspect_family", *args, **kwargs))

    def merge_branches(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate merge_branches to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("merge_branches", *args, **kwargs))

    def rule_distribution(self, *args: Any, **kwargs: Any) -> Mapping[str, Any]:
        """Delegate rule_distribution to the existing v4 Core implementation."""
        return cast(Mapping[str, Any], self._invoke("rule_distribution", *args, **kwargs))

    def recover_operation(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate recover_operation to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("recover_operation", *args, **kwargs))

    def inject_fault(self, *args: Any, **kwargs: Any) -> None:
        """Delegate inject_fault to the existing v4 Core implementation."""
        self._invoke("inject_fault", *args, **kwargs)

    def export_archive(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Delegate export_archive to the existing v4 Core implementation."""
        return cast(dict[str, Any], self._invoke("export_archive", *args, **kwargs))
