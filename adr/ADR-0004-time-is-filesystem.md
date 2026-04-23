# ADR-0004: 时间由文件系统提供，不由 Frontmatter 提供

- **Status**: Accepted
- **Date**: 2026-04-23
- **Deciders**: ADMIN
- **Related**: [ADR-0001](./ADR-0001-library-api.md), [ADR-0003](./ADR-0003-stability-charter.md)

## ADMIN 决议（2026-04-23）

ADMIN 在审查 0.5.3 历史文件时发现：

> "文件有创建时间的，既然文件即协议，信里面不需要精确时间了"

这一观察直接推导出本 ADR。

---

## Context

FCoP 的核心哲学是「文件即协议」——所有的协作状态由文件本身承载，Git 历史是唯一权威事实。但 0.5.x 实现里，`write_task` / `write_report` 会往 frontmatter 塞一个 `created_at: YYYY-MM-DD HH:MM:SS`，同时：

- 文件系统自带 `mtime`（最近修改时间）
- `git log` 自带 `author-date` / `commit-date`（创建与修订的权威历史）
- 文件名已经带 `YYYYMMDD-NNN`（日期 + 当天序号）

所以 `created_at` 这个字段是**第四份时间信息**，而且是**唯一一份会由 agent 手写、可能出错、可能被伪造**的那份。

## Decision

### 核心原则：Single Source of Truth for Time

**时间由文件系统和 Git 提供，frontmatter 不记录任何时间字段**——Issue 除外。

### 详细规则

| 文件类型 | frontmatter 写时间吗 | 权威时间源 | 理由 |
|---|---|---|---|
| Task | ❌ 不写 | 文件名日期 + Git `author-date` + `mtime` | 文件不可变，`mtime` 即创建时间 |
| Report | ❌ 不写 | 同上 | 同上 |
| Issue `created_at` | ✅ 必须写 | frontmatter 本身 | Issue 允许 `open → closed` 状态迁移，`mtime` 被污染 |
| Issue `closed_at` | ✅ 关闭时写 | frontmatter 本身 | 计算 MTTR 需要 |

### 为什么 Issue 是例外

Issue 是 FCoP 中**唯一允许合法编辑**的文件类型（Rule 5 的狭义例外：status 字段可以从 `open` 单调迁移到 `closed`，并追加 `closed_at` / `resolution`）。这意味着：

- `mtime` 在 Issue 上表示**最近一次状态迁移**，不再等于**创建时间**
- Git 历史在 close issue 时会多一条 commit，首条 commit 才是创建
- 为了让消费者（看板、MTTR 报表、SLA 告警）不用反查 Git，Issue 必须在 frontmatter 显式记两个时间点

Task 和 Report 从来不会被编辑（一锤子买卖），所以 `mtime` 就是创建时间，无需冗余记录。

### 对已存在的 `created_at` 的处理

**Grandfather 条款**：

- 0.5.x / 0.6.0 之前写入的 task/report 文件中的 `created_at`：**保留不动**（Rule 5 文件不可变优先于本 ADR）
- `fcop.Project` 读取老文件时：`created_at` 作为 `extra.created_at` 透传到 `TaskFrontmatter`，不报错
- `inspect_task` / `inspect_report`：遇到 `created_at` 字段，**不判违规**，仅在详细输出中给出软提示「`created_at` is discouraged in 0.6+; rely on Git history / mtime」
- 0.6.0 起的 `Project.write_task` / `write_report`：**不再生成** `created_at`

### 对 Issue `created_at` / `closed_at` 的强化

- 0.6.0 起，`Project.write_issue`：**必须**写入 `created_at`
- `close_issue`：**必须**写入 `closed_at`
- `inspect_issue`：缺这两个字段（按状态判定）→ **FAIL**

## Consequences

### 积极

1. **减少伪造风险**：agent 无法伪造 `created_at`；真实时间靠 Git + 文件系统，agent 改不了
2. **减少时区歧义**：frontmatter 从不写时间，不需要约定时区格式（UTC？本地？）
3. **符合「只落真话」原则**（Rule 0.c）：不强制记录可能出错的冗余事实
4. **DRY**：不在多处维护同一信息的四份拷贝
5. **Issue 的例外规则反而更清晰**：Issue 确实需要时间字段，这成了明确的标志性差异

