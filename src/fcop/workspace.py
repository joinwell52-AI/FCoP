"""Pure protocol workspace observations shared by MCP and Toolkit.

These are non-atomic observations of durable facts, never recovery actions.
Validation delegates to the existing v4 encoding/schema/relation/receipt checks.
"""
from __future__ import annotations

from pathlib import Path

from fcop import Project
from fcop.errors import FcopError, _V4Code
from fcop.v4.creation import _Creation
from fcop.v4.encoding import (
    BUCKETS,
    STAGES,
    canonical,
    digest,
    fail,
    parse_envelope,
    read_json,
    safe_path,
)
from fcop.v4.receipts import RECEIPT_CONTRACT, classify, validate_receipt
from fcop.v4.schema import _validate


def _open(root: Path | str) -> tuple[Project, _Creation]:
    project = Project(root)
    creation = _Creation.open_if_declared(project.path)
    if creation is None:
        raise fail(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "A canonical 4.0 workspace is required")
    creation._check()
    return project, creation


def _paths(root: Path, kind: str) -> list[Path]:
    folders = [f"_lifecycle/{s}" for s in STAGES] if kind == "TASK" else [BUCKETS[kind]]
    return sorted(p for folder in folders for p in safe_path(root, f"fcop/{folder}").glob("*.md"))


def _envelope(project: Project, creation: _Creation, path: Path) -> dict:
    safe_path(project.path, path.relative_to(project.path).as_posix())
    fields = creation._validate(parse_envelope(path), path)
    identity = fields[fields["type"].lower() + "_id"]
    resolved, _ = creation._resolve(identity)
    if resolved != path:
        raise fail(_V4Code.INVALID_ENVELOPE, "Noncanonical envelope path", subject=identity)
    warnings = creation._relations(fields)
    result = {**fields, "path": str(path), "warnings": warnings}
    if fields["type"] == "TASK":
        state = project.inspect_state(task_id=identity)
        if state["last_transition"] is None or state["last_transition"]["to"] != state["stage"]:
            raise fail(_V4Code.INVALID_ENVELOPE, "Lifecycle directory and transition disagree", subject=identity)
        if state["stage"] != "inbox" and state["current_attempt_id"] is None:
            raise fail(_V4Code.ATTEMPT_MISMATCH, "Current attempt is not provable", subject=identity)
        result.update(state)
    return result


def list_envelopes(root: Path | str, kind: str, *, filters: dict | None = None,
                   offset: int = 0, limit: int | None = None) -> dict:
    project, creation = _open(root)
    if offset < 0 or (limit is not None and limit < 0):
        raise fail(_V4Code.INVALID_ENVELOPE, "Invalid pagination")
    values = [_envelope(project, creation, p) for p in _paths(project.path, kind)]
    for key, value in (filters or {}).items():
        if value is not None:
            values = [v for v in values if v.get(key) == value]
    return {"items": values[offset:None if limit is None else offset + limit], "total": len(values)}


