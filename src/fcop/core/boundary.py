"""FCoP v1.0 Boundary 抽象 reference impl（per ADR-0020）。

把 ``boundary.schema.json`` 与 ADR-0020 §决议 5 的 4 条规则从纸搬到
代码里。本模块只负责**判定**——不负责把判定接进 Project.write_*；
那是 :mod:`fcop.project` 与 :class:`fcop.Project` 的工作（仅
``write_review`` 在 v1.0 主动接，其他写入路径维持 0.7.x 行为不变）。

公开面（按 ADR-0001 ``core.*`` 是 internal，但本模块有清晰单一职责
所以可被 Project 与 fcop-mcp 等下游间接使用）：

- :data:`LAYER_DEFAULTS` —— 3 个 layer 的默认 capability bundle
- :data:`BOUNDARY_RULES` —— 4 条规则 id 常量
- :data:`CAPABILITY_VOCAB` —— v1.0 frozen 10 token 词表
- :func:`lookup_capability` —— 按 role code 查 capability
- :func:`validate_action` —— 按 4 条规则给出违规列表

参见 ``adr/ADR-0020-agent-boundary-and-capability.md``。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from fcop.models import AgentLayer, BoundaryViolation, Capability

if TYPE_CHECKING:
    from fcop.models import TeamConfig

__all__ = [
    "CAPABILITY_VOCAB",
    "LAYER_DEFAULTS",
    "BOUNDARY_RULES",
    "RULE_NO_ADMIN_PROGRAMMATIC_CREATE",
    "RULE_NO_GOVERNANCE_FISSION",
    "RULE_NO_WORKER_REVIEWS_GOVERNANCE",
    "RULE_EXPLICIT_OVERRIDES_LAYER",
    "RULE_UNKNOWN_CAPABILITY",
    "lookup_capability",
    "validate_action",
]


# ── 常量 ────────────────────────────────────────────────────────────


CAPABILITY_VOCAB: frozenset[str] = frozenset(
    {
        "file_io",
        "task_io",
        "modify_code",
        "review_decision",
        "approve_release",
        "escalate",
        "spawn_agent",
        "override",
        "archive",
        "mark_done",
    }
)
"""V1.0 frozen capability token 词表（10 个）。

扩 token 必须发新 ADR + bump MINOR。词表必须与
``boundary.schema.json#/$defs/capabilityToken/enum`` 完全相符；
``test_layer_defaults_align_with_schema`` 在 CI 上守门。
"""


RULE_NO_ADMIN_PROGRAMMATIC_CREATE = "NO_ADMIN_PROGRAMMATIC_CREATE"
RULE_NO_GOVERNANCE_FISSION = "NO_GOVERNANCE_FISSION"
RULE_NO_WORKER_REVIEWS_GOVERNANCE = "NO_WORKER_REVIEWS_GOVERNANCE"
RULE_EXPLICIT_OVERRIDES_LAYER = "EXPLICIT_OVERRIDES_LAYER"
RULE_UNKNOWN_CAPABILITY = "UNKNOWN_CAPABILITY"

BOUNDARY_RULES: tuple[str, ...] = (
    RULE_NO_ADMIN_PROGRAMMATIC_CREATE,
    RULE_NO_GOVERNANCE_FISSION,
    RULE_NO_WORKER_REVIEWS_GOVERNANCE,
    RULE_EXPLICIT_OVERRIDES_LAYER,
)
"""ADR-0020 §决议 5 的 4 条规则 id（顺序按表）。

``RULE_UNKNOWN_CAPABILITY`` 是 ADR-0020 §决议 5 §补充规则中的
warning-only 扩展，**不**在本元组里——它不属于 4 条 normative
boundary 规则，仅是 advisory。
"""


# layer → default capability bundle，per ADR-0020 §decision 表。
# admin 的 cannot 列表特意为空——admin 在协议层可做一切，但
# `lookup_capability` 会拒绝 fcop.json 里把 layer 设为 "admin" 的角色
# （那是 NO_ADMIN_PROGRAMMATIC_CREATE 的工作）。
LAYER_DEFAULTS: dict[AgentLayer, tuple[tuple[str, ...], tuple[str, ...]]] = {
    AgentLayer.WORKER: (
        ("file_io", "task_io"),
        ("approve_release", "escalate", "spawn_agent"),
    ),
    AgentLayer.GOVERNANCE: (
        ("file_io", "task_io", "review_decision"),
        ("modify_code", "spawn_agent"),
    ),
    AgentLayer.ADMIN: (
        ("file_io", "task_io", "review_decision", "escalate", "override"),
        (),
    ),
}
"""每个 layer 的 ``(default_can, default_cannot)`` 元组。

