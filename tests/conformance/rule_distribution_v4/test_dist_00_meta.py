"""Static integrity guards; none substitute for production behavior coverage."""

import ast
import re
from pathlib import Path

import pytest

from .conftest import (
    ALLOWLIST,
    INPUT_HEAD,
    OWNED,
    REPO,
    SUITE_FILES,
    WP4C_2_ACCEPTED_HEAD,
    WP4C_2_INPUT_HEAD,
    assert_historical_allowlist,
    field,
    git,
    historical_delivery_paths,
    input_blob,
    sha,
    snapshot,
    structured_code,
)
from .driver import DistributionNotImplementedError

HERE = Path(__file__).parent


def sources():
    return {p.name: p.read_text(encoding="utf-8") for p in HERE.glob("*.py")}


def behavior_functions():
    return [
        n
        for name, source in sources().items()
        if name.startswith("test_dist_") and name != "test_dist_00_meta.py"
        for n in ast.parse(source).body
        if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")
    ]


def has_executable_logic(statements):
    """Find non-placeholder statements inside control suites, not by count.

    This is a bounded static anti-stub guard, not a proof of reachability or
    behavioral correctness. The independent assertions/action/effect guards
    below remain mandatory. Nested definitions alone do not execute a test.
    """
    for node in statements:
        if isinstance(node, (ast.Pass, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While)):
            if has_executable_logic(node.body) or has_executable_logic(node.orelse):
                return True
            continue
        if isinstance(node, (ast.With, ast.AsyncWith)):
            if has_executable_logic(node.body):
                return True
            continue
        if isinstance(node, ast.Try):
            suites = [node.body, node.orelse, node.finalbody, *(h.body for h in node.handlers)]
            if any(has_executable_logic(suite) for suite in suites):
                return True
            continue
        if isinstance(node, ast.Match):
            if any(has_executable_logic(case.body) for case in node.cases):
                return True
            continue
        # Includes docstrings, Ellipsis, bare return/return None and
        # constant-only placeholder results; no statement is counted.
        if isinstance(node, (ast.Expr, ast.Return)) and (
            node.value is None or isinstance(node.value, ast.Constant)
        ):
            continue
        if isinstance(node, ast.Assert) and isinstance(node.test, ast.Constant):
            continue
        if isinstance(node, ast.Raise):
            exc = node.exc.func if isinstance(node.exc, ast.Call) else node.exc
            if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
                continue
        return True
    return False


@pytest.mark.parametrize(
    "body",
    [
        "if ready:\n    result = run()\n    assert result == expected\nelse:\n    reject()",
        "if ready:\n    if nested:\n        assert run() == expected\n    else:\n        reject()",
        "if a:\n    assert run()\nelif b:\n    reject()\nelse:\n    assert other()",
        "try:\n    assert run()\nexcept ValueError:\n    reject()\nfinally:\n    inspect()",
        "match value:\n    case 1:\n        assert run()\n    case _:\n        reject()",
        "for value in values:\n    assert run(value) == expected",
        "while pending():\n    assert run()",
        "with context():\n    assert run()",
    ],
    ids=["single-if", "nested-if", "if-elif-else", "try", "match", "for", "while", "with"],
)
def test_meta_guard_accepts_real_control_logic(body):
    assert has_executable_logic(ast.parse(body).body)


@pytest.mark.parametrize(
    "body",
    [
        "pass",
        "...",
        '"docstring only"',
        '"docstring"\n...',
        "",
        "if ready:\n    pass\nelse:\n    ...",
        "if ready:\n    if nested:\n        ...",
        "return None",
        "return",
        "raise NotImplementedError",
        "raise NotImplementedError()",
        "assert True",
        "def never_called():\n    assert run()",
    ],
    ids=[
        "pass",
        "ellipsis",
        "docstring",
        "docstring-ellipsis",
        "empty-body",
        "empty-branches",
        "nested-empty",
        "return-none",
        "bare-return",
        "not-implemented",
        "not-implemented-call",
        "constant-assert",
        "definition-only",
    ],
)
def test_meta_guard_rejects_placeholders(body):
    assert not has_executable_logic(ast.parse(body).body)


