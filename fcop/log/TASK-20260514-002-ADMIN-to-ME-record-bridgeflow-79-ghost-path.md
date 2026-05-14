---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260514-002
sender: ADMIN
recipient: ME
priority: P2
thread_key: adr-0022-field-feedback
related: [ADR-0022, ADR-0021, ADR-0006]
session_id: sess-20260514-me-02
---

# 入档 · Bridgeflow #79 幽灵路径事件 · ADR-0022 第一份野外缺陷反馈

## 背景

ADMIN 通过 chat 给 FCoP 总部一份**外部项目反馈**：

`codeflow-shell` 项目(Bridgeflow)的 PM-01 在自披露 #79 中发现并根治了一个由 FCoP **ADR-0022 workspace 路径迁移**间接引发的幽灵路径 bug，并派生出一条新的自约束规则。

按 Rule 0.a，这件事必须在 FCoP 总部入档——它是 ADR-0022 自 2026-05-09 落地以来的第一份野外缺陷反馈，值得作为协议演化的活素材永久留痕。

## 事件原文（ADMIN 转述）

### 服务 startup log 变化

**修复前**：

```
↳ PM→worker:    fcop/tasks
↳ ADMIN direct: docs/agents/tasks   ← 旧幽灵路径
↳ report loop:  fcop/reports
```

**修复后**：

```
↳ PM→worker:    fcop/tasks          ← ADMIN→PM 也走这里
↳ report loop:  fcop/reports
```

`docs/agents/tasks/` 那行彻底消失。现在从「输入」页发消息，任务文件直接写进 `fcop/tasks/`，完全在 FCoP 协议体系内流转。

### Bridgeflow PM-01 入档要点（2026-05-14 13:38 CST）

- **PM #73~#79 自披露全部入档**
- **D58~D64 决策档入档**
- **Charter 7（AI 行为必须可见）首次定稿**
- **技术债 4 项登记**
- **幽灵路径 bug #79 当日根治**
- **FCoP ADR-0022 双 workspace 冲突消除**，`fcop.Project()` 无参初始化恢复正常
- `/api/v2/chat/history` 接口上线，聊天完全打通，ADMIN↔PM-01 对话可见

### PM-01 错位 #79 关键事实

| 维度 | 内容 |
|---|---|
| **错位编号** | PM #79 |
| **根因** | D6 迁移（5/11）遗漏代码层引用，`adminTasksDir` 指向旧路径整整 3 天 |
| **双违反** | 幽灵文件（违反 Rule 0.a 文件即协议）+ FCoP ADR-0022 ConfigError（双 workspace 并存） |
| **派生规则** | **自约束 9.1 派生条款 v3**：路径迁移后必须全仓 `grep -r` 扫旧路径引用，**不能只做 fs 层迁移** |
| **修复闭环** | 代码改 → 幽灵文件迁移 → 空目录删除 → FCoP 初始化恢复正常 → 服务重启验证 |

## 协议层意义

### 这事暴露了 ADR-0022 §"Design Details" item 3 的覆盖缺口

ADR-0022 顾问扫描器（advisor scan）当前只覆盖：

- `.gitignore`
- `.cursor/rules/*.mdc`
- `AGENTS.md` / `CLAUDE.md`
- `README*.md`

**未覆盖**：业务代码层（`.ts` / `.js` / `.py` / `.go` / `.rs` 等）里 hard-code 的字符串字面量，例如 Bridgeflow `web-panel.ts` 里的 `adminTasksDir = "docs/agents/tasks"`。

ADR-0022 原文写：

> 顾问扫描：检测 `.gitignore` / `.cursor/rules/*.mdc` / `AGENTS.md` / `CLAUDE.md` / `README*.md` 中的 `docs/agents` 字符串引用，**列出但不自动改写**

这条规则的潜台词是「字符串字面量都在配置/文档文件里」——但 Bridgeflow 这个 case 证明：**业务代码里也会 hard-code 协议路径**，而且这种 hard-code 比配置文件更隐蔽（看不见的代码 + 编译产物的延迟暴露）。

### Bridgeflow PM-01 自约束 9.1 v3 是对 ADR-0022 的实质补充

> 路径迁移后必须全仓 `grep -r` 扫旧路径引用，不能只做 fs 层迁移

这条规则**应当被反向回流到 FCoP 协议层**——具体形式留给 ADMIN 决定：

- **选项 A**：作为 ADR-0022 的非破坏性 amendment（但 ADR body 已 frozen，需要走「下一序号同前缀」？）
- **选项 B**：作为新 ADR 编号（ADR-0028+），主题「Workspace migration code-layer scan」
- **选项 C**：仅作为 `fcop migrate-workspace` 工具的一项功能增强（advisor scan 扩展到全仓 `grep`）+ 归档现场记录

## 验收标准

1. ✅ 本 task 落 `fcop/tasks/TASK-20260514-002-*.md`（已落，即本文件）
2. ⬜ 在 `fcop/shared/` 落一份 `DECISION-20260514-adr-0022-field-feedback-bridgeflow-79.md`，记录这次野外反馈 + 三个选项 + 暂不立即决断（留 ADMIN 后续决定）
3. ⬜ 写 `REPORT-20260514-002-ME-to-ADMIN.md` 收尾，引用 DECISION 文件路径
4. ⬜ archive `TASK-20260514-002` + `REPORT-20260514-002` 到 `fcop/log/`
5. ⬜ git add / commit / push origin / push backup（按 v2.0.2 同款双 push 节奏）

## 备注

- 本事件是 ADR-0022 自 2026-05-09 v1.0 RC 落地以来的**第一份野外缺陷反馈**——具有协议演化的史料价值
- 不立即修订 ADR-0022 也不立即开新 ADR——只**结构化入档**，等 ADMIN 决定何时正式响应
- Essay 留作 todo（候选标题：`essays/the-ghost-path-three-days-on.md`），不强制本次产出
