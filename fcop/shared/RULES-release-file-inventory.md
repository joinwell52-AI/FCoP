---
protocol: fcop
version: 1
kind: shared
prefix: RULES
sender: ME
recipient: TEAM
related: [TASK-20260513-013, REPORT-20260513-011, REPORT-20260513-012]
thread_key: release-sync-discipline
session_id: sess-20260513-me-05
---

# RULES · 发版涉及文件总清单 / Release File Inventory

> **Scope**: FCoP 自仓发版纪律的**物理化沉淀**,不是 FCoP 协议本身。
> 配套文件 `RULES-release-sync-checklist.md` 写"为什么、底线在哪",
> 本文件写"具体动哪些文件、怎么动、怎么验"。
>
> **Discipline level**: 按 FCoP 未来可能成为外部协作协议标准的严谨度
> 写——命名、字段、引用都允许被外部团队 / IDE 厂商 / 学术论文直接引用
> 为 `Inventory §C` / `Inventory §F.3` 等(ADMIN 红线 3,2026-05-13
> 22:32 +08:00)。
>
> **Authoritative source pointer**: `docs/release-process.md`(SOP)
> 是发版**流程**的权威源;本文件是发版**文件清单**的权威源。两份
> 在 §SOP 对应行字段交叉引用,避免漂移。

---

## 0. 三条 ADMIN 红线 / Three Lines ADMIN Drew

| 编号 | 红线 | 来源 |
|---|---|---|
| **红线 1** | "FCoP 短期内会有很多发版,各处文档一定要同步;发版前不要遗漏,因为 PyPI 不能补发。" | 2026-05-13 21:55 +08:00 + REPORT-011 |
| **红线 2** | "一条龙发版+备份!" | 2026-05-13 22:28 +08:00 + REPORT-013 |
| **红线 3** | "如果未来 FCoP 成为一种标准,我们现在要非常认真才行。" | 2026-05-13 22:32 +08:00(元红线) |

红线 3 是**态度坐标系**——本清单的每一行都按"被外部引用一次"的成本
写,不允许"差不多""大概那一段"。

---

## 1. 字段约定 / Field Convention

| 字段 | 含义 | 取值范围 |
|---|---|---|
| **类别代号** | `A`–`L`,长期稳定不重命名 | `A`/`B`/.../`L` |
| **类别名(zh / en)** | 双语,与 SOP 一致 | — |
| **描述** | 这一类是什么,为何独立成类 | 1–3 句 |
| **文件枚举** | 精确路径,不写通配 | 完整 repo-relative path |
| **改动义务** | 何种发版触发本类必须改动 | 见下方"改动义务取值" |
| **锁版风险** | 不可回滚程度 | `none` / `CDN-cacheable` / `PyPI long_description ⚠` / `Git tag ⚠` / `Zenodo DOI ⚠` |
| **SOP 对应行** | 与 SOP 章节的双向锚点 | `§C.1 第 N 项` / `§G 第 M 条` / `§阶段 4.5` |

**改动义务取值**:

- `every release` — 每版发版必改(版本号、CHANGELOG 等)
- `on protocol change` — 协议规则有 bump 时改(`fcop-rules.mdc` 等)
- `on essay add` — 新增 essay 时改(essays-grid、`essays/README.md`)
- `on team template change` — 团队模板有 bump 时改
- `on rule change only` — 协议规则有动才改(否则保持)
- `on tag push` — 由 `release.yml` 自动产生,人不直接编辑

---

## 2. 文件清单 12 类 / 12 Categories

### A. 包源版本号 / Package Source Versions

- **描述**:`fcop` 与 `fcop-mcp` 双包的**唯一**版本号源,所有 wheel /
  sdist / PyPI 元数据从这里读出。两包独立 SemVer,但 v1.0+ 之后惯例
  保持同步 bump。
- **文件枚举**:
  - `src/fcop/_version.py`
  - `mcp/src/fcop_mcp/_version.py`
