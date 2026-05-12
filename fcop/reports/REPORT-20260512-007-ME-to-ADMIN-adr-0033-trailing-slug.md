---
protocol: fcop
version: 1
kind: report
report_id: REPORT-20260512-007
sender: ME
recipient: ADMIN
task_id: TASK-20260512-006
priority: P1
status: done
thread_key: adr-0033-trailing-slug-adoption
risk_level: low
created_at: "2026-05-12T23:05:00+08:00"
---

# REPORT · ADR-0033 落地完成(并行模式)

> 回执 `TASK-20260512-006-ADMIN-to-ME.md`。
> ADMIN 决策:**A · 协议收编**,**并行执行**(2026-05-12 22:51)。

## TL;DR

**协议收编完成。`fcop@1.6.0` / `fcop-mcp@1.6.0` / `fcop_protocol_version
2.4.0` 已就绪,可发布。**

5 个 Phase 全部完成,1057 个单测通过(新增 31 个 slug 测试),零回归。
代码补丁 + 单测 + 文档 + ADR + release notes + 版本号 全链路对齐。

本 REPORT 自身就是新文法的活证据 ——
文件名 `REPORT-20260512-007-ME-to-ADMIN-adr-0033-trailing-slug.md` 由
1.6.0 文法直接生成,trailing slug `adr-0033-trailing-slug` 通过
`parse_report_filename` 正确返回。

## 做了什么 · What

### Phase 1 · 代码补丁 ✅

- `src/fcop/core/filename.py`:
  - 新增 `_SLUG = r"[a-z](?:[a-z0-9-]*[a-z0-9])?"` 子模式
  - 新增 `SLUG_RE` 导出常量
  - `TASK_FILENAME_RE` / `REPORT_FILENAME_RE` / `ISSUE_FILENAME_RE`
    末尾追加可选 `(?:-(_SLUG))?`
  - `TaskFilename` / `ReportFilename` / `IssueFilename` dataclass
    增加 `slug: str | None = None` 字段
  - `parse_*_filename` 解析并返回 slug
  - `build_*_filename` 接受可选 `slug=` 参数
  - `_check_components` 校验 slug 合规
- 既有 111 个 filename 单测全部通过(零回归)

**关键设计决策**:`_SLUG` 文法为 `[a-z](?:[a-z0-9-]*[a-z0-9])?`,
比 task 文档原拟的 `[a-z0-9][a-z0-9-]*` 更严格:

| 维度 | TASK-006 原拟 | 实际采用 | 理由 |
|---|---|---|---|
| 起手字符 | `[a-z0-9]` | `[a-z]` | 与 `_ROLE`(允许 `OPS-001`)消歧 |
| 收尾字符 | 任意 | `[a-z0-9]` | 禁止 `foo-`(零信息 + 不雅观) |

消歧推理详见 ADR-0033 §3.1 / §3.2。

### Phase 2 · 单元测试 ✅

`tests/test_fcop/test_core_filename.py` 新增 31 个测试:

- `TestTaskTrailingSlug`:parse TASK 含 slug(包含 codeflow 现场样本)
- `TestBuildTaskFilenameWithSlug`:build 含 slug + 拒绝非法
- `TestReportTrailingSlug`:REPORT 三类
- `TestIssueTrailingSlug`:ISSUE 三类
- `TestSlugRegexExport`:`SLUG_RE` 文法 pinning

**回归证据**:
- 旧 `TASK-20260423-017-ADMIN-to-PM.md` 仍 parse 通过,`slug=None`
- 现场样本 `TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md` 现在
  parse 返回 `slug="phase-a-fix-naming"`
- 非法 slug(`Foo` / `1foo` / `foo-` / `foo_bar` / `foo.bar` / `foo bar`)
  全部抛 `ValueError`
- 大写后缀消歧:`...-PM-to-OPS.D1.md` 仍解析为 `slot=D1, slug=None`

**测试结果**:1057/1057 通过(含新增 31 个,不含一个**预先存在**的
`test_tool_surface_matches_snapshot` 漂移问题——独立跟踪,详见末尾)。

### Phase 3 · 文档同步 ✅

`src/fcop/rules/_data/fcop-protocol.mdc`:

- frontmatter `fcop_protocol_version`:2.3.0 → **2.4.0**
- "## File Naming" 节后追加 "### Trailing slug (optional)" 子节
  (双语 + 文法 + 不参与 routing 说明 + 现场样本 + 何时用 / 何时不用)
- 末尾 changelog 加 v2.4 条目(标注 `fcop@1.6.0`)

**未改的文件**(刻意):

- `src/fcop/rules/_data/fcop-rules.mdc`:规则本体未变,trailing slug
  是 commentary 层 additive convention,无新规则
- `.cursor/rules/fcop-protocol.mdc`(项目根部署副本):待 ADMIN 安装
  1.6.0 后通过 `redeploy_rules()` 同步(per Rule 8 + ADR-0006,Agent
  不得自行覆盖项目根规则文件)

### Phase 4 · ADR + Release Notes ✅

- `adr/ADR-0033-trailing-slug-filename-adoption.md`:全文落盘
  - §1 背景(codeflow 22+ 现场 + 协议三方不一致论证)
  - §2 决策(协议收编 + 文法增量 + 不参与 routing + 完全向后兼容)
  - §3 设计细节(消歧推理 + 与 REVIEW.subject_short 关系)
  - §4 实施清单 + 版本规划
  - §5 影响与迁移(零成本)
  - §6 备选方案(A 禁止 / B 维持灰色 / **C 收编 ← 采纳**)
  - §7 验收(全部 ✅)
  - §8 发布(与 codeflow Mode 1 解耦)
  - §9 后续追踪(redeploy_rules + slug 反模式观测 + snapshot 漂移)
