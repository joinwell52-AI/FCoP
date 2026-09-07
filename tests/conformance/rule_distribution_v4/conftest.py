"""Deterministic INPUT fixtures and independent output/effect assertions.

Only Scenario.put writes, bounded to tmp_path. Expected projections are never
written as production outputs. Successful adoption/deployment receipts must
come from actual production operations, never from fixture setup.
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import re
import subprocess
from pathlib import Path

import pytest

from .driver import PUBLIC_ENTRY, DistributionNotImplementedError, RuleDistributionConformanceDriver

INPUT_HEAD = "921be62c32ccccece53be74e7e565b1b37731fbe"
REPO = Path(__file__).resolve().parents[3]
BEGIN = b"<!-- fcop:v4:begin -->\n"
END = b"<!-- fcop:v4:end -->\n"
MODULES = [
    "workspace",
    "envelopes",
    "relations",
    "authorization",
    "idempotency",
    "recovery",
    "lifecycle",
    "compatibility",
    "convergence",
]
SEQUENTIAL = MODULES[:-1]
RELATIONS = ["parent", "branch_of", "subject_ref", "references"]
WORKSPACE_ID = "urn:uuid:00000000-0000-4000-8000-000000000001"
EXCLUDED_RC = "87cf212d1cb75cefd0da6da7e5f0f4c7eaedbc231c784b985c3e2e51856abc4c"
DEPS = [
    [],
    ["workspace"],
    ["workspace", "envelopes"],
    ["workspace", "envelopes", "relations"],
    ["workspace"],
    ["workspace"],
    ["workspace", "envelopes", "relations", "authorization", "idempotency", "recovery"],
    ["workspace"],
    SEQUENTIAL,
]
OWNED = {
    "workspace": ["F4.1.1", *[f"F4.2.{i}" for i in range(1, 7)], "F4.12.1"],
    "envelopes": [f"F4.3.{i}" for i in range(1, 6)],
    "relations": ["F4.5.1", "F4.5.2", "F4.5.5"],
    "authorization": [f"F4.7.{i}" for i in range(1, 8)],
    "idempotency": [f"F4.8.{i}" for i in range(1, 6)],
    "recovery": [f"F4.9.{i}" for i in range(1, 12)],
    "lifecycle": [*[f"F4.4.{i}" for i in range(1, 8)], *[f"F4.6.{i}" for i in range(1, 5)]],
    "compatibility": [
        *[f"F4.0.{i}" for i in range(1, 4)],
        *[f"F4.1.{i}" for i in range(2, 5)],
        *[f"F4.10.{i}" for i in range(1, 4)],
        *[f"F4.11.{i}" for i in range(1, 6)],
        *[f"F4.12.{i}" for i in range(2, 5)],
    ],
    "convergence": ["F4.5.3", "F4.5.4", *[f"F4.6.{i}" for i in range(5, 9)]],
}
ERRORS = [
    "RULE_MANIFEST_INVALID",
    "RULE_ARTIFACT_MISMATCH",
    "RULE_SELECTION_INVALID",
    "RULE_HOST_UNAVAILABLE",
    "RULE_PROJECTION_LIMIT",
    "RULE_OWNERSHIP_CONFLICT",
    "RULE_ADOPTION_REQUIRED",
    "RULE_DEPLOYMENT_RECOVERY_REQUIRED",
]
HOSTS = {"codex": "AGENTS.md", "cursor": ".cursor/rules/fcop-v4.mdc", "claude-code": "CLAUDE.md"}
SUITE_FILES = [
    "__init__.py",
    "conftest.py",
    "driver.py",
    "test_dist_00_meta.py",
    "test_dist_01_06_manifest.py",
    "test_dist_07_12_profiles.py",
    "test_dist_13_20_projection.py",
    "test_dist_21_24_assembly_compat_mcp.py",
    "test_dist_25_30_failures_artifacts_context_gates.py",
]
ALLOWLIST = (
    {f"tests/conformance/rule_distribution_v4/{p}" for p in SUITE_FILES}
    | {f"reports/FCOP-4.0-WP4C.2-{s}.md" for s in ["CONFORMANCE-PLAN", "RED-BASELINE", "RESULT"]}
    | {"reviews/fcop-4.0/wp4c.2/MANIFEST.md"}
)


def sha(data):
    """Independent raw-byte expected value, not a loader/digest implementation."""
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    """Serialize fixture INPUT, not production receipts/results."""
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def snapshot(root):
    """Include directories, files and symlinks; do not follow symlink targets."""
    result = {}
    for current, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(current) / name
            key = p.relative_to(root).as_posix()
            result[key] = (
                ("link", os.readlink(p))
                if p.is_symlink()
                else (("dir", None) if p.is_dir() else ("file", p.read_bytes()))
            )
    return result


def field(result, name):
    """An empty method or missing postcondition never becomes a success."""
    assert result is not None, "EMPTY_IMPLEMENTATION_RESULT"
    if isinstance(result, dict):
        assert name in result, f"MISSING_RESULT_FIELD:{name}"
        return result[name]
    assert hasattr(result, name), f"MISSING_RESULT_FIELD:{name}"
    return getattr(result, name)


def structured_code(error):
    if isinstance(error, DistributionNotImplementedError):
        raise error
    code = getattr(error, "code", None) or getattr(error, "error_code", None)
    assert isinstance(code, str), "Structured error required; exception text is not a code"
    return code


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args])


def input_blob(path):
    return git("show", f"{INPUT_HEAD}:{path}")


class Scenario:
    def __init__(self, sandbox, node=None, host="codex"):
        self.sandbox = sandbox
        self.root = sandbox / "workspace"
        self.package = sandbox / "package"
        self.node = node
        self.driver = None
        self.profile = {
            "host_id": host,
            "profile_version": "1.0-candidate.1",
            "supported_entry_kinds": ["cursor-mdc" if host == "cursor" else "markdown"],
            "reference_mode": "none",
            "projection_mode": "bounded_embed",
            "target_paths": [HOSTS[host]],
            "preserve_regions": [[BEGIN.decode().strip(), END.decode().strip()]],
            "max_projection_bytes": 65536,
            "encoding": "UTF-8-no-BOM",
            "newline": "LF",
            "languages": ["en"],
        }
        self.manifest = {
            "manifest_schema": "fcop-rule-distribution/v1",
            "protocol_version": "4.0",
            "package_version": "4.0.0-fixture.1",
            "artifacts": [],
        }
        for i, module in enumerate(MODULES):
            for lang in ["en", "zh"]:
                body = (
                    f"# {module} ({lang})\n"
                    + "\n".join(f"Non-normative fixture citation: {ref}." for ref in OWNED[module])
                    + "\n"
                ).encode()
                self.put(self.package / f"{module}.{lang}.md", body)
                self.manifest["artifacts"].append(
                    {
                        "module_id": module,
                        "source_path": f"{module}.{lang}.md",
                        "language": lang,
                        "sha256": sha(body),
                        "size_bytes": len(body),
                        "normative_clause_refs": OWNED[module].copy(),
                        "depends_on": DEPS[i].copy(),
                        "load_order": (i + 1) * 10,
                        "audience": "business-agent",
                        "required_when": "branch-family" if module == "convergence" else "common",
                        "conflicts_with": [],
                    }
                )
        self.put(
            self.root / "fcop/fcop.json",
            json_bytes(
                {
                    "protocol": "fcop",
                    "protocol_version": "4.0",
                    "workspace_id": WORKSPACE_ID,
                    "encoding": {"name": "fcop-filesystem", "version": "4.0"},
                    "profiles": [],
                }
            ),
        )
        self.put(
            self.sandbox / "inputs/admin-selection.md",
            b"Explicit offline ADMIN selection fixture.\n",
        )
        self.flush()

    def put(self, path, data):
        """All test writes are confined to the pytest fixture sandbox."""
        path = Path(path)
        assert path.resolve().is_relative_to(self.sandbox.resolve())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def flush(self):
        self.put(self.package / "manifest.json", json_bytes(self.manifest))
        self.put(self.sandbox / "inputs/profile.json", json_bytes(self.profile))

    def request(self, **overrides):
        result = {
            "manifest_path": str(self.package / "manifest.json"),
            "host_profile_path": str(self.sandbox / "inputs/profile.json"),
            "workspace_id": WORKSPACE_ID,
            "protocol_version": "4.0",
            "assembly_id": "sequential",
            "selected_modules": SEQUENTIAL.copy(),
            "selected_languages": ["en"],
            "admin_selection_ref": {
                "path": str(self.sandbox / "inputs/admin-selection.md"),
                "sha256": sha((self.sandbox / "inputs/admin-selection.md").read_bytes()),
            },
            "recorded_at": "2026-09-07T00:00:00+00:00",
        }
        result.update(overrides)
        return result

    def invoke(self, action, request=None, *, readonly=False):
        before = snapshot(self.sandbox)
        code = None
        try:
            if self.driver is None:
                self.driver = RuleDistributionConformanceDriver(self.root)
            return self.driver.invoke(action, self.request() if request is None else request)
        except Exception as exc:
            code = getattr(exc, "code", None)
            raise
        finally:
            after = snapshot(self.sandbox)
            changed = sorted(
                k for k in before.keys() | after.keys() if before.get(k) != after.get(k)
            )
            if self.node is not None:
                self.node.user_properties.append(
                    (
                        "operation_evidence",
                        json.dumps(
                            {
                                "action": action,
                                "public_entry": PUBLIC_ENTRY,
                                "structured_error": code,
                                "changed_paths": changed,
                                "zero_write_verified": before == after,
                            }
                        ),
                    )
                )
            if readonly or code == "RULE_DISTRIBUTION_NOT_IMPLEMENTED":
                assert after == before, f"UNEXPECTED_FILE_EFFECT:{changed}"

    def reject(self, action, code, request=None):
        before = snapshot(self.sandbox)
        with pytest.raises(Exception) as caught:
            self.invoke(action, request)
        assert snapshot(self.sandbox) == before, "Rejection modified files/directories"
        error = caught.value
        assert structured_code(error) == f"toolkit:{code}"
        assert field(error, "operation") == action
        assert field(error, "subject_ref")
        assert "secret-fixture-token" not in str(field(error, "details"))

    def adopt(self):
        result = self.invoke("adopt")
        ref = field(result, "adoption_receipt_ref")
        receipt = self.read_receipt(ref, "adoptions")
        assert receipt["workspace_id"] == WORKSPACE_ID
        assert receipt["receipt_schema"] == "fcop-rule-adoption/v1"
        assert receipt["rule_manifest_sha256"] == sha((self.package / "manifest.json").read_bytes())
        assert receipt["selected_modules"] == SEQUENTIAL
        assert receipt["selected_languages"] == ["en"]
        assert not any((self.root / p).exists() for p in self.profile["target_paths"])
        return ref

    def read_receipt(self, ref, kind):
        rel = field(ref, "path")
        digest = field(ref, "sha256")
        assert rel == f"fcop/internal/rule-distribution/{kind}/{digest}.json"
        p = self.root / rel
        data = p.read_bytes()
        assert sha(data) == digest
        return json.loads(data)

    def deploy(self, adoption=None):
        ref = self.adopt() if adoption is None else adoption
        request = self.request(adoption_receipt_ref=ref)
        before = snapshot(self.sandbox)
        plan = self.invoke("plan", request, readonly=True)
        assert snapshot(self.sandbox) == before
        output = field(plan, "targets")
        assert output
        result = self.invoke("apply", self.request(adoption_receipt_ref=ref, plan=plan))
        receipt_ref = field(result, "deployment_receipt_ref")
        receipt = self.read_receipt(receipt_ref, "deployments")
        assert receipt["adoption_receipt_ref"] == ref
        assert receipt["action"] == "deploy"
        assert {t["path"] for t in receipt["targets"]} == set(self.profile["target_paths"])
        for target in receipt["targets"]:
            p = self.root / target["path"]
            assert sha(p.read_bytes()) == target["after_sha256"]
            assert p.read_bytes() == field(
                next(t for t in output if field(t, "path") == target["path"]), "after_bytes"
            )
        return receipt_ref, receipt

    def expected_embed(self, modules=None, languages=None):
        """Independent literal RD-13/15 oracle, NEVER written to a target."""
        modules = SEQUENTIAL if modules is None else modules
        languages = ["en"] if languages is None else languages
        header = (
            f"<!-- fcop:package={self.manifest['package_version']};manifest={sha((self.package / 'manifest.json').read_bytes())};"
            f"host={self.profile['host_id']}@{self.profile['profile_version']};assembly="
            f"{'parallel' if modules == MODULES else 'sequential'};language={','.join(languages)} -->\n"
        ).encode()
        body = b""
        for module in modules:
            for lang in languages:
                raw = (self.package / f"{module}.{lang}.md").read_bytes()
                body += (
                    f"<!-- fcop:module={module};language={lang};sha256={sha(raw)} -->\n".encode()
                    + raw
                    + b"\n"
                )
        prefix = (
            b"---\ndescription: FCoP 4.0 selected guidance\nalwaysApply: true\n---\n\n"
            if self.profile["host_id"] == "cursor"
            else b""
        )
        return prefix + BEGIN + header + body + END


@pytest.fixture
def case(tmp_path, request):
    return Scenario(tmp_path, request.node)


def race_worker(root, barrier, queue, request):
    """Perform real production apply requests after a cross-process barrier."""
    barrier.wait(timeout=30)
    try:
        result = RuleDistributionConformanceDriver(Path(root)).invoke("apply", request)
        queue.put({"pid": os.getpid(), "result": result, "code": None})
    except Exception as exc:
        queue.put(
            {"pid": os.getpid(), "code": getattr(exc, "code", None), "error": type(exc).__name__}
        )


def concurrent_apply(case, requests):
    ctx = multiprocessing.get_context("spawn")
    barrier, queue = ctx.Barrier(2), ctx.Queue()
    workers = [
        ctx.Process(target=race_worker, args=(str(case.root), barrier, queue, r)) for r in requests
    ]
    before = snapshot(case.sandbox)
    try:
        for worker in workers:
            worker.start()
        results = [queue.get(timeout=60) for _ in workers]
        for worker in workers:
            worker.join(timeout=10)
            assert worker.exitcode == 0
        assert len({r["pid"] for r in results}) == 2
        if any(r["code"] == "RULE_DISTRIBUTION_NOT_IMPLEMENTED" for r in results):
            assert snapshot(case.sandbox) == before
            case.node.user_properties.append(
                (
                    "operation_evidence",
                    json.dumps(
                        {
                            "action": "apply:two-spawn-processes",
                            "public_entry": PUBLIC_ENTRY,
                            "structured_error": "RULE_DISTRIBUTION_NOT_IMPLEMENTED",
                            "changed_paths": [],
                            "zero_write_verified": True,
                            "process_ids": [r["pid"] for r in results],
                        }
                    ),
                )
            )
            raise DistributionNotImplementedError("apply:two-spawn-processes")
        return results
    finally:
        for worker in workers:
            if worker.is_alive():
                worker.terminate()
                worker.join(timeout=5)
        queue.close()


def metadata(function):
    text = function.__doc__ or ""
    return (
        re.search(r"DIST-\d{2}", text).group(),
        re.search(r"RD-[0-9/ -]+", text).group().strip(),
        re.search(r"Owner: (WP4C\.\d)", text).group(1),
    )
