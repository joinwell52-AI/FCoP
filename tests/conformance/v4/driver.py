"""Test-only adapter that invokes production FCoP 4.0 behavior.

The adapter never implements protocol behavior. It resolves a public production
entry point, requires the complete semantic request, calls it, and returns the
unmodified result. Missing capability is a deliberate red light.
"""

from __future__ import annotations

import inspect
import multiprocessing
from dataclasses import asdict, is_dataclass
from pathlib import Path
from queue import Empty
from typing import Any, Callable, Mapping, Sequence

from fcop import Project


ACTION_CLAUSES: dict[str, str] = {
    "create_workspace": "F4.2.1-F4.2.3",
    "derive_workspace": "F4.2.4-F4.2.6",
    "create_task": "F4.3.1-F4.3.2; F4.5; F4.8",
    "read_task": "F4.4.1; F4.9.3",
    "write_report": "F4.3.3-F4.3.4; F4.6.1-F4.6.2",
    "write_issue": "F4.3.1-F4.3.3; F4.5.1",
    "write_review": "F4.3.3; F4.3.5; F4.6; F4.7",
    "mark_human_approved": "F4.3.3; F4.3.5; F4.7",
    "transition": "F4.4.1-F4.4.7",
    "inspect_state": "F4.4.1; F4.9.3",
    "list_branches": "F4.5.3-F4.5.4; F4.6.5",
    "family_digest": "F4.6.5-F4.6.8",
    "recover_operation": "F4.9.1-F4.9.11",
    "inject_fault": "F4.9.4; F4.9.9-F4.9.10",
    "export_archive": "F4.4.6; F4.9.4",
}


class V4NotImplemented(AssertionError):
    """Production has no callable surface for a required 4.0 action."""

    code = "V4_NOT_IMPLEMENTED"

    def __init__(self, test_id: str, clause: str, action: str, actual: str) -> None:
        self.test_id = test_id
        self.clause = clause
        self.action = action
        self.actual = actual
        super().__init__(
            f"[{test_id}] {clause}: production action {action!r} is not "
            f"implemented for the complete semantic request; actual={actual}; "
            f"code={self.code}"
        )


def result_field(result: Any, name: str) -> Any:
    """Read an observable result field; ``None`` and empty stubs fail."""
    if result is None:
        raise AssertionError(f"empty implementation returned None; required field={name}")
    if isinstance(result, Mapping):
        if name not in result:
            raise AssertionError(f"result mapping lacks required field {name!r}: {result!r}")
        return result[name]
    if not hasattr(result, name):
        raise AssertionError(f"result object lacks required field {name!r}: {result!r}")
    return getattr(result, name)


def digest_value(result: Any) -> str:
    """Accept a direct digest string or a non-empty result.digest field."""
    value = result if isinstance(result, str) else result_field(result, "digest")
    if not isinstance(value, str) or len(value) != 64:
        raise AssertionError(f"invalid digest result: {value!r}")
    return value


def error_code(exc: BaseException) -> str:
    """Extract only a structured machine error code.

    Free-form exception text is deliberately never parsed.  A production
    rejection must expose ``code`` or ``error_code`` on its formal error
    object; otherwise F4.10.2 has not been satisfied.
    """
    if isinstance(exc, V4NotImplemented):
        raise exc
    for name in ("code", "error_code"):
        value = getattr(exc, name, None)
        if isinstance(value, str) and value:
            return value
    raise AssertionError(
        "exception has no structured FCoP 4.0 code/error_code; "
        f"free text is not a machine contract: {exc!r}"
    )


def capture_error(call: Callable[[], Any]) -> BaseException:
    """Execute an invalid operation and require a real production rejection."""
    try:
        result = call()
    except V4NotImplemented:
        raise
    except BaseException as exc:
        return exc
    raise AssertionError(f"invalid operation unexpectedly returned {result!r}")


def _serializable_result(result: Any) -> dict[str, Any]:
    if result is None:
        return {"returned": None}
    if isinstance(result, Mapping):
        return {"returned": dict(result)}
    if is_dataclass(result):
        return {"returned": asdict(result)}
    observed: dict[str, Any] = {}
    for name in (
        "task_id", "path", "digest", "status", "classification", "state",
        "authorization_ref", "attempt_id", "existing", "created",
    ):
        if hasattr(result, name):
            value = getattr(result, name)
            observed[name] = str(value) if isinstance(value, Path) else value
    return {"returned": observed or repr(result)}


