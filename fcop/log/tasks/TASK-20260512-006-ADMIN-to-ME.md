---
protocol: fcop
version: 1
kind: task
task_id: TASK-20260512-006
sender: ADMIN
recipient: ME
priority: P1
thread_key: adr-0033-trailing-slug-adoption
risk_level: low
created_at: "2026-05-12T22:55:00+08:00"
---

# ADR-0033 · TASK / REPORT / ISSUE 文件名 trailing-slug 收编

## 背景 · Why

P4.9 sprint(codeflow + D:\FCoP)期间,agent 自发涌现一种长文件名:

```
TASK-20260512-022-PM-to-OPS-fcop-mcp-1-5-1-housekeeping-commit.md
TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md
TASK-20260512-009-PM-to-OPS-codeflow-json-rm.md
... 共 22+ 件(codeflow 端)
```

按现行 `TASK_FILENAME_RE`(`src/fcop/core/filename.py:99-101`)的
`_ROLE = [A-Z][A-Z0-9_]*(?:-[A-Z0-9_]+)*`,这种文件名 lexical 不合规
(`parse_task_filename` 返回 None)。但 `fcop_audit` 6 个 scan 全部
不查这一类,事实放行。Rule 5 又锁死"改名修复"路径——已落盘文件不能改名。

ADMIN 决策(2026-05-12 22:51):**A · 协议收编**。理由:agent 之间
看得懂——文件名一眼看出任务主题,信息价值高,是 essay D 谈的
"类型 1 涌现"(高复用)的标准收编候选。

## 范围 · What

新增**可选 trailing-slug 段**到 TASK / REPORT / ISSUE 三类文件名:

```
TASK-{date}-{NNN}-{SENDER}-to-{RECIPIENT}[.{SLOT}][-{slug}].md
REPORT-{date}-{NNN}-{REPORTER}-to-{RECIPIENT}[-{slug}].md
ISSUE-{date}-{NNN}-{REPORTER}[-{slug}].md
```

`{slug}` 语法(沿用 REVIEW 的 `subject_short` 现成约定):

```
[a-z0-9][a-z0-9-]*  (lowercase letters / digits / hyphens, 起手非 hyphen)
长度建议 ≤ 40 字符(soft limit,不强制)
```

**slug 不参与 routing**——它只是人类可读标签,routing 仍由
`{SENDER}/{RECIPIENT}/{SLOT}` 决定。slug 缺失 / 存在均合规。

REVIEW 文件名**不**加 slug(它已有 `-on-{subject_short}` 段,
功能等价,无需重复)。

## 实施步骤 · How

### Phase 1 · 协议规则补丁(MINOR additive)

- [ ] `src/fcop/core/filename.py`:
  - 在 `_ROLE` 后增加 `_SLUG = r"[a-z0-9][a-z0-9-]*"`
  - 改 `TASK_FILENAME_RE` 在 `(?:\.(_ROLE))?` 后追加 `(?:-(_SLUG))?`
  - 改 `REPORT_FILENAME_RE` 在 `(_ROLE)\.md$` 前追加 `(?:-(_SLUG))?`
  - 改 `ISSUE_FILENAME_RE` 在 `(_ROLE)\.md$` 前追加 `(?:-(_SLUG))?`
- [ ] `TaskFilename` / `ReportFilename` / `IssueFilename` dataclass 加
  `slug: str | None = None` 字段;`render()` 同步
- [ ] `parse_task_filename` / `parse_report_filename` /
  `parse_issue_filename` 返回 slug
- [ ] `build_task_filename` / `build_report_filename` /
  `build_issue_filename` 加 `slug` 关键字参数(可选)
- [ ] `_check_components` 处理 slug 校验(用新增 `_SLUG_RE`)

### Phase 2 · 单元测试

- [ ] `tests/core/test_filename.py` 新增:
  - parse 含 slug 的 task / report / issue 文件名
  - parse 不含 slug 的回归测试(向后兼容)
  - build 显式带 slug
  - 非法 slug 拒绝(大写 / 起手 hyphen / 含 underscore)
  - 现场样本回归:
    `TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md` → 应解析为
    `(date=20260512, seq=25, sender=PM, recipient=OPS, slot=None,
    slug="phase-a-fix-naming")`

### Phase 3 · 协议文档同步

