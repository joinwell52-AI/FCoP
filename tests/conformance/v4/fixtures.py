"""Disk arrangements and independent oracles for FCoP 4.0 tests."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

WORKSPACE_A = "urn:uuid:11111111-1111-4111-8111-111111111111"
WORKSPACE_B = "urn:uuid:22222222-2222-4222-8222-222222222222"
ATTEMPT_A = "urn:uuid:aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
ISSUER_PROOF = {"scheme": "test-profile-proof-v1", "value": "valid"}


class DeterministicProfileEvaluator:
    """Injected Profile boundary that records and returns one tri-state result.

    This fixture decides no Core behavior.  Production must call it and apply
    the F4.7.4 AUTHORIZED/DENIED/UNKNOWN policy itself.
    """

    RESULTS = frozenset({"AUTHORIZED", "DENIED", "UNKNOWN"})

    def __init__(self, result: str) -> None:
        if result not in self.RESULTS:
            raise ValueError(f"invalid test Profile result: {result}")
        self.result = result
        self.calls: list[dict[str, Any]] = []

    def __call__(self, *, profile_ref: str, issuer: str, proof: Any) -> str:
        self.calls.append(
            {"profile_ref": profile_ref, "issuer": issuer, "proof": proof}
        )
        return self.result
ATTEMPT_B = "urn:uuid:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


def _frontmatter(fields: Mapping[str, Any], body: str) -> bytes:
    yaml_text = yaml.safe_dump(
        dict(fields), allow_unicode=True, sort_keys=False, default_flow_style=False
    )
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    return f"---\n{yaml_text}---\n\n{normalized_body}\n".encode()


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"not an FCoP envelope: {path}")
    return dict(yaml.safe_load(text.split("---\n", 2)[1]))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot_tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_bytes(path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def canonical_family_digest(
    root_task_id: str, branches: Sequence[Mapping[str, str]]
) -> str:
    value = {
        "contract": "fcop-family-v1",
        "root_task_id": root_task_id,
        "branches": sorted(
            [dict(item) for item in branches], key=lambda item: item["branch_task_id"]
        ),
    }
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


@dataclass
class WorkspaceFixture:
    root: Path
    workspace_id: str = WORKSPACE_A

    def create(self, *, profiles: Sequence[str] = ("profile:test",)) -> WorkspaceFixture:
        manifest = {
            "protocol": "fcop",
            "protocol_version": "4.0",
            "workspace_id": self.workspace_id,
            "encoding": {"name": "fcop-filesystem", "version": "4.0"},
            "profiles": list(profiles),
        }
        (self.root / "fcop").mkdir(parents=True, exist_ok=True)
        (self.root / "fcop" / "fcop.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8", newline="\n",
        )
        for stage in ("inbox", "active", "review", "done", "archive"):
            (self.root / "fcop" / "_lifecycle" / stage).mkdir(parents=True, exist_ok=True)
        for bucket in ("reports", "issues", "reviews", "operations", "cold"):
            (self.root / "fcop" / bucket).mkdir(parents=True, exist_ok=True)
        return self

    @property
    def manifest_path(self) -> Path:
        return self.root / "fcop" / "fcop.json"

    def task(
        self, task_id: str, *, stage: str = "inbox", attempt_id: str | None = None,
        parent: str | None = None, branch_of: str | None = None,
        references: Sequence[str] = (),
        transitions: Sequence[Mapping[str, Any]] | None = None,
        body: str = "fixture task",
    ) -> Path:
        if transitions is None:
            transitions = ()
            if attempt_id is not None:
                transitions = (
                    {
                        "at": "2026-09-03T00:00:01+08:00",
                        "attempt_id": attempt_id,
                        "by": "ME",
                        "from": "inbox",
                        "to": "active",
                        "tool": "claim_task",
                    },
                )
        fields: dict[str, Any] = {
            "protocol": "fcop", "version": 4, "type": "TASK", "task_id": task_id,
            "workspace_id": self.workspace_id, "sender": "ME", "recipient": "ME",
            "created_at": "2026-09-03T00:00:00+08:00", "subject": f"fixture {task_id}",
            "transitions": list(transitions), "references": list(references),
        }
        if attempt_id:
            fields["attempt_id"] = attempt_id
        if parent:
            fields["parent"] = parent
        if branch_of:
            fields["branch_of"] = branch_of
        path = self.root / "fcop" / "_lifecycle" / stage / f"{task_id}.md"
        path.write_bytes(_frontmatter(fields, body))
        return path

    def report(
        self, report_id: str, *, task_id: str, attempt_id: str,
        report_kind: str = "final", references: Sequence[str] = (),
        body: str = "fixture report",
    ) -> Path:
        fields = {
            "protocol": "fcop", "version": 4, "type": "REPORT", "report_id": report_id,
            "workspace_id": self.workspace_id, "sender": "ME", "recipient": "ME",
            "created_at": "2026-09-03T00:01:00+08:00", "subject_ref": task_id,
            "attempt_id": attempt_id, "report_kind": report_kind, "result": "done",
            "references": list(references),
        }
        path = self.root / "fcop" / "reports" / f"{report_id}.md"
        path.write_bytes(_frontmatter(fields, body))
        return path

    def issue(self, issue_id: str, *, subject_ref: str) -> Path:
        fields = {
            "protocol": "fcop", "version": 4, "type": "ISSUE", "issue_id": issue_id,
            "workspace_id": self.workspace_id, "sender": "ME", "recipient": "ME",
            "created_at": "2026-09-03T00:02:00+08:00", "subject_ref": subject_ref,
            "severity": "medium", "references": [],
        }
        path = self.root / "fcop" / "issues" / f"{issue_id}.md"
        path.write_bytes(_frontmatter(fields, "fixture issue"))
        return path

    def review(
        self, review_id: str, *, task_id: str, review_kind: str, decision: str,
        attempt_id: str | None = None, family_digest: str | None = None,
        references: Sequence[str] = (), profile_ref: str | None = None,
        transition: Mapping[str, str] | None = None,
        issued_at: str = "2026-09-03T00:03:00+08:00",
        expires_at: str | None = "2099-01-01T00:00:00+00:00",
        authorization_scope: str | None = None,
        extra: Mapping[str, Any] | None = None,
    ) -> Path:
        fields: dict[str, Any] = {
            "protocol": "fcop", "version": 4, "type": "REVIEW", "review_id": review_id,
            "workspace_id": self.workspace_id, "sender": "ME", "recipient": "ME",
            "created_at": issued_at, "review_kind": review_kind, "subject_ref": task_id,
            "decision": decision, "references": list(references),
        }
        optional = {
            "attempt_id": attempt_id, "family_digest": family_digest,
            "profile_ref": profile_ref, "transition": dict(transition) if transition else None,
            "issued_at": issued_at if profile_ref else None,
            "expires_at": expires_at if profile_ref else None,
            "authorization_scope": authorization_scope,
            "operation_kind": "lifecycle_transition" if profile_ref else None,
        }
        fields.update({key: value for key, value in optional.items() if value is not None})
        if extra:
            fields.update(dict(extra))
        path = self.root / "fcop" / "reviews" / f"{review_id}.md"
        path.write_bytes(_frontmatter(fields, "fixture review"))
        return path

    def receipt(
        self, operation_id: str, *, source: Path, target: Path, stage: str,
        content_digest: str, corrupt: bool = False,
    ) -> Path:
        path = self.root / "fcop" / "operations" / f"{operation_id}.json"
        if corrupt:
            path.write_bytes(b"{corrupt")
        else:
            value = {
                "operation_id": operation_id,
                "source": source.relative_to(self.root).as_posix(),
                "target": target.relative_to(self.root).as_posix(),
                "stage": stage,
                "content_digest": content_digest,
            }
            path.write_text(
                json.dumps(value, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
            )
        return path

    def task_paths(self, task_id: str) -> list[Path]:
        return sorted((self.root / "fcop" / "_lifecycle").glob(f"*/{task_id}.md"))

    def envelope_paths(self, envelope_id: str) -> list[Path]:
        return sorted((self.root / "fcop").glob(f"**/{envelope_id}.md"))

    def raw_envelope(
        self, relative_path: str, fields: Mapping[str, Any], body: str = "fixture"
    ) -> Path:
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_frontmatter(fields, body))
        return path
