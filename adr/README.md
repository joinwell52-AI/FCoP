# FCoP Architecture Decision Records (ADR)

本目录保存 FCoP 协议和参考实现（`fcop`、`fcop-mcp`）演进过程中的**架构决策记录**。

## 什么是 ADR

ADR（Architecture Decision Record）是**一次性的决策快照**：

- 记录**做出决策的当下**的背景、约束、可选方案、选定方案、代价
- 一旦发出，**不再修改内容**，只追加 `Status` 字段变化（Proposed → Accepted → Deprecated → Superseded by ADR-NNNN）
- 通过持续累积形成**决策史**，让后来者不用再把同样的讨论走一遍

和 spec（规范）的区别：

| | spec（`private/fcop-repo/spec/`）| ADR（`private/fcop-repo/adr/`） |
|---|---|---|
| 回答什么 | "FCoP 是什么" | "我们为什么这么做" |
| 时间属性 | 永远描述最新状态 | 记录某个历史决策点 |
| 修改策略 | 持续更新、bump 版本号 | 不改内容，只改 Status |
| 读者 | 协议使用者、实现者 | 贡献者、未来的自己 |

## 命名约定

```
ADR-NNNN-kebab-case-title.md
```

- `NNNN`：四位数字，从 `0001` 开始
- `kebab-case-title`：简短描述性标题
- 一份 ADR = 一个主题，别塞两件事

示例：

- `ADR-0001-library-api.md`
- `ADR-0002-package-split-and-migration.md`
- `ADR-0003-mcp-transport-choice.md`（未来可能）

## 文档结构模板

每份 ADR 都遵守以下结构（按需可裁剪，但头两节必须有）：

```markdown
# ADR-NNNN: 决策标题

- **Status**: Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
- **Date**: YYYY-MM-DD
- **Deciders**: 参与决策的角色（ADMIN / PM / DEV / …）
- **Related**: 相关 ADR 或 spec 章节

## Context

背景、问题、约束。**不要**写解决方案。读者读完 Context 应该能自己想清楚"确实得做点什么"。

## Decision

一句话决策。之后是决策的细节展开。

## Design Details

设计细节：API 签名、数据结构、算法、流程图等。

## Non-Goals

明确"这份决策**不**涵盖"什么——避免读者过度解读。

## Alternatives Considered

考虑过但没选的方案，以及**为什么没选**。

## Consequences

### Positive

- 好处 1
- 好处 2

### Negative

- 代价 1
- 代价 2

### Neutral

- 需要跟进的事 1
- 需要跟进的事 2

## Timeline（可选）

实施时间表。
```

## 当前 ADR 索引

| 编号 | 标题 | Status | 日期 |
|---|---|---|---|
| [ADR-0001](./ADR-0001-library-api.md) | `fcop` Library API（`import fcop`）| Accepted | 2026-04-22 |
| [ADR-0002](./ADR-0002-package-split-and-migration.md) | Package Split（`fcop` + `fcop-mcp`）& 0.5 → 0.6 Migration | Accepted | 2026-04-22 |
| [ADR-0003](./ADR-0003-stability-charter.md) | Pre-1.0 Stability Charter | Accepted | 2026-04-23 |
| [ADR-0004](./ADR-0004-time-is-filesystem.md) | 时间由文件系统提供，不由 Frontmatter 提供 | Accepted | 2026-04-23 |
| [ADR-0005](./ADR-0005-agent-output-layering.md) | Agent 产出物分层（Observation Output Lifecycle） | Accepted | 2026-04-23 |

## 工作流

1. 遇到**需要讨论的架构/协议决策**时，起草一份 ADR（`Status: Proposed`）
2. 在 issue / PR / 任务文件里讨论，吸收意见后更新 ADR 内容
3. 决策敲定后，把 `Status` 改为 `Accepted`，合入主干
4. 后续如果决策被推翻，**不要删 ADR**，把 Status 改为 `Superseded by ADR-XXXX`，保留历史

## 参考

- Michael Nygard, "Documenting Architecture Decisions" (2011)
- ADR GitHub org: <https://adr.github.io/>
