---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260513-001
sender: ADMIN
recipient: ME
priority: P1
risk_level: low
thread_key: release-sop-v2
session_id: sess-20260513-me-01
created_at: "2026-05-13T00:55:00+08:00"
related:
  - TASK-20260512-009  # v1.6.0 一条龙发版主刀任务(已归档)
  - REPORT-20260512-009
---

# 沉淀 v1.6.0 一条龙发版经验为标准发版 SOP

## 背景 / Background

ADMIN 在 v1.6.0 发版闭环后明确指令:

> 非常好,以后发版按这个来!

`v1.6.0` 是 FCoP **第一次完整跑通"一条龙发版"**——从 ADR-0033 起草、代码实现、
文档同步、P=E 对齐、GitHub Actions 自动发布、到 Rule 0.a.1 闭环全链路落文件可
审计。本次实际执行流程**比 `docs/release-process.md` 现有 SOP 多出 9 处实战经
验**,且现有 SOP 的版本号示例还停留在 `0.6.0rc1` 时代,与 1.x SemVer 阶段不符。

本任务把这 9 处经验吸收回 `docs/release-process.md`,让下次发版有可复用的 SOP
v2,不再依赖某个人的记忆。

## 现有 SOP 与实战的 9 处差异 / 9 Gaps

| # | 项 | 现状 (release-process.md) | 实战 (v1.6.0) |
|---|---|---|---|
| 1 | 版本号示例 | 全文 `0.6.0rc1` | 应升级到 `1.x.y` 形式 |
| 2 | mcp 依赖约束 | `fcop>=A.B,<A.(B+1)` (MINOR 锁) | 实际是 `fcop>=1.0,<2.0` (MAJOR 锁,符合 1.x SemVer) |
| 3 | lint/mypy 范围 | "全绿" 一刀切 | 应明确 `src tests mcp/src` 是 release-gate;`scripts/` 历史 lint 不阻塞 |
| 4 | **P=E 同步前置** | 缺 | `redeploy_rules()` 或 `Project.deploy_protocol_rules(force=True)` 必须在 tag 前跑;否则 `.cursor/rules/*.mdc` + `AGENTS.md` + `CLAUDE.md` 会落后 |
| 5 | **文档版本号漂移检查** | 缺 | `README.md` "Current release"、`letter-to-admin.{zh,en}.md` 摘要块、`tests/test_fcop/test_rules.py` 硬断言 — 三个点必查 |
| 6 | **Rule 0.a.1 闭环** | 缺 | 发版载体 `TASK-*-release-x-y-z.md` + 配套 `REPORT-*` + archive 是发版的强制 deliverable,不是可选 |
| 7 | **MCP server 跑旧 wheel 时的应对** | 缺 | 若 `fcop_report()` 显示 MCP server 跑的是旧 `fcop@X.Y.Z`、本地源码已是新版,直接调 Python API `Project(...).deploy_protocol_rules()` 绕过 MCP 工具 |
| 8 | **PyPI CDN 传播延迟** | 缺 | `release.yml` 成功后,`pip install` 公网可能要等几分钟;PyPI JSON API 比 `pip` 索引更早可见 |
| 9 | **GitHub Actions Node 20 弃用** | 缺 | 2026-06-02 前升级 `actions/checkout@v4` 等到 Node24 兼容版,否则未来 CI 会红 |

## 要做的事 / Deliverables

1. 改写 `docs/release-process.md`:
   - 版本号示例统一升到 `1.x.y` (用 `v1.6.0` / 假想下次 `v1.7.0` 作示例)
   - "核心约束" 段保留,但 ADR-0003 SemVer 子段去掉 0.6.N 残留措辞
   - "发布前检查清单" 4 段(A/B/C/D)**重写**:
     - A. 代码层 — 加 MAJOR 锁说明 + `_version.py` 双包对齐
     - B. 测试 & CI — **明确 release-gate 范围**(`src tests mcp/src`),`scripts/` 标为"非阻塞"
     - C. 文档层 — **新增三连**:`README.md` Current release / `letter-to-admin.{zh,en}.md` 摘要块 / `tests/test_fcop/test_rules.py` 硬断言
     - D. Git — 不变
   - **新增 段**:`P=E 同步(发 tag 前最后一步)` — 讲 `redeploy_rules()` 和 Python API 两条路径
   - **新增 段**:`Rule 0.a.1 闭环作为发版交付物` — TASK/REPORT/archive 三件套
   - "发布步骤" 段重写:阶段 1 本地 build + smoke / 阶段 2 (RC 才走 TestPyPI) / 阶段 3 push tag 触发 `release.yml` / 阶段 4 闭环
   - "发布后验证" 段:加 PyPI CDN 传播延迟说明 + PyPI JSON API 比 pip 索引更早可见的事实
   - "常见故障与回滚" 段:加"MCP server 跑旧版怎么办" + "release.yml Node 20 弃用"两条
2. 不动 `CHANGELOG.md` 的语义内容(只在改 SOP 时附一段元信息说本次只是 docs)
3. 不发新版本号(本次只改文档,不改 `_version.py`)

## 验收 / Acceptance

- [ ] `docs/release-process.md` 不再出现 `0.6.0rc1` 或 `0.6.N` 字样作为示例(可在历史段落保留)
- [ ] 9 处差异全部落到文件,每条都有可执行步骤(命令 / 文件路径 / 验证方法)
- [ ] 新文件能在不读本 TASK 的情况下被下次发版独立看懂
- [ ] `git status` 干净后 commit + push origin main
- [ ] 写 `REPORT-20260513-001-ME-to-ADMIN-release-sop-v2-after-1-6-0.md` 总结
- [ ] TASK + REPORT 一起 archive 到 `fcop/log/`,Rule 0.a.1 闭环

## 风险与回滚 / Risk & Rollback

- **风险等级 low**:本任务只改 `docs/release-process.md` 一份维护者文档,不动
  代码、不动协议规则、不发新版本号。如下次发版按新 SOP 走出问题,回滚只需
  `git revert <commit>` 即可恢复旧版 SOP。
- 不触发 `write_task` 的 v1.1 `needs_human` 流程(low risk)。
- 不属于 Rule 7 高危动作(无网络 / 防火墙 / 删除数据 / 推 main / 公网发布)。

## 备注 / Notes

本任务文件名本身演示 ADR-0033 trailing-slug 语法:
`TASK-20260513-001-ADMIN-to-ME-release-sop-v2-after-1-6-0.md`
└─ slug 段:`release-sop-v2-after-1-6-0`
