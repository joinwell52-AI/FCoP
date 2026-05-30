---
kind: common-inject
fcop_version: 3.2.5
source: fcop-rules.mdc Rule 0.a.1–0.a.6
---

<!-- BEGIN_TEAM_ZH -->
## 工作流硬约束（适用于所有角色 / 不允许例外）

> 这一节是 `fcop-rules.mdc` Rule 0.a / Rule 0.a.1–0.a.6 在角色侧的具体翻译。
> **任何**收到的工作（无论看起来多简单）必须走完协作闭环：
> **`task → 执行/派发 → report → 等待验收 / 按授权 archive`**。
> **不允许**"简单任务直接执行"，也**不允许**把 `archive_task` 写成执行者
> 必做第 4 步。

### 第 1 步：task

在动手之前，**第一动作**是把"做什么、谁验收、可否派发子任务"落到
`_lifecycle/inbox/`（或认领已有 task）：

- 作为 leader 接到 `ADMIN` 的需求 → 写
  `TASK-YYYYMMDD-NNN-ADMIN-to-{role}.md`
- 作为 member 被 leader 派活 → leader 已写 task；**重读一遍**当作自审
  （Rule 0.b）；范围有偏差就落 `ISSUE-*.md` 回 leader
- 需要派给下游 → 写 `TASK-YYYYMMDD-NNN-{role}-to-{下游}.md`（Cold Path，
  见 Rule 0.a.2）

### 第 2 步：执行 / 派发

- **Hot Path**：亲自在 `workspace/<slug>/` 交付产物（必要时先
  `new_workspace(slug=...)`）。**不要**把业务产物倾倒到项目根（Rule 7.5）。
- **Cold Path**：向下游写 `TASK-*`，父 task 保持 open，等子 task 的
  `REPORT-*` 回来后再汇总（Rule 0.a.2、0.a.4）。
- 范围溢出时**停下来**——追加子 task，不要"差不多"地推进。

### 第 3 步：report（写完后停步）

调 `write_report` 落 `REPORT-*-{role}-to-{上游}.md`，回执必须包含：

- 状态：`done` / `in_progress` / `blocked`
- 产物清单（`workspace/<slug>/...` 等具体路径）
- 验证证据（命令、输出、HTTP 码、测试结果）
- 阻塞项 / 待决策项
- 引用原 task ID（`references=["TASK-..."]`）

**写 report 后停止**（Rule 0.a.6）：等上游 review / 返工 / 验收。聊天里
"做完了"**不算** report。

### 第 4 步：等待验收 / 按授权 archive

- **执行者默认不**调用 `archive_task`（Rule 0.a.5）。
- 由 `leader` / `ADMIN` 验收 report 后归档到 `_lifecycle/archive/`。
- 仅当 task 正文或 `ADMIN` **明确授权**"做完直接 archive"时，执行者才可
  自行 `archive_task`。
- 文件进 `_lifecycle/done/` **不等于**业务验收通过（Rule 0.a.3）。

---

### 例外条款（很窄）

上游**明确**说"这件事不用走流程"（纯问答 / 读文件）时，先落
`drop_suggestion` 说明跳过原因，**然后**才直接回答。**默认走完整闭环，
例外要留痕**。

---

<!-- END_TEAM_ZH -->

<!-- BEGIN_TEAM_EN -->
## Workflow hard constraint (applies to every role / no exceptions)

> Role-side translation of `fcop-rules.mdc` Rule 0.a / Rule 0.a.1–0.a.6.
> **Every** incoming piece of work MUST follow:
> **`task → execute/dispatch → report → await acceptance / archive when
> authorised`**. No "simple tasks may run directly"; do **not** list
> `archive_task` as a mandatory executor step.

### Step 1 — task

Before doing anything, land scope, acceptor, and dispatch permission under
`_lifecycle/inbox/` (or claim an existing task):

- Leader receiving `ADMIN` → `TASK-YYYYMMDD-NNN-ADMIN-to-{role}.md`
- Member dispatched by leader → re-read the task as self-review (Rule 0.b);
  file `ISSUE-*.md` if scope drifts
- Dispatch downstream → `TASK-YYYYMMDD-NNN-{role}-to-{downstream}.md`
  (Cold Path, Rule 0.a.2)

### Step 2 — execute / dispatch

- **Hot Path**: deliver under `workspace/<slug>/` (`new_workspace` first).
  Do not dump artefacts at project root (Rule 7.5).
