"""One-shot injector: prepend the "workflow hard constraint" section to
every bundled role charter under ``src/fcop/teams/_data/*/roles/*.md``.

Why this exists. 0.6.3 shipped 17 role charters whose only enforcement
of the canonical ``task → do → report → archive`` cycle was prose,
spread across "Responsibilities" / "Working principles" / "Common
mistakes". In the field that prose got softened to "simple tasks may
run directly" — the exact pattern that let agents skip the file
trail. 0.6.4 fixes it as a *bug*, not a feature: every charter now
opens with a hard-constraint section right under its main heading
that translates ``fcop-rules.mdc`` Rule 0.a.1 into a role-side
4-step contract with no exception clause for "simple" work.

The injector is idempotent — if a charter already contains the
canonical anchor (``"工作流硬约束"`` for zh, ``"Workflow hard
constraint"`` for en) it is skipped. solo/roles/ME.md was hand-
authored with the constraint already in place; it stays untouched.

Run from the repo root::

    py -3.12 scripts/inject_workflow_constraint.py

The script writes to disk and prints a per-file action summary so a
follow-up ``git diff`` shows exactly what landed.
"""

from __future__ import annotations

import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
ROLES_GLOB = "src/fcop/teams/_data/*/roles/*.md"

ZH_ANCHOR = "## 工作流硬约束"
EN_ANCHOR = "## Workflow hard constraint"

# zh template — {role} placeholder is replaced with the role code
# pulled out of the frontmatter (e.g. "PM", "DEV", "LEAD-QA").
ZH_BLOCK = """\
## 工作流硬约束（适用于所有角色 / 不允许例外）

> 这一节是 `fcop-rules.mdc` Rule 0.a / Rule 0.a.1 在角色侧的具体翻译。
> **任何**收到的工作（无论看起来多简单）必须**严格按 4 步走**：
> `task → 做 → report → archive`。**不允许**"简单任务直接执行"
> 这种软约束——一旦给"简单任务"开例外，所有任务都会自称"简单"。

### 第 1 步：先写 task

在动手之前，**第一动作**是把"做什么"落到 `docs/agents/tasks/`：

- 作为 leader 接到 `ADMIN` 的需求 → 写
  `TASK-YYYYMMDD-NNN-ADMIN-to-{role}.md`
- 作为 member 被 leader 派活 → leader 已经写了 task，自己**重读一遍**
  当作自审（Rule 0.b）；范围有偏差就落 `ISSUE-*.md` 回 leader，不
  要"差不多照着做"
- 需要派给下游 → 写
  `TASK-YYYYMMDD-NNN-{role}-to-{下游}.md`

### 第 2 步：再做

把代码 / 脚本 / 数据 / 内容落到 `workspace/<slug>/`（必要时先
`new_workspace(slug=...)`）。**不要**把业务产物倾倒到项目根（Rule 7.5）。

执行过程中如果范围溢出 task，**停下来**——回第 1 步追加一份子 task，
不要"反正差不多"地推进。

### 第 3 步：再写 report

调 `write_report` 落 `REPORT-*-{role}-to-{上游}.md`，回执必须包含：

- 状态：`done` / `in_progress` / `blocked`
- 产物清单（指向具体路径，例如 `workspace/<slug>/...`）
- 验证证据（跑了什么命令、看到什么输出 / HTTP 码 / 测试结果）
- 阻塞项 / 待决策项
- 引用原 task 的 ID（`references=["TASK-..."]`）

聊天里那段"做完了"的总结**不算** report。`REPORT-*.md` 不存在 = 工作没发生。

### 第 4 步：再 archive

leader（或 `ADMIN`）验收 report 后调 `archive_task` 把 task + 对应
report 搬到 `log/`。**默认不主动 archive**——除非派单里明确授权
"做完直接 archive"。

---

### 例外条款（很窄）

如果上游在派单里**明确**说"这件事不用走流程"（典型场景：纯问答 /
查询 / 读个文件），落一份 `drop_suggestion` 备忘说明跳过原因，**然后**
才直接回答。**默认走 4 步，例外要留痕**。

---

"""

