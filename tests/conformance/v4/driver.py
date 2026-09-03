"""Test-only adapter from the frozen FCoP 4.0 contract to FCoP 3.2.5.

This module intentionally contains no working 4.0 implementation.  It calls
or inspects the current public 3.2.5 surface and raises ``V4_NOT_IMPLEMENTED``
when the observable capability required by the frozen contract is absent.
"""

from __future__ import annotations

import inspect
import json
import multiprocessing
from dataclasses import dataclass
from pathlib import Path
from queue import Empty
from typing import Any, Callable

from fcop import Project
from fcop.lifecycle import ALLOWED_TRANSITIONS, Stage


ACTION_CLAUSES: dict[str, str] = {
    "create_workspace": "F4.2.1-F4.2.3",
    "derive_workspace": "F4.2.4-F4.2.6",
    "create_task": "F4.3.1-F4.3.2; F4.8.1-F4.8.5",
    "read_task": "F4.4.1; F4.9.3",
    "transition": "F4.4.1-F4.4.7",
    "write_report": "F4.3.3-F4.3.4; F4.6.1-F4.6.2",
    "write_review": "F4.3.3; F4.3.5; F4.7.1-F4.7.7",
    "replace_report": "F4.3.3-F4.3.4",
    "inspect_state": "F4.4.1; F4.9.3",
    "list_branches": "F4.5.3-F4.5.4; F4.6.5",
    "recover_operation": "F4.9.1-F4.9.11",
    "inject_fault": "F4.9.4; F4.9.9-F4.9.10",
}


class V4NotImplemented(AssertionError):
    """A deliberate red light tied to one frozen conformance obligation."""

    code = "V4_NOT_IMPLEMENTED"

    def __init__(self, test_id: str, clause: str, expected: str, actual: str) -> None:
        self.test_id = test_id
        self.clause = clause
        self.expected = expected
        self.actual = actual
        super().__init__(
            f"[{test_id}] {clause}: expected {expected}; actual {actual}; "
            f"code={self.code}"
        )


@dataclass(frozen=True)
class WorkspaceObservation:
    root: Path
    manifest: dict[str, Any]


def _legacy_create_worker(
    root: str,
    ready: multiprocessing.synchronize.Event,
    output: multiprocessing.queues.Queue,
) -> None:
    """Compete to create one semantic request through the real 3.2.5 API."""
    ready.wait()
    try:
        task = Project(Path(root)).write_task(
            sender="ADMIN",
            recipient="ME",
            priority="P2",
            subject="same semantic create request",
            body="same body\n",
        )
        output.put(("ok", task.task_id, str(task.path)))
    except BaseException as exc:  # pragma: no cover - child evidence path
        output.put(("error", type(exc).__name__, str(exc)))


def _surface_probe_worker(
    ready: multiprocessing.synchronize.Event,
    output: multiprocessing.queues.Queue,
    action: str,
    required_parameters: tuple[str, ...],
) -> None:
    """Synchronize two real processes at a missing 4.0 commit surface."""
    ready.wait()
    method = getattr(Project, action, None)
    parameters = set(inspect.signature(method).parameters) if method is not None else set()
    output.put((action, method is not None, sorted(set(required_parameters) - parameters)))


