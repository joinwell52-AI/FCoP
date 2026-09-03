"""Static driver wiring checks; these are not behavioral conformance credit."""

from __future__ import annotations

import ast
from pathlib import Path

from .driver import ACTION_CLAUSES, V4ConformanceDriver


def test_driver_declares_every_semantic_action() -> None:
    expected = {
        "create_workspace", "derive_workspace", "create_task", "read_task",
        "write_report", "write_issue", "write_review",
        "mark_human_approved", "transition", "inspect_state", "list_branches",
        "family_digest", "recover_operation", "inject_fault", "export_archive",
    }
    assert set(ACTION_CLAUSES) == expected
    assert all(callable(getattr(V4ConformanceDriver, name, None)) for name in expected)


def test_surface_probe_is_not_a_race_primitive() -> None:
    assert not hasattr(V4ConformanceDriver, "parallel_surface_probe")


def test_every_contract_test_has_arrange_act_assert() -> None:
    root = Path(__file__).parent
    files = [*root.glob("test_c[0-8]_*.py"), root / "test_mcp_surface_contract.py"]
    missing: list[str] = []
    for path in files:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                segment = ast.get_source_segment(source, node) or ""
                absent = [word for word in ("Arrange", "Act", "Assert") if word not in segment]
                if absent:
                    missing.append(f"{path.name}::{node.name}:{','.join(absent)}")
    assert not missing, f"contract tests missing explicit AAA sections: {missing}"
