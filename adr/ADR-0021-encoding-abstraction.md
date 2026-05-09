# ADR-0021: Encoding Abstraction — Markdown as Reference Encoding

- **Status**: Accepted
- **Date**: 2026-05-09
- **Accepted-on**: 2026-05-09（随 TASK-20260509-003 物化 `encoding.schema.json` 落地；workspace_dir 子决议 ADR-0022 独立 sign-off）
- **Deciders**: ADMIN
- **Related**: [ADR-0015](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md) §抽象 2 Encoding + §术语表（"FCoP Reference Encoding"）；[ADR-0016](./ADR-0016-json-schema-for-7-abstractions.md) `encoding.schema.json`；子决议：[ADR-0022](./ADR-0022-workspace-directory-convention.md)（`workspace_dir` 默认从 `docs/agents/` 改为 `fcop/`）

## TL;DR

**中文**：把 Encoding 抽象切成两面——**IPC Surface**（协议必须管：TASK/REPORT/ISSUE/REVIEW envelope grammar）+ **Open Knowledge Surface**（agent 自由命名：`SPEC-` / `STATUS-` / `GUIDE-` 等涌现前缀，协议只承认 grammar 不限定语义）。Markdown 是 v1.0 的**唯一推荐 reference encoding**，不是协议本体——未来 alternative encoding（JSON / SQLite）正交。

**English**: Splits Encoding into two facets — the **IPC Surface** (which the protocol must govern: TASK/REPORT/ISSUE/REVIEW envelope grammar) and the **Open Knowledge Surface** (where agents invent names freely: `SPEC-` / `STATUS-` / `GUIDE-` prefixes the protocol only acknowledges as grammar, not as semantics). Markdown is v1.0's **sole recommended reference encoding** — not the protocol itself; future alternative encodings (JSON / SQLite) remain orthogonal.

## Context

外部架构反馈中存在一个看似矛盾的张力：

> 第一段："Markdown 绑定过深 —— 协议必须把协议和文件格式分离"
> 第二段："文件即 IPC 是体系里最原创的一刀，FCoP 像 Agent 世界的 Plan9"

ADR-0015 charter §背景已调和：**不剥离 Markdown，但要分层**。Markdown 是 FCoP v1.0 的 **reference encoding**，不是协议本体。这给未来 JSON / SQLite / event stream 留接口，同时保留"文件即 IPC"的原创性。

POSIX 类比：FCoP 之于 Encoding = POSIX 之于 file system。POSIX 不规定文件存储在 ext4 / xfs / NTFS，但规定 read/write/seek 的 contract。FCoP 不规定消息存储在 Markdown / JSON / SQLite，但规定 envelope contract。

## Decision

引入 **Encoding Abstraction**，含**两个 surface** 与一份 reference encoding：

```
┌──────────────────────────────────────────────────────────────────────┐
│  FCoP Encoding Abstraction (协议本体)                                │
│  ┌─ Surface 1: IPC Surface (强 contract) ──────────────────────────┐ │
│  │  - 4 类 envelope: TASK / REPORT / ISSUE / REVIEW                │ │
│  │  - filename grammar 严格（含 sender / recipient / seq）         │ │
│  │  - frontmatter 必填字段                                          │ │
│  │  - workspace_dir 子目录: tasks/ reports/ issues/ reviews/        │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│  ┌─ Surface 2: Open Knowledge Surface (弱 contract) ───────────────┐ │
│  │  - 默认目录: shared/                                             │ │
│  │  - filename grammar: {ALL-CAPS-PREFIX}-{kebab-slug}[.{lang}].md  │ │
│  │  - PREFIX 由 agent 自创，FCoP spec **不枚举**（防 ossify）       │ │
│  │  - frontmatter 可选（knowledge 不强求 envelope 字段）            │ │
│  │  - 已观察到的 agent invention（informative，非冻结）：           │ │
│  │      GUIDE-* / SPEC-* / STATUS-* / TEAM-* / LETTER-*             │ │
│  └──────────────────────────────────────────────────────────────────┘ │
│  - workspace_dir contract（默认 fcop/，见 ADR-0022）                  │
└──────────────────────────────────────────────────────────────────────┘
                          ▼ implements
┌─────────────────────────────────────────────────────────┐
│  FCoP Reference Encoding (v1.0 唯一推荐实现)            │
│  - Markdown body + YAML frontmatter                     │
│  - filename = TASK-{date}-{seq}-{from}-to-{to}.md       │
│  - filesystem layout = fcop/{tasks,reports,issues,      │
│                              reviews,shared,log}/       │
└─────────────────────────────────────────────────────────┘
                          ▼ alternative encodings (v1.x)
┌─────────────────────────────────────────────────────────┐
│  Future: JSON / SQLite / Event Stream / CRDT            │
│  - 由第三方实现，必须满足 Encoding Abstraction contract │
└─────────────────────────────────────────────────────────┘
```

