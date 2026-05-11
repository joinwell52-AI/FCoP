"""Skill Resolver — tool_name → risk level.

Static registry lookup only.  No AI judgment, no dynamic thresholds.

Missing entry policy: default Safe (fail-open — governance never
blocks by absence of config).

Registry format (loaded from skill_registry.yaml or passed as dict):
  write_task:
    risk: Sensitive
    category: task_mutation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # optional; gracefully absent → YAML load disabled
    _YAML_OK = True
except ImportError:
    _YAML_OK = False


@dataclass(frozen=True)
class SkillMeta:
    tool: str
    risk_level: str          # "Safe" | "Sensitive" | "Critical"
    category: str = "general"
    domain: str = "neutral"  # "execution" | "governance" | "neutral" (ADR-0031 §9.1)
    capabilities: list[str] = field(default_factory=list)


# Built-in defaults for fcop-mcp's own 30 tools.
_BUILTIN: dict[str, dict[str, Any]] = {
    # ── Destructive → Critical ──────────────────────────────────────────
    "delete_task":   {"risk": "Critical", "category": "destructive_mutation"},
    "delete_review": {"risk": "Critical", "category": "destructive_mutation"},
    # ── State-mutating → Sensitive ──────────────────────────────────────
    "write_task":          {"risk": "Sensitive", "category": "task_mutation"},
    "write_review":        {"risk": "Sensitive", "category": "review_mutation"},
    "mark_human_approved": {"risk": "Sensitive", "category": "approval_mutation"},
    "set_project_dir":     {"risk": "Sensitive", "category": "config_mutation"},
    # ── Read-only → Safe ────────────────────────────────────────────────
    "list_tasks":    {"risk": "Safe", "category": "task_read"},
    "read_task":     {"risk": "Safe", "category": "task_read"},
    "list_reviews":  {"risk": "Safe", "category": "review_read"},
    "read_review":   {"risk": "Safe", "category": "review_read"},
    "get_project_dir": {"risk": "Safe", "category": "config_read"},
    "read_agent":    {"risk": "Safe", "category": "agent_read"},
    "list_agents":   {"risk": "Safe", "category": "agent_read"},
    "read_skill":    {"risk": "Safe", "category": "skill_read"},
    "list_skills":   {"risk": "Safe", "category": "skill_read"},
    "list_reports":  {"risk": "Safe", "category": "report_read"},
    "read_report":   {"risk": "Safe", "category": "report_read"},
    "fcop_check":    {"risk": "Safe", "category": "audit_read"},
}

# User-overridable registry (loaded from skill_registry.yaml or env config).
_user_registry: dict[str, dict[str, Any]] = {}

# Auto-load the bundled skill_registry.yaml at import time so domain
# fields are always available without requiring an explicit call.
_BUNDLED_YAML = Path(__file__).parent / "skill_registry.yaml"


def _load_bundled() -> None:
    if not _YAML_OK or not _BUNDLED_YAML.exists():
        return
    try:
        import yaml as _yaml
        with _BUNDLED_YAML.open(encoding="utf-8") as fh:
            data = _yaml.safe_load(fh) or {}
        _user_registry.update(data)
    except Exception:  # noqa: BLE001
        pass  # gracefully degrade — missing YAML is non-fatal


_load_bundled()


def load_registry_yaml(path: str | Path) -> None:
    """Load (or override) skill registry from a YAML file (requires PyYAML).

    Entries in *path* take precedence over the bundled skill_registry.yaml.
    """
    if not _YAML_OK:
        raise RuntimeError("PyYAML is not installed; run: pip install pyyaml")
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    _user_registry.update(data)


def resolve_skill(tool_name: str) -> SkillMeta:
    """Lookup order: user_registry → builtin → Safe default."""
    raw = _user_registry.get(tool_name) or _BUILTIN.get(tool_name)
    if not raw:
        return SkillMeta(tool=tool_name, risk_level="Safe", category="unknown")
    return SkillMeta(
        tool=tool_name,
        risk_level=raw.get("risk", "Safe"),
        category=raw.get("category", "general"),
        domain=raw.get("domain", "neutral"),
        capabilities=list(raw.get("capabilities", [])),
    )
