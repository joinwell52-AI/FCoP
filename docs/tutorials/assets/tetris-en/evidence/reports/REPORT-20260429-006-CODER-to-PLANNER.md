---
protocol: fcop
version: 1
sender: CODER
recipient: PLANNER
priority: P1
references:
- TASK-20260429-006
status: done
---

# Comet Loom Rework Report

## Artifact

- `workspace/comet-loom/comet-loom.html`

## Changed Behavior

- Fixed the core stacking loop: normal locked pieces now remain on the board instead of being immediately removed by motif detection.
- Changed falling pieces from single-color shapes to mixed-color thread constellations, so ordinary locks do not automatically form same-color motif groups.
- Reworked motif detection so a motif requires newly locked cells to connect with older board cells in a 3+ orthogonal/diagonal matching group. A plain fresh piece alone is explicitly excluded.
- Added visible motif staging: matched cells are marked/highlighted briefly, then removed with particle bursts.
- Kept horizontal weft-line clears independent from motif clears.
- Strengthened skins with distinct body backgrounds and canvas cell rendering modes. `Deep Aurora`, `Solar Loom`, `Rain Archive`, `Moss Galaxy`, and `Paper Lanterns` now use different moods/patterns; at least `Deep Aurora`, `Solar Loom`, and `Paper Lanterns` are visibly distinct immediately on selection.
- Updated the rules text to explain the corrected motif rule.

## Verification Performed

- Static dependency scan with ripgrep for `http(s)://`, `<script src>`, `<link href>`, `@import`, and `cdn`: no matches found.
- IDE lint check for `workspace/comet-loom/comet-loom.html`: no linter errors reported.
- Node syntax/token check against the single embedded script: `PASS syntax, single embedded script, no missing rework tokens`.
- Headless gameplay simulation against the embedded game logic:
  - Started a new game and hard-dropped the first piece; confirmed locked cells remained on the board.
  - Hard-dropped a second piece; confirmed board cell count increased, showing stacking works.
  - Constructed an explicit motif with two older cells plus one fresh matching cell; confirmed the group was marked/highlighted first, then removed after the delay.
  - Switched `Deep Aurora`, `Solar Loom`, and `Paper Lanterns`; confirmed distinct skin classes/render paths.
  - Result: `PASS headless gameplay simulation: first lock persists, second stacks, constructed motif marks then removes, three skins switch distinctly`.

## Known Limitations / Browser Assumptions

- Verification used a Node-based mocked DOM/canvas simulation rather than a manually launched browser window in this environment.
- The game still assumes a modern browser with Canvas 2D and CSS custom property support. A small Canvas `roundRect` polyfill remains included.
- Motif clears intentionally leave empty spaces after removal; gravity collapse is still not implemented, matching the original brief.

## Archive Status

- Not archived. PLANNER explicitly instructed: `Do not archive this task until PLANNER has inspected and accepted the rework.`