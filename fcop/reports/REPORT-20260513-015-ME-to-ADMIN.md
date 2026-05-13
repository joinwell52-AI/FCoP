---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260513-015
sender: ME
recipient: ADMIN
task_id: TASK-20260513-015
thread_key: v2-0-2-glama-badge
session_id: sess-20260513-ME-015
status: done
related:
  - REPORT-20260513-014   # stage-1 双包 lockstep 升级 v2.0.2 + MCP registry 入驻文档化
---

# Glama AI badge 入双语 README · stage-1.5 收尾

## 摘要 / Abstract

按 ADMIN 23:25 指派,把 Glama AI 收录 badge 加进 FCoP 仓库**英中双 README**,
独立 stage-1.5 commit + 三方 push(origin + backup)。同时 §G 扫描时发现两份
`letter-to-admin.*.md` 模板存在 stage-1 隐藏遗漏(摘要标题还写 v2.0.0),
本任务范围不动,**如实记录给 ADMIN 决策**(Rule 0.c)。

## 范围声明 / Scope statement

- ✅ **本仓库**(FCoP)README × 2
- ❌ **CodeFlow 仓库**(ADMIN 提到的另一个仓库)— 不归本会话/本角色管,
  须由 CodeFlow 项目自己的 agent 操作

## 交付 / Deliverables

| 文件 | 改动 | 行号 |
|---|---|---|
| `README.md` | 在 MCP Registry badge 之后、Zenodo DOI 之前插入 Glama `<a><img></a>` | 42–44 |
| `README.zh.md` | 同上,alt 文案改中文("FCoP MCP 服务器 · Glama 收录") | 42–44 |
| `fcop/tasks/TASK-20260513-015-...-glama-badge-into-readme.md` | 任务文件(新建) | — |
| `fcop/reports/REPORT-20260513-015-ME-to-ADMIN.md` | 本报告 | — |

**两份 README 共改 6 行(各加 3 行 HTML)+ TASK / REPORT 各 1 份 = 总 4 文件**。

### 不改的(刻意)/ What stays untouched

| 文件 | 不改理由 |
|---|---|
| `CHANGELOG.md` | v2.0.2 段已 commit + push 到 origin/backup(`d79d438`),不回填(append-only 精神) |
| `docs/index.html` | ADMIN 字面只指派 README,不擅自扩张 |
| `mcp/README.md`(PyPI long_description) | 加 Glama 信息会形成 PyPI ↔ Glama 自指;且只在 fcop-mcp@2.0.2 上传后才生效。留 stage-2 |
| `src/fcop/rules/_data/letter-to-admin.*.md` | 详见下面【§G 扫描发现】节,不在本任务范围且属规则数据模板 |

## 验证 / Verification

### ReadLints

```
README.md            : 0 errors
README.zh.md         : 0 errors
TASK-015             : 0 errors
```

### §G 6 条扫描

| # | 项 | 命令 | 结果 |
|---|---|---|---|
| 1 | 公网文档旧版本号(2.0.0 / 2.0.1) | `rg -e '\b(2\.0\.0\|2\.0\.1)\b' README.md README.zh.md` | 命中均为 stage-1 已规划的历史叙事("unchanged from v2.0.0" / "consolidates fcop-mcp@2.0.1" / 版本表历史行),SOP 注解明确"CHANGELOG 历史段命中可忽略",此处等价 ✅ |
| 2 | letter-to-admin 版本号 | `rg -e 'fcop_protocol_version\|fcop_rules_version\|vX\.Y\.Z\|v1\.6\.0' src/fcop/rules/_data/letter-to-admin.*` | **命中** `v2.0.0` 摘要标题 + `fcop_protocol_version: 1.5.0` 史实引用 ⚠️(详见下) |
| 3 | _version.py 双包一致 | `py -3.10 -c "import fcop._version, fcop_mcp._version; ..."` | `versions aligned: 2.0.2` ✅ |
| 4 | CHANGELOG [2.0.2] 段 | `rg -e '^## \[2\.0\.2\]'` | 命中 line 11 ✅ |
| 5 | ADR Proposed | `rg -e '^Status: Proposed' adr/` | 0 命中 ✅ |
| 6 | backup remote 配置 | `git remote -v \| findstr "^backup"` | 2 行(fetch + push)✅ |

## §G 扫描发现 / §G audit finding(Rule 0.c)

**事实**:

- `src/fcop/rules/_data/letter-to-admin.zh.md:9` 写 `> **v2.0.0 摘要**(当前版本,2026-05-13)`
- `src/fcop/rules/_data/letter-to-admin.en.md:9` 写 `> **v2.0.0 summary** (current, 2026-05-13)`
- 仓库 `_version.py` 已经是 `2.0.2`(stage-1 升完)
- 两份 letter 摘要正文描述的 feature(两图对偶 / Rule 4.6 / `deploy_internal_template` 等)**在 v2.0.2 周期里没变** — 漏的只是版本号 tag

**根因**:SOP §G #2 的 grep pattern 是 `'fcop_protocol_version|fcop_rules_version|vX\.Y\.Z|v1\.6\.0'`,
跨多版本升级(1.6.0 → 2.0.2)时**中间版本号** `v2.0.0` 不在 pattern 里。所以
stage-1 §G 扫描时**报通过**,但实际有遗漏。**SOP §G 的模板盲点**。

**本任务为何不顺手修**:

1. ADMIN 字面指派只覆盖"Glama badge 入 README",letter-to-admin 不在范围(Rule 1)
2. `src/fcop/rules/_data/letter-to-admin.*.md` 是规则数据模板(由 `init_*` 工具部署到新项目的 `fcop/LETTER-TO-ADMIN.md`),与 `.cursor/rules/*.mdc` 同源,Rule 8 + ADR-0006 精神是 agent 不应自行改写规则部署源
3. 这两份的修改属于"规则数据小修",在 stage-2 commit 合并最自然

**给 ADMIN 的三选一**:

- **A.stage-2 一起补**(推荐):等 ADMIN PyPI/Zenodo/registry 三件齐活后,stage-2 final commit 一次性把 letter-to-admin 两份摘要标题升到 v2.0.2(简单字符串替换,跟 CITATION.cff 一起改)
- **B.立即独立 stage-1.6**:本会话再发一个小 commit 专修 letter-to-admin,三方 push,SHA 验证
- **C.SOP 也改**:借机把 SOP §G #2 的 pattern 扩成"扫全部历史版本号" — 这是更深的修补,要写 ADR + 更新 release-process.md

我建议 **A**(简单 + 自然 + 不增中间 commit),但 C 的 SOP 修补也确实是个值得做的"反向吸收"动作 — 这是 §G 第一次暴露自身盲点,记录下来对未来发版有价值。

## Commit & push

**stage-1.5 commit message(草稿)**:

```
docs(readme): add Glama AI MCP server badge to bilingual READMEs (stage-1.5)

ADMIN milestone 2026-05-13 23:25 +08:00:
> "fcop-mcp 已经上了 Glama.ai 的目录...你现在可以把这个 badge 加到
>  FCoP 和 CodeFlow 两个仓库的 README 里"

This commit:
- README.md: insert Glama card badge between MCP Registry and Zenodo
  DOI badges (lines 42-44)
- README.zh.md: same, with Chinese alt text "FCoP MCP 服务器 · Glama 收录"
- TASK-20260513-015 + REPORT-20260513-015: ledger for the change

Why stage-1.5 (not amend stage-1 d79d438):
- stage-1 d79d438 already pushed to origin + backup; no force-push
- Rule 5 append-only history honored
- v2.0.2 release tag still reserved for stage-2 (after ADMIN finishes
  PyPI dual-pack upload + Zenodo new snapshot + mcp-publisher publish)

Scope deliberately narrow:
- CodeFlow repo NOT touched (different project, different agent)
- mcp/README.md NOT touched (PyPI long_description, would form
  PyPI <-> Glama self-reference; defer to stage-2)
- docs/index.html NOT touched (ADMIN指派字面只覆盖 README)
- CHANGELOG.md NOT touched (v2.0.2 段已 commit/push;append-only)

§G audit surfaced a separate stage-1 oversight unrelated to this
commit: src/fcop/rules/_data/letter-to-admin.{zh,en}.md still write
"v2.0.0 summary (current)" in their abstract titles. NOT fixed here
(out of scope, regulator-template territory); flagged to ADMIN in
REPORT-015 for stage-2 absorption.

Per Rule 0.a.1 four-step cycle: task -> do -> report -> archive
(archive after this commit lands).
```

## Verification after push(待跑 / Pending)

- [ ] `git rev-parse HEAD`
- [ ] `git ls-remote origin main`
- [ ] `git ls-remote backup main`
- [ ] 三者字节一致

## 下一步 / Next

1. ADMIN 看本报告 + 选 A / B / C
2. 不论选哪个,先把 stage-1.5 这次 commit + push + SHA 验证落定
3. 之后按 ADMIN 选择执行;若选 A,letter-to-admin 升 v2.0.2 留 stage-2 final commit
