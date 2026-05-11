---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
subject: Rule 1 角色身份唯一性硬化（一人一角色、从磁盘账本判定、ADMIN 受约束）——0.7.0 预站
references:
- ISSUE-20260427-002-ME.md; ISSUE-20260427-001-ME.md; TASK-20260427-001-ADMIN-to-ME.md;
  src/fcop/rules/_data/fcop-rules.mdc Rule 1/4/7/8; src/fcop/rules/_data/fcop-protocol.mdc
  UNBOUND 节 + Architectural Principle
---

## 起因

2026-04-27 下午。ADMIN 在 dogfood 合拢后接连抛出三个制约问题，逐次锁紧了同一道子：

1. 「两个 agent，如果我们都说他是 ME，会发生什么情况？」
2. 「这里问题是，如果有两个一样的 ME，那么犯错的是 admin；我们要从落盘的文件去分析，因为文件即协议；如果再用的已经有角色的报告了，就不能发生冲突，即使是临时性的 temp，也不能产生本质的角色冲突。」
3. 「每个 agent，都要 admin 确认身份，但是 admin 不能把同一身份给多 agent！」

从「现象」到「原则」到「安位」，本任务是这条原则的站台。

## ADMIN 立的三条推论

1. **「角色被谁占着」≡「磁盘上是谁在用这个角色码写文件」**。`docs/agents/tasks/`、`reports/`、`issues/`、`log/` 是占用状态的**唯一权威源**，和 `fcop.json` 同等级：fcop.json 说「这个角色存在」，tasks/reports/log 说「这个角色正活跃」。

2. **ADMIN 双 bind 是 ADMIN 的失误，但协议必须接得住**。agent 在 BOUND 之前**自己**去翻文件账本，发现角色已被使用就**拒绝默认占领**，反向问 ADMIN：「ME 已被 `sess-...` 写过 N 份文件，你是要交班、协审、还是另立角色？」

3. **「临时」/「temp」不是 bypass 通行证**。任何要写盘的 agent 都要拿到和已有角色码不重合的代号。临时身份 = 临时**角色码**，不是临时**借用 ME**。「我就快速顶一下」在协议里不是合法理由。

## 合并后的 Rule 1 不变量

> **角色 ↔ 身份 是一对一映射。ADMIN 是不可借出的人类角色（→ 0 个 agent）；其他每个角色至多 1 个 agent；身份必须由 ADMIN 显式指派且不得重复发放。**

这是现有 Rule 1 「ADMIN 这个**特殊角色**不能被指派」的对偶升级：不仅 ADMIN 一对零，**任何**非 ADMIN 角色也一对一。

ADMIN 受协议约束并不是新事——Rule 7 早就写过：「本规则约束 OPS，也约束任何实际执行破坏性动作的角色（包括 ADMIN 本人）。」本任务只是把这个性质从 Rule 7 拓到 Rule 1。

## 双 bind 现场的执行链路（不需新工具）

```
ADMIN: 「你是 ME」
   │
   ▼
Agent（新 session）：
   1) fcop_report → 看到 ME 占用状态：ACTIVE，last session_id ≠ 我
   2) 触发 Rule 1 + Rule 8 联动：拒绝 BOUND 转换
   3) 落一份 .fcop/proposals/double-bind-{ts}.md：
      - 「ADMIN 试图把 ME 指派给我，但磁盘上 ME 已被 sess-... 占用」
      - 三选一推荐：handoff / co-review / 另立角色码
   4) 报告 ADMIN，等回复
   5) ADMIN 说「那你做 co-reviewer」 → 接受 BOUND，但只读+只写二审段落
      或 ADMIN 说「那旧那个先归档」 → 等旧 session 写 handoff TASK
      或 ADMIN 说「叫你 ME-2 吧」 → 走 create_custom_team / init_* force=True
```

**0 个新工具**。现有的 `fcop_report` 输出 + `.fcop/proposals/` 下落盘 + Rule 8 拒绝权合起来就够了。

## 修订清单（趋紧后的最终版）

