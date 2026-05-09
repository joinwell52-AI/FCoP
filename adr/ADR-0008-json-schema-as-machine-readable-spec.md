# ADR-0008: JSON Schema as Machine-Readable Spec

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0007](./ADR-0007-fcop-1.0-protocol-freeze-charter.md)（1.0 charter，本 ADR 落地版本：1.0.0）；外部参考：[CodeFlow §3.1 原则 #1](https://github.com/joinwell52-AI/codeflow-pwa/blob/main/docs/design/codeflow-v2-on-fcop-sdk.md)

## Context

FCoP `0.7.2` 没有任何 JSON Schema 文件，所有协议字段约束散在：

- `src/fcop/core/schema.py`：`PROTOCOL_VERSION`、`REQUIRED_TASK_FRONTMATTER_KEYS`、`OPTIONAL_TASK_FRONTMATTER_KEYS` 等 frozenset
- `src/fcop/project.py`：`_VALID_REPORT_STATUSES` 等模块级 frozenset
- `src/fcop/core/frontmatter.py`：`_KNOWN_KEYS`
- `src/fcop/core/filename.py`：filename 正则

CodeFlow §3.1 原则 #1 要求"JSON Schema 作为机器可读规范"，否则跨语言 mirror 与 fuzz test 跑不通。

## Decision

`spec/schemas/` 落 5 个 JSON Schema 文件作为协议的 **single source of truth**：

```
spec/schemas/
├── agent.schema.json
├── task.schema.json
├── review.schema.json
├── session.schema.json   # 1.0 仅占位（含 $schema + 必填字段宣言；实现留 1.x 后续）
└── skill.schema.json     # 同上
```

`core/schema.py` 与各 dataclass 的字段集合**反过来由 schema 派生 / 对照**——schema.json 改了，dataclass 测试 fail。

## Design Details

- 选库：`jsonschema`（Python 生态最常见，PyPI footprint 中等）vs `fastjsonschema`（更快，依赖更少）—— 1.0 阶段先选 `jsonschema`，1.x 后续再 benchmark
- 新增 `tests/test_schemas/`：每个 schema 至少 3 个 test（合法、缺必填、非法值）
- 新增 `tests/test_fcop/test_schema_dataclass_alignment.py`：对每个 dataclass 跑 schema match，确保两源不漂移
- `spec/schemas/*.schema.json` 的 `$id` 用 `https://fcop.dev/schemas/{name}/v1.0.json` 命名（与 CodeFlow §3.2 `$schema` URL 一致）
- 每个 schema 的 `$id` 含版本号 → 1.1 升级时 schema 文件复制为 v1.1 与 v1.0 共存（CodeFlow §3.1 原则 #3 的 minor 兼容承诺）
- 增加 `jsonschema>=4.0,<5.0` 进 `pyproject.toml` 主依赖

## Tests Checklist

- [ ] `tests/test_schemas/test_agent_schema.py`（合法 / 缺必填 / 非法值各 1）
- [ ] `tests/test_schemas/test_task_schema.py`（合法 / 缺必填 / 非法值 + 0.7.x 旧文件兼容）
- [ ] `tests/test_schemas/test_review_schema.py`（与 ADR-0009 联合）
- [ ] `tests/test_schemas/test_session_schema.py`（仅占位字段）
- [ ] `tests/test_schemas/test_skill_schema.py`（仅占位字段）
- [ ] `tests/test_fcop/test_schema_dataclass_alignment.py`（5 个 dataclass × schema 对照）
- [ ] `tests/test_fcop/test_pyproject_pins.py` 加 `jsonschema` 依赖在合理 range

## Backwards Compatibility

- 加新文件、加新依赖 → 对 0.7.x 用户**完全透明**（旧代码不 import schemas/）
- `core/schema.py` 的 frozenset 在 1.0 内**继续可用**，仅多一层 schema-derived 校验
- 旧 TASK / REPORT / ISSUE 文件全部按 `task.schema.json` v1.0 通过

## Open Questions

1. `jsonschema` vs `fastjsonschema` 最终二选一 → ADR-0008 完整稿前 benchmark
2. `spec/schemas/*.schema.json` 是手写还是从 dataclass 自动生成 → 倾向手写（避免循环依赖）
3. `session.schema.json` / `skill.schema.json` 的占位字段最小集 → 与 ADR-0014 协调

## Sign-off

待 ADR-0007 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
