---
title: FCoP Grew a Project Tree
published: true
description: "How a Grid Runner mini-game task on CodeFlowMu revealed parent, thread_key, Phase dispatch, and CHILD_TASKS_OPEN archives forming a project tree — and why FCoP needs additive spec/0003."
tags: ai, agents, fcop, governance
cover_image: https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-cover.png
canonical_url: https://github.com/joinwell52-AI/FCoP/blob/main/essays/from-mini-game-to-project-tree.en.md
---

![Cover · FCoP Grew a Project Tree](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-cover.png)

# FCoP Grew a Project Tree

**Subtitle: How a Mini-Game Task Revealed Product Evolution Inside a Multi-Agent Workflow**

Author: FCoP Maintainer · 2026-06-14

Note: Some screenshots are from the Chinese CodeFlowMu console. They are included as workflow evidence; the key protocol signals are the task IDs, lifecycle states, and FCoP fields explained in the captions.

I originally wanted the PM in CodeFlowMu to coordinate DEV, OPS, and QA around a small local mini-game.

The game turned out not to be the important part.

The task tree was.

During one failed archive attempt, FCoP exposed something that had not yet been formally written into the protocol: **a project tree**.

This article is not really about the Grid Runner game itself. It is about a structural change that appeared while debugging a multi-agent workflow: FCoP was designed to manage task flow. In this run, it started to express product evolution.

---

## 1. Why Start with a Mini-Game?

**FCoP** is a multi-agent collaboration protocol. Its core idea is simple: agents should not only “talk” in chat. Their work must land as files. Tasks, reports, review records, and lifecycle transitions all live inside the project directory, so that anyone can later inspect what happened, who did what, and whether the work was actually closed.

**CodeFlowMu** is an AI collaboration workflow system built on top of FCoP. As ADMIN, I use a Web console to assign work to PM. PM then decomposes the work for DEV, OPS, and QA. The console makes the workflow easier to operate, but the real ledger still lives on disk: `TASK-*.md`, `REPORT-*.md`, and the lifecycle folders under `fcop/_lifecycle/`.

This test was not meant to build a large product. It was meant to check whether multiple roles could complete a full collaboration loop around a small target:

```text
ADMIN creates task → PM decomposes → DEV/OPS/QA execute → REPORT → review → archive
```

So I chose a very small probe: **Grid Runner**.

Grid Runner is a local HTML / CSS / JavaScript mini-game. The player moves on a grid, collects coins, avoids monsters, and reaches an exit. The rules are simple, but the task is still rich enough for DEV to implement, OPS to verify the local runtime path, and QA to actually play and score it.

![Grid Runner gameplay screenshot](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-fig2-gameplay.png)

*Figure 1. The small game used as the workflow probe. The game itself was intentionally simple; the real test was whether PM, DEV, OPS, and QA could complete the FCoP loop around it.*

On June 13, I assigned the first task to PM through the console:

```text
TASK-20260613-020
Grid Runner v0.1
thread_key: panel-task-020
```

PM followed the normal workflow and assigned work to DEV, OPS, and QA. After the reports came back, task 020 entered `done`.

At this point, everything looked ordinary. Nobody mentioned a “project tree.” Nobody mentioned “phase tasks.” It looked like a single completed task line.

---

## 2. Phase 2 Arrived, But I Had Not Yet Seen the Tree

After the first version was accepted, the product did not stop.

I assigned a second task to PM:

```text
TASK-20260614-004
Grid Runner Phase 2: product upgrade
references:
  - TASK-20260613-020
thread_key: panel-task-020
```

The goal of 004 was to turn the demo into a more product-like lightweight game: a main menu, five levels, power-ups, local progress storage, a result screen, and visual effects.

PM then decomposed it:

```text
005 DEV  Implement Phase 2
006 OPS  Verify file:// execution
007 QA   Playtest and accept
008 DEV  Fix the missing magnet tile in level 4
009 OPS  Re-check the fix
```

