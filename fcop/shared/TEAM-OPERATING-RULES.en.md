---
protocol: fcop
version: 1
kind: rules
sender: TEMPLATE
recipient: TEAM
team: solo
doc_id: TEAM-OPERATING-RULES
updated_at: 2026-04-26
---

# solo Operating Rules

This document defines how solo mode operates — "when to write a task, what
a report looks like, when to escalate, how to self-review".

## 1. Basic routing

1. `ADMIN ↔ ME` is the only channel — direct, no intermediary.
2. "Chat-only answers" don't substitute for task files. Whatever `ADMIN`
   says in chat, `ME` must **first** write it as
   `TASK-*-ADMIN-to-ME.md` (under `tasks/`), **then** act.
3. `ME` is **not** allowed to "do first, file the task afterward" —
   this was the most common 0.6.3 violation; 0.6.4 fixes it via the
   hard constraint section in `roles/ME.md`.
4. Solo has no peer roles, so no "side dispatch" risk — but it does have
   a **"self-review bypass" risk**: `ME` must use files (not mental
   reasoning) to separate "proposer" from "reviewer".

## 2. Task dispatch rules

### ADMIN files directly to ME

In solo, every task is `ADMIN -> ME` — **no exceptions**.

| `ADMIN` says in chat | `ME` should do |
|---|---|
| "Build XX tool" | Write `TASK-*-ADMIN-to-ME.md` first, then pick a slug |
| "Change YY" | Write task, then change |
| "Fix ZZ bug" | Write task, then fix |
| "Take a look at this code" (pure consulting) | Task not strictly required; if `ME` provides advice, log it via `ISSUE-*` or `.fcop/proposals/`, don't leave it only in chat |
| "Upgrade fcop" | `ME` invokes `upgrade_fcop()` directly — this is ADMIN's direct execution authorization, no need for a task first |

> Boundary: **any instruction that produces in-project file changes must
> go through a task**; pure Q&A doesn't strictly require one. When unsure,
> file the task.

### ME does not dispatch to ADMIN

In solo `ME` cannot "send a task to ADMIN". When `ME` needs ADMIN to
decide (pick option, confirm risk, approve high-risk action), use a
**`REPORT-*-ME-to-ADMIN.md` with a "pending ADMIN decision" section** —
do not fabricate `TASK-*-ME-to-ADMIN.md`. The latter would violate the
"`ADMIN` is always the human input end" protocol convention.

## 3. Report rules

1. Every `TASK-*-ADMIN-to-ME.md` must have a matching
   `REPORT-*-ME-to-ADMIN.md`.
2. Reports must include:
   - Status (`done` / `in_progress` / `blocked`)
   - Completed content + artifact paths (pointing into `workspace/<slug>/`)
   - Blockers / pending-ADMIN-decision items
   - Verification evidence (commands run, HTTP codes seen, output captured)
3. **Verbal sync isn't a report** — what `ADMIN` reads in the chat box
   doesn't count if it's not in `REPORT-*` (Rule 0.a).
4. After ADMIN reviews, ADMIN decides when to call `archive_task()` to
   move task + report into `log/`.

## 4. Issue rules

1. `ME` should **proactively** file `ISSUE-*-ME.md` for:
   - Protocol-level conflicts ("this rule seems contradictory")
   - fcop / fcop-mcp tool bugs ("`init_solo` doesn't expose `force`")
   - Workflow violations ("I just skipped the task and went straight to
     producing artifacts")
2. Issues don't replace tasks/reports — they're **additional** memos.
3. `ME` does **not** modify the close status of an issue — `ADMIN`
   decides when to close.

## 5. Self-review (Rule 0.b in solo)

Solo has only one AI, but Rule 0.b "no single AI completes decision-to-
execution alone" still applies. Concretely:

1. After receiving a task, **first write it as a file** — this freezes
   "proposer ME" into a file.
2. Before acting, **re-read what you just wrote** — this is "reviewer
   ME" cross-checking "proposer ME" (goals correct? scope creep?
   acceptance criteria clear?).
3. For complex tasks, write a `_plan.md` under `workspace/<slug>/`,
   re-read it before executing.
4. When writing the report, **re-read the task** — make sure the report
   actually answers every point of the task.

The file IS the second role. That's how solo discipline holds.

## 6. Escalation conditions

`ME` must explicitly mark "pending ADMIN decision" in the report
(rather than self-execute) when:

- Task scope clearly exceeds ADMIN's wording (interpretation gap)
- High-risk action (deleting data, `git push --force`, modifying
  `.cursor/rules/*.mdc`, `fcop.json`, or `shared/` protocol files)
- External dependency unavailable / blocking / costly / triggers security
- Multiple solutions with trade-offs (perf vs simplicity vs compatibility)
- ADMIN's instruction conflicts with FCoP protocol — never silently
  comply; file `ISSUE-*` or `.fcop/proposals/` for ADMIN to arbitrate

## 7. High-risk action rules

Solo has no "second confirmer" — so `ME` must explicitly write down,
in the task / report:

- This is a high-risk action (reason)
- I plan to do it like this (specific commands / steps)
- Rollback plan

Write it down, then execute. If you can't even write a rollback plan,
**don't execute** — file an issue and wait for ADMIN.

## 8. Documents and archival

1. Process files go in `tasks/` / `reports/` / `issues/`, **append-only**
   (issue close is a protocol-permitted exception).
2. Shared knowledge / long-term conventions go in `shared/`, in-place
   updates allowed.
3. Business artifacts (code, data, scripts) go **entirely** in
   `workspace/<slug>/`, **never** the project root.
4. After loop closure, **ADMIN** calls `archive_task()` (`ME` doesn't
   archive on its own unless task explicitly authorizes "archive after
   completion").

## 9. Operating ethos

The goal of solo isn't "AI gets it done quickly" — it's "even with one
AI, no discipline is dropped".

- Slower is fine; skipping task / report is not.
- Simple tasks **also** can't skip task / report — once you let "simple"
  through, every task starts calling itself simple. This is the 0.6.3
  field-test lesson.
- When unsure, write it in the task / report for ADMIN to see; don't
  silently guess.

The file protocol is the only discipline solo doesn't deform.
