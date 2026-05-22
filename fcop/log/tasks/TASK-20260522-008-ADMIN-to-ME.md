---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P2
thread_key: readme-banner-prompt-links-20260522
subject: README banner 加 install / bringup prompt 链接
---

## 背景

ADMIN 看到主页 README 顶部 banner（`Project homepage · 简体中文 · Getting started · MCP Tools (35) · Field Report · Natural Protocol · 3.0 Spec · ADR Index`）后指出：装 fcop-mcp 与起项目的两份 agent prompt 应该在这里就能点到，不要藏在中段表格里。

related: TASK-20260522-007-ADMIN-to-ME

## 要做

在 `README.md` line 13-20 与 `README.zh.md` line 13-20 的 `<p align="center">` banner 内，**Getting started / 上手 FCoP** 之后插入两条新链接：

- `Install prompt` → `src/fcop/rules/_data/agent-install-prompt.en.md`（README.zh.md 用 `.zh.md`）
- `Bringup prompt` → `src/fcop/rules/_data/agent-bringup-prompt.en.md`（README.zh.md 用 `.zh.md`）

中文标签待定。

## 不做

- 不改 banner 其它链接顺序
- 不动第二排 badges
- 不改中段 "You want to…" 表
- 不发新版本

## 验收

1. README.md / README.zh.md 双语 banner 各加 2 条链接，链路活
2. inventory_drift.py 三类警告清零
3. 写 REPORT-008，archive TASK-008
