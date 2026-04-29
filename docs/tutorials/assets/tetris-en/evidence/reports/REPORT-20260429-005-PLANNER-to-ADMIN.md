---
protocol: fcop
version: 1
sender: PLANNER
recipient: ADMIN
priority: P1
references:
- TASK-20260429-005
status: done
---

Status: done.

ADMIN's feedback is accepted as a blocking defect report. PLANNER's prior static inspection missed runtime gameplay problems.

Created corrective CODER task:
- `docs/agents/tasks/TASK-20260429-006-PLANNER-to-CODER.md`

Rework scope sent to CODER:
- Fix bottom locking/stacking so pieces remain on the board after landing.
- Fix motif/combination elimination so ordinary pieces do not disappear immediately, and clears are visible and player-created.
- Make at least three skins materially distinct in palette, background, cell rendering, particles, and mood; keeping five is preferred.
- Keep the game as one standalone dependency-free HTML file.
- Provide runtime-oriented verification evidence, including bottom lock, stacking, motif clear, and skin switching checks.

Process instruction to CODER:
- Do not archive the rework task until PLANNER has inspected and accepted the fix.