显式 ``can`` / ``cannot`` 字段会被 :func:`lookup_capability` 与这里
的默认 union（cannot 更高优先级，规则 ``EXPLICIT_OVERRIDES_LAYER``）。
"""


# ── lookup ──────────────────────────────────────────────────────────


def _coerce_layer(raw: object) -> AgentLayer:
    """把 fcop.json 里的字符串/None 强转 AgentLayer，未知值 raise。"""
    if raw is None or raw == "":
        return AgentLayer.WORKER
    if isinstance(raw, AgentLayer):
        return raw
    if isinstance(raw, str):
        try:
            return AgentLayer(raw)
        except ValueError as exc:
            raise ValueError(
                f"unknown layer {raw!r}; expected one of "
                f"{[l.value for l in AgentLayer]}"
            ) from exc
    raise TypeError(f"layer must be str or AgentLayer, got {type(raw).__name__}")


def _coerce_token_list(raw: object, *, field: str) -> tuple[str, ...]:
    """fcop.json 里 list[str] / None / str 三种形状归一为 tuple[str, ...]。"""
    if raw is None:
        return ()
    if isinstance(raw, str):
        s = raw.strip()
        return (s,) if s else ()
    if isinstance(raw, (list, tuple)):
        out: list[str] = []
        for item in raw:
            s = str(item).strip()
            if s:
                out.append(s)
        return tuple(out)
    raise TypeError(
        f"{field} must be a list, string, or null; got {type(raw).__name__}"
    )


def lookup_capability(role_code: str, config: TeamConfig) -> Capability:
    """按 role code 查 :class:`Capability`，未声明字段回落 layer default。

    解析顺序：
    1. 取 ``config.extra["_role_labels"][role_code]``（dict-form fcop.json
       的 leftover；本任务把 layer/can/cannot 也走这条路径，无需新加
       字段，per TASK-005 §决议 1）
    2. ``layer = parsed.get("layer", "worker")``
       —— 显式 ``"admin"`` → raise ``BoundaryViolationError(NO_ADMIN_PROGRAMMATIC_CREATE)``
    3. 取 layer 默认 ``(default_can, default_cannot)``
    4. 显式 ``can`` / ``cannot`` 与 default union（cannot 优先级最高
       per rule ``EXPLICIT_OVERRIDES_LAYER``——若 token 同时在 can 与
       cannot，cannot 胜）

    Args:
        role_code: 必须先经 :func:`fcop.core.schema.validate_role_code`
            校验合法（本函数不再做形式校验，假定 caller 已检查）。
        config: 项目的 :class:`fcop.models.TeamConfig`。

    Returns:
        合并后的 :class:`Capability`。

    Raises:
        BoundaryViolationError: fcop.json.roles 里把某 role 的 layer
            显式设为 ``"admin"`` —— 触发 ``NO_ADMIN_PROGRAMMATIC_CREATE``
            规则。
    """
    role_meta = (
        config.extra.get("_role_labels", {}) if config.extra else {}
    )
    parsed = role_meta.get(role_code, {}) if isinstance(role_meta, dict) else {}
    if not isinstance(parsed, dict):
        parsed = {}

    raw_layer = parsed.get("layer")
    layer = _coerce_layer(raw_layer)
    is_explicit = any(
        k in parsed for k in ("layer", "can", "cannot")
    )

    if layer is AgentLayer.ADMIN:
        # NO_ADMIN_PROGRAMMATIC_CREATE：fcop.json 显式声明 admin role 即拒
        from fcop.errors import BoundaryViolationError

        violation = BoundaryViolation(
            rule_id=RULE_NO_ADMIN_PROGRAMMATIC_CREATE,
            actor=role_code,
            action="lookup_capability",
            target=None,
            message=(
                f"role {role_code!r} declares layer='admin' in fcop.json — "
                "the admin layer is reserved for human operators and MUST "
                "NOT be created programmatically (ADR-0020 rule "
                f"{RULE_NO_ADMIN_PROGRAMMATIC_CREATE})"
            ),
        )
        raise BoundaryViolationError(
            f"role {role_code!r} cannot be declared with layer='admin'",
            violations=[violation],
        )

    default_can, default_cannot = LAYER_DEFAULTS[layer]
    explicit_can = _coerce_token_list(parsed.get("can"), field="can")
    explicit_cannot = _coerce_token_list(
        parsed.get("cannot"), field="cannot"
    )

    # union（保持顺序，dedup）
    can = _ordered_union(default_can, explicit_can)
    cannot = _ordered_union(default_cannot, explicit_cannot)

    return Capability(
        code=role_code,
        layer=layer,
        can=can,
        cannot=cannot,
        is_explicit=is_explicit,
    )


def _ordered_union(*seqs: tuple[str, ...]) -> tuple[str, ...]:
    """保序去重 union。"""
    seen: set[str] = set()
    out: list[str] = []
    for seq in seqs:
        for item in seq:
            if item not in seen:
                seen.add(item)
                out.append(item)
    return tuple(out)


# ── validate ────────────────────────────────────────────────────────


def validate_action(
    actor: Capability,
    action: str,
    *,
    target: Capability | None = None,
) -> list[BoundaryViolation]:
    """按 ADR-0020 §决议 5 的 4 条规则 + UNKNOWN_CAPABILITY 给违规列表。

    空列表 ≡ 该操作允许。

    Args:
        actor: 发起方 capability。
        action: capability token；通常应在 :data:`CAPABILITY_VOCAB` 内。
        target: 受影响方 capability；仅在 review_decision / 跨角色
            动作场景需要传。

    规则触发顺序（同时多条触发会全列出来）：
    1. UNKNOWN_CAPABILITY（warning） —— action 不在词表
    2. EXPLICIT_OVERRIDES_LAYER（error） —— action 在 actor.cannot
    3. NO_GOVERNANCE_FISSION（error） —— governance + spawn_agent
    4. NO_WORKER_REVIEWS_GOVERNANCE（error） —— worker review_decision
       on governance target
    """
    out: list[BoundaryViolation] = []

    if action not in CAPABILITY_VOCAB:
        out.append(
            BoundaryViolation(
                rule_id=RULE_UNKNOWN_CAPABILITY,
                actor=actor.code,
                action=action,
                target=target.code if target is not None else None,
                message=(
                    f"action {action!r} is not in the v1.0 capability "
                    f"vocabulary {sorted(CAPABILITY_VOCAB)}; "
                    "advisory only — extending the vocab requires a new ADR."
                ),
                severity="warning",
            )
        )

    # EXPLICIT_OVERRIDES_LAYER：显式 cannot 列表里有 action → 拒
    # （同时也覆盖 layer default 把 action 放进 can 的情况）
    if action in actor.cannot:
        out.append(
            BoundaryViolation(
                rule_id=RULE_EXPLICIT_OVERRIDES_LAYER,
                actor=actor.code,
                action=action,
                target=target.code if target is not None else None,
                message=(
                    f"role {actor.code!r} explicitly forbids {action!r} "
                    f"via cannot list (rule {RULE_EXPLICIT_OVERRIDES_LAYER})"
                ),
            )
        )

    # NO_GOVERNANCE_FISSION：governance agent 不能 spawn_agent
    if (
        actor.layer is AgentLayer.GOVERNANCE
        and action == "spawn_agent"
    ):
        out.append(
            BoundaryViolation(
                rule_id=RULE_NO_GOVERNANCE_FISSION,
                actor=actor.code,
                action=action,
                target=target.code if target is not None else None,
                message=(
                    f"governance role {actor.code!r} cannot spawn another "
                    f"agent (rule {RULE_NO_GOVERNANCE_FISSION})"
                ),
            )
        )

    # NO_WORKER_REVIEWS_GOVERNANCE：worker 不能 review_decision 一个
    # governance subject
    if (
        actor.layer is AgentLayer.WORKER
        and action == "review_decision"
        and target is not None
        and target.layer is AgentLayer.GOVERNANCE
    ):
        out.append(
            BoundaryViolation(
                rule_id=RULE_NO_WORKER_REVIEWS_GOVERNANCE,
                actor=actor.code,
                action=action,
                target=target.code,
                message=(
                    f"worker role {actor.code!r} cannot review_decision "
                    f"a governance role {target.code!r} "
                    f"(rule {RULE_NO_WORKER_REVIEWS_GOVERNANCE})"
                ),
            )
        )

    return out