- [ ] `src/fcop/rules/fcop-rules.mdc`:Rule 3 `Metadata Integrity` 节
  保持不变(slug 不入 frontmatter);**版本日志**新增 2.3.0 条目
  `(per ADR-0033)`
- [ ] `src/fcop/rules/fcop-protocol.mdc`:`File Naming` 节增加
  "Optional trailing slug"小节(中英双语 + 示例 +"不参与 routing"
  说明)
- [ ] `fcop_rules_version`:`2.2.0 → 2.3.0`
- [ ] `fcop_protocol_version`:`2.0.0 → 2.1.0`
- [ ] 部署的 host-neutral 4 件套(`.cursor/rules/*.mdc` + `AGENTS.md`
  + `CLAUDE.md`)同步重生成

### Phase 4 · ADR + Release notes

- [ ] 写 `adr/ADR-0033-trailing-slug-filename-adoption.md`,含:
  - 背景:codeflow + D:\FCoP 双现场 22+ 件涌现证据
  - 决策:A · 协议收编
  - 影响范围 + 向后兼容性证明
  - 拒绝的备选 B(禁止)被 Rule 5 锁死的推理
- [ ] 起草 `fcop 1.2.0` release notes(MINOR · additive),含:
  - 协议层 fcop_rules_version 2.3.0 + fcop_protocol_version 2.1.0
  - 行为变化:`parse_*_filename` 多返一字段(向后兼容,旧 caller 不读 slug 即可)
  - codeflow 等下游用户升级后,历史长文件名追溯性合规

## 验收标准 · DoD

- [ ] 单测全绿(新增 + 回归)
- [ ] `re.fullmatch(TASK_FILENAME_RE,
  'TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md')` → match,
  groups 含 `slug='phase-a-fix-naming'`
- [ ] 旧文件名 `TASK-20260512-006-ADMIN-to-ME.md` 仍 parse 通过,
  `slug=None`
- [ ] `fcop-rules.mdc` / `fcop-protocol.mdc` / `AGENTS.md` / `CLAUDE.md`
  内容一致(diff 只在版本号 + 新增的"Optional trailing slug"节)
- [ ] ADR-0033 落盘,链接 essay D + codeflow emergence-log

## 节奏 · When

**等 ADMIN 拍 kickoff 时机**——两个选项:

| 选项 | 含义 | ETA |
|---|---|---|
| **并行** | 现在就开始 Phase 1-4;codeflow 那边 Phase A/B/C 同时跑 | ~3-4 工时,5/13 中午前完成 |
| **串行** | 等 codeflow Mode 1 ALL GREEN 后再开 | 5/13 下午起,5/14 完成 |

**ME 推荐**:并行——两条工作线无依赖,总周期短一半。codeflow PM
跑的是当前 wheel 版本,fcop 新版 release 不会自动升级它,不会扰乱
Phase A/B/C。

## 风险 · Risks

| 风险 | 处置 |
|---|---|
| trailing-slug 与 slot 段(`.{ROLE}`)文法歧义 | slug 用 hyphen 前导(`-{slug}`),slot 用 dot 前导(`.{SLOT}`),正则可区分;但若 `_ROLE` 段包含 hyphen + 大写(如 `AUTO-TESTER`),分界仍清楚因为 slug 强制小写起手 |
| 历史 task 文件不带 slug,新代码读 slug=None | 向后兼容,无破坏 |
| 工具(`list_tasks` 等)显示 slug 还是隐藏? | 默认显示完整文件名(已是现状),不改 |
| codeflow 跑 Mode 1 期间升级 fcop 撞 release? | codeflow 用 pinned wheel,不自动升;Mode 1 闭环后由 ADMIN 手动升 |

## 协议合规守则

- Rule 0.a.1:四步走(本 task 是第 1 步)
- Rule 5:协议演化通过新文件 + ADR-0033,**不**改任何已落盘文件
- Rule 0.c:emergence-log 引用要带出处(codeflow PM 长文件名清单 +
  D:\FCoP regex 实测结果)
- Rule 7:无破坏性操作(纯增量,向后兼容)
- 升级语义:**MINOR additive**——`fcop@1.2.0`,既有项目零成本兼容

---

**status**:WAITING — 等 ADMIN 拍 kickoff 时机(并行 / 串行)
**next**:ADMIN 拍 → ME 开 Phase 1
