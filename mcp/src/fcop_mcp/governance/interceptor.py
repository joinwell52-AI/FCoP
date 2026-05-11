"""FCoPGovernanceMiddleware — FastMCP on_call_tool hook.

SMB / audit-first design (ADR-0030-bis).

Role: behavior ledger, NOT an enforcement firewall.

Three things only:
  1. Skill lookup  — tool_name → risk level
  2. Risk tagging  — Safe / Sensitive / Critical
  3. Event log     — append-only, always before call_next

Execution behavior:
  - Safe:      log → allow
  - Sensitive: log (REVIEW_TAG) → allow
  - Critical:  log (CRITICAL_TAG) → allow

There is no blocking.  Blocking adds ×3 complexity for near-zero SMB
benefit.  The audit event IS the governance artifact.

Install:
    from fcop_mcp.governance import FCoPGovernanceMiddleware
    mcp.add_middleware(FCoPGovernanceMiddleware())
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

import mcp.types as mt
from fastmcp.server.middleware import CallNext, Middleware, MiddlewareContext

from .events import emit_event
from .skill_resolver import resolve_skill

# risk level → audit tag (pure 3-entry table, no policy engine needed)
_RISK_TAG: dict[str, str] = {
    "Safe": "ALLOW",
    "Sensitive": "REVIEW_TAG",
    "Critical": "CRITICAL_TAG",
}


def _args_hash(args: dict[str, Any] | None) -> str:
    canonical = json.dumps(args or {}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _session_id(context: MiddlewareContext[Any]) -> str | None:
    try:
        fc = context.fastmcp_context
        if fc is not None:
            return str(getattr(fc, "client_id", None) or getattr(fc, "session_id", None))
    except Exception:
        pass
    return None


class FCoPGovernanceMiddleware(Middleware):
    """Stateless audit middleware — find skill, tag risk, write log, allow."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[mt.CallToolRequestParams],
        call_next: CallNext,
    ) -> Any:
        params = context.message
        tool_name: str = params.name
        args: dict[str, Any] = params.arguments or {}

        # 1. Resolve
        skill = resolve_skill(tool_name)

        # 2. Tag
        tag = _RISK_TAG.get(skill.risk_level, "ALLOW")

        # 3. Log (append-only; MUST precede call_next)
        emit_event(
            {
                "type": "tool_call",
                "tool": tool_name,
                "risk": skill.risk_level,
                "tag": tag,
                "args_hash": _args_hash(args),
                "session_id": _session_id(context),
                "ts": time.time(),
            }
        )

        # 4. Always allow — the log is the governance artifact
        return await call_next(context)