| 文件 | 改动 |
|---|---|
| `src/fcop/rules/_data/fcop-rules.mdc` | **改 Rule 1**——「贯穿两阶段的硬约束」那一节加一条：「ADMIN 不得把同一角色码指派给多个 agent；磁盘账本是占用状态的唯一权威源。」 Rule 4 的 thread-driver 那条不动 |
| `src/fcop/rules/_data/fcop-protocol.mdc` | **改 UNBOUND 协议那一节**：在「等 ADMIN 明确指派」步骤后加一段——agent 转 BOUND 前，必须先用 `fcop_report` 输出的 occupancy 段对照自己的 session_id；冲突时按 Rule 8 拒绝、落 `.fcop/proposals/`、向 ADMIN 出三选一 |
| `src/fcop/rules/_data/letter-to-admin.{zh,en}.md` | 加一段 ADMIN 纪律提醒：「FCoP 协议约束 ADMIN：你不能把 ME 同时给两个 agent。要让两个 agent 协作请用 team 模式；要协审请明说『你是 ME 的 co-reviewer』。」 |
| `mcp/src/fcop_mcp/server.py` `fcop_report` | UNBOUND 分支输出增加 occupancy 段：逐角色统计 open tasks/reports/issues + archived + last session_id seen + 状态标签 |
| 【不动】 | `init_*`；不引入 lock/lease 文件；frontmatter 不改；不加新工具 |

## 验收标准（0.7.0 实现后）

- `fcop_report()` （包括 UNBOUND 与 initialised 两分支）输出底部含「角色占用 / Role occupancy」段，逐角色列出：open tasks 数 + open reports 数 + open issues 数 + archived 数 + last session_id seen + 状态标签（UNUSED / ARCHIVED / ACTIVE）。
- `fcop-rules.mdc` 中 Rule 1 「贯穿两阶段的硬约束」含「一角色一 agent」条款；中英各一份。
- `fcop-protocol.mdc` UNBOUND 节含 agent 转 BOUND 前的 occupancy 自检步骤 + 三选一出口。
- `letter-to-admin.{zh,en}.md` 含 ADMIN 纪律提醒（双 bind 禁令明文）。
- `fcop_protocol_version: 1.4.0 → 1.5.0`、`fcop_rules_version: 1.6.0 → 1.7.0`。
- 包版本 `fcop` / `fcop-mcp` 从 0.6.5 跳 0.7.0（minor bump）。
- 新增测试：双 bind 场景下 agent 拒绝转 BOUND + 落 `.fcop/proposals/` 的 happy/sad path 各一道。
- 现有 587 passed 基线不降。

## 范围外明确不做

- **不引入运行时 lock / lease 文件**。`.fcop/sessions/<role>.lock` 是我上一轮草拟的 0.6.7 候选 B，ADMIN 明确否定。理由：违反 `fcop-protocol.mdc`「Tools are a Convenience Layer」公理——协议长在文件系统上，不能拼接运行时状态。
- **不改 frontmatter 语义**。`session_id` 字段 v1.1 已落地，本轮只读不改。
- **不改 init_***。初始化不是双 bind 现场。

## 责任人

ME（本角色）负责抽明、起草、验证；ADMIN 拍板启动 0.7.0 发布窗口。本任务本身讯息是**“落设计记录 + 排队”**，实现不在本轮会话范围内。REPORT 会以 status=in_progress 走，任务保持 OPEN，等 ADMIN 启动 0.7.0。

## 关联

- ISSUE：`ISSUE-20260427-002-ME.md`（同轮落盘、作为裂缝追踪）
- 上游违规：`ISSUE-20260427-001-ME.md`（tripwire 覆盖不到手工 git，0.7.0 可一起修）
- 上游任务：`docs/agents/log/tasks/TASK-20260427-001-ADMIN-to-ME.md`（0.6.6 文档级 patch）
- 原生说明书：`docs/agents/LETTER-TO-ADMIN.md`、`fcop://letter/zh`
- 架构公理：`fcop-protocol.mdc` 「Architectural Principle: Tools are a Convenience Layer」一节