def test_meta_exact_ids_and_grouping():
    functions = behavior_functions()
    assert len(functions) == 30
    assert {n.name for n in functions} == {f"test_dist_{i:02}" for i in range(1, 31)}
    for n in functions:
        assert re.findall(r"DIST-\d{2}", ast.get_docstring(n)) == [
            n.name.replace("test_dist_", "DIST-")
        ]
    assert set(sources()) == set(SUITE_FILES)


def test_meta_matrix_trace_and_owner_exception():
    matrix = input_blob("reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md").decode()
    for n in behavior_functions():
        doc = ast.get_docstring(n)
        test_id = re.search(r"DIST-\d{2}", doc).group()
        row = next(line for line in matrix.splitlines() if line.startswith(f"| {test_id} |"))
        assert re.search(r"RD-[0-9/]+", doc).group() == row.split("|")[2].strip()
        assert re.findall(r"Owner: (WP4C\.\d)", doc) == [row.split("|")[-2].strip()]
        assert all(word in doc for word in ["Arrange", "Act", "Assert"])
    control = next(n for n in behavior_functions() if n.name == "test_dist_30")
    assert "Owner: WP4C.2" in ast.get_docstring(control)
    assert not any(
        isinstance(n, ast.Name) and n.id in {"case", "RuleDistributionConformanceDriver"}
        for n in ast.walk(control)
    )


def test_meta_no_skip_xfail_or_empty_tests():
    for source in sources().values():
        tree = ast.parse(source)
        assert not any(
            isinstance(n, ast.Attribute) and n.attr in {"skip", "skipif", "xfail"}
            for n in ast.walk(tree)
        )
        assert not any(isinstance(n, ast.Pass) for n in ast.walk(tree))
    for n in behavior_functions():
        assert has_executable_logic(n.body), f"PLACEHOLDER_TEST:{n.name}"
        assert any(
            isinstance(a, ast.Assert)
            or isinstance(a, ast.Call)
            and isinstance(a.func, ast.Attribute)
            and a.func.attr == "reject"
            for a in ast.walk(n)
        )
        assert not any(
            isinstance(a, ast.Assert) and isinstance(a.test, ast.Constant) for a in ast.walk(n)
        )


def test_meta_driver_has_only_public_forwarding():
    tree = ast.parse(sources()["driver.py"])
    imports = {n.module for n in tree.body if isinstance(n, ast.ImportFrom)}
    assert imports == {"pathlib", "fcop"}
    klass = next(
        n
        for n in tree.body
        if isinstance(n, ast.ClassDef) and n.name == "RuleDistributionConformanceDriver"
    )
    assert {n.name for n in klass.body if isinstance(n, ast.FunctionDef)} == {"__init__", "invoke"}
    invoke = next(n for n in klass.body if isinstance(n, ast.FunctionDef) and n.name == "invoke")
    returns = [n for n in ast.walk(invoke) if isinstance(n, ast.Return)]
    assert len(returns) == 1
    assert ast.unparse(returns[0].value) == "entry(action=action, request=request)"
    assert not any(
        isinstance(n, (ast.For, ast.While, ast.Try, ast.DictComp, ast.ListComp))
        for n in ast.walk(klass)
    )
    assert "deploy_protocol_rules" not in sources()["driver.py"]


