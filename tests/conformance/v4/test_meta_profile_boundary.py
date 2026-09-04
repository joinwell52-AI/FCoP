"""Adapter/static checks only; never counted as production behavior passes."""

from pathlib import Path
import inspect

import pytest

from . import driver as driver_module
from .driver import CALLER_AUTHORITY_FIELDS, V4ConformanceDriver
from .fixtures import DeterministicProfileEvaluator


class RecordingProject:
    """Records wiring only. Implements no FCoP authorization or transition."""

    def __init__(self, root: Path, *, trusted_profiles: object) -> None:
        self.registry = trusted_profiles
        self.requests: list[dict] = []

    def transition(self, **request: object) -> object:
        self.requests.append(request)
        return "wiring-only"


def test_registry_crosses_initialization_only(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(driver_module, "Project", RecordingProject)
    trusted = DeterministicProfileEvaluator("DENIED")
    registry = {"profile:test": trusted}
    driver = V4ConformanceDriver(tmp_path, trusted_profiles=registry)
    registry["profile:test"] = DeterministicProfileEvaluator("AUTHORIZED")
    driver.transition(test_id="meta", clause="meta", profile_ref="profile:test", authorization_ref="R")
    assert driver.project.registry["profile:test"] is trusted
    assert driver.project.requests == [{"profile_ref": "profile:test", "authorization_ref": "R"}]
    assert trusted.calls == []  # Driver does not make the authorization decision.


@pytest.mark.parametrize("action", ["transition", "create_task", "recover_operation"])
@pytest.mark.parametrize("field", ["profile_evaluator", "profile_resolver", "trusted_profiles", "caller_judge"])
def test_business_adapter_rejects_caller_authority(tmp_path: Path, action: str, field: str) -> None:
    driver = V4ConformanceDriver(tmp_path)
    forged = DeterministicProfileEvaluator("AUTHORIZED")
    value = {"profile:test": forged} if field == "trusted_profiles" else forged
    with pytest.raises(TypeError, match="caller authority is forbidden"):
        getattr(driver, action)(test_id="meta", clause="meta", **{field: value})
    assert forged.calls == []


def test_existing_production_business_signatures_do_not_advertise_judges(tmp_path: Path) -> None:
    driver = V4ConformanceDriver(tmp_path)
    for action in ("transition", "create_task", "recover_operation"):
        for name in driver._CANDIDATES[action]:
            method = getattr(driver.project, name, None)
            if callable(method):
                assert not CALLER_AUTHORITY_FIELDS.intersection(inspect.signature(method).parameters)
    # Absent v4 surfaces are covered as V4_NOT_IMPLEMENTED in behavioral tests;
    # this static check cannot earn behavioral conformance credit.
