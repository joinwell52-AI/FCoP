# 从 FCoP 2.x 升级到 FCoP 3.0

> **TL;DR**：FCoP 3.0 引入新的目录拓扑（`_lifecycle/`）作为规范的状态真相。运行 `python -m fcop migrate --to-v3` 即可完成一次性、git-aware 的迁移。

---

## 为什么 FCoP 3.0 是 breaking change

FCoP 1.x / 2.x 把目录用作**类型分类**（`tasks/`、`reports/`、`issues/`、`log/`）。任务的当前生命周期状态写在文件内（YAML frontmatter），不写在文件系统里。

FCoP 3.0 把目录本身提升为**状态真相**：

```
fcop/
├── _lifecycle/        ← 新增：状态住这里
│   ├── inbox/         ← created
│   ├── active/        ← claimed
│   ├── review/        ← pending confirmation
│   ├── done/          ← completed
│   └── archive/       ← closed（替代 fcop/log/tasks/）
├── reports/           ← 不变（不再归档）
├── issues/            ← 不变（resolved 字段携带状态）
└── shared/            ← 不变
```

核心声明：

> **文件即协议；位置定义状态；事件记录历史。**
> *（Canonical 一句话，依据 [ADR-0040](../adr/ADR-0040-canonical-one-liner-two-layer-convention.md)；v1 版"文件位置即真相；其它一切都是踪迹"作为历史题词保留在 2026-05-21 及之前归档的 essays/reviews 中。）*

这一变化解锁：

- **无需读文件即可观察状态**：`ls fcop/_lifecycle/active/` 直接告诉你所有在飞的任务
- **原子 claim 语义**：`claim_task` 变成单次 `os.rename()`，消除困扰多 Agent 设置的重复派发类 bug
- **审计级历史**：每次 `mv` 在文件内写入 `transitions:` 事件，提供防篡改的 PAST 踪迹

完整规范：[`spec/fcop-3.0-spec.zh.md`](../spec/fcop-3.0-spec.zh.md) · [`spec/fcop-3.0-rfc.zh.md`](../spec/fcop-3.0-rfc.zh.md)

---

## 需要迁移什么

| 2.x 位置 | 3.0 位置 | 说明 |
|---|---|---|
| `fcop/tasks/*.md` | `fcop/_lifecycle/inbox/*.md` | 所有开放任务先入 `inbox/` |
| `fcop/log/tasks/*.md` | `fcop/_lifecycle/archive/*.md` | 已闭合任务直接入 `archive/` |
| `fcop/log/reports/*.md` | `fcop/reports/*.md` | Reports 是 append-only，无归档概念 |
| `fcop/log/issues/*.md` | `fcop/issues/*.md` | 已解决 issue 加 `resolved: true` |
| `fcop/log/`（空目录）| （删除）| 不再有顶层 `log/` |
| `fcop/shared/*` | `fcop/shared/*` | 不变 |

---

## 一键迁移

升级双包（lockstep 必需，per ADR-0002）：

```bash
pip install -U "fcop>=3.0,<4.0" "fcop-mcp>=3.0,<4.0"
```

在项目根目录运行迁移器：

```bash
python -m fcop migrate --to-v3
```

迁移器会：

1. 创建 5 个 `_lifecycle/` 子目录
2. 按上表把每个 2.x 文件移动到 3.0 位置
3. 为每个被迁移的文件追加一条**合成 transition 事件**：
   ```yaml
   transitions:
     - at: <file-mtime>
       from: null
       to: <current-stage>
       by: migration
       tool: fcop_migrate_v3
   ```
4. 删除空 `log/` 目录
5. 打印逐文件摘要

迁移器是 **git-aware** 的：检测到 git 仓库时用 `git mv`，保留 history。

---

## 验证迁移

完成后运行：

```bash
python -m fcop status
```

应当看到类似输出：

```
FCoP 3.0 project at <root>
  _lifecycle/inbox/    : 3 tasks
  _lifecycle/active/   : 2 tasks
  _lifecycle/review/   : 0 tasks
  _lifecycle/done/     : 12 tasks
  _lifecycle/archive/  : 47 tasks
  reports/             : 89 files
  issues/              : 14 files (3 unresolved)
```

或调用 `fcop_audit()`（通过 MCP server）做深度一致性检查。

---

## 没有 `transitions:` 的文件怎么办

迁移前已存在、且未被迁移器触及的文件（罕见边缘情况）视为**合法历史产物**。仍然可读。但**任何新迁移必须开始追加事件**。

迁移器会为大多数文件追加合成 baseline 事件，所以这种 fallback 通常用不上。