def test_meta_effect_assertions_and_real_process_race():
    for n in behavior_functions():
        if n.name == "test_dist_30":
            continue
        calls = [
            a.func.attr
            for a in ast.walk(n)
            if isinstance(a, ast.Call) and isinstance(a.func, ast.Attribute)
        ]
        assert set(calls) & {"invoke", "reject", "adopt", "deploy"}, n.name
    fixture = sources()["conftest.py"]
    assert "snapshot(self.sandbox)" in fixture
    assert "before == after" in fixture
    assert 'get_context("spawn")' in fixture and "ctx.Barrier(2)" in fixture
    assert 'invoke("apply", request)' in fixture
    assert "parallel_surface_probe" not in fixture
    assert 'raise DistributionNotImplementedError("apply:two-spawn-processes")' in fixture


def test_meta_tmp_only_writes_and_no_network():
    fixture = ast.parse(sources()["conftest.py"])
    put = next(n for n in ast.walk(fixture) if isinstance(n, ast.FunctionDef) and n.name == "put")
    assert "is_relative_to(self.sandbox.resolve())" in ast.unparse(put)
    assert "Scenario(tmp_path, request.node)" in sources()["conftest.py"]
    for source in sources().values():
        for n in ast.walk(ast.parse(source)):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                names = (
                    [n.module or ""] if isinstance(n, ast.ImportFrom) else [a.name for a in n.names]
                )
                assert not any(
                    x.split(".")[0] in {"requests", "httpx", "socket", "urllib"} for x in names
                )
    assert not any("D:\\FCoP" in s for s in sources().values())


def test_meta_frozen_core_hashes_and_sixty_ids():
    paths = (
        git("ls-tree", "-r", "--name-only", INPUT_HEAD, "tests/conformance/v4")
        .decode()
        .splitlines()
    )
    assert len(paths) == 18
    combined = ""
    for p in paths:
        expected = input_blob(p)
        assert sha(git("show", f"HEAD:{p}")) == sha(expected)
        assert (
            git("hash-object", "--path", p, str(REPO / p)).strip()
            == git("rev-parse", f"{INPUT_HEAD}:{p}").strip()
        )
        if Path(p).name.startswith("test_"):
            combined += expected.decode()
    ids = set(
        re.findall(
            r"\b(?:C[0-8]-(?:[A-Z]+-)*[A-Z]*\d{2}|AT-\d{2}|MCP-[A-Z]+-\d{2}|RELEASE-GATE-01)\b(?!-)",
            combined,
        )
    )
    assert len(ids) == 60


def test_meta_frozen_contract_gate_and_manifest():
    paths = [
        "docs/fcop-4.0/rule-distribution-contract.md",
        "docs/fcop-4.0/rule-distribution-contract.zh.md",
        "reviews/fcop-4.0/gates/WP4C-1-RULE-DISTRIBUTION-CONTRACT-FROZEN.md",
        "reviews/fcop-4.0/wp4c.1/MANIFEST.md",
        "reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md",
    ]
    for p in paths:
        assert sha(git("show", f"HEAD:{p}")) == sha(input_blob(p))
        assert (
            git("hash-object", "--path", p, str(REPO / p)).strip()
            == git("rev-parse", f"{INPUT_HEAD}:{p}").strip()
        )
    # Historical candidate evidence remains pinned to its original input.
    assert (
        sha(input_blob("spec/fcop-4.0-spec.md"))
        == "0c5005ec754ee71d735e02c9ea403adbc35e8dff9ce98c13d8a42040cacbc8e9"
    )
    # ADMIN CLI release-identity amendment: exact current Stable spec blobs,
    # not the historical Candidate presentation. All other contracts stay fixed.
    stable_revision = "5c27e1bc90dce799aa7fa89e6cc717e01d47693e"
    stable_specs = {
        "spec/fcop-4.0-spec.md":
            "9e6fd97ed4f3fa4bf9178babd54fd671fe4cc5f7bf7b8ee985d1726fb8c0e491",
        "spec/fcop-4.0-spec.zh.md":
            "babe6acad7ddcd41ae06a3e9b21334b191576111905012f752a3052d5951dcf9",
    }
    for p, expected_sha in stable_specs.items():
        expected = git("show", f"{stable_revision}:{p}")
        assert sha(expected) == expected_sha
        assert git("show", f"HEAD:{p}") == expected
        assert (REPO / p).read_bytes() == expected
        assert (
            git("hash-object", "--path", p, str(REPO / p)).strip()
            == git("rev-parse", f"{stable_revision}:{p}").strip()
        )