At the time, I only saw this as “the next segment on the same line.” Task 020 was already complete; task 004 was the follow-up upgrade. My mental model was still a single-task model: **once 020 is done, it should be archivable.**

In the console, under `panel-task-020`, the structure was already visible: ADMIN-to-PM tasks 020 and 004 above, and PM-to-team execution tasks below. The tree was already on screen. I just had not yet read it as a tree.

![CodeFlowMu console archive view](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-fig3-panel-zh-full.png)

*Figure 2. CodeFlowMu console view. The UI is in Chinese, but the important protocol markers are the task IDs, `panel-task-020`, `report_missing`, and lifecycle states.*

---

## 3. The Archive Failed, and I Saw the Project Tree for the First Time

On the morning of June 14, I clicked “Archive” on task 020 in the CodeFlowMu console.

Task 020 was the initial Grid Runner version. DEV, OPS, and QA had all reported back. PM had already submitted a summary. The console showed it as completed. I expected it to move into `_lifecycle/archive/`.

But the archive did not go through.

The core message was: there were still open child tasks. At the protocol level, this was `CHILD_TASKS_OPEN`.

I asked PM in the ADMIN ↔ PM chat:

> Do the child tasks of this one overlap with 004? Wasn’t 004 opened as a separate new task?

My confusion was concrete: 004 was clearly a later Phase 2 task. Why should it block the archive of 020?

PM answered: this was not an ID collision. It was a parent-child relationship. Task 020 still had Phase 2 task 004 underneath it. Task 004 had then produced 005, 006, and 007; the QA path further led to 008 and 009. The lower tasks had to be closed before 020 could be archived.

Then PM drew a text tree in the chat:

```text
020  Grid Runner initial version
└── 004  Phase 2
    ├── 005–007  implementation, ops check, playtest
    └── 008–009  bug fix and re-check
```

![PM drew the 020 → 004 → 005–007 tree in chat](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-fig-chat-pm-tree.png)

*Figure 3. PM explained the failed archive by drawing the task relation as a tree: 020 as the root, 004 as Phase 2, and 005–009 as execution / fix tasks.*

That was the first moment I saw the “project tree.”

It did not come from a protocol spec. It did not come from a dedicated UI prompt. It came from PM trying to explain why 020 could not be archived, by drawing the relationship that already existed on disk.

![Archive was blocked](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-fig4-archive-block.png)

*Figure 4. The archive attempt was blocked because child tasks were still open. This is where the single-task view broke down and the project-tree view became necessary.*

At that point, the meaning changed:

```text
020 was no longer just the Grid Runner v0.1 task.
020 had become the project root of the Grid Runner product line.

004 was not an independent new project.
004 was Phase 2 under 020.
```

So `CHILD_TASKS_OPEN` was not wrong.

From a single-task view, 020 was complete. From a project-tree view, the Phase 2 branch below 020 had not yet closed. A phase can be complete while the whole project tree is not yet ready to archive.

---

## 4. This Was Not AI Inventing an Organization. It Was a Shape Produced by Protocol Composition.

This was not an AI agent inventing a new project management method.

What actually mattered were several rules that already existed:

```text
thread_key       tracks the same collaboration thread
references       marks which delivery a task continues from
parent           expresses parent-child relation
REPORT           requires roles to write back results
CHILD_TASKS_OPEN prevents a parent from being archived while children are open
```

Add one ordinary behavior: after the first version was accepted, ADMIN assigned Phase 2, and PM decomposed it under the same collaboration thread.

Nobody had designed a “project tree” button. Nobody started by saying “we are building an Epic / Milestone hierarchy.” But those rules stacked together, and the disk began to express this structure:

```text
Project Root → Phase → Execution Task → Fix Task → Archive
```

In the actual Grid Runner run, it looked like this:

```text
TASK-20260613-020  Grid Runner v0.1 / project root
└── TASK-20260614-004  Phase 2 product upgrade
    ├── TASK-20260614-005  DEV implementation
    ├── TASK-20260614-006  OPS verification
    ├── TASK-20260614-007  QA playtest
    ├── TASK-20260614-008  DEV fix
    └── TASK-20260614-009  OPS re-check
```

This is what I call **controlled emergence**.

It is “emergence” because the project tree was not hard-coded in advance.

It is “controlled” because it was not random. It was constrained by the file protocol, task references, PM decomposition, and archive guards.

The rules were small. The original intention was narrow. But once a real project continued across versions, the structure appeared.

---

## 5. EVAL Also Read the Tree

After I recognized the tree in chat, I manually ran EVAL from the CodeFlowMu console.

This EVAL is not a formal audit, and it does not replace the FCoP ledger. It is an internal collaboration-state scan. It reads TASK files, REPORT files, and frontmatter under `_lifecycle/`, then writes suspected structures into `GAP-*-panel-scan.md` under `fcop/internal/eval/`.

The scan reported `project_tree_emergence`:

```text
Root task: TASK-20260613-020
Phase task: TASK-20260614-004
Execution tasks: TASK-20260614-005, 006, 007, 008
Pattern: main task -> phase task -> execution task
Value: FCoP has emerged product-evolution tree and project-management capability from task-flow management
```

This means the tree was not only an explanation PM drew in chat. The file relationships themselves were readable by a program.

Still, EVAL should be treated as heuristic cross-checking. Sometimes it also identifies smaller local fix chains as subtrees, such as `004 → 007 → 008` or `004 → 008 → 009`. Those local readings are useful, but they do not replace the canonical reading: **020 is the project root of the Grid Runner product line, and 004 is Phase 2 under it.**