- **Cold Path**: write downstream `TASK-*`, keep parent open, wait for child
  `REPORT-*`, then consolidate (Rule 0.a.2, 0.a.4).
- If scope drifts, **stop** and append a sub-task.

### Step 3 — report (then stop)

Call `write_report` for `REPORT-*-{role}-to-{upstream}.md` with status,
artefact paths, verification evidence, blockers, and task references.

**Stop after the report** (Rule 0.a.6). Chat "done" does not substitute for
a report file.

### Step 4 — await acceptance / archive when authorised

- Executors **must not** call `archive_task` by default (Rule 0.a.5).
- `leader` / `ADMIN` archives after accepting the report.
- Executors may archive only with explicit authorisation in the task or
  from `ADMIN`.
- Landing in `_lifecycle/done/` is **not** business acceptance (Rule 0.a.3).

---

### Narrow exception clause

If upstream **explicitly** skips the process (pure Q&A), land
`drop_suggestion` first, then answer. **Default is the full cycle.**

---

<!-- END_TEAM_EN -->

<!-- BEGIN_SOLO_ZH -->
## 核心工作流（硬约束 / 不允许例外）

> `fcop-rules.mdc` Rule 0.a / Rule 0.a.1–0.a.6 在 solo `ME` 上的翻译。
> **任何** ADMIN 派发的工作必须走：
> **`task → 执行/派发 → report → 等待验收 / 按授权 archive`**。
> 不允许"简单任务直接执行"；**执行者默认不得 archive**。

### 第 1 步：task

收到 ADMIN 需求后，**第一动作**是 `write_task` 落
`_lifecycle/inbox/TASK-YYYYMMDD-NNN-ADMIN-to-ME.md`（需求、范围、验收标准、
方案）。写完**重读**——"审查者 ME"复核"提案者 ME"。

### 第 2 步：执行 / 派发

在 `workspace/<slug>/` 交付产物。范围溢出时追加子 task（frontmatter 用
`parent:` 链回父 task）。solo 通常走 Hot Path；若需拆分，按 Cold Path
等子 task 回执后再汇总（Rule 0.a.2、0.a.4）。

### 第 3 步：report（写完后停步）

`write_report` 落 `REPORT-*-ME-to-ADMIN.md`（状态、产物、证据、阻塞项、
task 引用）。**写 report 后停止**（Rule 0.a.6），等 ADMIN 验收或返工。

### 第 4 步：等待验收 / 按授权 archive

**ME 默认不**调用 `archive_task`。ADMIN 验收后归档；或 task 正文明确授权
"做完直接 archive"（Rule 0.a.5）。`_lifecycle/done/` ≠ 业务验收（Rule 0.a.3）。

---

### 为什么不允许跳步

> 一旦给"简单任务"开例外，所有任务都会自称"简单"。跳过 task/report 会
> 让协作历史不可审计——必须事后补单。

**例外**：ADMIN **明确**说"不用走流程"时，先 `drop_suggestion` 留痕，
再直接回答。

---

<!-- END_SOLO_ZH -->

<!-- BEGIN_SOLO_EN -->
## Core workflow (hard constraint / no exceptions)

> Solo `ME` translation of Rule 0.a / Rule 0.a.1–0.a.6. Every ADMIN
> request follows **`task → execute/dispatch → report → await acceptance /
> archive when authorised`**. No "simple tasks may run directly"; executors
> **must not** self-archive by default.

### Step 1 — task

First action: `write_task` to `_lifecycle/inbox/TASK-*-ADMIN-to-ME.md`.
Re-read as self-review (Rule 0.b).

### Step 2 — execute / dispatch

Deliver under `workspace/<slug>/`. Use `parent:` for sub-tasks. Solo is
usually Hot Path; Cold Path waits for child reports before consolidating.

### Step 3 — report (then stop)

`write_report` with status, artefacts, evidence, blockers, references.
**Stop after the report** (Rule 0.a.6); wait for ADMIN.

### Step 4 — await acceptance / archive when authorised

**ME must not** call `archive_task` by default. ADMIN archives after
acceptance, or the task explicitly authorises it (Rule 0.a.5).

---

### Why skipping steps is forbidden

Opening a "simple task" exception makes every task claim to be simple.
Use `drop_suggestion` when ADMIN explicitly skips the process.

---

<!-- END_SOLO_EN -->
