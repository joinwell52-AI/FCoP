---
protocol: fcop
version: 1
sender: ADMIN
recipient: ME
priority: P1
thread_key: readme-3.0-sync-20260522
subject: README 3.0 同步整改 (batch-remediation)
---

## 背景

ADMIN 授权批量整改 README 与 README.zh.md，把版本同步到 v3.0.1。

## 授权

- scope: batch-remediation
- files: [README.md, README.zh.md]
- batch_id: readme-3.0-sync-20260522

## 要做的事

1. 修改 README.md 与 README.zh.md 头部 badge `release-3.0.0` → `release-3.0.1`
2. "Recent releases" / "近期发版" 表格在最顶上插入 v3.0.1 与 v3.0.0 两行
3. "Current release" / "当前发布" 段从 v2.0.2 改写为 v3.0.1（一句话摘要 + 提 v3.0.0 "文件夹即状态"纪元）
4. "Earlier releases" 列表把 v2.0.2 / v2.0.0 加进来

## 验收

- 两份 README 顶上的 release badge 都是 3.0.1
- 两份 README 的 "Recent releases" / "近期发版" 表都有 3.0.1 + 3.0.0 行（指 CHANGELOG）
- "Current release" / "当前发布" 段反映 3.0.1 而非 2.0.2
- 不动 essays / 仓库结构 / 设计原则等无关章节
- 改动只限 batch 授权清单内的 2 个文件

## 引用

- CHANGELOG.md L11 (3.0.1 path-consolidation patch)
- CHANGELOG.md L47 (3.0.0 protocol-level MAJOR)
- 上一次 fcop_report() 输出确认 fcop / fcop-mcp 均为 3.0.1，rules / protocol 均为 3.0.0

## 上一会话交班说明

ADMIN 在 2026-05-22 11:47 隐式确认 "sess-20260513-me-05 已结束，ME 交班给本会话" —— 凭 "开始啊" 一句加 11:34 的 double-bind proposal 上下文推出。proposal 已落 .fcop/proposals/double-bind-20260522-1134.md。