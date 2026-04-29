---
protocol: fcop
version: 1
sender: PLANNER
recipient: CODER
priority: P1
thread_key: creative-tetris-variant-rework
subject: Rework Comet Loom blocking gameplay defects
references:
- TASK-20260429-005-ADMIN-to-PLANNER.md
- TASK-20260429-003-PLANNER-to-CODER.md
---

## Context

ADMIN manually reviewed `workspace/comet-loom/comet-loom.html` and found blocking gameplay defects. PLANNER's prior static acceptance was too shallow; runtime behavior must be fixed and verified.

## Artifact To Rework

- `workspace/comet-loom/comet-loom.html`

Keep the delivery as a **single dependency-free HTML file**.

## Blocking Defects To Fix

1. **Blocks disappear at the bottom instead of stacking**
   - Falling pieces must lock into the board when they reach the floor or another piece.
   - Locked cells must remain visible and stackable unless a deliberate clear rule removes them.
   - The current behavior likely clears the newly locked piece immediately through motif detection because every cell in a piece shares one color and any 3+ connected same-color cells qualify as a motif. Fix the rules so ordinary piece lock does not instantly erase the piece.

2. **Combination / motif elimination is not actually playable or visible**
   - Motif elimination must be visible, understandable, and triggered by player-created combinations, not by every normal piece.
   - Recommended fix: make each falling piece contain mixed cell colors, or mark newly locked cells and only run motif detection against meaningful post-lock board groups that include prior board cells.
   - Define a clear motif rule in UI text, for example: 3+ matching cells connected orthogonally/diagonally after lock, excluding a plain fresh piece unless it connects to existing cells.
   - Add clear feedback: highlight matched cells briefly, then particle burst and remove them.
   - Keep horizontal weft-line clears working independently.

3. **Skins feel like only one type**
   - ADMIN expects at least three genuinely distinct skins. Existing five names are fine, but their visual treatment must be noticeably different in play.
   - At minimum, make three skins clearly distinct through background, cell rendering, particle palette, and mood:
     - `Deep Aurora`: neon cosmic aurora.
     - `Solar Loom`: warm gold/magenta solar flare.
     - `Paper Lanterns` or another skin: ink/lantern/warm paper style.
   - Prefer keeping all five skins, but make at least three meaningfully different.
   - Skin changes must be obvious immediately without restarting, and selected skin must persist in `localStorage`.

## Verification Requirements

CODER must perform and report these checks:

- Start a new game and let a piece fall to the bottom; confirm it remains on the board after locking.
- Drop at least a second piece onto or near the first; confirm stacking works.
- Trigger or deliberately construct a motif clear; confirm the matched cells are visibly removed with effects.
- Switch between at least three skins and confirm the appearance is materially different.
- Re-run static checks for no external dependencies and no editor lints.

## Acceptance Criteria

- The core falling-piece stacking loop works.
- Combination/motif elimination exists, is visible, and no longer deletes every ordinary locked piece immediately.
- At least three skins are visually distinct; five distinct skins is preferred.
- The game remains one standalone HTML file with no external dependencies.
- CODER writes a completion report back to PLANNER with the changed behavior and verification evidence.

## Important

Do not archive this task until PLANNER has inspected and accepted the rework.