class V4ConformanceDriver:
    """Resolve semantic actions onto the real ``fcop.Project`` object."""

    _CANDIDATES: dict[str, tuple[str, ...]] = {
        "create_workspace": ("create_workspace", "init_v4", "init_solo", "init"),
        "derive_workspace": ("derive_workspace", "fork_workspace"),
        "create_task": ("create_task", "write_task"),
        "read_task": ("read_task",),
        "write_report": ("write_report",),
        "write_issue": ("write_issue",),
        "write_review": ("write_review",),
        "mark_human_approved": ("mark_human_approved",),
        "transition": ("transition", "transition_task"),
        "inspect_state": ("inspect_state",),
        "list_branches": ("list_branches",),
        "family_digest": ("family_digest", "compute_family_digest"),
        "recover_operation": ("recover_operation",),
        "inject_fault": ("inject_fault", "set_fault_injection"),
        "export_archive": ("export_archive", "export_cold_storage"),
    }

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.project = Project(self.root)

    def _resolve(
        self, action: str, kwargs: Mapping[str, Any], *, test_id: str, clause: str
    ) -> Callable[..., Any]:
        diagnostics: list[str] = []
        for candidate in self._CANDIDATES[action]:
            method = getattr(self.project, candidate, None)
            if method is None:
                diagnostics.append(f"{candidate}=absent")
                continue
            signature = inspect.signature(method)
            accepts_var_kw = any(
                parameter.kind is inspect.Parameter.VAR_KEYWORD
                for parameter in signature.parameters.values()
            )
            missing = sorted(
                key for key in kwargs if key not in signature.parameters and not accepts_var_kw
            )
            if missing:
                diagnostics.append(f"{candidate}=missing_parameters:{missing}")
                continue
            return method
        raise V4NotImplemented(test_id, clause, action, "; ".join(diagnostics))

    def _invoke(self, action: str, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        method = self._resolve(action, kwargs, test_id=test_id, clause=clause)
        return method(**kwargs)

    def create_workspace(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("create_workspace", test_id=test_id, clause=clause, **kwargs)

    def derive_workspace(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("derive_workspace", test_id=test_id, clause=clause, **kwargs)

    def create_task(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("create_task", test_id=test_id, clause=clause, **kwargs)

    def read_task(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("read_task", test_id=test_id, clause=clause, **kwargs)

    def write_report(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("write_report", test_id=test_id, clause=clause, **kwargs)

    def write_issue(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("write_issue", test_id=test_id, clause=clause, **kwargs)

    def write_review(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("write_review", test_id=test_id, clause=clause, **kwargs)

    def mark_human_approved(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("mark_human_approved", test_id=test_id, clause=clause, **kwargs)

    def transition(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("transition", test_id=test_id, clause=clause, **kwargs)

    def inspect_state(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("inspect_state", test_id=test_id, clause=clause, **kwargs)

    def list_branches(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("list_branches", test_id=test_id, clause=clause, **kwargs)

    def family_digest(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("family_digest", test_id=test_id, clause=clause, **kwargs)

    def recover_operation(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("recover_operation", test_id=test_id, clause=clause, **kwargs)

    def inject_fault(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("inject_fault", test_id=test_id, clause=clause, **kwargs)

    def export_archive(self, *, test_id: str, clause: str, **kwargs: Any) -> Any:
        return self._invoke("export_archive", test_id=test_id, clause=clause, **kwargs)


def _operation_worker(
    root: str,
    ready: multiprocessing.queues.Queue,
    start: multiprocessing.synchronize.Event,
    output: multiprocessing.queues.Queue,
    command: Mapping[str, Any],
) -> None:
    driver = V4ConformanceDriver(Path(root))
    ready.put("ready")
    start.wait()
    action = str(command["action"])
    kwargs = dict(command["kwargs"])
    try:
        result = getattr(driver, action)(**kwargs)
        output.put({"status": "returned", **_serializable_result(result)})
    except BaseException as exc:  # pragma: no cover - child-process evidence
        output.put(
            {
                "status": "error",
                "code": getattr(exc, "code", None),
                "type": type(exc).__name__,
                "message": str(exc),
            }
        )


def run_concurrent_operations(
    root: Path, commands: Sequence[Mapping[str, Any]], *, timeout: float = 30.0
) -> list[dict[str, Any]]:
    """Run real production operations in synchronized spawned processes."""
    ctx = multiprocessing.get_context("spawn")
    ready = ctx.Queue()
    start = ctx.Event()
    output = ctx.Queue()
    workers = [
        ctx.Process(target=_operation_worker, args=(str(root), ready, start, output, command))
        for command in commands
    ]
    for worker in workers:
        worker.start()
    for _ in workers:
        try:
            ready.get(timeout=timeout)
        except Empty as exc:
            raise AssertionError("worker did not reach the synchronization barrier") from exc
    start.set()
    for worker in workers:
        worker.join(timeout=timeout)
        if worker.is_alive():
            worker.terminate()
            worker.join(timeout=5)
            raise AssertionError("concurrent production operation timed out")
    results: list[dict[str, Any]] = []
    for _ in workers:
        try:
            results.append(output.get(timeout=timeout))
        except Empty as exc:
            raise AssertionError("concurrent production operation returned no result") from exc
    return results
