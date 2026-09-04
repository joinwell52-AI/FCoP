"""Private WP3A creation plane. No lifecycle moves or authorization decisions."""

from __future__ import annotations

import os
import re
import tempfile
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from fcop.core.config import parse_team_config
from fcop.errors import ConfigError, V4ProtocolError, _V4Code
from fcop.v4.encoding import (
    BUCKETS,
    ID_RE,
    OP_RE,
    STAGES,
    canonical,
    digest,
    envelope_bytes,
    fail,
    normalize,
    operation_lock,
    parse_envelope,
    parse_json,
    publish,
    publish_directory,
    read_json,
    safe_path,
    strict_text,
    supported_local,
    sync_directory,
)


def _uuid(value: Any) -> bool:
    try:
        return isinstance(value, str) and UUID(value).urn == value
    except ValueError:
        return False


def _manifest(value: dict[str, Any]) -> dict[str, Any]:
    if value.get("protocol") != "fcop":
        raise fail(
            _V4Code.UNSUPPORTED_PROTOCOL, "Expected protocol fcop", operation="open_workspace"
        )
    if value.get("protocol_version") != "4.0":
        raise fail(
            _V4Code.UNSUPPORTED_WORKSPACE_VERSION,
            "Unsupported workspace version",
            operation="open_workspace",
        )
    if value.get("encoding") != {"name": "fcop-filesystem", "version": "4.0"}:
        raise fail(
            _V4Code.UNSUPPORTED_ENCODING,
            "Unsupported filesystem encoding",
            operation="open_workspace",
        )
    profiles = value.get("profiles")
    if (
        not _uuid(value.get("workspace_id"))
        or not isinstance(profiles, list)
        or not all(isinstance(item, str) and item for item in profiles)
        or len(set(profiles)) != len(profiles)
    ):
        raise fail(
            _V4Code.INVALID_ENVELOPE,
            "Invalid workspace identity or adopted Profile set",
            operation="open_workspace",
        )
    return value


def _request(kwargs: Mapping[str, Any], allowed: set[str], required: set[str]) -> dict[str, Any]:
    unknown = set(kwargs) - allowed
    if unknown or required - set(kwargs):
        raise fail(_V4Code.INVALID_ENVELOPE, "Unexpected or missing request fields")

    # No business request can carry judging logic, even through nesting.
    def check(value: Any) -> None:
        if callable(value):
            raise fail(
                _V4Code.AUTHORIZATION_INVALID, "Business requests cannot carry authority evaluators"
            )
        if isinstance(value, Mapping):
            for key, nested in value.items():
                if key in {
                    "evaluator",
                    "policy",
                    "trusted_profiles",
                    "profile_result",
                    "profile_evaluator",
                    "profile_resolver",
                    "caller_judge",
                }:
                    raise fail(_V4Code.AUTHORIZATION_INVALID, "Caller judging logic is forbidden")
                check(nested)
        elif isinstance(value, (tuple, list)):
            for nested in value:
                check(nested)

    check(kwargs)
    return dict(kwargs)