- `adr/README.md`:索引新增 ADR-0033 行
- `CHANGELOG.md`:新增 `[1.6.0]` 完整 release notes 条目
- `src/fcop/_version.py`:1.5.1 → **1.6.0**
- `mcp/src/fcop_mcp/_version.py`:1.5.1 → **1.6.0**(同步,两包都走
  hatch dynamic version,改一处即生效)

**版本对齐总账**:

| 资产 | 旧 | 新 | 类型 |
|---|---|---|---|
| `fcop` package | 1.5.1 | **1.6.0** | MINOR additive |
| `fcop-mcp` package | 1.5.1 | **1.6.0** | MINOR additive |
| `fcop_protocol_version` | 2.3.0 | **2.4.0** | MINOR additive |
| `fcop_rules_version` | 2.2.0 | (不变) | — |

按 ADR-0003 SemVer §MINOR additive:新增可选语法 + 向后兼容 +
既有行为零变化。

### Phase 5 · 回执 + archive(本步) ✅(进行中)

- 本 REPORT 落盘(走 Rule 0.a.1 第 3 步)
- 接下来 `archive_task(TASK-20260512-006)` 完成第 4 步

## 验收清单 · DoD

对照 TASK-006 §"验收标准":

- [x] 单测全绿:1057/1057 通过(新增 31,既有零回归)
- [x] `re.fullmatch(TASK_FILENAME_RE, 'TASK-20260512-025-PM-to-OPS-phase-a-fix-naming.md')`
      → match,groups 含 `slug='phase-a-fix-naming'`
- [x] 旧文件名 `TASK-20260512-006-ADMIN-to-ME.md` 仍 parse 通过,`slug=None`
- [x] `fcop-protocol.mdc` 内容更新到 2.4.0(`fcop-rules.mdc` / `AGENTS.md` /
      `CLAUDE.md` 由 ADMIN 通过 `redeploy_rules()` 同步,本任务不直改)
- [x] ADR-0033 落盘,索引收录,链接到同期 task

## 与 TASK-006 原计划的偏差 · Deviations

3 处小幅调整,均**实质等价**或**更严格**:

1. **目标版本 1.2.0 → 1.6.0**:TASK-006 写时 `fcop` 是 1.1.x 心智账,
   实际当前是 **1.5.1**。按 SemVer MINOR additive 增量,目标版本订正
   为 **1.6.0**。同理 protocol version 2.1.0 → 2.4.0。
   (CHANGELOG / ADR-0033 / protocol.mdc 三处版本号已对齐到 1.6.0/2.4.0)
2. **`_SLUG` 起手收紧到 `[a-z]`**:TASK-006 原拟 `[a-z0-9]`(沿用
   REVIEW.subject_short)。实施过程中发现与 `_ROLE` 段(允许 `OPS-001`)
   存在歧义,改为 `[a-z]` 起手保证唯一解析。决策推理详见 ADR-0033 §3.1。
3. **`fcop_rules_version` 不动**:TASK-006 原拟 2.2.0 → 2.3.0;实施
   过程中确认 trailing slug 是 commentary 层(`fcop-protocol.mdc`)
   convention,不动 `fcop-rules.mdc` 本体,所以 rules version 保持 2.2.0。
   只升 protocol version 2.3.0 → **2.4.0**。

## 后续 · Next

### 等 ADMIN 触发

1. **`redeploy_rules()`**:把 `.cursor/rules/fcop-protocol.mdc`
   + `AGENTS.md` + `CLAUDE.md` 同步到 2.4.0(per Rule 8 + ADR-0006,
   ME 不得自行调用)
2. **发布 1.6.0**:`fcop` + `fcop-mcp` 双包发布;codeflow 端 Mode 1
   收尾后再升级,两条线无依赖

### ME 自行跟进

- (独立)向 ADMIN 上报 `test_tool_surface_matches_snapshot` 中
  `fcop_audit` 工具消失的 snapshot 漂移问题——预先存在,与本 ADR 无关,
  应起独立 task 修复

## 引用 · Citations

- 现场触发:`TASK-20260512-006-ADMIN-to-ME.md`(本 task 全文)
- ADR 全文:`adr/ADR-0033-trailing-slug-filename-adoption.md`
- 代码改动:
  - `src/fcop/core/filename.py:_SLUG, SLUG_RE, TASK_FILENAME_RE,
    TaskFilename, parse_task_filename, build_task_filename`
    (及对应 REPORT / ISSUE 三组)
  - `tests/test_fcop/test_core_filename.py:TestTaskTrailingSlug` 起
    新增 5 个测试类(31 个测试)
- 文档:
  - `src/fcop/rules/_data/fcop-protocol.mdc`("File Naming" 节
    "Trailing slug (optional)" 子节)
  - `CHANGELOG.md:[1.6.0]` 条目
- ADMIN 决策点(2026-05-12 22:51):"A,协议收编,因为 agent 之间看得懂"
- ADMIN 节奏选择(2026-05-12 22:52):"并行(ME 推荐)"

---

**status**:DONE
**closes**:TASK-20260512-006
**next**:`archive_task(TASK-20260512-006)`