class V4ConformanceDriver:
    """Thin probe driver; never manufactures a successful 4.0 result."""

    def __init__(self, root: Path) -> None:
        self.root = root

    @staticmethod
    def _missing(
        test_id: str, clause: str, expected: str, actual: str
    ) -> V4NotImplemented:
        return V4NotImplemented(test_id, clause, expected, actual)

    @staticmethod
    def _parameters(callable_obj: Callable[..., Any]) -> set[str]:
        return set(inspect.signature(callable_obj).parameters)

    def require_parameters(
        self,
        callable_obj: Callable[..., Any],
        required: set[str],
        *,
        test_id: str,
        clause: str,
    ) -> None:
        actual = self._parameters(callable_obj)
        missing = sorted(required - actual)
        if missing:
            raise self._missing(
                test_id,
                clause,
                f"public parameters {sorted(required)}",
                f"3.2.5 surface lacks {missing}",
            )

    def create_workspace(self, *, test_id: str, clause: str) -> WorkspaceObservation:
        project = Project(self.root)
        project.init_solo(
            deploy_rules=False,
            deploy_role_templates=False,
            deploy_internal_template=False,
        )
        manifest_path = self.root / "fcop" / "fcop.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected = {
            "protocol": "fcop",
            "protocol_version": "4.0",
            "workspace_id": "canonical lowercase UUID URN",
            "encoding": {"name": "fcop-filesystem", "version": "4.0"},
            "profiles": [],
        }
        required = {"protocol", "protocol_version", "workspace_id", "encoding", "profiles"}
        if not required.issubset(manifest) or manifest.get("protocol_version") != "4.0":
            raise self._missing(
                test_id,
                clause,
                f"4.0 manifest {expected}",
                f"real manifest keys/version are {sorted(manifest)}/{manifest.get('protocol_version')!r}",
            )
        return WorkspaceObservation(self.root, manifest)

    def derive_workspace(self, *, test_id: str, clause: str) -> Any:
        method = getattr(Project, "derive_workspace", None)
        if method is None:
            raise self._missing(
                test_id, clause, "explicit writable fork with a new workspace_id",
                "Project.derive_workspace is absent",
            )
        return method

    def create_task(self, *, test_id: str, clause: str) -> None:
        self.require_parameters(
            Project.write_task,
            {"operation_id", "operation_kind", "branch_of"},
            test_id=test_id,
            clause=clause,
        )

    def read_task(self, *, test_id: str, clause: str) -> None:
        if not hasattr(Project, "read_task"):
            raise self._missing(test_id, clause, "v4 TASK reader", "Project.read_task absent")
        self.inspect_state(test_id=test_id, clause=clause)

    def transition(
        self,
        from_stage: str | None,
        to_stage: str,
        *,
        test_id: str,
        clause: str,
        should_exist: bool = True,
    ) -> None:
        actual = {
            (
                None if item.from_stage is None else item.from_stage.value,
                item.to_stage.value,
            )
            for item in ALLOWED_TRANSITIONS
        }
        edge = (from_stage, to_stage)
        present = edge in actual
        if present != should_exist:
            expectation = "legal 4.0 edge" if should_exist else "rejected 4.0 edge"
            raise self._missing(
                test_id,
                clause,
                f"{edge} is {expectation}",
                f"3.2.5 transition table contains={present}; table={sorted(map(str, actual))}",
            )

    def write_report(self, *, test_id: str, clause: str) -> None:
        self.require_parameters(
            Project.write_report,
            {"subject_ref", "attempt_id", "report_kind", "result", "references"},
            test_id=test_id,
            clause=clause,
        )

    def write_review(self, *, test_id: str, clause: str) -> None:
        self.require_parameters(
            Project.write_review,
            {"review_kind", "attempt_id", "family_digest", "authorization_ref", "profile_ref", "references"},
            test_id=test_id,
            clause=clause,
        )

    def replace_report(self, *, test_id: str, clause: str) -> None:
        self.write_report(test_id=test_id, clause=clause)

    def inspect_state(self, *, test_id: str, clause: str) -> None:
        method = getattr(Project, "inspect_state", None)
        if method is None:
            raise self._missing(
                test_id, clause, "fail-closed unique-path state inspection",
                "Project.inspect_state is absent",
            )

    def list_branches(self, *, test_id: str, clause: str) -> None:
        method = getattr(Project, "list_branches", None)
        if method is None:
            raise self._missing(
                test_id, clause, "branch_of family enumeration",
                "Project.list_branches is absent",
            )

    def recover_operation(self, *, test_id: str, clause: str) -> None:
        method = getattr(Project, "recover_operation", None)
        if method is None:
            raise self._missing(
                test_id, clause, "durable lifecycle receipt recovery",
                "Project.recover_operation is absent (legacy session recovery is a different contract)",
            )

    def inject_fault(self, *, test_id: str, clause: str) -> None:
        from fcop.lifecycle import atomic

        params = self._parameters(atomic.commit)
        if not {"fault_stage", "receipt"}.issubset(params):
            raise self._missing(
                test_id, clause, "abstract PREPARED/TARGET_DURABLE/COMMITTED fault injection",
                f"atomic.commit parameters are {sorted(params)}",
            )

    def require_authorization(self, *, test_id: str, clause: str) -> None:
        self.write_review(test_id=test_id, clause=clause)

    def require_family(self, *, test_id: str, clause: str) -> None:
        self.list_branches(test_id=test_id, clause=clause)

    def require_recovery(self, *, test_id: str, clause: str) -> None:
        self.recover_operation(test_id=test_id, clause=clause)

    def race_same_create(self, *, test_id: str, clause: str) -> None:
        Project(self.root).init_solo(
            deploy_rules=False,
            deploy_role_templates=False,
            deploy_internal_template=False,
        )
        ctx = multiprocessing.get_context("spawn")
        ready = ctx.Event()
        output = ctx.Queue()
        workers = [
            ctx.Process(target=_legacy_create_worker, args=(str(self.root), ready, output))
            for _ in range(2)
        ]
        for worker in workers:
            worker.start()
        ready.set()
        for worker in workers:
            worker.join(timeout=20)
            if worker.is_alive():
                worker.terminate()
                worker.join(timeout=5)
                raise AssertionError(f"[{test_id}] child process did not terminate")
        results = []
        for _ in workers:
            try:
                results.append(output.get(timeout=5))
            except Empty as exc:
                raise AssertionError(f"[{test_id}] missing child result") from exc
        successes = [item for item in results if item[0] == "ok"]
        unique_tasks = {item[1] for item in successes}
        if len(successes) != 2 or len(unique_tasks) != 1:
            raise self._missing(
                test_id,
                clause,
                "two processes, one durable operation key, one TASK and identical Existing result",
                f"real 3.2.5 process results={results}",
            )

    def parallel_surface_probe(
        self,
        action: str,
        *,
        required_parameters: tuple[str, ...] = (),
        test_id: str,
        clause: str,
        expected: str,
    ) -> None:
        ctx = multiprocessing.get_context("spawn")
        ready = ctx.Event()
        output = ctx.Queue()
        workers = [
            ctx.Process(
                target=_surface_probe_worker,
                args=(ready, output, action, required_parameters),
            )
            for _ in range(2)
        ]
        for worker in workers:
            worker.start()
        ready.set()
        for worker in workers:
            worker.join(timeout=20)
        results = [output.get(timeout=5) for _ in workers]
        if not all(item[1] and not item[2] for item in results):
            raise self._missing(
                test_id, clause, expected,
                f"two synchronized processes observed surface={results}",
            )


def actual_v3_edges() -> set[tuple[str | None, str]]:
    """Expose the immutable real table for narrowly scoped assertions."""
    return {
        (None if item.from_stage is None else item.from_stage.value, item.to_stage.value)
        for item in ALLOWED_TRANSITIONS
    }


V4_EDGES = {
    (None, Stage.INBOX.value),
    (Stage.INBOX.value, Stage.ACTIVE.value),
    (Stage.ACTIVE.value, Stage.REVIEW.value),
    (Stage.REVIEW.value, Stage.DONE.value),
    (Stage.REVIEW.value, Stage.ACTIVE.value),
    (Stage.DONE.value, Stage.ACTIVE.value),
    (Stage.DONE.value, Stage.ARCHIVE.value),
}