v1.0 保证：Reference Encoding 可被任何 Alternative Encoding **无损转换**（通过两个 surface 各自的 contract）。

### 为什么是两个 surface（哲学根 → field evidence）

Open Knowledge Surface 不是工程分类，是协议哲学的直接体现——见 [ADR-0015 §FCoP is discovered, not invented](./ADR-0015-fcop-1.0-ai-os-protocol-charter.md#fcop-is-discovered-not-invented)：

> **Field datum**：用户在真实 FCoP 项目 `D:\cyberv\cybervcar\docs\agents/shared/` 里观察到 agent 在**没有任何 spec 指导**的情况下自发涌现 5 类命名前缀（GUIDE / SPEC / STATUS / TEAM / LETTER），全部遵守 `{ALL-CAPS-PREFIX}-{kebab-slug}[.{lang}].md` 这一相同 grammar。

如果协议只承认 IPC Surface（4 类 envelope），shared/ 里这些 agent invention 会变成"超出 spec 的灰色地带"——但它们**实际占了真实 FCoP 项目 50%+ 的 agent 输出**。把 shared/ 排除出协议 = 把 FCoP 的真实主体排除出协议。

两个 surface 的设计原则：

| 维度 | IPC Surface | Open Knowledge Surface |
|---|---|---|
| 谁定义 | FCoP spec 预定义（封闭） | agent 自创（开放） |
| filename 严格度 | 强（含 sender/recipient/seq） | 弱（仅 PREFIX-slug 形式） |
| frontmatter | 必填字段 | 可选 |
| 协议演进风险 | 高（任何字段加都是协议级动作） | 零（agent 想发明就发明） |
| 类比（POSIX）| pipes / message queues | shared memory / `/usr/share/` |

**v1.0 Open Knowledge Surface 不枚举具体 PREFIX 词表**——这是核心约束。一旦 spec 写出"GUIDE / SPEC / STATUS 是合法前缀"就 ossify 了 agent 创造力，违反 §FCoP is discovered 的第 1 条 tiebreaker。GUIDE / SPEC / STATUS / TEAM / LETTER 仅作为 **informative example** 出现在 release notes / getting-started 中，不出现在 spec / schema 里。

## Design Details

- `encoding.schema.json` 定义抽象层 contract，**两个 surface 各一份**：
  - **IPC Surface**：4 类 envelope（TASK / REPORT / ISSUE / REVIEW）共用 frontmatter base：`protocol`, `version`, `sender`, `recipient`, `priority`, `subject`；filename grammar 用严格正则；时序约定 seq 单调递增、同 date 内不重复
  - **Open Knowledge Surface**：filename grammar 仅约定 `^[A-Z][A-Z0-9-]*-[a-z0-9-]+(\.[a-z]{2,5})?\.md$`（PREFIX 自由 + slug + 可选语言后缀）；frontmatter 全部可选；**不枚举** PREFIX 词表
  - **`workspace_dir`**：项目根下的协议命名空间目录；v1.0 默认 `fcop/`（见 [ADR-0022](./ADR-0022-workspace-directory-convention.md)）；alternative encoding 必须遵守同一 contract
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
5. **Open Knowledge Surface 的 PREFIX 词表收录路径**：v1.x 是否要把 agent invention 收录进 spec？倾向 **不收录**——保持纯 informative；但 v1.x release notes 可以新增 §「observed agent inventions this release」段，作为社区参考

## Sign-off

待 ADR-0015 charter 通过后，本 ADR 由 ADMIN 直接 sign 进入 Accepted。
