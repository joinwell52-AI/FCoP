---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260522-009
sender: ME
recipient: ADMIN
task_id: TASK-20260522-009
parent: TASK-20260522-009
related: [TASK-20260522-007, REPORT-20260522-007]
thread_key: bringup-prompt-defects
session_id: sess-20260522-me-09
status: done
---

# REPORT-009 · `agent-bringup-prompt.{zh,en}.md` §5 两处事实错已修

## 做了什么

按 TASK-009 修两份 bringup prompt 的 §5：

### 1. 五桶名字改对

`intent / plan / execution / verification / archive` →
`inbox / active / review / done / archive`

依据：`src/fcop/lifecycle/state.py` 的 `Stage` enum（`INBOX`/`ACTIVE`/
`REVIEW`/`DONE`/`ARCHIVE`），与 fcop 库 `_apply_init` → `ensure_lifecycle_dirs`
实际落盘一致。原 prompt（TASK-007 写的那版）里那五个名字是凭印象抄
的，从未跟代码对过。

### 2. 删掉"v3 仍保留 tasks/ + log/"的错误说法

老说法：`└── (兼容五桶: tasks/ reports/ issues/ shared/ log/ —— v3 仍保留)`

新说法分两部分：

- §5 顶部加 callout 明说 fresh init **不再创建** `tasks/` 和 `log/`，
  并指向 `python -m fcop migrate --to-v3` 给老 v2 项目。
- 目录树里只列实际仍保留的：`reports/` `issues/` `reviews/`。

依据：3.0.2 的 commit `5ab9e73` 已把 `tasks/`/`log/` 从 fresh init 路径
退场（spec §6 钦定），改写到 `_lifecycle/inbox/` 与 `_lifecycle/archive/`。

中英两份同步改。

## 验证

1. grep 校验五桶错名零命中（仅剩"v3 仍保留 / kept in v3"两处合法引用，
   指向 reports/issues/reviews）：

   ```
   $ rg "intent/|plan/|execution/|verification/|v3 仍保留|kept in v3" \
       src/fcop/rules/_data/agent-bringup-prompt.{zh,en}.md
   src\fcop\rules\_data\agent-bringup-prompt.zh.md
     163:  ├── reports/                       ← 报告（v3 仍保留）
     164:  ├── issues/                        ← 问题单（v3 仍保留）
     165:  └── reviews/                       ← 审查（v3 仍保留）
   src\fcop\rules\_data\agent-bringup-prompt.en.md
     177:  ├── reports/                       ← reports (kept in v3)
     178:  ├── issues/                        ← issues (kept in v3)
     179:  └── reviews/                       ← reviews (kept in v3)
   ```

   错的桶名（`intent/`/`plan/`/`execution/`/`verification/`）零命中。

2. ReadLints 两份文件无新增警告。

## 影响范围

- **prompt 即时生效**：用户从 GitHub raw 链接（README banner 第 5 个）
  打开，下次刷新就拿新版，不需要发新 wheel。
- **打 wheel 时同步生效**：下次 `fcop` 包发版，`src/fcop/rules/_data/`
  下两份新文本会被打进去，离线 / 内网用户也能拿到。
- **不动代码、不改测试、不动 fcop.json `protocol_version`**——纯文档错字
  修复，按 ADR-0003 §1.x 不需要 bump。

## 不在本 task 范围（按 TASK-009 §"不在本 task 范围"）

- `agent-install-prompt.{zh,en}.md` 的 uvx 缓存防呆 → 单独 TASK-010。
- 这个仓本身的 v3 拓扑迁移（其实**不该**做——这是 fcop 库开发仓，
  `fcop/` 是吃自己狗粮的演示，不是用户项目）→ 暂搁置，待你定。
- 释 fcop / fcop-mcp 任何代码 → 不动。

## 双 commit 计划

- commit A（产品）：`docs(prompt): fix bringup prompt §5 lifecycle bucket names + drop v2 dirs`
  - `src/fcop/rules/_data/agent-bringup-prompt.zh.md`
  - `src/fcop/rules/_data/agent-bringup-prompt.en.md`
- commit B（治理）：`fcop: archive TASK-009 + REPORT-009`
  - `fcop/log/TASK-20260522-009-ADMIN-to-ME.md`
  - `fcop/log/REPORT-20260522-009-ME-to-ADMIN.md`

待你说"推"我就 push main。

## 致歉

刚才把开发仓口语化成"本项目"是嘴瓢，措辞已纠正。事实判断没错——
prompt 那两处该改，本会话只动 prompt 文档，不动 fcop/ 演示账本拓扑。
