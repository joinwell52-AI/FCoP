"""Retained path and executable-input boundaries after Host retirement."""

from __future__ import annotations

import hashlib
import os
import subprocess

import pytest

from fcop.errors import FcopError
from fcop.v4.rule_distribution._files import path_at

from .test_v4_rule_distribution import distribution as distribution
from .test_v4_rule_distribution import snapshot


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def reject_unchanged(distribution, action, request, code):
    before = snapshot(distribution[3].parent)
    with pytest.raises(FcopError) as caught:
        distribution[0].rule_distribution(action=action, request=request)
    assert caught.value.code == "toolkit:" + code
    assert snapshot(distribution[3].parent) == before


@pytest.mark.parametrize("path", ["../outside", "/absolute", "C:/outside", "C:relative", "\\\\server\\share", "nul", "COM1.txt", "x/../y", "x\x00y", "x.", "x "])
def test_target_paths_reject_without_creating_directories(distribution, path):
    before = snapshot(distribution[3].parent)
    with pytest.raises(FcopError) as caught:
        path_at(distribution[3], path, "RULE_OWNERSHIP_CONFLICT", "plan")
    assert caught.value.code == "toolkit:RULE_OWNERSHIP_CONFLICT"
    assert snapshot(distribution[3].parent) == before


def test_native_junction_is_not_a_distribution_root(distribution):
    root = distribution[3]
    outside = root.parent / "outside"
    outside.mkdir()
    link = root / "alias"
    if os.name == "nt":
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(outside)], capture_output=True, check=False)
        assert result.returncode == 0, result.stderr
    else:
        link.symlink_to(outside, target_is_directory=True)
    before = snapshot(outside)
    with pytest.raises(FcopError) as caught:
        path_at(root, "alias/entry.md", "RULE_OWNERSHIP_CONFLICT", "plan")
    assert caught.value.code == "toolkit:RULE_OWNERSHIP_CONFLICT"
    assert snapshot(outside) == before


@pytest.mark.parametrize("field", ["profile_evaluator", "profile_resolver", "model_probe", "trusted_profiles", "nested"])
def test_business_request_cannot_supply_executable_authority(distribution, field):
    value = {"nested": {"judge": lambda: "AUTHORIZED"}} if field == "nested" else {field: lambda: "AUTHORIZED"}
    reject_unchanged(distribution, "read_resource", {"resource_uri": "fcop://rules", "admin_selection_ref": value}, "RULE_HOST_UNAVAILABLE")


def test_cyclic_request_rejects_without_recursion_or_writes(distribution):
    cycle = {}
    cycle["child"] = cycle
    reject_unchanged(distribution, "read_resource", {"resource_uri": "fcop://rules", "admin_selection_ref": cycle}, "RULE_SELECTION_INVALID")
