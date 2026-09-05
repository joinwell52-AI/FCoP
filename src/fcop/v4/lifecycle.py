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
        from fcop.v4.creation import _request

        allowed = {
            "task_id", "from_stage", "to_stage", "tool", "actor",
            "report_ref", "review_ref", "authorization_ref", "family_digest",
            "profile_ref",
        }
        request = _request(
            kwargs,
            allowed,
            {"task_id", "from_stage", "to_stage", "tool", "actor"},
        )
        task_id = request["task_id"]
        edge = (request["from_stage"], request["to_stage"])
        if not isinstance(task_id, str) or not task_id.startswith("TASK-"):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid TASK identity")
        if edge not in {
            (None, "inbox"), ("inbox", "active"), ("active", "review"),
            ("review", "done"), ("review", "active"), ("done", "active"),
            ("done", "archive"),
        }:
            raise fail(_V4Code.INVALID_TRANSITION, "Not a Base transition", subject=task_id)
        if edge == ("done", "archive"):
            raise fail(
                _V4Code.OPERATION_NOT_IMPLEMENTED,
                "T7 remains outside the WP3C lifecycle plane",
                operation="transition",
                subject=task_id,
            )
        if edge == (None, "inbox"):
            raise fail(_V4Code.INVALID_TRANSITION, "T1 is create_task, not transition")
        if not isinstance(edge[0], str) or not isinstance(edge[1], str):
            raise fail(_V4Code.INVALID_TRANSITION, "Transition stages must be strings")
        concrete_edge = (edge[0], edge[1])
        expected_tool = {
            ("inbox", "active"): "claim_task",
            ("active", "review"): "submit_task",
            ("review", "done"): "approve_task",
            ("review", "active"): "reject_task",
            ("done", "active"): "reopen_task",
        }[concrete_edge]
        if request["tool"] != expected_tool or not isinstance(request["actor"], str):
            raise fail(_V4Code.INVALID_TRANSITION, "Tool/actor does not match the edge")
        if edge in {("review", "done"), ("review", "active"), ("done", "active")} and request.get(
            "family_digest"
        ) is not None:
            raise fail(_V4Code.AUTHORIZATION_INVALID, "WP3C transitions do not consume family_digest")
        if edge == ("inbox", "active") and any(
            request.get(name) is not None
            for name in (
                "report_ref", "review_ref", "authorization_ref", "family_digest", "profile_ref"
            )
        ):
            raise fail(_V4Code.INVALID_TRANSITION, "T2 consumes no evidence or authorization")
        if edge == ("active", "review") and any(
            request.get(name) is not None
            for name in ("review_ref", "authorization_ref", "family_digest", "profile_ref")
        ):
            raise fail(_V4Code.INVALID_TRANSITION, "T3 consumes only a REPORT")

        root_id = family_root_for(self.creation, task_id)
        with family_boundary(self.root, self.creation.manifest["workspace_id"], root_id):
            self.creation._check()
            if family_root_for(self.creation, task_id) != root_id:
                raise fail(_V4Code.RECOVERY_REQUIRED, "Family identity changed across lock")
            return self._under_lock(request)

    def _request_digest(self, request: Mapping[str, Any]) -> str:
        from fcop.v4.encoding import canonical

        value = {
            "contract": "fcop-lifecycle-transition-request-v1",
            "workspace_id": self.creation.manifest["workspace_id"],
            "task_id": request["task_id"],
            "from_stage": request["from_stage"],
            "to_stage": request["to_stage"],
            "tool": request["tool"],
            "actor": request["actor"],
            "report_ref": request.get("report_ref"),
        }
        if request["from_stage"] in {"review", "done"}:
            value.update(
                {
                    "review_ref": request.get("review_ref"),
                    "authorization_ref": request.get("authorization_ref"),
                    "family_digest": request.get("family_digest"),
                    "profile_ref": request.get("profile_ref"),
                }
            )
        return digest(canonical(value))

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
            visible_attempt = self._visible_attempt(task_id, source_stage, target_stage)
            receipts = [
                item for item in receipts if item[1]["attempt_id"] == visible_attempt
            ]
        exact = [
            item
            for item in receipts
            if item[1]["normalized_transition_digest"] == request_digest
        ]
        if len(exact) > 1:
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Multiple receipts claim the same lifecycle operation",
                subject=task_id,
            )
        if exact:
            return self._recover(*exact[0], existing=True)

        authorized = source_stage in {"review", "done"}
        if authorized:
            from fcop.v4.authorization import find_consumptions

            auth_ref = request.get("authorization_ref")
            if isinstance(auth_ref, str) and find_consumptions(self.creation, auth_ref):
                raise fail(
                    _V4Code.AUTHORIZATION_REUSED,
                    "Authorization was consumed by a different transition",
                    subject=task_id,
                )

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
        source_attempt_id: str | None = None
        target_attempt_id: str | None = None
        authorization_ref: str | None = None
        authorization_digest: str | None = None
        profile_ref: str | None = None
        if source_stage == "inbox":
            attempt_id = uuid4().urn
            target_attempt_id = attempt_id
            event: dict[str, Any] = {
                "at": datetime.now(timezone.utc).isoformat(),
                "attempt_id": attempt_id,
                "by": request["actor"],
                "from": "inbox",
                "to": "active",
                "tool": "claim_task",
            }
            if receipts:
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "A conflicting receipt already claims T2",
                    subject=task_id,
                )
        elif source_stage == "active":
            attempt_id = current_attempt(fields)
            source_attempt_id = target_attempt_id = attempt_id
            current_receipts = [
                item for item in receipts if item[1]["attempt_id"] == attempt_id
            ]
            if current_receipts:
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "A conflicting receipt claims the current T3 round",
                    subject=task_id,
                )
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
        else:
            from fcop.v4.authorization import validate_gate

            source_attempt_id = current_attempt(fields)
            current_receipts = [
                item
                for item in receipts
                if item[1].get("source_attempt_id") == source_attempt_id
            ]
            if current_receipts:
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "A conflicting receipt claims the current authorized round",
                    subject=task_id,
                )
            gate = validate_gate(
                self.creation,
                request,
                fields,
                attempt_id=source_attempt_id,
            )
            evidence_ref = list(gate.evidence_ref)
            evidence_digest = list(gate.evidence_digest)
            authorization_ref = gate.authorization_ref
            authorization_digest = gate.authorization_digest
            profile_ref = gate.profile_ref
            target_attempt_id = (
                uuid4().urn if target_stage == "active" else source_attempt_id
            )
            attempt_id = target_attempt_id
            event = {"at": datetime.now(timezone.utc).isoformat()}
            if target_stage == "active":
                event["attempt_id"] = target_attempt_id
            event.update(
                {
                    "authorization_digest": authorization_digest,
                    "authorization_ref": authorization_ref,
                    "by": request["actor"],
                    "evidence_digest": evidence_digest,
                    "evidence_ref": evidence_ref,
                    "from": source_stage,
                    "to": target_stage,
                    "tool": request["tool"],
                }
            )
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
        if authorized:
            receipt.update(
                {
                    "review_ref": request.get("review_ref"),
                    "authorization_ref": authorization_ref,
                    "authorization_digest": authorization_digest,
                    "profile_ref": profile_ref,
                    "request_profile_ref": request.get("profile_ref"),
                    "source_attempt_id": source_attempt_id,
                    "target_attempt_id": target_attempt_id,
                }
            )
        receipt_path = publish_prepared(self.root, receipt)
        return self._finish(receipt_path, receipt, source, target, target_bytes, existing=False)

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
        del source_fields
        if not receipt["evidence_ref"]:
            return
        observed: list[str] = []
        for reference in receipt["evidence_ref"]:
            try:
                path, _ = self.creation._resolve(reference)
            except Exception as exc:
                raise fail(
                    _V4Code.EVIDENCE_DIGEST_MISMATCH,
                    "Lifecycle evidence is no longer resolvable",
                ) from exc
            observed.append(digest(path.read_bytes()))
        if observed != receipt["evidence_digest"]:
            code = (
                _V4Code.EVIDENCE_DIGEST_MISMATCH
                if receipt.get("authorization_ref") is not None
                else _V4Code.RECOVERY_REQUIRED
            )
            raise fail(code, "Lifecycle evidence bytes changed")
        authorization_ref = receipt.get("authorization_ref")
        if authorization_ref is not None:
            try:
                path, authorization = self.creation._resolve(authorization_ref)
            except Exception as exc:
                raise fail(
                    _V4Code.EVIDENCE_DIGEST_MISMATCH,
                    "Authorization REVIEW is no longer resolvable",
                ) from exc
            if digest(path.read_bytes()) != receipt.get("authorization_digest"):
                raise fail(
                    _V4Code.EVIDENCE_DIGEST_MISMATCH,
                    "Authorization REVIEW bytes changed",
                )
            if (
                authorization.get("review_id") != authorization_ref
                or authorization.get("profile_ref") != receipt.get("profile_ref")
            ):
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "Receipt Profile does not match its Authorization REVIEW",
                )

    def _recover(
        self, receipt_path: Path, receipt: dict[str, Any], *, existing: bool = True
    ) -> dict[str, Any]:
        state = classify(self.root, receipt)
        source = safe_path(self.root, receipt["source_path"])
        target = safe_path(self.root, receipt["target_path"])
        if state == "NOT_COMMITTED":
            target_bytes = self._target_from_receipt(receipt, source)
            return self._finish(
                receipt_path, receipt, source, target, target_bytes, existing=existing
            )
        if state == "RECOVERABLE_DUPLICATE":
            fields = self.creation._validate(parse_envelope(source), source)
            self._verify_evidence(receipt, fields)
            remove_authoritative(source)
            receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
            return self._result(receipt_path, receipt, target, existing=existing)
        if state == "COMMITTED":
            fields = self.creation._validate(parse_envelope(target), target)
            self._verify_evidence(receipt, fields)
            if receipt["stage"] != "COMMITTED":
                receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
            return self._result(receipt_path, receipt, target, existing=existing)
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
        *,
        existing: bool,
    ) -> dict[str, Any]:
        source_fields = self.creation._validate(parse_envelope(source), source)
        self._verify_evidence(receipt, source_fields)
        publish(target, target_bytes)
        receipt = set_stage(self.root, receipt_path, receipt, "TARGET_DURABLE")
        remove_authoritative(source)
        receipt = set_stage(self.root, receipt_path, receipt, "COMMITTED")
        return self._result(receipt_path, receipt, target, existing=existing)

    def _result(
        self,
        receipt_path: Path,
        receipt: Mapping[str, Any],
        target: Path,
        *,
        existing: bool,
    ) -> dict[str, Any]:
        return {
            "task_id": receipt["task_id"],
            "from_stage": receipt["from_stage"],
            "to_stage": receipt["to_stage"],
            "path": str(target),
            "status": "COMMITTED",
            "attempt_id": receipt["attempt_id"],
            "receipt_ref": receipt_path.relative_to(self.root).as_posix(),
            "existing": existing,
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