EN_BLOCK = """\
## Workflow hard constraint (applies to every role / no exceptions)

> This section translates `fcop-rules.mdc` Rule 0.a / Rule 0.a.1 onto
> the role side. **Every** incoming piece of work (no matter how
> trivial it looks) MUST follow the four-step cycle:
> `task → do → report → archive`. The "simple tasks may run directly"
> soft-constraint is **NOT permitted** — open that exception once and
> every task will start claiming to be "simple".

### Step 1 — write the task first

Before doing anything, the **first action** is to land "what we're
about to do" under `docs/agents/tasks/`:

- Acting as leader receiving an `ADMIN` request → write
  `TASK-YYYYMMDD-NNN-ADMIN-to-{role}.md`.
- Acting as member dispatched by your leader → the leader already
  wrote the task; **re-read it once as a self-review** (Rule 0.b).
  If scope drifts, file an `ISSUE-*.md` back to the leader instead
  of "close enough".
- Need to dispatch downstream → write
  `TASK-YYYYMMDD-NNN-{role}-to-{downstream}.md`.

### Step 2 — do the work

Land code / scripts / data / content under `workspace/<slug>/`
(create with `new_workspace(slug=...)` first if needed). Do **not**
dump artefacts at the project root (Rule 7.5).

If scope drifts mid-execution, **stop** — go back to Step 1 and add
a sub-task. Don't "close enough" your way forward.

### Step 3 — write the report

Call `write_report` to land `REPORT-*-{role}-to-{upstream}.md`. It
must contain:

- Status: `done` / `in_progress` / `blocked`.
- Artefact list (concrete paths, e.g. `workspace/<slug>/...`).
- Verification evidence (commands run, output observed,
  HTTP codes, test results).
- Blockers / open decisions.
- Reference to the originating task ID
  (`references=["TASK-..."]`).

The "I'm done" line in chat does **not** count as a report. No
`REPORT-*.md` on disk = the work did not happen.

### Step 4 — then archive

After the leader (or `ADMIN`) accepts the report, call
`archive_task` to move the task + matching report into `log/`.
**Don't self-archive by default** unless the dispatch explicitly
authorised "archive on completion".

---

### Narrow exception clause

If the upstream **explicitly** says in the dispatch "skip the
process for this one" (typical: pure Q&A / lookup / file read),
land a `drop_suggestion` memo explaining the skip, **then** answer
directly. **The default is the 4-step cycle; every exception must
leave a trace.**

---

"""


_FRONTMATTER_RE = re.compile(
    r"^---\n(?P<body>.*?)\n---\n", re.DOTALL
)
_ROLE_FIELD_RE = re.compile(r"^role:\s*(\S+)\s*$", re.MULTILINE)


def _is_english(path: pathlib.Path) -> bool:
    return path.name.endswith(".en.md")


def _extract_role(text: str) -> str | None:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    role_match = _ROLE_FIELD_RE.search(match.group("body"))
    if not role_match:
        return None
    return role_match.group(1)


def _inject(path: pathlib.Path) -> str:
    """Return one of: ``"injected"`` / ``"already-has-anchor"`` /
    ``"skipped-no-h1"`` / ``"skipped-no-role"``.

    The H1 heading line is the anchor we splice after — it's
    consistent across both languages (``# PM 岗位职责`` /
    ``# PM — Role Charter``). Anything else (frontmatter, blank
    lines) stays in front of the H1.
    """
    text = path.read_text(encoding="utf-8")
    is_en = _is_english(path)
    anchor = EN_ANCHOR if is_en else ZH_ANCHOR

    if anchor in text:
        return "already-has-anchor"

    role = _extract_role(text)
    if role is None:
        return "skipped-no-role"

    block_template = EN_BLOCK if is_en else ZH_BLOCK
    block = block_template.replace("{role}", role)

    h1_re = re.compile(r"^# .+$", re.MULTILINE)
    h1_match = h1_re.search(text)
    if h1_match is None:
        return "skipped-no-h1"

    # Insert immediately after the H1 line (and the blank line that
    # follows it, so the existing visual rhythm survives). We anchor
    # on the index of the **next** heading after the H1; if none,
    # fall back to inserting right after the H1.
    insert_at = h1_match.end()
    # Skip the trailing newline already consumed by `end()`; we want
    # the block to start on a fresh blank line so the rendered output
    # has a clean separator under the H1.
    new_text = (
        text[:insert_at] + "\n\n" + block.rstrip() + "\n" + text[insert_at:]
    )
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return "injected"


def main() -> int:
    files = sorted(REPO_ROOT.glob(ROLES_GLOB))
    if not files:
        print(f"no role files matched glob {ROLES_GLOB!r} under {REPO_ROOT}")
        return 1

    counts: dict[str, int] = {}
    for path in files:
        action = _inject(path)
        counts[action] = counts.get(action, 0) + 1
        rel = path.relative_to(REPO_ROOT)
        print(f"  {action:20s}  {rel}")

    print()
    print("Summary:")
    for action, count in sorted(counts.items()):
        print(f"  {action:20s}  {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
