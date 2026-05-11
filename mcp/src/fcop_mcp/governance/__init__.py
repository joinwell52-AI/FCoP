"""FCoP Capability Governance — Layer 1 behavior audit middleware.

SMB / audit-first design (ADR-0030-bis).

Three things only: find skill → tag risk → write event log.
No blocking.  No approval tokens.  No policy engine.

Usage:
    from fcop_mcp.governance import FCoPGovernanceMiddleware
    mcp.add_middleware(FCoPGovernanceMiddleware())
"""

from .events import emit_event
from .interceptor import FCoPGovernanceMiddleware
from .skill_resolver import SkillMeta, load_registry_yaml, resolve_skill

__all__ = [
    "FCoPGovernanceMiddleware",
    "resolve_skill",
    "SkillMeta",
    "load_registry_yaml",
    "emit_event",
]
