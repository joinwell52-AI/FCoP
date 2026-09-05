"""Private durable receipts and five-state classification for T2/T3."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

from fcop.errors import V4ProtocolError, _V4Code
from fcop.v4.encoding import (
    ID_RE,
    canonical,
    digest,
    fail,
    publish,
    read_json,
    replace_durable,
    safe_path,
)

RECEIPT_CONTRACT = "fcop-lifecycle-receipt-v1"
RECEIPT_STAGES = {"PREPARED", "TARGET_DURABLE", "COMMITTED"}
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


def _uuid_urn(value: Any) -> bool:
    try:
        return isinstance(value, str) and UUID(value).urn == value
    except ValueError:
        return False


def receipt_path(root: Path, operation_id: str) -> Path:
    if not _uuid_urn(operation_id):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid internal operation identity")
    return safe_path(root, f"fcop/operations/transition-{UUID(operation_id).hex}.json")


def _relative_path(value: Any, *, task_id: str, stage: str) -> str:
    expected = f"fcop/_lifecycle/{stage}/{task_id}.md"
    if (
        not isinstance(value, str)
        or value != expected
        or "\\" in value
        or any(part in {"", ".", ".."} for part in value.split("/"))
        or Path(value).is_absolute()
        or Path(value).drive
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Noncanonical receipt path")
    return value


def validate_receipt(root: Path, path: Path, value: dict[str, Any]) -> dict[str, Any]:
    required = {
        "contract", "version", "operation_id", "workspace_id", "task_id",
        "operation_kind", "from_stage", "to_stage", "tool", "actor",
        "report_ref",
        "source_path", "target_path", "source_digest", "target_digest",
        "normalized_transition_digest", "evidence_ref", "evidence_digest",
        "attempt_id", "transition", "stage",
    }
    if set(value) != required or value.get("contract") != RECEIPT_CONTRACT:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Damaged lifecycle receipt")
    if value.get("version") != 1 or value.get("operation_kind") != "lifecycle_transition":
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid lifecycle receipt contract")
    if not _uuid_urn(value.get("workspace_id")):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt workspace identity")
    operation_id = value.get("operation_id")
    if not _uuid_urn(operation_id):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt identity conflicts with filename")
    assert isinstance(operation_id, str)
    if path != receipt_path(root, operation_id):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt identity conflicts with filename")
    task_id = value.get("task_id")
    source = value.get("from_stage")
    target = value.get("to_stage")
    if (
        not isinstance(task_id, str)
        or not ID_RE.fullmatch(task_id)
        or not task_id.startswith("TASK-")
        or source not in {"inbox", "active"}
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt subject")
    if not isinstance(source, str) or not isinstance(target, str):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt edge")
    if (source, target) not in {("inbox", "active"), ("active", "review")}:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt edge is outside WP3B")
    tool = value.get("tool")
    actor = value.get("actor")
    expected_tool = "claim_task" if source == "inbox" else "submit_task"
    if tool != expected_tool or not isinstance(actor, str) or not actor:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt actor/tool conflicts with edge")
    _relative_path(value.get("source_path"), task_id=task_id, stage=source)
    _relative_path(value.get("target_path"), task_id=task_id, stage=target)
    for key in ("source_digest", "target_digest", "normalized_transition_digest"):
        if not isinstance(value.get(key), str) or not SHA256_RE.fullmatch(value[key]):
            raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt digest")
    refs, digests = value.get("evidence_ref"), value.get("evidence_digest")
    if (
        not isinstance(refs, list)
        or not all(isinstance(item, str) for item in refs)
        or not isinstance(digests, list)
        or len(refs) != len(digests)
        or not all(isinstance(item, str) and SHA256_RE.fullmatch(item) for item in digests)
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt evidence alignment")
    if not _uuid_urn(value.get("attempt_id")):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt attempt")
    event = value.get("transition")
    expected_event_keys = (
        {"at", "attempt_id", "by", "from", "to", "tool"}
        if source == "inbox"
        else {"at", "by", "evidence_digest", "evidence_ref", "from", "to", "tool"}
    )
    if not isinstance(event, dict) or not isinstance(event.get("at"), str):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt event timestamp")
    at = event["at"]
    try:
        stamp = datetime.fromisoformat(at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt event timestamp") from exc
    if stamp.utcoffset() is None:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt event timestamp requires timezone")
    if (
        not isinstance(event, dict)
        or set(event) != expected_event_keys
        or event.get("from") != source
        or event.get("to") != target
        or event.get("tool") != tool
        or event.get("by") != actor
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt transition event")
    report_ref = value.get("report_ref")
    if report_ref is not None and (
        not isinstance(report_ref, str)
        or not ID_RE.fullmatch(report_ref)
        or not report_ref.startswith("REPORT-")
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt REPORT reference")
    if source == "inbox":
        if (
            event.get("attempt_id") != value["attempt_id"]
            or refs
            or digests
            or report_ref is not None
        ):
            raise fail(_V4Code.RECOVERY_REQUIRED, "T2 receipt carries forbidden evidence")
    elif (
        len(refs) != 1
        or event.get("evidence_ref") != refs
        or event.get("evidence_digest") != digests
        or report_ref not in {None, refs[0]}
    ):
        raise fail(_V4Code.RECOVERY_REQUIRED, "T3 receipt evidence conflicts with event")
    expected_request = {
        "contract": "fcop-lifecycle-transition-request-v1",
        "workspace_id": value.get("workspace_id"),
        "task_id": task_id,
        "from_stage": source,
        "to_stage": target,
        "tool": tool,
        "actor": actor,
        "report_ref": report_ref,
    }
    if digest(canonical(expected_request)) != value["normalized_transition_digest"]:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Receipt request digest is inconsistent")
    if value.get("stage") not in RECEIPT_STAGES:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt stage")
    return value


def matching_receipts(
    root: Path, *, workspace_id: str, task_id: str, from_stage: str, to_stage: str
) -> list[tuple[Path, dict[str, Any]]]:
    operations = safe_path(root, "fcop/operations")
    found: list[tuple[Path, dict[str, Any]]] = []
    seen: set[str] = set()
    for path in sorted(operations.glob("transition-*.json")):
        try:
            value = validate_receipt(root, path, read_json(path))
        except V4ProtocolError as exc:
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Unreadable or conflicting lifecycle receipt",
                subject=task_id,
            ) from exc
        operation_id = value["operation_id"]
        if operation_id in seen:
            raise fail(_V4Code.RECOVERY_REQUIRED, "Duplicate lifecycle receipt identity")
        seen.add(operation_id)
        if (
            value["workspace_id"] == workspace_id
            and value["task_id"] == task_id
            and value["from_stage"] == from_stage
            and value["to_stage"] == to_stage
        ):
            found.append((path, value))
    return found


def publish_prepared(root: Path, value: dict[str, Any]) -> Path:
    path = receipt_path(root, value["operation_id"])
    validate_receipt(root, path, value)
    publish(path, canonical(value) + b"\n")
    return path


def set_stage(root: Path, path: Path, value: dict[str, Any], stage: str) -> dict[str, Any]:
    if stage not in RECEIPT_STAGES:
        raise fail(_V4Code.RECOVERY_REQUIRED, "Invalid receipt stage update")
    updated = dict(value)
    updated["stage"] = stage
    validate_receipt(root, path, updated)
    replace_durable(path, canonical(updated) + b"\n")
    return updated


def classify(root: Path, value: dict[str, Any]) -> str:
    source = safe_path(root, value["source_path"])
    target = safe_path(root, value["target_path"])
    source_exists, target_exists = source.is_file(), target.is_file()
    source_match = source_exists and digest(source.read_bytes()) == value["source_digest"]
    target_match = target_exists and digest(target.read_bytes()) == value["target_digest"]
    stage = value["stage"]
    if source_exists and not target_exists and source_match and stage == "PREPARED":
        return "NOT_COMMITTED"
    if source_exists and target_exists:
        if source_match and target_match and stage == "TARGET_DURABLE":
            return "RECOVERABLE_DUPLICATE"
        if not (source_match and target_match):
            return "DIVERGENT_DUPLICATE"
        return "INDETERMINATE"
    if not source_exists and target_exists and target_match and stage in {
        "TARGET_DURABLE", "COMMITTED"
    }:
        return "COMMITTED"
    return "INDETERMINATE"
