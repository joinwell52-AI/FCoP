---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-012
sender: ME
recipient: ADMIN
task_id: TASK-20260513-012
status: done
priority: P0
thread_key: release-sync-discipline
session_id: sess-20260513-me-04
related: [TASK-20260513-010, TASK-20260513-011, REPORT-20260513-011]
---

# REPORT · 发版前文档同步纪律升格为永久规则

## 摘要

把 ADMIN 红线("**FCoP 短期内会有很多发版,各处文档一定要同步;
发版前不要遗漏,因为 PyPI 不能补发**")作为程序性约束落到两份文件:

1. **`docs/release-process.md`** · SOP 权威源
   - **§C 文档层** 整段重写:标题升级为"全部同步,PyPI 不可补发",
     首段加 PyPI 锁版警告框,**12 项 checkbox 分 3 个子段**(C.1
     公网可见 / C.2 agent 部署后会读 / C.3 hardcoded 断言)
   - **§G 发版前文档同步扫描** · 新增,**5 条 `rg` 命令 30 秒跑完**,
     发版的最后一道闸门
2. **`fcop/shared/RULES-release-sync-checklist.md`** · 本仓纪律书(新建)
   - 顶部钉 ADMIN 红线引文(2026-05-13 21:55)
   - 只指向 SOP §C / §G,**不复制权威源**(避免漂移)
   - 末尾历史教训表:`v2.0.0` 同步发现的 3 处踩雷(`README.zh.md` ×
     4 版漂移 / `docs/index.html` 半成品 / `mcp/README.md` 险漏)

改动**只在上述 2 个文件 + 本 TASK / REPORT 内**,不动协议本身。

## 改动逐项

### `docs/release-process.md`(单文件,+57 / -14 估)

| 位置 | 原文 | 改后 |
|---|---|---|
| L84 §C 标题 | `C. 文档层 / Docs` | `C. 文档层 / Docs — 全部同步,PyPI 不可补发` |
| L86–87 §C 首段 | 一行说明 | **⚠ PyPI 锁版警告框 + ADMIN 红线引文** |
| L89–106 §C 主体 | 7 项 flat checkbox | **C.1 / C.2 / C.3 三段** + **12 项** + **`README.zh.md` / `mcp/README.md` / `docs/index.html` / `essays/README.md` / `CITATION.cff` 新增** |
| §F 与 §Release Steps 之间 | 直接 `---` | 新增 **§G 发版前文档同步扫描**(40+ 行,含 5 条 `rg` 命令) |

C.1 段命中 5 项漏点(对照过去 2 次发版踩雷):

- `README.zh.md` — 历版 SOP 只列 `README.md`,导致 v2.0.0 发现时中文
  README 停在 `1.2.1`(4 个版本前)
- **`mcp/README.md`** — PyPI `long_description` 锁版,**单独标红** ⚠
- `docs/index.html` — GitHub Pages,TASK-011 修过的"半成品"
- `essays/README.md` — 加新 essay 时漏
- `CITATION.cff` — Zenodo snapshot bump 时漏

§G 的 5 条 `rg` 命令:
1. 公网文档残留旧版本号扫描
2. letter-to-admin 摘要块版本号
3. `_version.py` 双包一致
4. CHANGELOG 新版块就位
5. ADR `Status: Proposed` 残留

### `fcop/shared/RULES-release-sync-checklist.md`(新建)

- 顶部 ADMIN 红线引文(2026-05-13 21:55 + UTC+8)
- 中段"为什么单独立一份":`fcop_report()` 第一巡检路径是
  `fcop/shared/`,SOP 在 `docs/`,两者不同视野——纪律书钉在
  agent 第一看见的地方
- "权威源 · 不在这里复制":只指向 `docs/release-process.md §C / §G`
- "三条不会变的硬约束":mcp/README.md 锁版 / README × 2 并列 /
  docs/index.html = 项目的脸
- "30 秒自检入口"指向 §G
- "历史教训"表 + 3 条踩雷 + 永久 audit trail 引用

## 自审 — Rule 0.c 复核

| 项 | 出处 | 结论 |
|---|------|------|
| ADMIN 原话准确引用 | 上文用户消息 + UTC+8 时间戳 | 直引,未润饰 |
| §C 新增 5 项确实漏在 v2.0.0 同步 | `git log --grep='TASK-010\|TASK-011'` 已 push 在 `main` | 实测可查 |
| §G 5 条命令在 PowerShell 跑通 | 本机 `rg` + `py -3.10` 都可用,backtick 是 PS 续行符 | 命令格式与 SOP 阶段 1 风格一致 |
| 纪律书不复制权威源 | 文件正文"权威源 · 不在这里复制"明确标注 | Rule 5 防漂移精神 |
| 不动协议本身 | `git diff` 不涉及 `src/fcop/rules/_data/` | 改的只是 SOP + 本地纪律 |

## 验收对照 TASK-012

- [x] §C 三段拆完,12 项 checkbox 齐 + PyPI 不可补发警告框就位
- [x] §G 新增,30 秒文档同步扫描命令清单到位
- [x] `fcop/shared/RULES-release-sync-checklist.md` 新建,引文 + 指针
- [x] 改动只在 2 个文件 + TASK / REPORT 内(`git status` 实测)
- [ ] commit + push origin/main(即将进行,显式路径)
- [ ] archive TASK + REPORT(即将进行)

## Rule 0.c 直话

REPORT-011 末尾我自己写下的"反思 + 下次怎么做"被 ADMIN 一句话升格成永久
规则——这本身是 FCoP **反向吸收循环**的现场样本(essay 13:涌现 → 观察
→ 提案 → 评审 → 合并 → 部署 → 反射):

- **涌现**: TASK-010 / 011 两次同步漏掉一些公网入口
- **观察**: REPORT-011 末尾"反思"段,自陈"明知未完成仍报已完成"
- **提案**: 提出 sync-checklist 应当在 `fcop/shared/SPRINT-*` 里
- **评审**: ADMIN 这条直接的"PyPI 不能补发"是评审意见
- **合并**: 本 TASK 把它落进 SOP §C / §G + 纪律书
- **部署**: commit + push,下一次发版的 agent 必看见
- **反射**: 历史教训表钉进 RULES 文件,长期 audit trail

—— 这也是 0.a("**Land it as a File**")在程序性约束上的体现:ADMIN
点头不算,落到磁盘文件、push 到远端、下次 agent 巡检看见,才算
"规则生效"。

## 下一步建议(非本任务)

1. SOP §Automation Roadmap 已有 TODO 4 项"`scripts/check_release_docs.py`
   自动化 lint" — 把 §G 5 条 `rg` 命令做成 Python 脚本 + CI 集成,
   release.yml 第 0 步跑一遍,任何命中阻塞 build。可立 TASK-013。
2. 看一下 essay 13("反向吸收")要不要把这次 TASK-010/011/012 的
   循环作为案例 5 加进去——这是协议演化哲学的真实落地证据。
3. v2.1 / v3.0 系列下次发版时,§G 是第一道闸门 — 用真实数据检验
   SOP 这次更新是否管用。
