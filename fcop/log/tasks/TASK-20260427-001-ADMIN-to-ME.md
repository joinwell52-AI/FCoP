---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
subject: 0.6.6 文档级 patch：跨表面一致性自查 + 修复（追溯落档）
references:
- commit 274ce06; commit 87e178a; docs/releases/0.6.6.md
---

## 上下文

2026-04-27，ADMIN 在会话里发起两轮工作：

1. 「自我检查所有文档、GitHub、PyPI，看下是否逻辑一致；fcop-mcp 那么多功能究竟什么作用？」
2. 「按 0.6.6 出文档级 patch（不动包，PyPI 不重发，只刷 GitHub 上的 README 和 mcp 子包源码 README——下次发包会带过去）」
3. 「该补齐的补齐，该重写的重写」

本任务把上面三轮会话压缩为一份追溯任务单。**追溯落档原因**：ME 在执行整个流程中违反了 Rule 0.a.1，全程没写 `TASK-*.md`、没写 `REPORT-*.md`、没归档，直接动手编辑 + 两次 commit + 两次 push。ADMIN 第四轮明确指出：「你做好记录啊，你自己不按 fcop 要求做记录」——本任务即为协议侧的纠正补登。

## 自查阶段（Phase 1）发现的漂移点

- `docs/mcp-tools.md` L12 写「资源 10 个」，真值 12（9 静态 + 3 模板），漏列 0.6.4 加的 `fcop://prompt/install` zh + en。
- `mcp/README.md`（即 PyPI fcop-mcp 长描述）只提了 0.6.4，**0.6.5 在 PyPI 页面完全无声**——用户看到 0.6.5 wheel 但读不到这版改了什么。
- `LETTER-TO-ADMIN.{zh,en}.md` 顶部「0.6.4 摘要」块对 0.6.5 只字未提。
- 根 `README.md` / `README.zh.md` 的「0.6.3 highlights」长段（10 行混 5 个关注点）冻结在 0.6.3。

版本号、包定位、tool/resource 签名在所有表面都一致；漂移仅在「人读副本」一侧。

## ME 的应交付物

按文档级 patch 走，不动 `_version.py`、不发 PyPI、不打 tag。GitHub 主线刷新，下次代码发包自动捎带：

1. `docs/mcp-tools.md`：资源数 10 → 12，补 prompt/install zh+en 两行，`fcop_report` / `new_workspace` 行各加 0.6.5 行为说明。
2. `mcp/README.md`：在现有 0.6.4 注释后追加 0.6.5 Rule 0.a.1 tripwire 一段。
3. `LETTER-TO-ADMIN.{zh,en}.md`：保留「0.6.4 摘要」标题（避免破坏 `test_zh_contains_064_summary_marker`），块尾追加 0.6.5 polish bullet。
4. 根 `README.md` + `README.zh.md`：「0.6.3 highlights」长段重写为版本无关的 5 行 Pointers 表 + 3 行 Recent releases 表 + 「PyPI 同名 fcop」单独 blockquote。
5. `CHANGELOG.md` `[Unreleased]` 段、`docs/releases/0.6.6.md`：完整记录两个 commit 的范围、**明确不做的事**、验证命令。

## 验收标准

- `ruff check .`：clean。
- `pytest tests`：587/587 与 0.6.5 同基线。
- `tool_surface.json` / `public_surface.json` snapshot 不变。
- `get_letter_intro('zh')` 同时含「0.6.4 摘要」与「0.6.5 微调」（slice 安全）。
- `rg "0.6.3 highlights" README*.md` 无匹配。
- 根 README 两版结构对齐，pointers / releases 两表行数一致。

## 协议附注

本任务由 ME 在 ADMIN 第四轮反馈后用 `init_solo` 把仓库 dogfood 化、再补 `write_task` 落档。后续 `write_report` 与 `archive_task` 在同一 session 内完成。从此 FCoP 仓本身按 Solo 模式跑——以后 ADMIN 给的活，ME 走 task → do → report → archive，不再绕。