![Local Fix-chain slice detected by EVAL](https://raw.githubusercontent.com/joinwell52-AI/FCoP/main/essays/assets/from-mini-game-to-project-tree-fig6-eval-gap003.png)

*Figure 5. EVAL also detected local project-tree slices. This supported the observation, but the canonical reading remains 020 → 004 → 005/006/007/008.*

So the external story should still be grounded in TASK / REPORT / archive paths. EVAL only shows that the human intuition and the programmatic scan aligned.

---

## 6. The Protocol Was Not Wrong. The Console Had Not Explained the Tree.

My confusion did not come from a protocol error.

The opposite is closer to the truth: the protocol was protecting consistency. Since open child tasks remained below the parent, the parent could not be archived.

The real issue was that the console still mainly presented the workflow as a flat task lifecycle. It had not yet exposed the Project / Phase / Execution layer.

As a result, the same screen could mix several states:

```text
done              this delivery of 020 was completed
report_missing    some child path was still missing a report
CHILD_TASKS_OPEN  the root still had open children
```

Each state made sense on its own. But together, they looked contradictory to ADMIN: if the task is done, why can it not be archived?

Once the project-tree view appears, the contradiction disappears:

```text
phase complete ≠ project tree closed
task done ≠ root node archivable
```

This is not protocol debt. It is product-expression debt.

CodeFlowMu should add three things next:

1. **The console should display Project / Phase / Execution levels**, not only a flat task list.
2. **When PM creates a Phase, the edge type must be explicit**: continue the current main line, or create an independent thread.
3. **Archive blocking should explain the tree-shaped reason**, not only show `CHILD_TASKS_OPEN`; it should list which Phase and which child task are still open.

---

## 7. The Real Value of This Emergence

ADMIN’s real intent was simple: **020 had been accepted; continue with a Phase 2 product upgrade.**

But PM made a “project-manager-like” structural choice during execution: Phase 2 was kept inside the same `panel-task-020` thread, and the disk formed a **`020 → 004` product-evolution tree**.

**That is the emergence point.** It was not simply that ADMIN phrased the request incorrectly, nor that PM wrote a wrong field. Product intent and lifecycle representation overlapped in the same collaboration thread, and the tree shape grew out of that overlap.

This was not a simple mistake. It was two layers of truth stacked together:

| Layer | Judgment |
|---|---|
| Product semantics | ✅ Reasonable. 004 really was Grid Runner Phase 2, continuing from 020. |
| Lifecycle semantics | ⚠️ Risky. If 004 enters the same thread / parent relationship before 020 is fully archived, 020 can be blocked by `CHILD_TASKS_OPEN`. |
| Protocol capability | ✅ Emergent. FCoP grew a structure from “task flow” into “project root → phase → execution line.” |
| Console expression | ❌ Insufficient. The console still presented a single-task lifecycle, so users saw `done`, `report_missing`, and `child_open` mixed together. |

Grid Runner itself was just a mini-game. **The structure produced by the collaboration was more important than the game.**

Originally, FCoP only had a task flow:

```text
ADMIN → PM → DEV/OPS/QA → REPORT → REVIEW → DONE
```

But this Grid Runner run produced another shape:

```text
Project Root → Phase → Execution Tasks → Fix Line → Final Close
```

The tree on disk looked like this, consistent with the ASCII tree PM drew in chat:

```text
TASK-20260613-020  Grid Runner v0.1 / static-game milestone
└── TASK-20260614-004  Phase 2 product upgrade
    ├── 005 DEV
    ├── 006 OPS
    ├── 007 QA
    ├── 008 DEV fix
    └── 009 OPS fix
```

This matches the internal EVAL observation: it identified `020→004→005/006/007/008` as a “main task → phase task → execution task” project tree, and judged the value as: FCoP emerged product-evolution tree and project-management capability from task-flow management.

**The final reading should be consistent across the article, archive behavior, and future spec:**

- **020 is not a standalone completed project.** **004 is Phase 2 under 020.**
- Their child tasks do not overlap, but the business line is continuous; the `thread_key` is the same, and `references` / `parent` relationships are valid.
- Therefore, **020 entering `done/` does not mean the whole tree can be archived**. As long as 004 or 007 is still open, `CHILD_TASKS_OPEN` is reasonable. It is not a console bug. It is the protocol protecting tree consistency.

The valuable discoveries are:

1. **FCoP naturally grew Project / Phase / Execution layers.** From demo to product, from version one to later versions, from main line to phase, from execution to QA, from failure to fix, and from a single task’s `done` state to whole-tree archive, everything happened inside the same collaboration thread.
2. **`parent`, `thread_key`, and `references` already carry project-tree semantics**, not just task-reference semantics.
3. **The console still treats lifecycle mostly as single-task lifecycle**, so `done`, `report_missing`, and `child_open` can appear together and confuse the user. The tree exists in files; the UI has not caught up.
4. **The protocol should absorb this capability.** When PM creates a Phase, PM must choose: **continue the current main line** or **create an independent thread**. The system should not wait for an archive failure and then rely on chat to draw the tree.

In one sentence: this was controlled emergence. Grid Runner grew from a normal task flow into a product-iteration tree. **020 is the project root, and 004 is Phase 2, not a separate project.** Nobody added a new button for this. Existing protocol rules, real execution, and archive constraints stacked together. The shape became readable, auditable, and blockable. That is the life of a protocol.

---

## Conclusion

I will remember this Grid Runner two-line run as a case of **controlled emergence** in FCoP.

The core was **not** that AI invented project management.

It was this combination:

```text
parent
thread_key
references
PM Phase planning
CHILD_TASKS_OPEN
```

Together, these rules naturally formed a project tree.

So FCoP should not avoid this phenomenon. It should absorb it.

The next step is to add **[`spec/0003-project-tree-protocol.md`](https://github.com/joinwell52-AI/FCoP/blob/main/spec/0003-project-tree-protocol.md)**（proposed） while leaving 0001 and 0002 unchanged, and define **Project / Phase / Execution / Fix / Independent Project** clearly.

**In one sentence: FCoP grew a project tree; now the protocol needs to write it down.**

---

## Evidence Behind This Observation

This section keeps only **links and key excerpts**. The full source files are not pasted here, to avoid turning the article into a log dump. Primary TASK / EVAL originals from the CodeFlowMu dogfood run are catalogued in the [evidence archive](https://github.com/joinwell52-AI/FCoP/blob/main/essays/from-mini-game-to-project-tree-evidence/INDEX.md); figures in this essay live under [`essays/assets/`](https://github.com/joinwell52-AI/FCoP/tree/main/essays/assets).

| Evidence | Reference | Why it matters |
|---|---|---|
| Original task | [`TASK-20260613-020`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/from-mini-game-to-project-tree-evidence/TASK-20260613-020-ADMIN-to-PM.md) | The original Grid Runner v0.1 task. It later became the project root. Key field: `thread_key: panel-task-020`. |
| Phase 2 task | [`TASK-20260614-004`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/from-mini-game-to-project-tree-evidence/TASK-20260614-004-ADMIN-to-PM.md) | The later Grid Runner Phase 2 task. Key field: `references: TASK-20260613-020`, same thread. |
| EVAL source report | [`GAP-20260614-004-panel-scan`](https://github.com/joinwell52-AI/FCoP/blob/main/essays/from-mini-game-to-project-tree-evidence/GAP-20260614-004-panel-scan.md) | The internal EVAL scan triggered from the console. It detected `project_tree_emergence`. |

The key fields can be compressed into four lines:

```text
TASK-20260613-020: thread_key = panel-task-020
TASK-20260614-004: references = TASK-20260613-020
EVAL: project_tree_emergence
Archive guard: CHILD_TASKS_OPEN
```

### What EVAL Observed

The internal EVAL scan identified the Grid Runner line as a project tree:

```text
TASK-20260613-020  Grid Runner v0.1 / project root
└── TASK-20260614-004  Phase 2 product upgrade
    ├── TASK-20260614-005  DEV execution
    ├── TASK-20260614-006  OPS verification
    ├── TASK-20260614-007  QA playtest
    └── TASK-20260614-008  DEV fix
```

Its canonical reading was:

```text
020 → 004 → 005 / 006 / 007 / 008
```

In other words: **main task → phase task → execution task**.

EVAL also detected smaller local fix chains, such as:

```text
004 → 007 → 008
004 → 008 → 009
```

Those local observations are useful, but they do not replace the main-line interpretation: **020 is the project root of the Grid Runner product line, and 004 is Phase 2 under 020.**

### Terminology

The table below explains the FCoP terms used in this article without requiring readers to know Chinese.

| Term | Meaning in this article | Protocol marker |
|---|---|---|
| Collaboration thread | A continuous line of work that keeps related tasks together. In this case, Grid Runner stayed under the same thread. | `thread_key`, here `panel-task-020` |
| Continues from | A task explicitly builds on an earlier task or delivery. Phase 2 continued from the v0.1 task. | `references` |
| Parent task | A task that owns or contains lower-level tasks. A parent should not be archived while its children are still open. | `parent` |
| Open child tasks | Lower-level tasks are still not fully closed. This is why the archive attempt was blocked. | `CHILD_TASKS_OPEN` |
| Internal EVAL scan | A CodeFlowMu internal scan that reads TASK / REPORT files and detects possible workflow structures. It is supporting evidence, not the formal ledger. | `GAP-*-panel-scan.md` |
| Project-tree emergence | The observed pattern where FCoP task flow began to express a product structure: project root → phase → execution → fix. | `project_tree_emergence` |

## Further reading

- **FCoP repository**: [https://github.com/joinwell52-AI/FCoP](https://github.com/joinwell52-AI/FCoP)