class _Creation:
    """Private per-Project encoding context, not an independent public API."""

    def __init__(self, root: Path, manifest: dict[str, Any], *, invalid: bool = False) -> None:
        self.root = root
        self.manifest = manifest
        self.invalid = invalid

    @classmethod
    def open_if_declared(cls, root: Path) -> _Creation | None:
        path = root / "fcop" / "fcop.json"
        if not path.exists() and not path.is_symlink():
            return None
        # Classification and formal reads share strict bytes and duplicate-key
        # rejection. An ambiguous declaration must never reach a legacy writer.
        try:
            raw = safe_path(root, "fcop/fcop.json").read_bytes()
            declaration = parse_json(raw, classification=True)
        except (V4ProtocolError, OSError):
            # Preserve legacy construction / is_initialized / config behavior,
            # but never route an unclassifiable declaration to a legacy writer.
            return cls(root, {}, invalid=True)
        if "protocol" in declaration and declaration["protocol"] != "fcop":
            raise fail(_V4Code.UNSUPPORTED_PROTOCOL, "Unrecognized protocol declaration")
        if "protocol_version" not in declaration:
            old_version = declaration.get("version")
            if isinstance(old_version, str) and re.fullmatch(r"[123](?:\.\d+){0,2}", old_version):
                # Historical v2 manifests used a semver string although the
                # modern team-config parser expects an integer. Do not rewrite
                # them or impose that newer parser on legacy writer routing.
                return None
            try:
                legacy = parse_team_config(declaration, source=path)
            except ConfigError:
                return cls(root, {}, invalid=True)
            if legacy.version in {1, 2, 3}:
                return None
            raise fail(_V4Code.UNSUPPORTED_WORKSPACE_VERSION, "Unrecognized legacy version")
        version = declaration["protocol_version"]
        if isinstance(version, str) and re.fullmatch(r"[123](?:\.\d+){0,2}", version):
            return None
        strict_text(raw)
        return cls(root, _manifest(declaration))

    @classmethod
    def create(
        cls, root: Path, *, protocol_version: str, encoding: str, profiles: Sequence[str]
    ) -> _Creation:
        if isinstance(profiles, (str, bytes)) or not isinstance(profiles, Sequence):
            raise fail(
                _V4Code.INVALID_ENVELOPE, "profiles must be an array", operation="create_workspace"
            )
        value = _manifest(
            {
                "protocol": "fcop",
                "protocol_version": protocol_version,
                "workspace_id": uuid4().urn,
                "encoding": {"name": "fcop-filesystem", "version": "4.0"}
                if encoding == "fcop-filesystem/4.0"
                else encoding,
                "profiles": list(profiles),
            }
        )
        supported_local(root)
        workspace = safe_path(root, "fcop")
        if workspace.exists() or (root / "docs/agents").exists():
            raise fail(
                _V4Code.TARGET_ALREADY_EXISTS_DIFFERENT,
                "Workspace already exists",
                operation="create_workspace",
            )
        root.mkdir(parents=True, exist_ok=True)
        if any(root.glob(".fcop-init-*")):
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Unresolved initialization staging; evidence preserved",
                operation="create_workspace",
            )
        try:
            staging = Path(tempfile.mkdtemp(prefix=".fcop-init-", dir=root))
            sync_directory(root)
            publish(staging / "fcop.json", canonical(value) + b"\n")
            for relative in [
                *(f"_lifecycle/{stage}" for stage in STAGES),
                *BUCKETS.values(),
                "operations",
                "cold",
            ]:
                directory = staging / relative
                directory.mkdir(parents=True)
                sync_directory(directory)
                sync_directory(directory.parent)
            sync_directory(staging)
            publish_directory(staging, workspace)
        except OSError as exc:
            raise fail(
                _V4Code.RECOVERY_REQUIRED,
                "Workspace initialization interrupted; staging preserved",
                operation="create_workspace",
            ) from exc
        return cls(root, value)

    def handler(self, name: str) -> Callable[..., Any] | None:
        if self.invalid:
            if name == "is_initialized":
                return lambda: (self.root / "fcop/fcop.json").is_file()
            return self._invalid_declaration
        handlers: dict[str, Callable[..., Any]] = {
            "is_initialized": lambda: (self.root / "fcop/fcop.json").is_file(),
            "create_task": self.create_task,
            "write_task": self.create_task,
            "create_workspace": self.create_workspace,
            "derive_workspace": self.derive_workspace,
            "write_report": self.write_report,
            "write_issue": self.write_issue,
            "write_review": self.write_review,
            "mark_human_approved": self.mark_human_approved,
            "read_task": self.read_task,
            "inspect_state": self.inspect_state,
            "transition": self.transition,
            "finish_task": self.finish_task,
        }
        return handlers.get(name)

    def _invalid_declaration(self, *args: Any, **kwargs: Any) -> Any:
        raise fail(
            _V4Code.INVALID_ENVELOPE, "Unreadable workspace manifest", operation="workspace_binding"
        )

    def transition(self, **kwargs: Any) -> dict[str, Any]:
        self._check()
        if kwargs.get("tool") == "finish_task":
            return self.finish_task(**kwargs)
        edge = (kwargs.get("from_stage"), kwargs.get("to_stage"))
        if edge not in {
            (None, "inbox"),
            ("inbox", "active"),
            ("active", "review"),
            ("review", "done"),
            ("review", "active"),
            ("done", "active"),
            ("done", "archive"),
        }:
            raise fail(
                _V4Code.INVALID_TRANSITION,
                "Not a Base transition",
                operation="transition",
                subject=kwargs.get("task_id"),
            )
        raise fail(
            _V4Code.OPERATION_NOT_IMPLEMENTED,
            "Only create_task T1 is available in WP3A",
            operation="transition",
            subject=kwargs.get("task_id"),
        )

    def finish_task(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        raise fail(
            _V4Code.LEGACY_TRANSITION_NOT_ALLOWED,
            "finish_task cannot operate on v4",
            operation="finish_task",
            subject=kwargs.get("task_id"),
        )

    def _check(self, workspace_id: str | None = None) -> None:
        current = _manifest(read_json(safe_path(self.root, "fcop/fcop.json")))
        if current != self.manifest:
            raise fail(
                _V4Code.WORKSPACE_ID_MISMATCH,
                "Manifest changed after Project binding",
                operation="workspace_binding",
            )
        if workspace_id is not None and workspace_id != self.manifest["workspace_id"]:
            raise fail(
                _V4Code.WORKSPACE_ID_MISMATCH,
                "Request workspace identity mismatch",
                operation="workspace_binding",
            )
        supported_local(self.root)
        manifest_device = (self.root / "fcop/fcop.json").stat().st_dev
        for relative in [
            *(f"_lifecycle/{stage}" for stage in STAGES),
            *BUCKETS.values(),
            "operations",
            "cold",
        ]:
            directory = safe_path(self.root, f"fcop/{relative}")
            if not directory.is_dir():
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "Incomplete workspace layout",
                    operation="workspace_binding",
                )
            if os.stat(directory).st_dev != manifest_device:
                raise fail(
                    _V4Code.UNSUPPORTED_FILESYSTEM,
                    "Cross-device workspace layout",
                    operation="workspace_binding",
                )

    def create_workspace(self, **kwargs: Any) -> dict[str, Any]:
        raise fail(
            _V4Code.TARGET_ALREADY_EXISTS_DIFFERENT,
            "Workspace already exists",
            operation="create_workspace",
        )

    def derive_workspace(
        self, *, destination: Path | str, mode: str, retain_workspace_id: bool
    ) -> dict[str, Any]:
        self._check()
        if retain_workspace_id:
            raise fail(
                _V4Code.WORKSPACE_ID_CLONE_CONFLICT,
                "Writable derivation requires a new ID",
                operation="derive_workspace",
            )
        if mode != "independent-writable":
            raise fail(
                _V4Code.INVALID_ENVELOPE,
                "Unsupported derivation mode",
                operation="derive_workspace",
            )
        target = Path(destination).absolute()
        if target.is_relative_to(self.root) or self.root.is_relative_to(target):
            raise fail(
                _V4Code.RELATION_INVALID,
                "Derivation cannot overlap source",
                operation="derive_workspace",
            )
        # Derive configuration/identity, not a migration or a copy of old facts.
        derived = self.create(
            target,
            protocol_version="4.0",
            encoding="fcop-filesystem/4.0",
            profiles=self.manifest["profiles"],
        )
        return dict(derived.manifest)

    def _paths(self, envelope_id: str) -> list[Path]:
        if not isinstance(envelope_id, str) or not ID_RE.fullmatch(envelope_id):
            raise fail(
                _V4Code.RELATION_INVALID,
                "Invalid typed envelope reference",
                subject=str(envelope_id),
            )
        kind = envelope_id.split("-", 1)[0]
        folders = [f"_lifecycle/{stage}" for stage in STAGES] if kind == "TASK" else [BUCKETS[kind]]
        return [
            path
            for folder in folders
            if (path := safe_path(self.root, f"fcop/{folder}/{envelope_id}.md")).exists()
        ]

    def _validate(self, fields: dict[str, Any], path: Path) -> dict[str, Any]:
        kind = fields.get("type")
        if kind not in {"TASK", "REPORT", "ISSUE", "REVIEW"}:
            raise fail(
                _V4Code.INVALID_ENVELOPE, "Not one of the four formal envelopes", subject=path.stem
            )
        if (
            fields.get("protocol") != "fcop"
            or type(fields.get("version")) is not int
            or fields["version"] != 4
        ):
            raise fail(
                _V4Code.INVALID_ENVELOPE, "Invalid envelope protocol/version", subject=path.stem
            )
        if fields.get("workspace_id") != self.manifest["workspace_id"]:
            raise fail(
                _V4Code.WORKSPACE_ID_MISMATCH, "Envelope identity mismatch", subject=path.stem
            )
        typed_id = fields.get(kind.lower() + "_id")
        if (
            not isinstance(typed_id, str)
            or not ID_RE.fullmatch(typed_id)
            or typed_id != path.stem
            or not typed_id.startswith(kind + "-")
        ):
            raise fail(_V4Code.INVALID_ENVELOPE, "Filename/type/ID mismatch", subject=path.stem)
        if not all(
            isinstance(fields.get(key), str) and fields[key] for key in ("sender", "recipient")
        ):
            raise fail(_V4Code.INVALID_ENVELOPE, "Missing sender/recipient", subject=path.stem)
        try:
            stamp = fields.get("created_at")
            if isinstance(stamp, str):
                stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if not isinstance(stamp, datetime) or stamp.utcoffset() is None:
                raise ValueError("Timezone required")
        except (ValueError, TypeError) as exc:
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid created_at", subject=path.stem) from exc
        required = {
            "TASK": ("subject", "transitions"),
            "REPORT": ("subject_ref", "attempt_id", "report_kind", "result"),
            "ISSUE": ("subject_ref", "severity"),
            "REVIEW": ("subject_ref", "review_kind", "decision"),
        }[kind]
        for key in required:
            if key == "transitions":
                valid = isinstance(fields.get(key), list)
            else:
                valid = isinstance(fields.get(key), str) and bool(fields[key])
            if not valid:
                raise fail(_V4Code.INVALID_ENVELOPE, f"Missing/invalid {key}", subject=path.stem)
        if kind == "REPORT" and (
            not _uuid(fields["attempt_id"]) or fields["report_kind"] not in {"final", "replacement"}
        ):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid REPORT structure", subject=path.stem)
        refs = fields.get("references", [])
        if not isinstance(refs, list) or not all(isinstance(ref, str) and ref for ref in refs):
            raise fail(
                _V4Code.RELATION_INVALID,
                "references must be an array of strings",
                subject=path.stem,
            )
        return fields

    def _resolve(
        self, envelope_id: str, *, seen: frozenset[str] = frozenset()
    ) -> tuple[Path, dict[str, Any]]:
        paths = self._paths(envelope_id)
        if len(paths) != 1:
            raise fail(
                _V4Code.STATE_AMBIGUOUS if len(paths) > 1 else _V4Code.RELATION_INVALID,
                "Reference must resolve to exactly one envelope",
                subject=envelope_id,
            )
        path = paths[0]
        fields = self._validate(parse_envelope(path), path)
        if envelope_id in seen:
            raise fail(_V4Code.RELATION_INVALID, "Cyclic strong relation", subject=envelope_id)
        for key in ("parent", "branch_of"):
            target = fields.get(key)
            if target is not None:
                self._strong_task(target, seen=seen | {envelope_id})
        return path, fields

    def _strong_task(self, target: Any, *, seen: frozenset[str] = frozenset()) -> None:
        if not isinstance(target, str) or not target.startswith("TASK-"):
            raise fail(_V4Code.RELATION_INVALID, "Strong TASK relation must name one TASK")
        try:
            self._resolve(target, seen=seen)
        except V4ProtocolError as exc:
            raise fail(
                _V4Code.RELATION_INVALID, "Invalid strong TASK relation", subject=target
            ) from exc

    def _relations(self, fields: dict[str, Any]) -> list[dict[str, str]]:
        for key in ("parent", "branch_of"):
            if fields.get(key) is not None:
                self._strong_task(fields[key])
        if "subject_ref" in fields:
            target = fields["subject_ref"]
            if target != "workspace:" + self.manifest["workspace_id"]:
                self._strong_task(target)
        warnings = []
        refs = fields.get("references", [])
        if not isinstance(refs, (list, tuple)) or not all(
            isinstance(ref, str) and ref for ref in refs
        ):
            raise fail(_V4Code.RELATION_INVALID, "Invalid references")
        fields["references"] = sorted({normalize(ref) for ref in refs})
        for ref in fields["references"]:
            if "/" in ref or "\\" in ref or ".." in ref:
                raise fail(_V4Code.RELATION_INVALID, "References are IDs, not paths", subject=ref)
            try:
                self._resolve(ref)
            except V4ProtocolError:
                warnings.append({"code": _V4Code.REFERENCE_UNRESOLVED, "subject_ref": ref})
        return warnings

    def _common(self, kind: str, sender: str, recipient: str) -> dict[str, Any]:
        return {
            "protocol": "fcop",
            "version": 4,
            "type": kind,
            kind.lower() + "_id": kind + "-" + uuid4().hex,
            "workspace_id": self.manifest["workspace_id"],
            "sender": normalize(sender),
            "recipient": normalize(recipient),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def create_task(self, **kwargs: Any) -> dict[str, Any]:
        """Coordinate pure request planning and one short durable commit."""
        plan = self._plan_create(kwargs)
        return self._commit_create(plan)

    def _plan_create(self, kwargs: Mapping[str, Any]) -> dict[str, Any]:
        required = {"workspace_id", "operation_id", "sender", "recipient", "subject", "body"}
        allowed = required | {
            "operation_kind",
            "priority",
            "parent",
            "branch_of",
            "references",
            "thread_key",
            "risk_level",
        }
        request = _request(kwargs, allowed, required)
        self._check(request["workspace_id"])
        opid = request["operation_id"]
        if not isinstance(opid, str) or not OP_RE.fullmatch(opid):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid operation_id", operation=str(opid))
        if request.get("operation_kind", "create_task") != "create_task":
            raise fail(_V4Code.INVALID_ENVELOPE, "Wrong create operation kind", operation=opid)
        for relation in ("parent", "branch_of"):
            if request.get(relation) is not None and not isinstance(request[relation], str):
                raise fail(
                    _V4Code.RELATION_INVALID, "Strong relation must be a single ID", operation=opid
                )
        normalized = {
            "contract": "fcop-create-task-v1",
            "workspace_id": request["workspace_id"],
            "operation_kind": "create_task",
            "operation_id": opid,
            **{key: normalize(request[key]) for key in ("sender", "recipient", "subject")},
            "body": normalize(request["body"]).rstrip("\n") + "\n",
            "priority": normalize(request.get("priority", "P2")),
            "parent": normalize(request["parent"]) if request.get("parent") is not None else None,
            "branch_of": normalize(request["branch_of"])
            if request.get("branch_of") is not None
            else None,
            "references": request.get("references", []),
        }
        warnings = self._relations(normalized)
        if normalized["priority"] not in {"P0", "P1", "P2", "P3"} or not all(
            normalized[key] for key in ("subject", "sender", "recipient")
        ):
            raise fail(_V4Code.INVALID_ENVELOPE, "Invalid TASK fields", operation=opid)
        request_digest = digest(canonical(normalized))
        key = digest(
            canonical(
                {
                    name: normalized[name]
                    for name in ("workspace_id", "operation_kind", "operation_id")
                }
            )
        )
        fields = self._common("TASK", normalized["sender"], normalized["recipient"])
        fields.update(
            {
                name: normalized[name]
                for name in (
                    "subject",
                    "priority",
                    "parent",
                    "branch_of",
                    "references",
                    "operation_id",
                    "operation_kind",
                )
            }
        )
        fields["normalized_request_digest"] = request_digest
        fields["transitions"] = [
            {
                "at": fields["created_at"],
                "from": None,
                "to": "inbox",
                "by": fields["sender"],
                "tool": "create_task",
            }
        ]
        path = safe_path(self.root, f"fcop/_lifecycle/inbox/{fields['task_id']}.md")
        self._validate(fields, path)
        data = envelope_bytes(fields, normalized["body"])
        fact = {
            "contract": "fcop-create-task-v1",
            "key": key,
            "workspace_id": request["workspace_id"],
            "operation_kind": "create_task",
            "operation_id": opid,
            "task_id": fields["task_id"],
            "path": path.relative_to(self.root).as_posix(),
            "digest": request_digest,
            "content_digest": digest(data),
        }
        return {"fact": fact, "data": data, "warnings": warnings}

    def _commit_create(self, plan: dict[str, Any]) -> dict[str, Any]:
        planned_fact = plan["fact"]
        opid, key = planned_fact["operation_id"], planned_fact["key"]
        request_digest = planned_fact["digest"]
        warnings = plan["warnings"]
        operations = safe_path(self.root, "fcop/operations")
        fact_path = safe_path(self.root, f"fcop/operations/create-{key}.json")
        lock_path = safe_path(self.root, f"fcop/operations/create-{key}.lock")
        with operation_lock(lock_path):
            self._check(planned_fact["workspace_id"])
            # Scan durable records under the key lock, including duplicates at
            # noncanonical filenames. Never accept a copied/conflicting fact.
            matching = []
            for path in operations.glob("*.json"):
                try:
                    fact = read_json(safe_path(self.root, path.relative_to(self.root).as_posix()))
                except V4ProtocolError as exc:
                    raise fail(
                        _V4Code.RECOVERY_REQUIRED, "Unreadable operation fact", operation=opid
                    ) from exc
                if fact.get("key") == key:
                    matching.append((path, fact))
            if len(matching) > 1 or (matching and matching[0][0] != fact_path):
                raise fail(_V4Code.RECOVERY_REQUIRED, "Duplicate operation facts", operation=opid)
            if fact_path.exists():
                fact = read_json(fact_path)
                if (
                    not matching
                    or fact.get("operation_id") != opid
                    or fact.get("workspace_id") != planned_fact["workspace_id"]
                    or fact.get("operation_kind") != "create_task"
                ):
                    raise fail(
                        _V4Code.RECOVERY_REQUIRED, "Operation identity damaged", operation=opid
                    )
                if fact.get("digest") != request_digest:
                    raise fail(
                        _V4Code.OPERATION_ID_CONFLICT,
                        "Operation key already has a different digest",
                        operation=opid,
                    )
                try:
                    relative = fact["path"]
                    if (
                        not isinstance(relative, str)
                        or "\\" in relative
                        or any(part in {"", ".", ".."} for part in relative.split("/"))
                        or relative != f"fcop/_lifecycle/inbox/{fact['task_id']}.md"
                    ):
                        raise fail(_V4Code.RECOVERY_REQUIRED, "Noncanonical operation path")
                    initial_path = safe_path(self.root, relative)
                    path, fields = self._resolve(fact["task_id"])
                    valid = (
                        path == initial_path
                        and digest(path.read_bytes()) == fact["content_digest"]
                        and fields.get("operation_id") == opid
                        and fields.get("normalized_request_digest") == request_digest
                        and fields.get("operation_kind") == "create_task"
                    )
                except (KeyError, V4ProtocolError) as exc:
                    raise fail(
                        _V4Code.RECOVERY_REQUIRED, "Operation result is unprovable", operation=opid
                    ) from exc
                if not valid:
                    raise fail(
                        _V4Code.RECOVERY_REQUIRED,
                        "Operation result differs from durable fact",
                        operation=opid,
                    )
                return {
                    "task_id": fact["task_id"],
                    "path": str(path),
                    "digest": request_digest,
                    "existing": True,
                    "warnings": warnings,
                }
            for stage in STAGES:
                for path in safe_path(self.root, f"fcop/_lifecycle/{stage}").glob("TASK-*.md"):
                    old = parse_envelope(
                        safe_path(self.root, path.relative_to(self.root).as_posix())
                    )
                    if (
                        old.get("operation_id") == opid
                        and old.get("operation_kind") == "create_task"
                    ):
                        raise fail(
                            _V4Code.RECOVERY_REQUIRED,
                            "TASK exists without its durable operation fact",
                            operation=opid,
                        )
            if list(operations.glob(f".fcop-create-{fact_path.stem}-*.tmp")):
                raise fail(
                    _V4Code.RECOVERY_REQUIRED,
                    "Incomplete operation publication evidence",
                    operation=opid,
                )
            path = safe_path(self.root, planned_fact["path"])
            publish(path, plan["data"])
            publish(fact_path, canonical(planned_fact) + b"\n")
            return {
                "task_id": planned_fact["task_id"],
                "path": str(path),
                "digest": request_digest,
                "existing": False,
                "warnings": warnings,
            }

    def _append(self, kind: str, kwargs: dict[str, Any]) -> dict[str, Any]:
        common = {"workspace_id", "sender", "recipient", "body", "subject_ref"}
        required = (
            common
            | {
                "REPORT": {"attempt_id", "report_kind", "result"},
                "ISSUE": {"severity"},
                "REVIEW": {"review_kind", "decision"},
            }[kind]
        )
        allowed = required | {"references"}
        if kind == "REVIEW":
            allowed |= {
                "attempt_id",
                "family_digest",
                "authorization_ref",
                "profile_ref",
                "transition",
                "issued_at",
                "expires_at",
                "authorization_scope",
                "operation_kind",
                "issuer_proof",
            }
        request = _request(kwargs, allowed, required)
        self._check(request["workspace_id"])
        fields = self._common(kind, request["sender"], request["recipient"])
        for key, value in request.items():
            if key not in common or key == "subject_ref":
                fields[key] = normalize(value) if isinstance(value, str) else value
        warnings = self._relations(fields)
        path = safe_path(self.root, f"fcop/{BUCKETS[kind]}/{fields[kind.lower() + '_id']}.md")
        self._validate(fields, path)
        data = envelope_bytes(fields, request["body"])
        publish(path, data)
        return {
            kind.lower() + "_id": fields[kind.lower() + "_id"],
            "path": str(path),
            "warnings": warnings,
        }

    def write_report(self, **kwargs: Any) -> dict[str, Any]:
        return self._append("REPORT", kwargs)

    def write_issue(self, **kwargs: Any) -> dict[str, Any]:
        return self._append("ISSUE", kwargs)

    def write_review(self, **kwargs: Any) -> dict[str, Any]:
        return self._append("REVIEW", kwargs)

    def mark_human_approved(
        self, *, review_id: str, decision: str, approver: str, profile_ref: str, comment: str = ""
    ) -> dict[str, Any]:
        self._check()
        _, old = self._resolve(review_id)
        if old["type"] != "REVIEW":
            raise fail(_V4Code.INVALID_ENVELOPE, "Expected REVIEW", subject=review_id)
        return self.write_review(
            workspace_id=self.manifest["workspace_id"],
            sender=approver,
            recipient=old["recipient"],
            body=comment,
            subject_ref=old["subject_ref"],
            review_kind="assessment",
            decision=decision,
            profile_ref=profile_ref,
            references=[review_id],
        )

    def read_task(
        self, filename_or_id: str | None = None, *, task_id: str | None = None
    ) -> dict[str, Any]:
        self._check()
        identity = task_id or filename_or_id
        if not isinstance(identity, str) or not identity.startswith("TASK-"):
            raise fail(_V4Code.INVALID_ENVELOPE, "Expected TASK ID")
        path, fields = self._resolve(identity)
        return {**fields, "path": str(path)}

    def inspect_state(self, *, envelope_path: str | Path) -> dict[str, Any]:
        self._check()
        path = safe_path(self.root, str(envelope_path))
        fields = self._validate(parse_envelope(path), path)
        warnings = self._relations(fields)
        return {**fields, "path": str(path), "warnings": warnings}