- **改动义务**:`every release`(同步 bump,两文件版本号必须一致)
- **锁版风险**:`Git tag ⚠`(`release.yml` 的 `verify` job 校验 tag
  名 = `_version.py` = CHANGELOG 节标题三方一致,任何不一致 tag 必须
  bump 重发)
- **SOP 对应行**:`§G 第 3 条`(`py -3.10 -c "import fcop._version, fcop_mcp._version"` 双包版本一致校验)

### B. 协议规则源 / Protocol Rules Source (in package)

- **描述**:FCoP 协议规则与协议解释的**包内权威源**。`fcop` 包发布
  时,这些文件随 wheel 一起分发;下游 IDE 通过 `init_project` /
  `redeploy_rules` 把它们部署到项目根。
- **文件枚举**:
  - `src/fcop/rules/_data/fcop-rules.mdc`(规则,带 `fcop_rules_version` frontmatter)
  - `src/fcop/rules/_data/fcop-protocol.mdc`(协议解释,带 `fcop_protocol_version` frontmatter)
  - `src/fcop/rules/_data/letter-to-admin.zh.md`(中文 ADMIN 说明书)
  - `src/fcop/rules/_data/letter-to-admin.en.md`(英文 ADMIN 说明书)
  - `src/fcop/rules/_data/agent-install-prompt.zh.md`
  - `src/fcop/rules/_data/agent-install-prompt.en.md`
  - `src/fcop/rules/_data/internal-readme.zh.md`(v2.0.0 ADR-0034 新增)
  - `src/fcop/rules/_data/internal-readme.en.md`(v2.0.0 ADR-0034 新增)
  - `src/fcop/rules/_data/fcop-spec-v1.0.{zh,en}.md`
  - `src/fcop/rules/_data/fcop-spec-v1.1.{zh,en}.md`
- **改动义务**:
  - `fcop-rules.mdc` / `fcop-protocol.mdc` → `on protocol change`(frontmatter 内 `*_version` 必须同步 bump)
  - `letter-to-admin.{zh,en}.md` → `every release`(摘要段需写本版亮点)
  - `internal-readme.{zh,en}.md` → 添加 / 改动 internal-only 声明语法时
  - `fcop-spec-v*.{zh,en}.md` → 协议 frozen 后只追加,不修改
- **锁版风险**:`none`(发布到 PyPI 后 wheel 不可改,但 wheel 内文件本身在新版可改)
- **SOP 对应行**:`§C.2`(第 7–10 项,letter-to-admin × 2、rules.mdc、protocol.mdc);`§G 第 2 条`(letter-to-admin 摘要块版本号扫描)

### C. 协议规则镜像 / Protocol Rules Mirror (at project root)

- **描述**:`fcop` 包内规则在**项目根**的镜像。`fcop init_project` /
  `redeploy_rules` 把 B 部署到此处。Cursor 读 `.cursor/rules/*.mdc`,
  Codex / Claude Code 等 host 读 `AGENTS.md` / `CLAUDE.md`(ADR-0006
  host-neutral 四件套)。
- **文件枚举**:
  - `.cursor/rules/fcop-rules.mdc`
  - `.cursor/rules/fcop-protocol.mdc`
  - `AGENTS.md`
  - `CLAUDE.md`
- **改动义务**:`on protocol change`(由 `deploy_protocol_rules` 工具
  从 B 同步;**agent 不得手动编辑这四个文件**,Rule 8)
- **锁版风险**:`none`
- **SOP 对应行**:在 §C 隐式,与 B 联动(B 改完 `redeploy_rules()`
  自动写到 C)。本仓自身需手动同步:发版前必跑
  `Project.deploy_protocol_rules(force=True)`,**或在 `release.yml`
  内显式跑**(2026-05-13 v2.0.0 实战观测到过期镜像未更新事故)。

### D. 公网可见文档 / Visible on the Web

