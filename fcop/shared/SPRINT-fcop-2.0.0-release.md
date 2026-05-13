---
protocol: fcop
version: 1
kind: sprint-plan
sprint_id: SPRINT-fcop-2.0.0-release
sender: ME
audience: ADMIN
status: in_progress
created_at: "2026-05-13T13:30:00+08:00"
related:
  - adr/ADR-0034-fcop-internal-external-document-convention.md
  - docs/release-process.md
  - fcop/log/tasks/TASK-20260512-009-ADMIN-to-ME-release-1-6-0-full-pipeline.md
---

# SPRINT-fcop-2.0.0-release · fcop / fcop-mcp 2.0.0 哲学双图时代发版规划

> **本文件是 sprint 透明工作计划**。ADMIN 2026-05-13T13:06 一句"我想全部完成,
> 然后升级为 2.0.0"已经构成 sprint 启动信号——本 SPRINT 进入 in_progress
> 状态,C1-C12 边落 commit 边推送,ADMIN 通过 commit history 实时审计。
> §6 决策点 5 项用本文档的"推荐"作为 default;ADMIN 中途如要改,可随时
> 追加修订 commit。
>
> **Rule 7 守门点(D2)是唯一的强同步点**——dry-run pass 后 agent 必须
> 停手,等 ADMIN 在聊天里再发一句明确指令(如"push tag"/"PyPI 发布吧")
> 才进 D3 真实 release。

## 0. 一句话

把 ADR-0034 v2.1.1 Accepted 后的 architectural 协议升级,加上**"双图哲学时代"
的版本叙事**,通过 `fcop` / `fcop-mcp` 1.6.0 → **2.0.0** MAJOR bump 一次性落地。

## 1. 版本叙事 / Version Narrative

| 触发 | 版本号选择 | 理由 |
|---|---|---|
| ADMIN 13:06 决策"我想全部完成,然后升级为 2.0.0" | **fcop / fcop-mcp 1.6.0 → 2.0.0** | MAJOR — 哲学双图时代里程碑(执行哲学 + 演化哲学双图对偶,见 ADR-0034 §2.5.6) |
| 协议规则同步升级 | **rules 2.4.0 → 3.0.0** + **protocol commentary 2.4.0 → 3.0.0** | 与库 MAJOR 平行,反映"双图入协议"是规则层级的根本扩展(七大核心概念表新增可视化资产层) |
| SemVer 严格性 | **MAJOR 表叙事里程碑,非技术 BREAKING** | 参照 v1.0.0 先例(per ADR-0003 §1.x SemVer §MINOR additive,v1.0 即声明"additive expansion of the contract");本次 v2.0.0 同源——所有 API 向后兼容,内部默认行为不变 |

**重要**:CHANGELOG.md 必须显式标注"**No API breaking change despite the
MAJOR bump**"以免 PyPI 用户误以为有 breaking,这与 v1.0 的处理方式一致。

## 2. 范围 / Scope

C 阶段 12 sub-changes,严格映射到 ADR-0034 §5.2 中期升级清单(版本号按当前
baseline 重算):

