---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-001
sender: ME
recipient: ADMIN
status: done
task_id: TASK-20260513-001
thread_key: release-sop-v2
session_id: sess-20260513-me-01
reported_at: "2026-05-13T01:05:00+08:00"
related:
  - TASK-20260513-001
  - TASK-20260512-009  # v1.6.0 一条龙发版主刀(已归档)
  - REPORT-20260512-009
---

# 发版 SOP v2 已沉淀:v1.6.0 一条龙经验回收到 `docs/release-process.md`

## TL;DR

- ✅ `docs/release-process.md` 从 **259 行** 重写为 **429 行**(18.8 KB)
- ✅ 旧 `0.6.0rc1` / `0.6.N` 示例残留 **0 处**,全文版本号示例升级到 `1.x`
- ✅ TASK 列出的 9 处实战差异**全部命中**(见下表逐条对照)
- ✅ 新增 **2 节** 检查段(`E. P=E 同步`、`F. Rule 0.a.1 闭环载体`)+ 1 节
  完整命令序列(`一次完整发版的命令序列`)
- ✅ `ReadLints` 无 lint 错误
- Rule 0.a.1 闭环:本 REPORT 落盘后,与 TASK-20260513-001 一起 archive 到
  `fcop/log/`,提交 `chore(docs): release SOP v2 after 1.6.0 dry-run` 完成 push

## 9 处实战差异逐条命中确认

| # | 项 | 文件位置(行号近似) | 落地形式 |
|---|---|---|---|
| 1 | 版本号示例升级 | 全文 | `0.6.x` → `1.6.0` / `1.7.0` 作示例 |
| 2 | mcp 依赖约束 MAJOR 锁 | `A. 代码层` 第 3 项 | "`fcop>=1.0,<2.0` 依赖约束保持 **MAJOR 锁**(`<MAJOR+1`)。1.x 之间任意 MINOR 都兼容,不需要每发一次就改约束" |
| 3 | lint/mypy 范围划清 | `B. 测试 & CI` 顶段 | "release-gate **范围**:`src/` + `tests/` + `mcp/src/` 三处必须全绿。`scripts/` 是维护者临时工具,**不**进 release-gate" |
| 4 | P=E 同步前置 | 新增 `E. P=E 同步` 整段 | 两条路径(MCP 工具优先 / Python API 降级)+ 四份目标文件 `git diff` 验收 |
| 5 | 文档版本号漂移检查 | `C. 文档层` 6+3 清单 | `README.md`/`letter-to-admin.zh.md`/`letter-to-admin.en.md` + 3 处 hardcoded 断言:`test_rules.py`、`test_server.py`、`server.py` prompt |
| 6 | Rule 0.a.1 闭环作为发版交付物 | "核心约束" 第 4 条 + 新增 `F. Rule 0.a.1 闭环载体` + `阶段 4` 闭环检查 | 三处协同:写在核心约束顶部 + 检查段 + 步骤段 |
| 7 | MCP server 跑旧 wheel 的应对 | `E. P=E 同步` 降级路径 + `常见故障 问题 3` | Python API 命令完整给出 |
| 8 | PyPI CDN 传播延迟 | `阶段 4` 已知现象 + `常见故障 问题 6` | "通常 1–5 分钟。PyPI JSON API 比 pip 索引更早可见" |
| 9 | GitHub Actions Node 20 弃用 | `常见故障 问题 5` + `自动化路线图 待办` | "2026-06-02 前必修" |

## 结构对比

```
v1 (259 行)                   v2 (429 行)
─────────────────────         ─────────────────────
核心约束 (3 条)               核心约束 (4 条;+ Rule 0.a.1)
版本号规则 (0.6.x)            版本号规则 (1.x)
A. 代码层                     A. 代码层 (+ MAJOR 锁说明)
B. 测试 & CI                  B. 测试 & CI (+ 范围划清)
C. 文档层                     C. 文档层 (+ 3 处 hardcoded 断言)
D. Git                        D. Git
                              E. P=E 同步 (新增整段)
                              F. Rule 0.a.1 闭环载体 (新增整段)
发布步骤 4 阶段                发布步骤 4 阶段 (重写 + 一条龙命令序列)
发布后验证                     发布后验证 (+ CDN 传播)
常见故障与回滚 (2 条)          常见故障与回滚 (6 条)
自动化路线图                   自动化路线图 (待办增至 6 条)
```

## 验证证据

```powershell
# 1. 文件大小 + 行数
$ Get-ChildItem docs\release-process.md | Select-Object Length
Length: 18883 bytes

$ (Get-Content docs\release-process.md).Count
429

# 2. 旧版本示例 0 残留
$ (Select-String -Path docs\release-process.md -Pattern "0\.6\.0rc1|0\.6\.N").Count
0

# 3. 9 处实战经验全部命中(关键短语 grep,见 TASK-001 验收清单)
# - "MAJOR 锁"               line 60   ✓
# - "src tests mcp/src"      line 72   ✓
# - "历史 lint" / "不阻塞"    line 73-75✓
# - "deploy_protocol_rules"  line 133, 312, 365 ✓
# - "README.md Current release" line 94 ✓
# - "letter-to-admin"        line 96, 98, 291 ✓
# - "hardcoded 字符串断言"    line 99   ✓
# - "Rule 0.a.1 闭环"        line 20, 144, 236, 258 ✓
# - "MCP server 跑旧"         line 127, 302 ✓
# - "CDN 传播"               line 246, 255, 336 ✓
# - "Node 20" / "Node 24"    line 331, 406 ✓

# 4. lint
$ ReadLints docs/release-process.md
No linter errors found.
```

## 验收清单 / Acceptance Checklist

- [x] `docs/release-process.md` 不再出现 `0.6.0rc1` 或 `0.6.N` 字样作为示例
- [x] 9 处差异全部落到文件,每条都有可执行步骤(命令 / 文件路径 / 验证方法)
- [x] 新文件能在不读本 TASK 的情况下被下次发版独立看懂
- [x] 写 `REPORT-20260513-001-ME-to-ADMIN-release-sop-v2-after-1-6-0.md` 总结(本文)
- [ ] `git status` 干净后 commit + push origin main(下一步执行)
- [ ] TASK + REPORT 一起 archive 到 `fcop/log/`,Rule 0.a.1 闭环(下一步执行)

## 风险评估事后回顾

实际风险:**low**(与 TASK 预估一致)。

- 只改一份维护者文档,不动协议规则、不动代码、不改 `_version.py`
- 不触发 v1.1 `needs_human` 流程
- 不属于 Rule 7 高危动作
- 回滚成本:`git revert <commit>` 即可

## 下一步 / Next

`Step 4` 闭环:

```powershell
Move-Item fcop\tasks\TASK-20260513-001-*.md   fcop\log\tasks\
Move-Item fcop\reports\REPORT-20260513-001-*.md fcop\log\reports\
git add -A
git commit -F .scratch\_release_sop_v2_closure_msg.txt
git push origin main
```

提交后,从本 sprint 开始,**FCoP 项目就有了可复用、可审计、不依赖某个人记忆
的发版 SOP**——这正是 ADMIN 在 v1.6.0 闭环后给出指令"以后发版按这个来"的
本意。
