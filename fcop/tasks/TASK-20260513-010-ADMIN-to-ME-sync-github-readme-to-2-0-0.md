---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-010
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: fcop-2-0-0-public-sync
session_id: sess-20260513-me-04
---

# 同步 GitHub 主仓 README 至 v2.0.0

## 背景

ADMIN 现场反馈:

> https://github.com/joinwell52-AI/FCoP/blob/main/README.zh.md 这个发布链接和 https://github.com/joinwell52-AI/FCoP/tree/main 不同步!

诊断后 Rule 0.c 校实结论(逐条带出处):

| 项 | 当前事实 | 顶级 README 头部 |
|---|---|---|
| `src/fcop/_version.py` | `__version__ = "2.0.0"` | — |
| `mcp/src/fcop_mcp/_version.py` | `__version__ = "2.0.0"` | — |
| Git 最新 tag | `v2.0.0`(`git describe --tags --abbrev=0`) | — |
| MCP 工具实际数量 | **35**(`mcp/src/fcop_mcp/server.py` 中 `^@mcp\.tool` 命中 35 次) | `(32)` / `（32 个）` ← 落后 |
| 发布徽章 | 应为 `2.0.0` | `release-1.3.0` (en) / `发布-1.2.1` (zh) ← 落后 |
| 中文 L279 "当前发布" | `v1.2.1` | 应为 `v2.0.0` |
| 中文表 L195 | 仅到 `1.2.1`,缺 `1.3 / 1.4 / 1.5 / 1.6 / 2.0.0` | 必须补 |
| 英文表 L211/212 | 仅到 `1.3.0 / 1.2.1`,缺 `1.4 / 1.5 / 1.6 / 2.0.0` | 必须补 |
| `mcp/README.md` L12 / L14 | `v1.3.0 is the latest stable release` | 应为 `v2.0.0` |

也就是说,**不是 README.zh.md ↔ README.md 互相不同步,是两份 README 加上 mcp/README.md 都还停在 v1.3 时代**——GitHub `tree/main` 默认渲染英文 README,头部徽章 1.3.0 + MCP Tools (32),看上去像没发 2.0.0。

## 要求

1. 顶级两份 README 头部徽章 + MCP 工具数刷到 v2.0.0 / 35。
2. `README.md` "Recent releases" 表补 `v2.0.0 / v1.6.0 / v1.5.0 / v1.4.0` 四行(`v1.3.0 / v1.2.1` 保留为历史条目)。
3. `README.zh.md` "近期发版" 表对应补五行(`v2.0.0 / v1.6.0 / v1.5.0 / v1.4.0 / v1.3.0`)、L279 "当前发布" 改 `v2.0.0` + 一句话归纳后续版本要点。
4. `mcp/README.md` L12 / L14 重写 "latest stable release" 段:把 v2.0.0 设为最新,旧版本逐行降级为历史。
5. `spec-v1.1` 徽章 **保留不动** —— spec freeze 是协议层语义,v2.0.0 per ADR-0003 additive,**没有 spec bump**。
6. commit 一次,push origin/main,GitHub `tree/main` 上的默认渲染立即指向 v2.0.0。

## 验收

- `git grep -n "release-1\.3\.0\|%E5%8F%91%E5%B8%83-1\.2\.1\|MCP Tools (32)\|MCP 工具清单（32 个）\|当前发布[^v]*v1\."` 返回空。
- GitHub `tree/main` 上头部徽章显示 `release-2.0.0` + `MCP Tools (35)`。
- `mcp/README.md` 头段 `v2.0.0` 出现且为 "latest stable release"。

## 非范围

- `docs/index.html`(GitHub Pages)的全面 v2.0.0 改版属于另一个待办,本 TASK **不**收尾它(脏在工作树里,留作下一个 TASK)。
- PyPI 上 `fcop-mcp 2.0.0` 包的 long_description 仍是发版时的 v1.3 文案——PyPI 不允许同号重发,只能下次发版时同步,本 TASK **不**处理(会在 REPORT 里以"未验证可改"诚实落记)。

## 引用

- ADMIN 当面反馈(本会话 2026-05-13T20:18+08:00)
- 上传现场快照:`uploads/README.zh-0.md`(GitHub raw README.zh.md)、`uploads/main-1.md`(GitHub tree/main 渲染)
- `CHANGELOG.md` L11 (v2.0.0 段)、L162 (v1.6.0)、L276 (v1.5.0)、L333 (v1.4.0)、L389 (v1.3.0)
