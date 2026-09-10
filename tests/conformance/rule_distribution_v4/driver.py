"""Test-only public binding; no distribution algorithms or success defaults."""

from pathlib import Path

from fcop import Project

PUBLIC_ENTRY = "fcop.Project.rule_distribution"


class DistributionNotImplementedError(AssertionError):
    """A missing production capability is a red test, including rejection cases."""

    code = "RULE_DISTRIBUTION_NOT_IMPLEMENTED"

    def __init__(self, action):
        self.operation = action
        self.public_entry = PUBLIC_ENTRY
        super().__init__(f"{self.code}: {PUBLIC_ENTRY} ({action})")


class RuleDistributionConformanceDriver:
    """Forward an explicit semantic request; return the original result.

    The name is a test binding, not a production API introduced by this suite.
    Later authorized integration may bind this adapter to the public facade;
    no fallback to legacy writers, private modules, or signature probes exists.
    """

    def __init__(self, root: Path):
        self.project = Project(root)

    def invoke(self, action, request):
        entry = getattr(self.project, "rule_distribution", None)
        if not callable(entry):
            raise DistributionNotImplementedError(action)
        return entry(action=action, request=request)