- **描述**:**对外读者最多**的文档。bump 漏 = 对外撒谎(Rule 0.c
  反面)。其中 `mcp/README.md` 同时是 PyPI `long_description`,锁版
  风险最高。
- **文件枚举**(6 份):
  - `README.md` — 英文,GitHub 仓库首页(国际读者第一眼)
  - `README.zh.md` — 中文,GitHub 仓库首页(中文读者第一眼;v2.0.0
    之前的历版 SOP 漏列它,导致它停在 `1.2.1` × 4 版)
  - **`mcp/README.md`** — PyPI `long_description` ⚠ **锁版**
  - `docs/index.html` — GitHub Pages 首页 `https://joinwell52-ai.github.io/FCoP/`(version pill、"What is FCoP"、essays-grid 三处必同步)
  - `essays/README.md` — essay 目录索引(新增 essay 时改)
  - `CITATION.cff` — Zenodo 引用元数据(新 Zenodo snapshot 时改)
- **改动义务**:
  - `README.md` / `README.zh.md` / `mcp/README.md` → `every release`
  - `docs/index.html` → `every release`(version pill)+ `on essay add`(essays-grid)
  - `essays/README.md` → `on essay add`
  - `CITATION.cff` → 只在新建 Zenodo snapshot 时
- **锁版风险**:
  - `mcp/README.md` → **PyPI long_description ⚠**(twine upload 成功
    即永久定格;同版本号不允许重传)
  - `CITATION.cff` → **Zenodo DOI ⚠**(归档后该 DOI 内容不可改)
  - 其他 → `CDN-cacheable`(GitHub Pages 有 ~5min CDN 延迟,但可改)
- **SOP 对应行**:`§C.1`(第 1–6 项);`§G 第 1 条`(rg 公网文档版本号残留扫描)

### E. CHANGELOG

- **描述**:发版的**唯一规范变更记录**。`release.yml` 的 `github-release`
  job 从这里抽取本版本块作为 GitHub Release body。
- **文件枚举**:
  - `CHANGELOG.md`(Keep-a-Changelog 格式;日期分隔符**使用 em-dash `—`**
    而非 ASCII hyphen `-`,SOP §G 第 4 条 regex 需匹配 em-dash)
- **改动义务**:`every release`(`[Unreleased]` → `[X.Y.Z] — YYYY-MM-DD`
  + Added / Changed / Deprecated 三段最少齐全)
- **锁版风险**:`none`(本仓文件,任何时候可改;但 GitHub Release body
  抓取过的本版本块在 release 创建后改了不会回写)
- **SOP 对应行**:`§C.2`(第 11 项);`§G 第 4 条`(必须 1 hit 本版块)

### F. Hardcoded 断言与提示词 / Hardcoded Assertions & Prompts

- **描述**:测试和工具实现里**写死的版本号 / 摘要标签**。改版本号若
  不同步这些位置,测试红或 init_* 工具引导用户去读错版本号摘要。
- **文件枚举**(精确到行号):
  - `mcp/src/fcop_mcp/server.py:779` — 字符串 `"尤其是 vX.Y.Z 摘要那一段)"`
    在 init_* 工具回执的 ADMIN 引导段(2026-05-13 现场核对:全文件
    唯一一处版本号硬编码;其他版本字段都从 `_version.py` 动态读)
  - `tests/test_fcop/test_rules.py:104` — `assert "vX.Y.Z 摘要" in intro`(1 处)
  - `tests/test_fcop_mcp/test_server.py:163` — `assert "vX.Y.Z 摘要" in out`
  - `tests/test_fcop_mcp/test_server.py:182` — `assert "vX.Y.Z 摘要" in out`
  - `tests/test_fcop_mcp/test_server.py:196` — `assert "vX.Y.Z 摘要" in out`
- **改动义务**:`on protocol change`(letter-to-admin 摘要段写本版亮点
  时,同步把这 5 处的 `vX.Y.Z` 字面量改成新版)
