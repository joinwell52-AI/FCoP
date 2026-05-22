---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P2
references:
- TASK-20260522-001
status: done
---

## 完成项 / Done

按 batch-remediation 授权清单(`README.md` + `README.zh.md`)完成 4 项改动:

### 1. 头部 release badge
- `README.md` L34: `release-3.0.0` → `release-3.0.1`
- `README.zh.md` L34: 已是 `发布-3.0.1`(上次会话已落,验证 OK)

### 2. "近期发版" / "Recent releases" 表格
- 两份 README 在 v2.0.2 行**上方**插入两行: **v3.0.1**(路径整合补丁) + **v3.0.0**(协议级 MAJOR ·"文件夹即状态"纪元)
- 一句话摘要从 CHANGELOG.md L11 (3.0.1) + L47 (3.0.0) 收回,带链接到 `spec/fcop-3.0-spec.md` / `docs/MIGRATION-3.0.md` / `adr/ADR-0040-*.md`

### 3. "当前发布" / "Current release" 段
- 从 v2.0.2 重写为 v3.0.1,提到 v3.0.0 "文件夹即状态"纪元作为前置主版本
- 早期发布列表把 v2.0.2 + v2.0.0 加进来

### 4. 验收
- `Grep release-3\.0\.1|发布-3\.0\.1|\*\*3\.0\.1\*\*|v3\.0\.1` 在 README.md 命中 4 处, README.zh.md 命中 3 处 ✓
- 不动 essays / 仓库结构 / 设计原则等无关章节 ✓
- 改动只限 batch 授权清单内的 2 个文件 ✓

## 引用 / Citations
- `CHANGELOG.md` L11 (`## [3.0.1] — 2026-05-21 (Path-consolidation patch)`)
- `CHANGELOG.md` L47 (`## [3.0.0] — 2026-05-21 (Protocol-level MAJOR · "文件夹即状态"纪元)`)
- `fcop_report()` 输出: `fcop / fcop-mcp` 均为 3.0.1, `fcop_rules / fcop_protocol` 均为 3.0.0

## 上一会话双绑定 proposal
- `.fcop/proposals/double-bind-20260522-1134.md` 已落盘,本会话凭 ADMIN "开始啊" 隐式选 "交班" 完成 BOUND 转换

## 下一步 / Next
- 等 ADMIN 复核两份 README 的呈现效果
- 若 OK,可考虑后续 commit (本会话不主动 commit)