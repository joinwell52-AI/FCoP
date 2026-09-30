"""FCoP 4.x Core. Legacy symbols are lazy, explicit compatibility access."""
from typing import Any

from fcop._version import __version__
from fcop.project import Project

_COMPAT_EXPORTS = {'rules': ('fcop.rules', None), 'BoundaryViolationError': ('fcop.errors', 'BoundaryViolationError'), 'ConfigError': ('fcop.errors', 'ConfigError'), 'FcopError': ('fcop.errors', 'FcopError'), 'ProjectAlreadyInitializedError': ('fcop.errors', 'ProjectAlreadyInitializedError'), 'ProjectNotFoundError': ('fcop.errors', 'ProjectNotFoundError'), 'ProtocolViolation': ('fcop.errors', 'ProtocolViolation'), 'RoleNotFoundError': ('fcop.errors', 'RoleNotFoundError'), 'TaskNotFoundError': ('fcop.errors', 'TaskNotFoundError'), 'TeamNotFoundError': ('fcop.errors', 'TeamNotFoundError'), 'ValidationError': ('fcop.errors', 'ValidationError'), 'InspectionReport': ('fcop.inspection', 'InspectionReport'), 'RemediationStep': ('fcop.inspection', 'RemediationStep'), 'Violation': ('fcop.inspection', 'Violation'), 'AgentLayer': ('fcop.models', 'AgentLayer'), 'BoundaryViolation': ('fcop.models', 'BoundaryViolation'), 'Capability': ('fcop.models', 'Capability'), 'DeploymentReport': ('fcop.models', 'DeploymentReport'), 'DriftEntry': ('fcop.models', 'DriftEntry'), 'DriftReport': ('fcop.models', 'DriftReport'), 'Event': ('fcop.models', 'Event'), 'EventSource': ('fcop.models', 'EventSource'), 'EventSourceKind': ('fcop.models', 'EventSourceKind'), 'EventType': ('fcop.models', 'EventType'), 'Failure': ('fcop.models', 'Failure'), 'FailureReceipt': ('fcop.models', 'FailureReceipt'), 'FailureType': ('fcop.models', 'FailureType'), 'HumanApproval': ('fcop.models', 'HumanApproval'), 'HumanApprovalChannel': ('fcop.models', 'HumanApprovalChannel'), 'HumanApprovalDecision': ('fcop.models', 'HumanApprovalDecision'), 'HumanApprovalEvidence': ('fcop.models', 'HumanApprovalEvidence'), 'Issue': ('fcop.models', 'Issue'), 'Priority': ('fcop.models', 'Priority'), 'ProjectStatus': ('fcop.models', 'ProjectStatus'), 'RecentActivityEntry': ('fcop.models', 'RecentActivityEntry'), 'Recovery': ('fcop.models', 'Recovery'), 'RecoveryAction': ('fcop.models', 'RecoveryAction'), 'RecoveryOutcome': ('fcop.models', 'RecoveryOutcome'), 'Report': ('fcop.models', 'Report'), 'ResumePayload': ('fcop.models', 'ResumePayload'), 'RetryPlan': ('fcop.models', 'RetryPlan'), 'Review': ('fcop.models', 'Review'), 'ReviewDecision': ('fcop.models', 'ReviewDecision'), 'ReviewSubjectType': ('fcop.models', 'ReviewSubjectType'), 'RiskLevel': ('fcop.models', 'RiskLevel'), 'RoleOccupancy': ('fcop.models', 'RoleOccupancy'), 'RollbackPlan': ('fcop.models', 'RollbackPlan'), 'SessionRecoveryAction': ('fcop.models', 'SessionRecoveryAction'), 'SessionRecoveryResult': ('fcop.models', 'SessionRecoveryResult'), 'SessionRoleConflict': ('fcop.models', 'SessionRoleConflict'), 'Severity': ('fcop.models', 'Severity'), 'Skill': ('fcop.models', 'Skill'), 'SkillTool': ('fcop.models', 'SkillTool'), 'Task': ('fcop.models', 'Task'), 'TaskFrontmatter': ('fcop.models', 'TaskFrontmatter'), 'TeamConfig': ('fcop.models', 'TeamConfig'), 'ValidationIssue': ('fcop.models', 'ValidationIssue'), 'EventSubscription': ('fcop.compatibility.v3.project', 'EventSubscription'), 'teams': ('fcop.teams', None)}

def __getattr__(name: str) -> Any:
    import importlib
    if name not in _COMPAT_EXPORTS:
        raise AttributeError(name)
    module, attribute = _COMPAT_EXPORTS[name]
    loaded = importlib.import_module(module)
    value = loaded if attribute is None else getattr(loaded, attribute)
    globals()[name] = value
    return value


__all__ = ["Project", "__version__", *_COMPAT_EXPORTS]
