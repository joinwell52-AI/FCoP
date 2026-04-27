---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P2
references:
- TASK-20260427-005
- ISSUE-20260427-006
- REPORT-20260427-005
amends: REPORT-20260427-005
session_id: sess-20260427-me-071
status: done
---

# 0.7.1 收尾——决定不 yank + 4 处文档校准

## 状态

`status=done`。`amends: REPORT-20260427-005` 替代该报告 "Phase 23 待
ADMIN 启 yank" 一行的悬置态——0.7.1 release tail 至此真正闭合。

## 决策（一句话）

**`fcop-mcp 0.7.0` 留在 PyPI，不 yank。** yank 留作可逆应急手段。

## 四处文档校准证据

| 文件 | 改动要点 |
|---|---|
| `docs/releases/0.7.1.md` | 顶部 metadata 由 "Yanked" 改为 "kept on PyPI, not yanked" 并解释路径已自愈；post-mortem "What we are not doing" 末尾追加 "Yanking `fcop-mcp 0.7.0`" 条目；新增 H2 "Why we did not yank `fcop-mcp 0.7.0`" 含 PEP 592 行为对照表（5 行 install path × yank/不 yank） + 反悔触发条件 |
| `CHANGELOG.md` | `[0.7.1]` 段 "is being yanked from PyPI" 删除，改为 "stays on PyPI, **not yanked**: ... rationale recorded in `docs/releases/0.7.1.md`" |
| `docs/agents/issues/ISSUE-20260427-006-ME.md` | resolution 末尾改为"经 ADMIN 拍板**不 yank**：默认安装路径已自愈… yank 留作可逆应急手段，决策依据写入 `docs/releases/0.7.1.md`" |
| `docs/releases/RELEASE-CHECKLIST.md` | Phase 6 yank 项从"必须"改为"按需，可选"，给 PEP 592 简介 + yank 何时该做 / 何时跳过 / 必须记录决策与理由 |

`grep -ri "being yanked\|to be yanked\|待.*yank"` 全 Workspace 命中
为零。

## 协议自检（dogfood 0.7.1 新规）

- **Rule 5（新版，1.8.0）**：本次校准没有去改 REPORT-005 文本，
  而是用顺序 `REPORT-20260427-006` + frontmatter `amends:
  REPORT-20260427-005` 续接——正是 1.8.0 删除 `AMEND-*` / `*-v2.md`
  之后建议的标准做法。
- **Rule 0.a.1（新版，1.8.0）**：本次"决定 + 改 4 处 doc"先立
  TASK-005 → 改 → REPORT-006 → archive，再 commit；没有走 raw
  shell / IDE 直接落盘绕过 ledger 的捷径。
- **Rule 1（新版，1.8.0）**：全部写入由同一 session
  `sess-20260427-me-071` 完成，未派生子 agent。

## `Project.audit_drift()` 自检结果（dogfood）

跑 `audit_drift()` 实测：

```
git_available: True
drift entries: 6
  M CHANGELOG.md / docs/releases/0.7.1.md / docs/releases/RELEASE-CHECKLIST.md
    （本任务已修改、待 commit；属预期 in-flight 状态）
  ?? docs/worktree-本机-Bridgeflow-同步说明.md / mcp/uv.lock / uv.lock
    （会话开始前就存在的 untracked 本地文件；非本 release scope）
session/role conflicts: 1
  sess-20260427-me-071 -> ('ADMIN', 'ME')
```

**冲突解读**：本 session 既以 `sender: ADMIN` 写过 TASK
（TASK-004 / TASK-005 是 ME 替 ADMIN 转写的指令），又以
`sender: ME` 写过 REPORT。这是协议默认的 **ADMIN-via-ME 转写
模式**——ADMIN 在对话里口头给指令，ME 把它落成
`...-ADMIN-to-ME.md` 文件以保留指令的真正来源。Rule 1 1.8.0 的
角色唯一性条款明文豁免 `ADMIN` / `SYSTEM`（"non-`ADMIN` /
non-`SYSTEM` role code"），所以这不是冒充，是合法模式。

**但 `audit_drift()` 当前不知道这个豁免**——它把 ADMIN/SYSTEM
也算进 session/role 一致性里，会持续在所有正常项目里给出 1 条
冲突。**这是 0.7.1 留下的小坑**，应在 0.7.2 修：

候选改进（待立 ISSUE-007 / ISSUE-008）：

1. **`audit_drift()` 改成 ADMIN/SYSTEM-aware**：当冲突的角色集
   只在 `{ADMIN, SYSTEM, <一个普通角色>}` 范围内时降级为
   info（"ADMIN-via-ME 转写"），不报 high。
2. 或者协议层规定：ME 替 ADMIN 转写 TASK 时必须换一个独立
   `session_id`（如 `sess-...-admin-transcript`），让审计天然
   分清。方案 1 更轻；方案 2 更纯。

本次先把现象诚实记录在案，留给下个版本决策。

## ADMIN 下一步

无强制项。0.7.1 release 全程闭合：

- PyPI fcop 0.7.1 / fcop-mcp 0.7.1 已发布；
- v0.7.1 git tag + GitHub release 已发；
- 文档 / 账本与"不 yank"决策一致；
- yank 决策已记录 = 不做（PyPI 上 0.7.0 保留）。

可选 follow-up：是否要立 ISSUE-007 / ISSUE-008 把 `audit_drift()`
ADMIN-aware 的事排进 0.7.2 队列。