| # | 改动项 | 文件路径 | 提交单元 | 备注 |
|---|---|---|---|---|
| C1 | Rule 4.6 · `fcop/internal/` 桶规范(non-mandatory)新增 | `src/fcop/rules/fcop-rules.mdc` | C-rules | rules 2.4.0 → 3.0.0;Rule 4.6 子段含 ADR-0034 §4.1-4.5 全部词汇 |
| C2 | 第二张哲学图 · FCoP Semantic Evolution Loop 入"七大核心概念"表 | 同上 | C-rules | 严格原文吸收 ADR-0034 §2.5.6 钦定 ASCII 图 + 三句 Core Principle 中英双语,**不得**改一字 |
| C3 | §Internal/External Document Convention commentary 追加 | `src/fcop/rules/fcop-protocol.mdc` | C-protocol | protocol 2.4.0 → 3.0.0 |
| C4 | §双图对偶(执行 vs 演化)commentary 追加 | 同上 | C-protocol | 同上 |
| C5 | `Project.init(deploy_internal_template: bool = False)` opt-in 参数 | `src/fcop/project.py` | C-lib | opt-in,默认不创建,既有用户零影响 |
| C6 | `INTERNAL-README.md` 模板新增(含 ADR-0034 §4.3 声明语法 v1) | `src/fcop/templates/INTERNAL-README.md`(新文件) | C-lib | 由 C5 在 `deploy_internal_template=True` 时落到 `fcop/internal/` |
| C7 | `internal-only` 声明语法节加入 4 团队 OPERATING-RULES | `src/fcop/templates/teams/<team>/TEAM-OPERATING-RULES.{md,en.md}` × 4 = 8 文件 | C-templates | dev-team / media-team / mvp-team / qa-team |
| C8 | `internal-only` 声明检查(P3 non-blocking) | `src/fcop/audit.py` | C-lib | 不存在或缺字段不阻断,只 warn |
| C9 | `_version.py × 2` bump + AGENTS.md / CLAUDE.md 重新生成 + `.cursor/rules/*.mdc` 镜像同步 | `src/fcop/_version.py`、`mcp/src/fcop_mcp/_version.py`、`AGENTS.md`、`CLAUDE.md`、`.cursor/rules/fcop-rules.mdc`、`.cursor/rules/fcop-protocol.mdc` | C-bump | 1.6.0 → 2.0.0;镜像通过 `redeploy_rules()` 等价的脚本生成 |
| C10 | CHANGELOG.md 加 [2.0.0] 段(BREAKING / Added / Changed / Notes 风格) | `CHANGELOG.md` | C-changelog | 显式标"No API breaking" |
| C11 | unit tests 新增 + 1061+ 旧 test 全过(0 回归)+ ruff/mypy/pip_audit 全清 | `tests/` | C-tests | 至少 4 类新 test:internal-only parser、`Project.init` opt-in、audit 新检查、rules-version drift |
| C12 | README + LETTER-TO-ADMIN(zh/en)版本号 sync + ADR 索引补 ADR-0034 Accepted 行 | `README.md`、`README.zh.md`、`src/fcop/templates/LETTER-TO-ADMIN.{md,en.md}`、`adr/README.md`(若存在) | C-docs | 文档层级同步 |

D 阶段(release 触发):

| # | 动作 | 谁 | 备注 |
|---|---|---|---|
| D1 | dry-run + 本地全测(走 `docs/release-process.md` v2 one-pass 模式) | ME | 不动 git tag |
| **D2** | **⚠️ Rule 7 守门点 · STOP** | **等 ADMIN** | dry-run pass 后 agent 停手,ADMIN 确认 PyPI 发布 + 主干 tag push 才进 D3 |
| D3 | tag v2.0.0 + push 触发 GitHub Actions release.yml(5 jobs) | ME(ADMIN 二次确认后) | 沿用 v1.6.0 SOP |
| D4 | 验证 PyPI(`pypi.org/pypi/fcop/json` + `fcop-mcp/json`)+ GitHub Release v2.0.0 + 4 assets | ME | 自动等 5/5 jobs success |

E 阶段(release 后):

| # | 动作 | 谁 | 备注 |
|---|---|---|---|
| E1 | 本仓 + Bridgeflow + codeflow 调 `redeploy_rules()` | **仅 ADMIN**(Rule 8 + ADR-0006) | agent 不自调 |
| E2 | ADR-0034 Status: Accepted → Implemented + commit | ME | release 完才升 |
| E3 | 写 REPORT-008(整个 sprint 闭环报告)+ archive TASK-008 + commit | ME | 闭环 |

## 3. 提交策略 / Commit Strategy

按"逻辑单元一 commit"原则,预计 5-7 个 commit 完成 C-D-E:

| commit 编号 | 内容 | 包含 sub-change |
|---|---|---|
| (本 sprint 内已落) | A 阶段 4 步循环收尾 + B 阶段 ADR-0034 Accepted | 已 push:`92980c7`、`cbe6adb` |
| sprint-init | 落 SPRINT 文档 + TASK-008 | 本 commit + 下一 commit |
| C-rules | C1 + C2 | `src/fcop/rules/fcop-rules.mdc` |
| C-protocol | C3 + C4 | `src/fcop/rules/fcop-protocol.mdc` |
| C-lib + C-templates | C5 + C6 + C7 + C8 | python lib + 8 模板文件 |
| C-bump + C-docs + C-changelog | C9 + C10 + C12 | 版本号 sync + 镜像 + 文档 |
| C-tests | C11 | tests + 全测 pass |
| (D 阶段)release-tag | tag v2.0.0(ADMIN 二次确认后) | — |
| (E 阶段)post-release | E2 + E3 | ADR Status + REPORT-008 |

