"""Private WP3B T2/T3 planning and receipt-backed file transactions."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from uuid import UUID, uuid4

from fcop.errors import _V4Code
from fcop.v4.encoding import (
    BUCKETS,
    digest,
    fail,
    parse_envelope,
    publish,
    remove_authoritative,
    rewritten_envelope_bytes,
    safe_path,
)
from fcop.v4.linearization import family_boundary
from fcop.v4.receipts import (
    RECEIPT_CONTRACT,
    classify,
    matching_receipts,
    publish_prepared,
    set_stage,
)

if TYPE_CHECKING:
    from fcop.v4.creation import _Creation


def _uuid_urn(value: Any) -> bool:
    try:
        return isinstance(value, str) and UUID(value).urn == value
    except ValueError:
        return False


def current_attempt(fields: Mapping[str, Any]) -> str:
    """Return the attempt on the last valid entry-to-active transition."""
    transitions = fields.get("transitions")
    if not isinstance(transitions, list):
        raise fail(_V4Code.INVALID_ENVELOPE, "TASK transitions must be an array")
    for event in reversed(transitions):
        attempt = event.get("attempt_id") if isinstance(event, Mapping) else None
        source = event.get("from") if isinstance(event, Mapping) else None
        expected_tool = (
            {
                "inbox": "claim_task",
                "review": "reject_task",
                "done": "reopen_task",
            }.get(source)
            if isinstance(source, str)
            else None
        )
        if (
            isinstance(event, Mapping)
            and event.get("to") == "active"
            and expected_tool is not None
            and event.get("tool") == expected_tool
            and isinstance(event.get("at"), str)
            and isinstance(event.get("by"), str)
            and bool(event["by"])
            and _uuid_urn(attempt)
        ):
            assert isinstance(attempt, str)
            return attempt
    raise fail(_V4Code.ATTEMPT_MISMATCH, "Current active attempt is not provable")


def family_root_for(creation: _Creation, task_id: str) -> str:
    """Read only enough immutable relation data to select the family lock."""
    paths = creation._paths(task_id)
    if not paths:
        raise fail(_V4Code.RELATION_INVALID, "TASK does not exist", subject=task_id)
    roots: set[str] = set()
    for path in paths:
        fields = creation._validate(parse_envelope(path), path)
        root = fields.get("branch_of") or task_id
        if not isinstance(root, str) or not root.startswith("TASK-"):
            raise fail(_V4Code.RELATION_INVALID, "Invalid Branch Root", subject=task_id)
        roots.add(root)
    if len(roots) != 1:
        raise fail(_V4Code.RECOVERY_REQUIRED, "TASK copies disagree on family identity")
    return roots.pop()


def _reports_for(
    creation: _Creation, task_id: str, attempt_id: str
) -> list[tuple[Path, dict[str, Any]]]:
    reports: list[tuple[Path, dict[str, Any]]] = []
    folder = safe_path(creation.root, f"fcop/{BUCKETS['REPORT']}")
    for path in sorted(folder.glob("REPORT-*.md")):
        fields = creation._validate(parse_envelope(path), path)
        if fields.get("subject_ref") == task_id and fields.get("attempt_id") == attempt_id:
            reports.append((path, fields))
    return reports


def report_head(
    creation: _Creation, task_id: str, attempt_id: str
) -> tuple[Path, dict[str, Any]]:
    candidates = _reports_for(creation, task_id, attempt_id)
    if not candidates:
        raise fail(_V4Code.REPORT_REQUIRED, "Current attempt has no REPORT", subject=task_id)
    by_id = {fields["report_id"]: (path, fields) for path, fields in candidates}
    referenced: set[str] = set()
    for _, fields in candidates:
        if fields["report_kind"] != "replacement":
            continue
        prior = [ref for ref in fields.get("references", []) if ref in by_id]
        if len(prior) != 1 or prior[0] == fields["report_id"]:
            raise fail(
                _V4Code.REPORT_HEAD_AMBIGUOUS,
                "Replacement does not identify exactly one prior head",
                subject=task_id,
            )
        referenced.add(prior[0])
    heads = [entry for report_id, entry in by_id.items() if report_id not in referenced]
    if len(heads) != 1:
        raise fail(
            _V4Code.REPORT_HEAD_AMBIGUOUS,
            "Current attempt REPORT head is not unique",
            subject=task_id,
        )
    return heads[0]


class Lifecycle:
    """One private lifecycle component owned by the public Project facade."""

    def __init__(self, creation: _Creation) -> None:
        self.creation = creation
        self.root = creation.root

    def transition(self, **kwargs: Any) -> dict[str, Any]:
        self.creation._check()
        allowed = {
            "task_id", "from_stage", "to_stage", "tool", "actor",
            "report_ref", "review_ref", "authorization_ref", "family_digest",
        }
        if set(kwargs) - allowed or not {
            "task_id", "from_stage", "to_stage", "tool", "actor"
        }.issubset(kwargs):
            raise fail(_V4Code.INVALID_ENVELOPE, "Unexpected or missing transition fields")
        task_id = kwargs["task_id"]
        edge = (kwargs["from_stage"], kwargs["to_stage"])
        if not isinstance(task_id, str) or not task_id.startswith("TASK-"):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid TASK identity")
        if edge not in {
            (None, "inbox"), ("inbox", "active"), ("active", "review"),
            ("review", "done"), ("review", "active"), ("done", "active"),
            ("done", "archive"),
        }:
            raise fail(_V4Code.INVALID_TRANSITION, "Not a Base transition", subject=task_id)
        if edge not in {("inbox", "active"), ("active", "review")}:
            raise fail(
                _V4Code.OPERATION_NOT_IMPLEMENTED,
                "Only T2 and T3 are available in the WP3B lifecycle plane",
                operation="transition",
                subject=task_id,
            )
        expected_tool = "claim_task" if edge == ("inbox", "active") else "submit_task"
        if kwargs["tool"] != expected_tool or not isinstance(kwargs["actor"], str):
            raise fail(_V4Code.INVALID_TRANSITION, "Tool/actor does not match the edge")
        if edge == ("inbox", "active") and any(
            kwargs.get(name) is not None
            for name in ("report_ref", "review_ref", "authorization_ref", "family_digest")
        ):
            raise fail(_V4Code.INVALID_TRANSITION, "T2 consumes no evidence or authorization")
        if edge == ("active", "review") and any(
            kwargs.get(name) is not None
            for name in ("review_ref", "authorization_ref", "family_digest")
        ):
            raise fail(_V4Code.INVALID_TRANSITION, "T3 consumes only a REPORT")

        root_id = family_root_for(self.creation, task_id)
        with family_boundary(self.root, self.creation.manifest["workspace_id"], root_id):
            self.creation._check()
            if family_root_for(self.creation, task_id) != root_id:
                raise fail(_V4Code.RECOVERY_REQUIRED, "Family identity changed across lock")
            return self._under_lock(kwargs)

    def _request_digest(self, request: Mapping[str, Any]) -> str:
        from fcop.v4.encoding import canonical

        return digest(
            canonical(
                {
                    "contract": "fcop-lifecycle-transition-request-v1",
                    "workspace_id": self.creation.manifest["workspace_id"],
                    "task_id": request["task_id"],
                    "from_stage": request["from_stage"],
                    "to_stage": request["to_stage"],
                    "tool": request["tool"],
                    "actor": request["actor"],
                    "report_ref": request.get("report_ref"),
                }
            )
        )

    def _under_lock(self, request: Mapping[str, Any]) -> dict[str, Any]:
        task_id = request["task_id"]
        source_stage, target_stage = request["from_stage"], request["to_stage"]
        request_digest = self._request_digest(request)
        receipts = matching_receipts(
            self.root,
            workspace_id=self.creation.manifest["workspace_id"],
            task_id=task_id,
            from_stage=source_stage,
            to_stage=target_stage,
        )
        if source_stage == "active":
            attempt_id = self._visible_attempt(task_id, source_stage, target_stage)
            receipts = [
                item for item in receipts if item[1]["attempt_id"] == attempt_id
            ]
        if len(receipts) > 1:
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Multiple receipts claim the current lifecycle round",
                subject=task_id,
            )
        if receipts:
            path, receipt = receipts[0]
            if receipt["normalized_transition_digest"] != request_digest:
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "Unfinished transition receipt conflicts with this request",
                    subject=task_id,
                )
            return self._recover(path, receipt)

        source = safe_path(self.root, f"fcop/_lifecycle/{source_stage}/{task_id}.md")
        target = safe_path(self.root, f"fcop/_lifecycle/{target_stage}/{task_id}.md")
        if source.exists() and target.exists():
            if source.read_bytes() != target.read_bytes():
                raise fail(
                    _V4Code.TARGET_ALREADY_EXISTS_DIFFERENT,
                    "Lifecycle target already contains different bytes",
                    subject=task_id,
                )
            raise fail(_V4Code.STATE_AMBIGUOUS, "TASK has two authoritative paths")
        path, fields = self.creation._resolve(task_id)
        if path != source:
            raise fail(
                _V4Code.INVALID_TRANSITION,
                "Declared source does not match path NOW",
                subject=task_id,
            )
        self.creation._relations(fields)
        source_bytes = source.read_bytes()
        evidence_ref: list[str] = []
        evidence_digest: list[str] = []
        if source_stage == "inbox":
            attempt_id = uuid4().urn
            event: dict[str, Any] = {
                "at": datetime.now(timezone.utc).isoformat(),
                "attempt_id": attempt_id,
                "by": request["actor"],
                "from": "inbox",
                "to": "active",
                "tool": "claim_task",
            }
        else:
            attempt_id = current_attempt(fields)
            if request.get("report_ref") is not None:
                _, explicit = self.creation._resolve(request["report_ref"])
                if explicit.get("type") != "REPORT":
                    raise fail(_V4Code.REPORT_REQUIRED, "T3 evidence is not a REPORT")
                if explicit.get("attempt_id") != attempt_id:
                    raise fail(_V4Code.ATTEMPT_MISMATCH, "REPORT is from an old attempt")
            report_path, report = report_head(self.creation, task_id, attempt_id)
            if request.get("report_ref") not in {None, report["report_id"]}:
                raise fail(_V4Code.REPORT_HEAD_AMBIGUOUS, "Explicit REPORT is not current head")
            evidence_ref = [report["report_id"]]
            evidence_digest = [digest(report_path.read_bytes())]
            event = {
                "at": datetime.now(timezone.utc).isoformat(),
                "by": request["actor"],
                "evidence_digest": evidence_digest,
                "evidence_ref": evidence_ref,
                "from": "active",
                "to": "review",
                "tool": "submit_task",
            }
        updated = dict(fields)
        updated["transitions"] = [*fields["transitions"], event]
        target_bytes = rewritten_envelope_bytes(source, updated)
        operation_id = uuid4().urn
        receipt = {
            "contract": RECEIPT_CONTRACT,
            "version": 1,
            "operation_id": operation_id,
            "workspace_id": self.creation.manifest["workspace_id"],
            "task_id": task_id,
            "operation_kind": "lifecycle_transition",
            "from_stage": source_stage,
            "to_stage": target_stage,
            "tool": request["tool"],
            "actor": request["actor"],
            "report_ref": request.get("report_ref"),
            "source_path": source.relative_to(self.root).as_posix(),
            "target_path": target.relative_to(self.root).as_posix(),
            "source_digest": digest(source_bytes),
            "target_digest": digest(target_bytes),
            "normalized_transition_digest": request_digest,
            "evidence_ref": evidence_ref,
            "evidence_digest": evidence_digest,
            "attempt_id": attempt_id,
            "transition": event,
            "stage": "PREPARED",
        }
        receipt_path = publish_prepared(self.root, receipt)
        return self._finish(receipt_path, receipt, source, target, target_bytes)

    def _visible_attempt(
        self, task_id: str, source_stage: str, target_stage: str
    ) -> str:
        """Derive one round identity from visible TASK transition history."""
        attempts: set[str] = set()
        for stage in (source_stage, target_stage):
            path = safe_path(self.root, f"fcop/_lifecycle/{stage}/{task_id}.md")
            if path.is_file():
                fields = self.creation._validate(parse_envelope(path), path)
                attempts.add(current_attempt(fields))
        if len(attempts) != 1:
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Current lifecycle round is not uniquely provable",
                subject=task_id,
            )
        return attempts.pop()

    def _target_from_receipt(self, receipt: Mapping[str, Any], source: Path) -> bytes:
        fields = self.creation._validate(parse_envelope(source), source)
        if digest(source.read_bytes()) != receipt["source_digest"]:
            raise fail(_V4Code.RECOVERY_REQUIRED, "Source differs from receipt")
        updated = dict(fields)
        updated["transitions"] = [*fields["transitions"], receipt["transition"]]
        data = rewritten_envelope_bytes(source, updated)
        if digest(data) != receipt["target_digest"]:
            raise fail(_V4Code.RECOVERY_REQUIRED, "Target reconstruction differs from receipt")
        self._verify_evidence(receipt, fields)
        return data

    def _verify_evidence(
        self, receipt: Mapping[str, Any], source_fields: Mapping[str, Any]
    ) -> None:
        if not receipt["evidence_ref"]:
            return
        attempt_id = current_attempt(source_fields)
        report_path, report = report_head(self.creation, receipt["task_id"], attempt_id)
        if (
            receipt["evidence_ref"] != [report["report_id"]]
            or receipt["evidence_digest"] != [digest(report_path.read_bytes())]
        ):
            raise fail(_V4Code.RECOVERY_REQUIRED, "REPORT head changed after validation")

    def _recover(self, receipt_path: Path, receipt: dict[str, Any]) -> dict[str, Any]:
        state = classify(self.root, receipt)
        source = safe_path(self.root, receipt["source_path"])
        target = safe_path(self.root, receipt["target_path"])
        if state == "NOT_COMMITTED":
            target_bytes = self._target_from_receipt(receipt, source)
            return self._finish(receipt_path, receipt, source, target, target_bytes)
        if state == "RECOVERABLE_DUPLICATE":
            remove_authoritative(source)
            receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
            return self._result(receipt_path, receipt, target)
        if state == "COMMITTED":
            if receipt["stage"] != "COMMITTED":
                receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
            return self._result(receipt_path, receipt, target)
        raise fail(
            _V4Code.RECOVERY_REQUIRED,
            f"Lifecycle recovery is {state}; all evidence preserved",
            subject=receipt["task_id"],
        )

    def _finish(
        self,
        receipt_path: Path,
        receipt: dict[str, Any],
        source: Path,
        target: Path,
        target_bytes: bytes,
    ) -> dict[str, Any]:
        source_fields = self.creation._validate(parse_envelope(source), source)
        self._verify_evidence(receipt, source_fields)
        publish(target, target_bytes)
        receipt = set_stage(self.root, receipt_path, receipt, "TARGET_DURABLE")
        remove_authoritative(source)
        receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
        return self._result(receipt_path, receipt, target)

    def _result(
        self, receipt_path: Path, receipt: Mapping[str, Any], target: Path
    ) -> dict[str, Any]:
        return {
            "task_id": receipt["task_id"],
            "from_stage": receipt["from_stage"],
            "to_stage": receipt["to_stage"],
            "path": str(target),
            "status": "COMMITTED",
            "attempt_id": receipt["attempt_id"],
            "receipt_ref": receipt_path.relative_to(self.root).as_posix(),
        }

    def inspect_state(
        self, *, task_id: str | None = None, envelope_path: str | Path | None = None
    ) -> dict[str, Any]:
        self.creation._check()
        if task_id is not None and envelope_path is not None:
            raise fail(_V4Code.INVALID_ENVELOPE, "Choose task_id or envelope_path")
        if task_id is None:
            if envelope_path is None:
                raise fail(_V4Code.INVALID_ENVELOPE, "TASK identity is required")
            path = safe_path(self.root, str(envelope_path))
            fields = self.creation._validate(parse_envelope(path), path)
            warnings = self.creation._relations(fields)
            return {**fields, "path": str(path), "warnings": warnings}
        path, fields = self.creation._resolve(task_id)
        if fields["type"] != "TASK":
            raise fail(_V4Code.INVALID_ENVELOPE, "Expected TASK", subject=task_id)
        transitions = fields["transitions"]
        last = transitions[-1] if transitions else None
        try:
            attempt = current_attempt(fields)
        except Exception as exc:
            if getattr(exc, "code", None) != _V4Code.ATTEMPT_MISMATCH.value:
                raise
            attempt = None
        return {
            "task_id": task_id,
            "stage": path.parent.name,
            "path": str(path),
            "content_digest": digest(path.read_bytes()),
            "last_transition": last,
            "current_attempt_id": attempt,
        }
