---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P2
references:
- TASK-20260522-008
status: done
---

## 执行总结

按 TASK-008 验收三项全部达成。thread_key: readme-banner-prompt-links-20260522

## 产出 diff

### 1. README banner 双语加链（产品面）

- `README.md` line 15-17：`Getting started` 后插入两条链接
  - `<a href="src/fcop/rules/_data/agent-install-prompt.en.md">Install prompt</a>`
  - `<a href="src/fcop/rules/_data/agent-bringup-prompt.en.md">Bringup prompt</a>`
- `README.zh.md` line 15-17：`上手 FCoP` 后插入两条链接
  - `<a href="src/fcop/rules/_data/agent-install-prompt.zh.md">安装 prompt</a>`
  - `<a href="src/fcop/rules/_data/agent-bringup-prompt.zh.md">起项目 prompt</a>`

中文标签选了【安装 prompt】／【起项目 prompt】——与两份文档使用场景一一对应（安装 fcop-mcp · 起新项目）。

### 2. RULES-release-file-inventory 补登（治理面）

`fcop/shared/RULES-release-file-inventory.md` line 92-95，在 `agent-install-prompt.{zh,en}.md` 下面补上 `agent-bringup-prompt.{zh,en}.md` 两行，标注 v3.0.2 · TASK-007。

## 验收

| 项 | 状态 |
|---|---|
| README 双语 banner 各加 2 条链，链路存在 | ✅ |
| `python scripts/inventory_drift.py` 三类警告清零 | ✅ missing=0 unlisted=0 renamed?=0 |
| REPORT-008 + archive TASK-008 | ✅ 本报告 |

## drift 沉淀

TASK-007 推送后留下一个 `unlisted=2` 缺口：TASK-007 只动了 `src/`，漏进 `RULES-release-file-inventory.md` release surface 清单。本任务顺手补了那个缺口。下轮有机会可考虑加入 release_audit pre-commit hook。

## Commit 计划

1. **产品**：`README.md` + `README.zh.md` → `docs(readme): banner add install/bringup prompt links`
2. **治理**：`RULES-release-file-inventory.md` + `REPORT-008` + archive TASK-008 → `fcop: archive TASK-008 + sync inventory for bringup prompts`

## 下一步

ADMIN 确认后推送两个 commit。