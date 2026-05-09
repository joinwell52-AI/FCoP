# ADR-0016: JSON Schema for 7 Core Abstractions

- **Status**: Accepted
- **Date**: 2026-05-09
- **Accepted-on**: 2026-05-09（随 TASK-20260509-003 物化 + TASK-20260509-004 校验器落地）
- **Deciders**: ADMIN
- **Supersedes**: [ADR-0008](./ADR-0008-json-schema-as-machine-readable-spec.md)（5 类 schema 视角）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md)（charter，本 ADR 落地 §7 核心抽象冻结 #1）；[ADR-0017](./ADR-0017-review-file-type-minimal.md)；[ADR-0018](./ADR-0018-event-model.md)；[ADR-0019](./ADR-0019-failure-and-recovery-semantics.md)；[ADR-0020](./ADR-0020-agent-boundary-and-capability.md)；[ADR-0021](./ADR-0021-encoding-abstraction.md)

## TL;DR

**中文**：v1.0 把 7 抽象（Agent / IPC / Encoding / Event / Failure / Boundary / Audit）形式化为 7 份 **JSON Schema 2020-12**，物化到 `spec/schemas/`，作为协议唯一真相。Schema 通过 `referencing.Registry` 跨文件 `$ref` 解析；wheel 内 byte-identical 副本由测试守门。

**English**: v1.0 formalises the 7 abstractions (Agent / IPC / Encoding / Event / Failure / Boundary / Audit) as 7 **JSON Schema 2020-12** files under `spec/schemas/` — the single source of truth for the protocol body. Cross-file `$ref` resolves via `referencing.Registry`; a byte-identical copy ships in the wheel and is guarded by tests.

## Context

ADR-0008 把 spec 形式化为 5 类 schema（Agent / Task / Review / Session / Skill）——属于"对象 + 字段"视角。

ADR-0015 charter 把协议升级为 7 核心抽象（Agent / IPC / Encoding / Event / Failure / Boundary / Audit）——这 7 个不是"5 类对象的扩展"，是**协议本体的不同侧面**。Schema 形式化要按 7 抽象组织，而不是按对象。

CodeFlow §3.1 原则 #1（机器可读规范）+ §3.3.1.b（5 步流程）依赖本 ADR 提供机器可读的 JSON Schema。

## Decision

`spec/schemas/` 落 7 份 JSON Schema 文件作为协议 single source of truth：

```
spec/schemas/
├── agent.schema.json          # 抽象 1：Lifecycle + 身份
├── ipc-envelope.schema.json   # 抽象 3：4 类 envelope 公共 frontmatter
├── encoding.schema.json       # 抽象 2：filename grammar + encoding contract
├── event.schema.json          # 抽象 4：最小事件集
├── failure.schema.json        # 抽象 5：失败模式 + 恢复动作
├── boundary.schema.json       # 抽象 6：can / cannot capability
└── review.schema.json         # 抽象 7：REVIEW 最小 surface
```

`core/schema.py` 与 `models.*` dataclass 字段集合**反过来由 schema 派生 / 对照** —— schema.json 改了，dataclass 测试 fail。

## Design Details

- 选库：`jsonschema>=4.0,<5.0`（v1.0 阶段，后续 benchmark 决定是否切 fastjsonschema）
- 每个 schema 的 `$id` 用 `https://fcop.dev/schemas/{abstraction}/v1.0.json`
- 每个 schema 含版本号 → v1.1 升级时复制为 v1.1 与 v1.0 共存
- 新增 `tests/test_schemas/`：每抽象至少 3 个 case（合法 / 缺必填 / 非法值）
- 新增 `tests/test_fcop/test_schema_dataclass_alignment.py`：7 抽象 × dataclass 对照
- 增加 `jsonschema>=4.0,<5.0` 进 `pyproject.toml` 主依赖

## Tests Checklist

- [ ] `tests/test_schemas/test_agent_schema.py`
- [ ] `tests/test_schemas/test_ipc_envelope_schema.py`（4 envelope 共用）
- [ ] `tests/test_schemas/test_encoding_schema.py`（filename grammar）
- [ ] `tests/test_schemas/test_event_schema.py`（与 ADR-0018 联合）
- [ ] `tests/test_schemas/test_failure_schema.py`（与 ADR-0019 联合）
- [ ] `tests/test_schemas/test_boundary_schema.py`（与 ADR-0020 联合）
- [ ] `tests/test_schemas/test_review_schema.py`（与 ADR-0017 联合）
- [ ] `tests/test_fcop/test_schema_dataclass_alignment.py`
- [ ] `tests/test_fcop/test_pyproject_pins.py` 加 jsonschema

## Backwards Compatibility

- 加新文件、加新依赖 → 对 0.7.x 用户**完全透明**
- 旧 TASK / REPORT / ISSUE 文件 100% 通过 ipc-envelope.schema.json v1.0
- ADR-0008 § 提到的 5 类组织方式 superseded —— 新 7 抽象视角是 **superset**

## Open Questions

1. `Session` schema 是否也作为独立抽象进 v1.0？charter §抽象 5 把 Session hook 归 Failure；但 Session schema 本身可能值得单独成文件。**建议**：v1.0 不单独成 schema，仅作为 `failure.schema.json` 内子定义；v1.x 完整实现时再独立
2. `Skill` schema 是否进 v1.0？charter Non-Goals 已明确推 v1.1 → 不进
3. `core/schema.py` 的 `PROTOCOL_VERSION` 整数是否 bump？charter Non-Goals 明确不动
4. JSON Schema vs dataclass 双源真相 —— **schema 是真相**，dataclass 由 CI 强制对齐

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted（charter 已 Accepted；ADR-0016 是 charter §冻结 #1 的实施 ADR）。