def inspect_workspace(root: Path | str) -> dict:
    """Observe canonical facts, including incomplete operations, without writes."""
    project, creation = _open(root)
    errors, warnings, tasks, envelopes, families, operations = [], [], [], [], [], []

    def error(path, exc):
        errors.append(dict(path=str(path), code=str(getattr(exc, "code", "INVALID_DATA")), message=str(exc)))

    for part in [*(f"_lifecycle/{s}" for s in STAGES), *BUCKETS.values(), "operations", "cold"]:
        try:
            target = safe_path(project.path, f"fcop/{part}")
            if not target.is_dir():
                raise fail(_V4Code.INVALID_ENVELOPE, "Missing canonical directory")
        except (FcopError, OSError, ValueError) as exc:
            error(f"fcop/{part}", exc)
    for kind in ("TASK", "REPORT", "ISSUE", "REVIEW"):
        folders = [f"_lifecycle/{s}" for s in STAGES] if kind == "TASK" else [BUCKETS[kind]]
        for folder in folders:
            try:
                directory = safe_path(project.path, f"fcop/{folder}")
                for entry in directory.iterdir():
                    if not entry.is_file() or not entry.name.startswith(kind + "-") or entry.suffix != ".md":
                        error(entry, fail(_V4Code.INVALID_ENVELOPE, "Unexpected canonical bucket entry"))
            except (FcopError, OSError, ValueError) as exc:
                error(folder, exc)
    for kind in ("TASK", "REPORT", "ISSUE", "REVIEW"):
        try:
            paths = _paths(project.path, kind)
        except (FcopError, OSError, ValueError) as exc:
            error(kind, exc)
            continue
        for path in paths:
            try:
                item = _envelope(project, creation, path)
                envelopes.append(item)
                warnings.extend(item["warnings"])
                if kind == "TASK":
                    tasks.append(item)
            except (FcopError, OSError, ValueError) as exc:
                error(path, exc)
    from fcop.v4.merge import _read_receipt, inspect_locked
    for task in tasks:
        if not task.get("branch_of"):
            try:
                families.append(inspect_locked(creation, task["task_id"]))
            except (FcopError, OSError, ValueError) as exc:
                error(task["path"], exc)
    try:
        operation_paths = sorted(safe_path(project.path, "fcop/operations").glob("*.json"))
    except (FcopError, OSError, ValueError) as exc:
        error("fcop/operations", exc)
        operation_paths = []
    for path in operation_paths:
        try:
            safe_path(project.path, path.relative_to(project.path).as_posix())
            value = read_json(path)
            contract = value.get("contract")
            if contract == RECEIPT_CONTRACT:
                validate_receipt(project.path, path, value)
                # A completed historical receipt may precede subsequent transitions.
                state = "COMMITTED" if value["stage"] == "COMMITTED" else classify(project.path, value)
            elif contract == "fcop-create-task-v1":
                _validate("create-operation", value)
                key = digest(canonical({k: value[k] for k in ("workspace_id", "operation_kind", "operation_id")}))
                if value["key"] != key or path.name != f"create-{key}.json":
                    raise fail(_V4Code.IDEMPOTENCY_CONFLICT, "Create operation key/path mismatch")
                _, task = creation._resolve(value["task_id"])
                if task["normalized_request_digest"] != value["digest"] or task["operation_id"] != value["operation_id"]:
                    raise fail(_V4Code.IDEMPOTENCY_CONFLICT, "Create operation and TASK disagree")
                state = "COMMITTED"
            else:
                value = _read_receipt(creation, path)
                state = value.get("stage", "UNKNOWN")
            if value.get("workspace_id") != creation.manifest["workspace_id"]:
                raise fail(_V4Code.WORKSPACE_ID_MISMATCH, "Operation identity mismatch")
            operations.append(dict(path=str(path), contract=contract, state=state))
            if state != "COMMITTED":
                warnings.append(dict(path=str(path), code="RECOVERY_REQUIRED", state=state))
        except (FcopError, OSError, ValueError, KeyError) as exc:
            operations.append(dict(path=str(path), state="UNKNOWN"))
            error(path, exc)
    return {**creation.manifest, "tasks": tasks, "envelopes": envelopes,
            "counts": {s: sum(t["stage"] == s for t in tasks) for s in STAGES},
            "families": families, "operations": operations, "errors": errors, "warnings": warnings,
            "consistent": not errors, "observation": "non-atomic, read-only protocol facts"}


def validate_workspace(root: Path | str) -> dict:
    """Use the same protocol validators as inspection; return deterministic findings."""
    try:
        observed = inspect_workspace(root)
    except (FcopError, ValueError, OSError) as exc:
        return {"valid": False, "checked": 0, "errors": [{"path": str(root),
                "code": str(getattr(exc, "code", "INVALID_DATA")), "message": str(exc)}], "warnings": []}
    return {"valid": observed["consistent"], "checked": len(observed["envelopes"]),
            "errors": observed["errors"], "warnings": observed["warnings"]}