def test_meta_empty_result_and_text_error_rejected():
    # Test the independent assertion helper, not a monkeypatched production
    # success. Methods returning None/empty dict cannot satisfy any output field.
    for result in [None, {}, object()]:
        with pytest.raises(AssertionError):
            field(result, "after_bytes")
    with pytest.raises(AssertionError, match="Structured error required"):
        structured_code(ValueError("toolkit:RULE_MANIFEST_INVALID"))
    with pytest.raises(DistributionNotImplementedError):
        structured_code(DistributionNotImplementedError("validate"))


def test_meta_input_fixture_is_not_success_output(case):
    state = snapshot(case.sandbox)
    assert not any("/adoptions/" in p or "/deployments/" in p for p in state)
    assert not (case.root / "AGENTS.md").exists()
    assert len(case.manifest["artifacts"]) == 18
    assert sum(len(refs) for refs in OWNED.values()) == 73
    assert len({ref for refs in OWNED.values() for ref in refs}) == 73


def test_meta_allowlist_and_no_stage_advance():
    assert INPUT_HEAD == WP4C_2_INPUT_HEAD == "921be62c32ccccece53be74e7e565b1b37731fbe"
    assert WP4C_2_ACCEPTED_HEAD == "1f4df9cc650f63b9e842d806340eb31b768f708e"
    assert all(re.fullmatch(r"[0-9a-f]{40}", ref) for ref in (
        INPUT_HEAD, WP4C_2_INPUT_HEAD, WP4C_2_ACCEPTED_HEAD
    ))
    changes = historical_delivery_paths()
    assert len(changes) == 13
    assert changes == ALLOWLIST
    assert_historical_allowlist(changes)
    with pytest.raises(AssertionError):
        assert_historical_allowlist(changes | {"src/unapproved-fourteenth-path.py"})
    assert not git(
        "rev-list", "--merges", f"{WP4C_2_INPUT_HEAD}..{WP4C_2_ACCEPTED_HEAD}"
    ).strip()
    assert git("merge-base", "--is-ancestor", WP4C_2_ACCEPTED_HEAD, "HEAD") == b""
    later = "de213ec0f74f8976283a24986d4eb7de77c67142"
    assert git("merge-base", "--is-ancestor", later, "HEAD") == b""
    later_paths = set(git("diff", "--name-only", WP4C_2_ACCEPTED_HEAD, later).decode().splitlines())
    assert later_paths == {
        "taskbooks/fcop-4.0/WP4C.3/01-Canonical-Rule-Package-Manifest-Loader-and-Assemblies-Taskbook-v1.0.zh.md"
    }
    assert not changes & later_paths
    # Current untracked paths are not inputs to the history-only function.
    # Current-stage cleanliness/allowlist remain executor and Manifest checks.
    tree = ast.parse(sources()["conftest.py"])
    helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "historical_delivery_paths")
    assert not helper.args.args and not helper.args.kwonlyargs
    calls = [n for n in ast.walk(helper) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "git"]
    assert len(calls) == 1
    assert [ast.unparse(a) for a in calls[0].args] == [
        "'diff'", "'--name-only'", "WP4C_2_INPUT_HEAD", "WP4C_2_ACCEPTED_HEAD"
    ]
    assert historical_delivery_paths() == changes


def test_meta_projection_oracle_never_writes():
    tree = ast.parse(sources()["conftest.py"])
    oracle = next(
        n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "expected_embed"
    )
    assert not any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr in {"put", "write_bytes", "write_text", "mkdir", "invoke"}
        for n in ast.walk(oracle)
    )
    assert any(isinstance(n, ast.Return) for n in ast.walk(oracle))