## 4. Rule 7 守门点 / Rule 7 Gate

**Rule 7 高危范围明确包括"发布到公网制品仓库(PyPI)"+"推送到主干分支"。**

本 sprint 的 D2 是 Rule 7 守门点:

```
                                      ┌─────────────────────────┐
                                      │  ⚠️ STOP — Rule 7 gate  │
   C12 finished + dry-run pass ─────► │  ADMIN second confirm   │ ────► D3 tag push
                                      │  required for PyPI +    │
                                      │  main-branch tag push   │
                                      └─────────────────────────┘
```

ADMIN 二次确认的形式:在聊天里给一句明确指令(参照 v1.6.0 sprint
commit `7c23c4a` 时的实际做法),例如:

- "OK 现在 push tag"
- "PyPI 发布吧"
- "走 release"

任一句即可。**ADMIN 13:06 那条"全部完成,升级 2.0.0"是 sprint 启动指令,
不构成 D2 二次确认**(Rule 7 要求 destruction-class 动作分两次确认,
sprint 启动是第一次,PyPI 发布是第二次)。

## 5. 风险评估 / Risk

| 风险 | 等级 | 缓解 |
|---|---|---|
| C2 第二张哲学图 ASCII 在 Markdown 渲染失真 | 低 | 复用 ADR-0034 §2.5.6 已 vettied 的 ASCII 块,本仓内同 ADR 渲染正常即不变样;v1.6.0 sprint 已验证 ASCII 图在 GitHub render 无问题 |
| C9 镜像 4 件套(`.cursor/*.mdc` + `AGENTS.md` + `CLAUDE.md`)字节对齐失败 | 中 | 沿用 fcop 包 `Project.deploy_protocol_rules()` 程序化生成,不手抄;commit 前 `git diff --stat` 校验 4 文件长度比例一致 |
| C11 旧 test 回归 | 中 | 每个子 commit 跑 `pytest -x` 一次;C5/C6/C7/C8 引入新行为应保证既有行为不变(opt-in 默认 False) |
| D3 tag push 后 GitHub Actions 失败 | 低 | v1.6.0 SOP v2 已在 `docs/release-process.md` §6 列出 5/5 jobs 的失败处理；问题对策已沉淀 |
| MAJOR bump 让 PyPI 用户误判 | 中 | CHANGELOG.md 显式标"No API breaking change despite MAJOR bump",参照 v1.0.0 先例 |
| 协议规则升级与下游(Bridgeflow / codeflow)兼容性 | 低 | rules 3.0.0 仅**新增** Rule 4.6 + 第二张图,既有 Rule 0-9 全部不变;下游执行 `redeploy_rules()` 可滚动升级 |

## 6. 决策点清单 / Decisions Awaiting ADMIN

ADMIN review 本 SPRINT 文档时**需明确表态**的 5 项:

1. **rules / protocol commentary 的版本号选择**
   - 推荐:`rules 2.4.0 → 3.0.0` + `protocol 2.4.0 → 3.0.0`(本文档默认)
   - 备选:`rules 2.4.0 → 2.5.0` + `protocol 2.4.0 → 2.5.0`(ADR-0034 §5.2 草稿期数字,但 baseline 已变)
   - 备选 2:`rules 2.4.0 → 2.5.0`,`protocol 2.4.0 → 3.0.0`(库 MAJOR + rules MINOR 的混合叙事)

2. **第二张哲学图 ASCII 落 `fcop-rules.mdc` 的位置**
   - 推荐:"七大核心概念"小节末尾(紧接七概念表后),与 line 54-72 既有"协议三层 stack 图"形成视觉对偶
   - 备选:新建"FCoP 双图对偶"独立子节,放在七大核心概念之后

3. **C7 团队模板 `internal-only` 声明语法节的位置**
   - 推荐:加在每个 team 的 `TEAM-OPERATING-RULES.md` 末尾,作为 §选用条目(opt-in)
   - 备选:仅在 Bridgeflow/codeflow 涉及自诊档案的团队加(`dev-team` + `qa-team` 两份)

