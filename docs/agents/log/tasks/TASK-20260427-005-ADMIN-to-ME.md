---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260427-005
sender: ADMIN
recipient: ME
priority: P2
related: [ISSUE-20260427-006, TASK-20260427-004]
session_id: sess-20260427-me-071
---

# 0.7.1 收尾：决定不 yank `fcop-mcp 0.7.0`，校准 4 处文档

## 背景

REPORT-20260427-005 把 "Phase 23 yank `fcop-mcp 0.7.0`" 列为
"待 ADMIN 启"。ADMIN 复盘后判断：

- `uvx fcop-mcp` / `pip install fcop-mcp` 不带版本钉都已落到
  0.7.1，新装路径自愈；
- 已经装 0.7.0 的旧用户 yank 救不回，必须 `pip install -U`；
- yank 真正能保护的只有"未来主动钉 `==0.7.0`"的人，且这群人
  目前几乎不存在；
- yank 可逆，下载量回升或第二个用户报修再 yank 也来得及。

结论：**0.7.1 不 yank**，决策与 yank 知识写进 release notes。

## 要求

1. `docs/releases/0.7.1.md` 顶部 metadata 块从 "Yanked: ..." 改为
   "kept on PyPI, not yanked"，并在 post-mortem 后新增一节
   "Why we did not yank `fcop-mcp 0.7.0`"，含 PEP 592 行为表 + 何时
   会反悔。
2. `CHANGELOG.md` `[0.7.1]` 把 "is being yanked from PyPI" 删除，
   改成"kept on PyPI, not yanked"并指向 release notes。
3. `docs/agents/issues/ISSUE-20260427-006-ME.md` resolution 把
   "待 ADMIN 走 twine yank 流程下架"改成"决定不 yank，理由记入
   release notes"。
4. `docs/releases/RELEASE-CHECKLIST.md` Phase 6 yank 项从"必须"改为
   "按需，可选；可逆；记录决策"，列出何时 yank / 何时跳过。

## 验收

- 四处文档无 "being yanked" / "待 ADMIN.*yank" 残留（grep 全空）。
- 新一节 "Why we did not yank" 把 PEP 592 行为按命令逐行讲清。
- TASK-005 + REPORT-006 入账并 archive；ISSUE-006 的 resolution 不
  动 closed 状态（已闭），仅修订 resolution 文本。
- followup commit 单独一条，不和 0.7.1 主提交混。
