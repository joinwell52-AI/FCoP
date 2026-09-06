"""Mechanical recovery for caller-supplied, workspace-local evidence.

This module owns no journal or lifecycle policy. It normalizes compact
observations and full lifecycle receipts into the single classifier in
``fcop.v4.receipts`` and applies only the frozen five-state mechanical actions.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import (
    OP_RE,
    canonical,
    digest,
    fail,
    parse_envelope,
    read_json,
    remove_authoritative,
    replace_durable,
    safe_path,
)
from fcop.v4.receipts import (
    RECEIPT_CONTRACT,
    RECEIPT_STAGES,
    SHA256_RE,
    classify,
    set_stage,
    validate_receipt,
)

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation

ReceiptKind = Literal["compact", "lifecycle", "none"]


def _workspace_path(root: Path, value: Path | str, *, role: str) -> Path:
    try:
        supplied = Path(value)
        resolved_root = root.resolve()
        resolved = (
            supplied.resolve(strict=False)
            if supplied.is_absolute()
            else (root / supplied).resolve(strict=False)
        )
        relative = resolved.relative_to(resolved_root)
        return safe_path(root, relative.as_posix())
    except (OSError, ValueError, V4ProtocolError) as exc:
        raise fail(
            _V4Code.RECOVERY_REQUIRED,
            f"Unsafe {role} recovery path",
            subject=str(value),
        ) from exc


def _task_edge(root: Path, source: Path, target: Path) -> tuple[str, str, str]:
    try:
        source_parts = source.relative_to(root).parts
        target_parts = target.relative_to(root).parts
    except ValueError as exc:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Recovery path escapes workspace") from exc
    if (
        len(source_parts) != 4
        or len(target_parts) != 4
        or source_parts[:2] != ("fcop", "_lifecycle")
        or target_parts[:2] != ("fcop", "_lifecycle")
        or source_parts[3] != target_parts[3]
        or not source_parts[3].startswith("TASK-")
        or not source_parts[3].endswith(".md")
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Recovery paths do not name one TASK")
    source_stage, target_stage = source_parts[2], target_parts[2]
    if (source_stage, target_stage) not in {
        ("inbox", "active"),
        ("active", "review"),
        ("review", "done"),
        ("review", "active"),
        ("done", "active"),
        ("done", "archive"),
    }:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Recovery edge is not a Base transition")
    return source_parts[3][:-3], source_stage, target_stage


def _validate_visible(creation: _Creation, path: Path, task_id: str) -> None:
    if not path.is_file():
        return
    try:
        fields = creation._validate(parse_envelope(path), path)
    except V4ProtocolError as exc:
        raise fail(
            _V4Code.RECOVERY_REQUIRED,
            "Visible recovery evidence is not a valid TASK",
            subject=task_id,
        ) from exc
    if fields.get("type") != "TASK" or fields.get("task_id") != task_id:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Recovery TASK identity mismatch")


def _compact_receipt(
    value: dict[str, Any],
    *,
    operation_id: str,
    source_relative: str,
    target_relative: str,
) -> dict[str, Any] | None:
    if set(value) != {"operation_id", "source", "target", "stage", "content_digest"}:
        return None
    from fcop.v4.schema import _validate

    try:
        _validate("recovery-observation", value, code=_V4Code.RECOVERY_REQUIRED)
    except V4ProtocolError:
        return None
    if (
        value.get("operation_id") != operation_id
        or value.get("source") != source_relative
        or value.get("target") != target_relative
        or value.get("stage") not in RECEIPT_STAGES
        or not isinstance(value.get("content_digest"), str)
        or not SHA256_RE.fullmatch(value["content_digest"])
    ):
        return None
    return {
        "source_path": source_relative,
        "target_path": target_relative,
        "source_digest": value["content_digest"],
        "target_digest": value["content_digest"],
        "stage": value["stage"],
    }


def _observation(
    creation: _Creation,
    *,
    operation_id: str,
    source: Path,
    target: Path,
    receipt: Path | None,
) -> tuple[dict[str, Any] | None, ReceiptKind, dict[str, Any] | None]:
    source_relative = source.relative_to(creation.root).as_posix()
    target_relative = target.relative_to(creation.root).as_posix()
    if receipt is None:
        if source.is_file() and not target.exists():
            content_digest = digest(source.read_bytes())
            return (
                {
                    "source_path": source_relative,
                    "target_path": target_relative,
                    "source_digest": content_digest,
                    "target_digest": content_digest,
                    "stage": "PREPARED",
                },
                "none",
                None,
            )
        return None, "none", None
    if not receipt.is_file():
        return None, "compact", None
    try:
        value = read_json(receipt)
    except V4ProtocolError:
        return None, "compact", None
    if value.get("contract") == RECEIPT_CONTRACT:
        try:
            full = validate_receipt(creation.root, receipt, value)
        except V4ProtocolError:
            return None, "lifecycle", value
        if (
            full.get("operation_id") != operation_id
            or full.get("workspace_id") != creation.manifest["workspace_id"]
            or full.get("source_path") != source_relative
            or full.get("target_path") != target_relative
        ):
            return None, "lifecycle", value
        return full, "lifecycle", full
    compact = _compact_receipt(
        value,
        operation_id=operation_id,
        source_relative=source_relative,
        target_relative=target_relative,
    )
    return compact, "compact", value


def _complete_receipt(
    creation: _Creation,
    path: Path | None,
    kind: ReceiptKind,
    value: dict[str, Any] | None,
) -> None:
    if path is None or value is None or kind == "none":
        return
    if kind == "lifecycle":
        if value.get("stage") != "COMMITTED":
            set_stage(creation.root, path, value, "COMMITTED")
        return
    if value.get("stage") != "COMMITTED":
        updated = dict(value)
        updated["stage"] = "COMMITTED"
        from fcop.v4.schema import _validate

        _validate("recovery-observation", updated, code=_V4Code.RECOVERY_REQUIRED)
        replace_durable(path, canonical(updated) + b"\n")


def recover_operation(
    creation: _Creation,
    *,
    operation_id: str,
    source_path: Path | str,
    target_path: Path | str,
    receipt_path: Path | str | None = None,
    filesystem: str = "local",
) -> dict[str, Any]:
    """Classify and mechanically recover one explicit workspace observation."""
    creation._check()
    if filesystem != "local":
        raise fail(
            _V4Code.UNSUPPORTED_FILESYSTEM,
            "Recovery requires a verified local filesystem",
            operation=operation_id if isinstance(operation_id, str) else None,
        )
    if not isinstance(operation_id, str) or not OP_RE.fullmatch(operation_id):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid recovery operation identity")
    source = _workspace_path(creation.root, source_path, role="source")
    target = _workspace_path(creation.root, target_path, role="target")
    task_id, _, _ = _task_edge(creation.root, source, target)
    receipt = (
        _workspace_path(creation.root, receipt_path, role="receipt")
        if receipt_path is not None
        else None
    )
    if receipt is not None:
        parts = receipt.relative_to(creation.root).parts
        if len(parts) != 3 or parts[:2] != ("fcop", "operations"):
            raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt is outside fcop/operations")
    _validate_visible(creation, source, task_id)
    _validate_visible(creation, target, task_id)
    observation, kind, receipt_value = _observation(
        creation,
        operation_id=operation_id,
        source=source,
        target=target,
        receipt=receipt,
    )
    if observation is None:
        return {
            "operation_id": operation_id,
            "classification": "INDETERMINATE",
            "error_code": _V4Code.RECOVERY_REQUIRED.value,
        }
    state = classify(creation.root, observation)
    if state == "RECOVERABLE_DUPLICATE":
        if kind == "compact" and source.read_bytes() != target.read_bytes():
            state = "DIVERGENT_DUPLICATE"
        else:
            remove_authoritative(source)
            _complete_receipt(creation, receipt, kind, receipt_value)
    elif state == "COMMITTED":
        _complete_receipt(creation, receipt, kind, receipt_value)
    result: dict[str, Any] = {
        "operation_id": operation_id,
        "task_id": task_id,
        "classification": state,
    }
    if state in {"DIVERGENT_DUPLICATE", "INDETERMINATE"}:
        result["error_code"] = _V4Code.RECOVERY_REQUIRED.value
    return result