---

## 我的自定义工具直接写 `tasks/` 怎么办

那些工具其实**已经违反** ADR-0035 Rule B（只有 L1 工具可在生命周期目录间移动文件）。迁移后：

- 改为调用 L1 工具（`create_task`、`claim_task` 等），不要直接写文件
- 如果是 L3/L4/L5 工具只**读**文件，继续可用——只需更新读取路径，从 `tasks/` 改为 `_lifecycle/<stage>/`

L1 / L2 / L3 / L4 / L5 分类详见 [`spec/fcop-3.0-spec.zh.md`](../spec/fcop-3.0-spec.zh.md) §8。

---

## `risk_level`、`assignee`、custody 字段呢

这些**位于** FCoP 3.0 范围**之外**（见 spec §3.2）。如果你 2.x 文件用了：

- `risk_level` 可继续留在 frontmatter 作为协调提示，但**不得**驱动状态迁移（直通路径请用 `finish_task(skip_review=true)`）
- `assignee` / `owner` / `custodian` 可作为信息性元数据存在，但**不得**被当作协议状态（见 `adr/NOTE-custody-is-not-a-layer.md`）

`fcop_audit()` 会标记任何用这些字段驱动迁移的代码路径。

---

## 回滚

迁移器**不**写反向脚本。如需回滚：

1. `git checkout` 到迁移前的 commit（如果用 git）
2. 或从备份恢复

我们刻意不提供 `fcop migrate --back-to-v2`，因为：

- 一旦 `transitions:` 事件被追加，删除它们违反 Rule F（只追加）
- 2.x 与 3.0 在概念上是不同协议（状态在 frontmatter vs 状态在路径）
- 迁移很快（典型项目几秒），降级到 2.x 后重跑迁移比维护反向路径更便宜

---

## 跨 runtime / 分布式部署

FCoP 3.0 假设每一个 `_lifecycle/` 根都位于**一致性单一边界的文件系统内**（spec §1.1.1）。如果你的 `fcop/` 位于：

- 不具备严格 POSIX 语义的分布式文件系统
- 启用缓存的 NFS
- 跨机器的共享 git worktree
- S3-fuse 挂载点

你**必须**自行提供外部一致性层（锁管理器、单写入网关）。FCoP 本身不处理分布式协调。

---

## 常见坑

| 坑 | 修复 |
|---|---|
| 忘记 lockstep 升级（`fcop-mcp` 还在 2.x，`fcop` 已升到 3.0）| `pip install -U "fcop>=3.0,<4.0" "fcop-mcp>=3.0,<4.0"` |
| Cursor 里 MCP server 缓存了旧工具列表 | 重启 Cursor；`uvx` 会拉新版 `fcop-mcp` |
| `_lifecycle/` 被 `.gitignore` 漏掉 | 显式纳入 git tracking；它是项目状态的一部分 |
| 自定义审计工具从 frontmatter 读 `current_state` | 改为从路径读（per Rule A）；frontmatter status 不再权威 |
| `os.rename()` 因 `_lifecycle/` 子目录跨挂载点而失败 | 移到同一挂载点（spec §1.1 硬约束）|

---

## 阅读清单

- [`spec/fcop-3.0-spec.zh.md`](../spec/fcop-3.0-spec.zh.md) — 中文单页正式规范
- [`spec/fcop-3.0-rfc.zh.md`](../spec/fcop-3.0-rfc.zh.md) — RFC 中文平行版
- [`adr/ADR-0035-lifecycle-directory-and-tool-layers.md`](../adr/ADR-0035-lifecycle-directory-and-tool-layers.md) — State Ontology
- [`adr/ADR-0036-lifecycle-event-layer.md`](../adr/ADR-0036-lifecycle-event-layer.md) — Event Layer
- [`adr/ADR-0038-fcop-boundary-charter.md`](../adr/ADR-0038-fcop-boundary-charter.md) — Boundary Charter
- [`adr/NOTE-custody-is-not-a-layer.md`](../adr/NOTE-custody-is-not-a-layer.md) — 为什么 custody 不是协议字段
- [`essays/the-day-we-almost-added-custody.md`](../essays/the-day-we-almost-added-custody.md) — 决策现场记录

---

## 求助

- 提 issue：https://github.com/joinwell52-AI/FCoP/issues
- 看 CHANGELOG：[`CHANGELOG.md`](../CHANGELOG.md) [3.0.0] 段
- 英文版本指南：[`docs/MIGRATION-3.0.md`](./MIGRATION-3.0.md)

---

*FCoP 3.0 迁移指南 · 2026-05-21*
