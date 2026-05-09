# ADR-0021: Encoding Abstraction — Markdown as Reference Encoding

- **Status**: Proposed
- **Date**: 2026-05-09
- **Deciders**: ADMIN（待批准）
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 2 Encoding + §术语表（"FCoP Reference Encoding"）；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `encoding.schema.json`

## Context

外部架构反馈中存在一个看似矛盾的张力：

> 第一段："Markdown 绑定过深 —— 协议必须把协议和文件格式分离"
> 第二段："文件即 IPC 是体系里最原创的一刀，FCoP 像 Agent 世界的 Plan9"

ADR-0015 charter §背景已调和：**不剥离 Markdown，但要分层**。Markdown 是 FCoP v1.0 的 **reference encoding**，不是协议本体。这给未来 JSON / SQLite / event stream 留接口，同时保留"文件即 IPC"的原创性。

POSIX 类比：FCoP 之于 Encoding = POSIX 之于 file system。POSIX 不规定文件存储在 ext4 / xfs / NTFS，但规定 read/write/seek 的 contract。FCoP 不规定消息存储在 Markdown / JSON / SQLite，但规定 envelope contract。

## Decision

引入 **Encoding Abstraction**，把 v1.0 显式分为两层：

```
┌─────────────────────────────────────────────────────────┐
│  FCoP Encoding Abstraction (协议本体)                   │
│  - IPC envelope contract（sender/recipient/type/seq）   │
│  - Filename grammar contract（4 类 envelope）           │
│  - Frontmatter required fields                          │
└─────────────────────────────────────────────────────────┘
                          ▼ implements
┌─────────────────────────────────────────────────────────┐
│  FCoP Reference Encoding (v1.0 唯一推荐实现)            │
│  - Markdown body + YAML frontmatter                     │
│  - filename = TASK-{date}-{seq}-{from}-to-{to}.md       │
│  - filesystem layout = docs/agents/{tasks,reports,…}/   │
└─────────────────────────────────────────────────────────┘
                          ▼ alternative encodings (v1.x)
┌─────────────────────────────────────────────────────────┐
│  Future: JSON / SQLite / Event Stream / CRDT            │
│  - 由第三方实现，必须满足 Encoding Abstraction contract │
└─────────────────────────────────────────────────────────┘
```

v1.0 保证：Reference Encoding 可被任何 Alternative Encoding **无损转换**（通过 Encoding Abstraction 的 contract）。

## Design Details

- `encoding.schema.json` 定义抽象层 contract：
  - IPC envelope 4 类（TASK / REPORT / ISSUE / REVIEW）共用 frontmatter base：`protocol`, `version`, `sender`, `recipient`, `priority`, `subject`
  - filename grammar 用正则表达（不绑定文件扩展名 .md）
  - 时序约定：seq 单调递增；同 date 内不重复
- `models.Encoding` 是抽象基类（v1.0 仅一份具体实现 `MarkdownEncoding`）
- `core/encoding/markdown.py` 把现有 `core/frontmatter.py` + `core/filename.py` 重组为 `MarkdownEncoding` 类
- `Project(encoding=...)` 构造参数（默认 `MarkdownEncoding()`）
- v1.0 不暴露 alternative encoding 注册机制；保留 `encoding=` 参数为未来留接口
- spec 文档明示："如要实现 alternative encoding，必须满足 `encoding.schema.json` 描述的 contract，并通过 `tests/test_encoding/test_contract_compliance.py`"

## Tests Checklist

- [ ] `tests/test_encoding/test_markdown_encoding.py` 新文件：encode/decode round-trip × 4 envelope
- [ ] `tests/test_encoding/test_contract_compliance.py` 新文件：抽象 contract 测试集（任何 encoding 必须通过）
- [ ] `tests/test_schemas/test_encoding_schema.py`
- [ ] `tests/test_fcop/test_public_surface.py` 快照增加 Encoding 抽象基类
- [ ] `tests/test_fcop/test_project.py` 加 `Project(encoding=...)` 构造测试

## Backwards Compatibility

- 现有 0.7.x 文件 100% 通过 MarkdownEncoding（默认）
- 现有 `Project()` 调用无需传 encoding 参数 → 默认 Markdown
- 现有 `core/frontmatter.py` / `core/filename.py` API **保留并 re-export** 自 `core/encoding/markdown.py`（避免破坏外部 import）
- ADR-0003 公开面：Encoding 抽象基类是新公开接口，进只进不出锁

## Open Questions

1. `Project()` 是否在 v1.0 暴露 `encoding=` 参数？**建议**是 —— 即使 v1.0 没人用，留接口避免 v1.x 改 API
2. `MarkdownEncoding` 内部细节是否完全隐藏？**建议**否 —— `core/frontmatter.parse_*` 等仍作为公开 helper（很多用户依赖）
3. spec 文档要不要给"如何实现 alternative encoding"的样板？**建议**v1.0 仅给 contract 文档；样板留 v1.x 真有用例时再写
4. CodeFlow TS mirror 是否需要 mirror Encoding 抽象？**建议**是 —— `packages/codeflow-protocol/encoding.ts` 镜像本 schema

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
