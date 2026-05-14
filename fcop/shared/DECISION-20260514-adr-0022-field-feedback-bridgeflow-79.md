---
protocol: fcop
version: 1
kind: decision
decision_id: DECISION-20260514-adr-0022-field-feedback-bridgeflow-79
sender: ME
recipient: TEAM
related: [ADR-0022, TASK-20260514-002]
thread_key: adr-0022-field-feedback
status: recorded
date: "2026-05-14"
---

# DECISION · ADR-0022 第一份野外缺陷反馈 · Bridgeflow #79

## TL;DR

Bridgeflow（`codeflow-shell`）项目 PM-01 在 2026-05-14 13:38 CST 入档自披露 #79：D6 路径迁移（2026-05-11）遗漏业务代码层引用，导致 `adminTasksDir` hard-code 指向旧 `docs/agents/tasks/` 路径**整整 3 天**，造成幽灵文件 + FCoP ADR-0022 `ConfigError`（双 workspace 并存）。

PM-01 当日完成根治（代码改 → 幽灵文件迁移 → 空目录删除 → FCoP 初始化恢复 → 服务重启验证），并派生新规则：

> **自约束 9.1 v3**：路径迁移后必须全仓 `grep -r` 扫旧路径引用，**不能只做 fs 层迁移**。

本 DECISION 文件**仅入档现场**，不立即修订 ADR-0022 / 不立即开新 ADR——决定何时正式响应留给 ADMIN。

## 根因

ADR-0022 §"Design Details" item 3 的「顾问扫描」覆盖范围：

```
.gitignore
.cursor/rules/*.mdc
AGENTS.md
CLAUDE.md
README*.md
```

**未覆盖**：业务代码层（`.ts` / `.js` / `.py` / `.go` 等）里 hard-code 的字符串字面量。

Bridgeflow `web-panel.ts` 里的 `adminTasksDir = "docs/agents/tasks"` 正落在这个盲区。`fcop migrate-workspace --apply` 不会扫到它；`fs.move` 完成后服务启动时一切看起来正常，直到三天后 `fcop.Project()` 检测到「`fcop/` 与 `docs/agents/` 双存在」抛 `ConfigError`，才把这个 hard-code 暴露出来。

## 协议层观察

### 1. ADR-0022 「列出但不自动改写」原则在野外的副作用

ADR-0022 当时刻意把 advisor scan 设计为「列出不改写」，理由是「规避误伤用户文档」（item 3 原文）。这个保守原则在配置/文档层是对的——用户的自然 docs 里也可能合法地提到 `docs/agents/`。

但**业务代码里 hard-code 的协议路径几乎不存在「合法的旧路径引用」**——它就是要跟随协议升级的。换句话说：

| 文件类型 | 「列出不改写」是否合理 |
|---|---|
| `README*.md` / 教程文档 | ✅ 合理（用户文档可能讲历史，旧路径有合法用法） |
| `.cursor/rules/*.mdc` / `AGENTS.md` | ✅ 合理（同上） |
| 业务源码 `.ts` / `.py` / `.js` / `.go` | ❌ **不合理**（hard-code 的协议路径几乎一定要随协议迁移） |

### 2. 暴露窗口的非对称性

`fs.move` 完成的瞬间，**文件系统层**看起来已经迁移完毕；但**进程内存层**的 hard-code 还指向旧路径。两者的不一致**只在重启 + 真实写入路径时才暴露**——Bridgeflow 这次是 PM 派给 worker 的 task 文件落到了旧路径，3 天才被发现。

这是典型的「迁移完成度幻觉」：CLI 报「迁移成功」≠ 全系统已对齐。

### 3. PM-01 派生规则的协议级价值

> 路径迁移后必须全仓 `grep -r` 扫旧路径引用，不能只做 fs 层迁移

这条规则**普适于任何 FCoP workspace 迁移场景**，不只是 `docs/agents/` → `fcop/`。未来若再发生类似 namespace 改名（如 v2.x 的某次升级），这条规则可以直接复用。

## 三种正式响应路径（留 ADMIN 后续决定）

### 选项 A · ADR-0022 的非破坏性 amendment

按 Rule 5「append-only」，给 ADR-0022 续写一段「2026-05-14 amendment」，把「业务代码层」加入 advisor scan 范围；ADR body frozen 原则保持不变（只追加 changelog 段）。

| 项 | 内容 |
|---|---|
| 协议变更等级 | PATCH（设计细节澄清，非语义变更） |
| 工程成本 | 中（需要 `fcop migrate-workspace` 升级 advisor scan + 测试） |
| 风险 | 极低（advisor 仍是「列出不改写」，只是覆盖面扩大） |

### 选项 B · 开新 ADR（ADR-0028+）

主题：「Workspace Migration: Code-Layer Scanning」。ADR-0022 不动，新 ADR 引用之并扩展 advisor scan 设计。

| 项 | 内容 |
|---|---|
| 协议变更等级 | MINOR（新增独立决策） |
| 工程成本 | 中（同选项 A） |
| 风险 | 低（独立 ADR 易于追溯） |

### 选项 C · 仅 tooling 增强 + 现场记录

不动 ADR、不开新 ADR。`fcop migrate-workspace` 直接把 advisor scan 扩展到全仓 `grep -r "docs/agents"` 默认行为；本 DECISION + TASK-20260514-002 + REPORT 留作历史现场。

| 项 | 内容 |
|---|---|
| 协议变更等级 | 无（纯实现增强） |
| 工程成本 | 低（一行 advisor scan 改造） |
| 风险 | 极低 |
| 局限 | 协议层没有正式记录这条规则——下次有人重做 advisor 时可能再遗漏 |

### ME 倾向

**选项 A 或选项 C（二选一即可）**——选项 B 偏重；ADR-0022 的「Design Details」段本就是设计细节决策，amendment 的合法性高。但选项 C 也合理——这件事工程上一行修就能解决，协议层的「不要只做 fs 层迁移」规则记进本 DECISION 已经留了痕。

## 不做什么

- ❌ 不立即修改 ADR-0022 body（ADR 文件 frozen）
- ❌ 不立即开新 ADR（等 ADMIN 决定路径）
- ❌ 不立即升级 `fcop migrate-workspace`（同上）
- ❌ 不为此发新版（v2.0.2 刚发完，等下一次正常 release window）

## 引用

- **ADR-0022**：`adr/ADR-0022-workspace-directory-convention.md`
- **TASK**：`fcop/tasks/TASK-20260514-002-ADMIN-to-ME-record-bridgeflow-79-ghost-path.md`
- **REPORT**：`fcop/reports/REPORT-20260514-002-ME-to-ADMIN.md`（即将落档）
- **外部现场**：Bridgeflow PM-01 自披露 #79 + Charter 7（AI 行为必须可见）首次定稿（2026-05-14 13:38 CST，`codeflow-shell` 项目）