- **锁版风险**:`none`
- **SOP 对应行**:`§C.3`(第 12 项;**SOP §C.3 之前的措辞"若有 vX.Y.Z
  摘要断言"含糊,实际 `test_server.py` 有 3 处不是 1 处,本清单精确
  化**)

### G. ADR (Architecture Decision Records)

- **描述**:协议级决策的不可篡改记录。发版**不允许**带着 `Status:
  Proposed` 的 ADR ——这表示决策未拍板,不能进 release。
- **文件枚举**:
  - `adr/ADR-*.md`(截至 v2.0.0 共 35 份:ADR-0001 至 ADR-0034,含
    ADR-0030-bis 一份补丁)
  - `adr/README.md`(ADR 索引)
- **改动义务**:
  - 新 ADR 落档 → 新增文件,`Status: Proposed → Accepted` 在发版前
  - ADR 实施完成 → `Status: Accepted → Implemented`(Rule 0.a.1 闭环)
  - `adr/README.md` 必须随新 ADR 同步更新
- **锁版风险**:`none`(本仓 append-only)
- **SOP 对应行**:`§C.3`(第 14 项,"每份 ADR `Status: Accepted`,
  不能带着 `Proposed` 发版");`§G 第 5 条`(`rg '^Status: Proposed' adr/`)

### H. 迁移指南 / Migration Guides

- **描述**:跨大版本(0.x → 1.0 / 1.x → 2.0)的迁移指引。**只在影响
  下游 agent 的迁移路径**时改动,普通 patch / minor 发版不动。
- **文件枚举**:
  - `docs/MIGRATION-0.6.md`(0.5 → 0.6 包拆分)
  - `docs/MIGRATION-1.0.md`(0.x → 1.0 AI-OS 重 framing)
  - `docs/MIGRATION-1.1.md`(1.0 → 1.1 v1.1 capabilities)
  - 未来 `docs/MIGRATION-X.Y.md` 按需新增
- **改动义务**:`on protocol change`(本版影响某段已有迁移指引时,在
  对应 `MIGRATION-*.md` 加一行;否则跳过)
- **锁版风险**:`none`
- **SOP 对应行**:`§C.3`(第 13 项)

### I. 包内样板与团队模板 / Sample Library & Team Templates

- **描述**:`fcop` 包内捆绑的样本团队模板,通过 `init_project` /
  `deploy_role_templates` 部署到下游项目的 `fcop/shared/`。**协议 Rule 4.5
  三层结构在 v2.0.0 后是 frozen 的**(`TEAM-README.md` + `TEAM-ROLES.md`
  + `TEAM-OPERATING-RULES.md` + `roles/{ROLE}.md`,zh + en)。
- **文件枚举**(样板):
  - `src/fcop/rules/_data/teams/{dev-team,media-team,mvp-team,qa-team}/*.{md,en.md}`
  - 本仓 `fcop/shared/` 自身的团队文档(因本仓也是 FCoP 项目):
    - `fcop/shared/TEAM-README.{md,en.md}`
    - `fcop/shared/TEAM-ROLES.{md,en.md}`
    - `fcop/shared/TEAM-OPERATING-RULES.{md,en.md}`
- **改动义务**:`on team template change`(协议规则有动且影响团队
  运作时,优先改包内样板再用 `deploy_role_templates(force=True)`
  同步到本仓)
- **锁版风险**:`none`(但下游已 deploy 的项目不会自动 pick up,需
  ADMIN 在下游项目主动跑 `deploy_role_templates`)
- **SOP 对应行**:未单列;变更团队样板的发版应在 CHANGELOG 显著标注。

### J. CI / Workflow

- **描述**:GitHub Actions 工作流,**`release.yml` 是发版主路径**——
  本地不再手动 `twine upload`,一切交给它的 5-job pipeline。
- **文件枚举**:
  - `.github/workflows/release.yml`(发版主路径,5 jobs)
  - `.github/workflows/test-fcop.yml`(`fcop` 包 CI)
  - `.github/workflows/test-fcop-mcp.yml`(`fcop-mcp` 包 CI)
- **改动义务**:
  - `release.yml` → 仅在发版流程结构变化时改(罕见;改 = Rule 7
    高危,需 ADMIN 二次确认)
  - `test-*.yml` → 测试矩阵 / Python 版本变化时
- **锁版风险**:`none`(本仓文件)。但**`release.yml` 改错 = 发版
  pipeline 红 = tag 占坑必须 bump**,等价 Rule 7 高危。
- **SOP 对应行**:`§阶段 3`(tag push 触发 `release.yml`);**新增建议**:
  `release.yml` 改动的 PR **必须**先用 `workflow_dispatch dry_run=true`
  验证(SOP §阶段 3 末尾已有"Dry run"说明)。

### K. 备份链路 / Backup Mirror

- **描述**:Git remote `backup` 指向 `joinwell52-AI/FCoP-backup`
  (private repo,2026-05-13 v2.0.0 后建仓)。**这不是"文件",是
  "remote 配置 + 命令序列"**,但发版每次必走,与文件清单同级重要。
- **远端清单**:
  - `origin` → `https://github.com/joinwell52-AI/FCoP.git`(public,主)
  - `backup` → `https://github.com/joinwell52-AI/FCoP-backup.git`(private,镜像)
- **改动义务**:`every release`(发版后立即 `git push backup main &&
  git push backup --tags`;append-only,**不允许** `--mirror` 以防"反备份")
- **锁版风险**:`Git tag ⚠`(tag push 后该 tag SHA 在 origin / backup
  双向永久绑定;backup 上的 tag SHA 必须与 origin byte-for-byte 一致)
- **SOP 对应行**:`§阶段 4.5`(备份镜像同步,完整 3 步命令 + 验证);
  `§G 第 6 条`(`git remote -v | Select-String '^backup\s'` 配置存在性扫描)

### L. ADMIN 仪式 / ADMIN Rituals

- **描述**:发版**前**的草稿与 Rule 0.a.1 四步循环产物。这些文件**不
  在 PyPI 也不在 GitHub Release 里**,但落在本仓的 `fcop/log/` 是永
  久 audit trail。
- **文件枚举**:
  - `.scratch/_v{X_Y_Z}_tag_msg.txt`(annotated tag message,git-ignored)
  - `.scratch/_release_{X_Y_Z}_closure_msg.txt`(commit message,git-ignored)
  - `fcop/tasks/TASK-{date}-{seq}-ADMIN-to-ME-release-{X.Y.Z}-*.md`(本版发版 TASK)
  - `fcop/reports/REPORT-{date}-{seq}-ME-to-ADMIN.md`(本版发版 REPORT)
  - `fcop/log/tasks/` + `fcop/log/reports/`(archive 目标目录)
- **改动义务**:`every release`(每版发版 TASK + REPORT 各 1 份;
  Rule 0.a.1 四步循环硬约束)
- **锁版风险**:`none`(本仓 append-only;`fcop/log/` 历史只增不改 Rule 5)
- **SOP 对应行**:`§阶段 4`(Rule 0.a.1 闭环 checklist)

---

## 3. 改动义务 × 类别 速查矩阵 / Quick Matrix

只看本次发版改了什么,反查应该动哪几类:

| 改了什么 | 必动类别 | 可选 |
|---|---|---|
| 仅版本号 bump(纯 release) | A · D · E · F · K · L | — |
| 协议规则改动 | A · **B · C** · D · E · F · L · K | G(新 ADR)· I(团队模板)· H(迁移) |
| 协议规则 + 新 ADR | A · B · C · D · E · F · **G** · L · K | H · I |
| 新增 essay | D(`essays/README.md` + `docs/index.html` essays-grid)· E · L | — |
| 团队模板有动 | A · D · E · **I** · L · K | B · C · G |
| 跨大版本(MAJOR) | A · B · C · D · E · F · G · **H** · I · L · K | J(若 release.yml 也要改) |

**最小发版集 = A + D + E + F + K + L**(6 类)——任何发版都必动这 6 类。

---

## 4. 自动化校验入口 / Audit Hooks

本清单设计为可被脚本与 CI 直接解析。**自 v3.0.2 起两条 audit 已落地**
(从 P3"未来实现"晋升为 P0 强制门禁):

- **`scripts/release_audit.py`**(已落地,v3.0.2):一次跑 R1–R12 共
  12 项检查,覆盖双 `_version.py` 对齐、`mcp/server.json`、CHANGELOG、
  公共门面文档、README 双语发版表、CITATION.cff、letter-to-admin、
  5 处 hardcoded `vX.Y.Z`、ADR Proposed 状态、backup remote、
  `mcp/pyproject.toml` pin、双语配对完整性。
  调用:`py -3 scripts/release_audit.py --new X.Y.Z --old A.B.C`。
  P0 失败 = 退出码 1 = 阻断发版。
- **`scripts/inventory_drift.py`**(已落地,v3.0.2):扫本文件 §2
  "文件枚举"与 `git ls-files` 比对,产出三类警告:
  - Class 1 `listed-but-missing` — 清单有、仓库无
  - Class 2 `tracked-but-unlisted` — 仓库有、清单无(governed root 内)
  - Class 3 `path-drift` — 同 basename 不同路径(疑似重命名)
  调用:`py -3 scripts/inventory_drift.py [--lenient]`。
  默认严格模式三类全归零;`--lenient` 仅 Class 1 阻断。
- **`audit.assertion_lines()`** 已纳入 `release_audit.py` R8 检查
  (5 处 hardcoded `vX.Y.Z` 字面量与 `_version.py` 对照)。

CI 集成:GitHub Actions `release-gate.yml` 在 tag push 时强制跑两脚本,
任一 P0 失败拒绝 tag。本地手工 `rg` 命令(SOP §G)仍保留为快速排查手段。

---

## 5. 双语意识 / Bilingual Discipline

本文件目前**仅中文版**。en 副版(`RULES-release-file-inventory.en.md`)
将在以下任一时机落档:

- 第一份外部团队询问 FCoP 发版纪律(主动触发)
- v2.x 后期某次发版前
- ADMIN 显式触发

**中文版优先**的原因:本团队主语言 = 中文;外部 IDE 团队通常会先翻
SOP(`docs/release-process.md` 双语)再翻清单,有时序差。

---

## 6. 变更日志 / Change Log

| 日期 | 版本 | 变更 | 关联 TASK |
|---|---|---|---|
| 2026-05-13 | v1.0(本文件落档) | 初版,12 类 6 字段全填实 | TASK-20260513-013 |
| 2026-05-22 | v1.1(随 fcop@3.0.2) | §4 audit hooks 从 P3 升 P0:`scripts/release_audit.py`(R1–R12)+ `scripts/inventory_drift.py`(三类漂移)落地为发版强制门禁;新增 ADR/MIGRATION/cursor-rules glob 覆盖;basename-only inventory 解析支持 | TASK-20260522-005 |

变更日志只 append,不重写历史(Rule 5)。

---

> 见也见 / See also:
> - `fcop/shared/RULES-release-sync-checklist.md`(纪律书 · 红线与态度)
> - `docs/release-process.md`(SOP · 流程权威源)
> - `fcop/log/reports/REPORT-20260513-011-ME-to-ADMIN.md`(红线 1 源头)
> - `fcop/log/reports/REPORT-20260513-013-ME-to-ADMIN.md`(红线 2 + 红线 3 源头,待落档)
> - Rule 0.a / 0.c / 2 / 5 / 7 / 8(协议层依据)