4. **CHANGELOG.md [2.0.0] 段标题语气**
   - 推荐:`## [2.0.0] — 2026-05-XX · The Two-Diagram Era / 双图哲学时代`
   - 备选:`## [2.0.0] — 2026-05-XX · ADR-0034 Implementation / ADR-0034 实施`

5. **ADR-0034 §5.2 数字现已与 baseline 不一致(草稿期写 rules 2.3.0,实际 baseline 2.4.0)**
   - 推荐:在 sprint 闭环时(E2 阶段)同步刷新 §5.2 数字,使其与实际落地一致(Rule 0.c)
   - 备选:留 §5.2 历史快照不动,在 §10.6 status transition log 里加一行"sprint actual vs §5.2 draft 偏差注释"

## 7. 不在本 sprint 范围 / Out of Scope

- ✗ 候选 ADR-0035(反向吸收作为第八核心概念)+ ADR-0036(六步路径形式化)+ ADR-0037(双图入协议作为独立 ADR)
  → 这些是 ADR-0034 §10.5 列的 **Follow-up 候选**,本 sprint 仅落 ADR-0034 §5.2 中期清单,Follow-up 等下次 sprint
  → 注:本 sprint **已包含** §5.2 中期清单的"第二张哲学图入 fcop-rules.mdc",所以 ADR-0037 候选实质上被本 sprint **吸收**了——下次 sprint 只需 ADR-0035 + ADR-0036
- ✗ Bridgeflow / codeflow 仓的 `redeploy_rules()` 调用 → ADMIN 自调(E1)
- ✗ 任何 release-process.md SOP 修订 → SOP 已 v2,本 sprint 不动
- ✗ workspace/ 路径或 Rule 7.5 的修订 → 本 sprint 不动

## 8. 启动条件 / Sprint Kickoff Conditions

**已启动**:ADMIN 2026-05-13T13:06 dispatch"我想全部完成,然后升级为 2.0.0"
构成 sprint 启动信号(REPORT-20260513-006 §4 已记录)。本 SPRINT 进入
in_progress,C1-C12 立即开干。

**仅有的强同步点**:**D2 Rule 7 守门**——dry-run pass 后 agent 停手,
等 ADMIN 二次确认 PyPI 发布 + 主干 tag push 才进 D3。任何中途若 ADMIN 在
聊天里给出修订意见(如"决策点 #1 我要选备选 2"),agent 立即追加修订
commit(Rule 5 append-only,绝不动 history)。

## 9. 时间预估 / Time Estimate

| 阶段 | 预估工作量 | 备注 |
|---|---|---|
| C1+C2 | 90 min | 协议规则文件最 sensitive,逐字落 |
| C3+C4 | 60 min | commentary 篇幅适中 |
| C5+C6+C7+C8 | 120 min | python lib 改动 + 8 模板文件 |
| C9+C12 | 30 min | bump + 镜像生成由脚本完成 |
| C10 | 20 min | CHANGELOG 段 |
| C11 | 90 min | tests + 全测验证 |
| D1 | 30 min | dry-run pass |
| D2 守门点 | 等 ADMIN | 不计 |
| D3+D4 | 30 min | tag push + 验证 |
| E2+E3 | 30 min | 闭环 |
| **总计** | **~8-9 小时**(不含等 ADMIN 决策时间) | 一次冲刺;若分多次,以 commit 边界为切片 |

## 10. References

- `adr/ADR-0034-fcop-internal-external-document-convention.md`(本 sprint 协议输入)
- `docs/release-process.md` v2(本 sprint 操作 SOP)
- `fcop/log/tasks/TASK-20260512-009-ADMIN-to-ME-release-1-6-0-full-pipeline.md`(v1.6.0 sprint 经验,可对照)
- `fcop/log/reports/REPORT-20260513-006-ME-to-ADMIN.md`(本 sprint 上游 ADR 草稿期闭环)
- `fcop/log/reports/REPORT-20260512-008-ME-to-ADMIN-adr-0033-sprint-commit.md`(ADR-0033 落地经验)

---

**等待 ADMIN 过基线**。