### 消极

1. **跨仓库移植成本**：如果有人复制 task 文件到另一个 Git 仓库，原始创建时间会丢失
   - **缓解**：这本来就是跨仓库移植的代价，不是 `created_at` 能救的（`created_at` 也是手写，同样可能错）
2. **离线浏览体验**：不看 Git 直接翻文件时，看不到创建时间
   - **缓解**：文件名已经有日期（到天），到分钟级别的需求很罕见
3. **审计需要 Git**：任何真实时间查询都要 `git log`
   - **缓解**：FCoP 本来就假定 Git 为事实载体，这是合理依赖

### 中立

- MCP tool 的行为变化属于 ADR-0003 第 4 条「返回结构向后兼容（字段加允许、删/改名禁止）」——`created_at` 是**写入端不再主动生成**，读取端仍能读老文件，所以不构成 tool 返回结构的破坏性变更

## Implementation Timeline

### 0.6.0rc1（本次落地的最小集）

1. `fcop/project.py` / `write_task` / `write_report`：
   - **现状**：这两个方法**已经**不写 `created_at`（0.6 重写时已舍弃），无需改动
   - 审计已验证 `TaskFrontmatter` 的可写字段里没有 `created_at`
2. `fcop/project.py` / `write_issue`：
   - **新增**：写入 `created_at`（ISO 8601 本地时间，秒级精度）
   - Issue frontmatter 从此必有 `created_at` 字段
3. 已存的 0.5.x / 手工编写的 task/report 文件里的 `created_at`：
   - 由 Grandfather 条款覆盖 —— 不删、不改、不报错
   - 读取时作为 `TaskFrontmatter.extra["created_at"]` 透传
4. `CHANGELOG.md`：在 0.6.0 条目下加一段说明
5. `MIGRATION-0.6.md`：在"frontmatter 差异"章节解释此条
6. Public API snapshot：不变（没新增 public 方法签名）

### 0.6.1 后续落地（Issue 状态机，非 RC 阻塞项）

- `Issue` dataclass 新增字段：`created_at: datetime`, `status: Literal["open","closed"] = "open"`, `closed_at: datetime | None = None`, `closed_by: str | None = None`, `resolution: str | None = None`
- `Project.close_issue(issue_id, *, closed_by, resolution)` 新方法 —— 对 Issue 文件进行**单调追加**编辑（唯一允许的 Rule 5 例外）
- `inspect_issue` 强化：status=closed 但缺 `closed_at` / `closed_by` / `resolution` → FAIL
- 这些都是 **additive** 改动，符合 ADR-0003 的 API 稳定性承诺

### 为什么分两步

Issue 状态机需要完整设计（谁能 close 别人的 issue？reopen 允许吗？），把它打包进 RC1 会推迟发布。RC1 先锁时间语义的大原则，状态机 0.6.1 再补。

## Alternatives Considered

### A. 继续保留 `created_at`，只是让它 optional

- **弊**：诱惑 agent 去写，一写就可能错；两份时间信息（mtime 和 created_at）不一致时不知道信哪份
- **被驳回**：不如直接一刀切

### B. `created_at` 仍必填但从文件系统自动生成

- **弊**：工具写入时的时间 ≠ 用户意图的时间（比如补录一周前的讨论）；而且 Git commit time 已经做了这件事
- **被驳回**：重复造轮子

### C. 全部都不写，包括 Issue

- **弊**：Issue 会被合法编辑，`mtime` 在 issue 上不可信；close 之后算 MTTR 需要两个时间点都在文件内
- **被驳回**：Issue 的 append-only-with-transitions 模型天然需要显式时间锚

## 适用范围

本 ADR 适用于 `fcop` 0.6.0 及以上版本。0.5.x 被 Grandfather 条款覆盖，现存的 0.5.x 文件无需迁移。
