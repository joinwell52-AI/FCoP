---
protocol: fcop
version: 1
sender: PLANNER
recipient: CODER
priority: P2
thread_key: creative-tetris-variant
subject: 'Implement single-file game: Comet Loom'
references:
- TASK-20260429-002-ADMIN-to-PLANNER.md
---

## Goal

Build a single-file, dependency-free HTML game named **Comet Loom**. It should be inspired by falling-block games but should not feel like ordinary Tetris with a new coat of paint. The core fantasy is that the player is weaving a living cosmic tapestry from falling comet-thread shapes.

## Theme

The board is a vertical loom suspended in space. Falling pieces are not blocks; they are **thread constellations**: glowing knots, ribbons, sparks, and comet tails. The player is trying to weave stable myth-patterns before the loom overflows.

Tone: dreamlike, kinetic, slightly strange, playful. The game should feel like weaving weather and starlight, not stacking bricks.

## Required Format

- Deliver exactly one playable HTML file.
- No external dependencies, CDNs, image assets, fonts, or build tools.
- All CSS and JavaScript must be embedded in the HTML file.
- Put the artifact under a new or existing `workspace/<slug>/` folder.

## Core Mechanics

Start from familiar falling-piece controls, then add these twists:

1. **Thread Shapes**
   - Use tetromino-like and pentomino-like shapes, but present them as thread constellations.
   - Pieces can move, rotate, soft drop, hard drop, and show a ghost preview.

2. **Weaving Instead Of Line Clearing**
   - Horizontal full rows still clear, but call them **completed weft lines**.
   - Add a second scoring layer: matching three or more same-colored cells diagonally or orthogonally after a lock creates a **motif burst** for bonus points.
   - Motif bursts should remove those matched cells or convert them into fading spark particles, then let empty spaces remain. Do not implement gravity collapse unless it is simple and stable.

3. **Loom Tension Meter**
   - The player has a `Tension` meter from 0 to 100.
   - Clearing weft lines lowers tension.
   - Locking pieces without clearing raises tension slightly.
   - At high tension, the drop speed increases and the background/effects become more intense.
   - At 100 tension, trigger game over with a dramatic loom-snap effect.

4. **Three Active Charms / Items**
   - `Needle`: deletes one chosen column or the column under the current piece.
   - `Knot`: freezes the current piece in place and turns all cells in it into wild color cells for motif matching.
   - `Gale`: shifts the whole board one cell left or right, wrapping empty space, with particle wind effects.
   - Charms should be earned from clearing lines, reaching combos, or collecting special glowing cells.
   - Use one key, such as `X`, to activate the currently held charm.

5. **Combo Identity**
   - Consecutive clears/motif bursts create named combo states: `Whisper`, `Chorus`, `Aurora`, `Myth`.
   - Show a short animated text label when a combo tier is reached.

## Skins

Include at least five selectable skins. They must change palette and mood, not just one accent color.

Suggested skins:

- `Deep Aurora`: cyan, violet, midnight blue.
- `Solar Loom`: gold, coral, hot magenta.
- `Rain Archive`: slate, teal, silver, rainy streaks.
- `Moss Galaxy`: green, amber, dark forest.
- `Paper Lanterns`: cream, red, ink, warm glow.

Persist the selected skin in `localStorage`.

## Effects

Include polished visual feedback:

- Animated background per skin, implemented with CSS and/or canvas.
- Glowing cells with gradients or highlights.
- Particle bursts on line clears, motif bursts, charm use, and game over.
- Screen shake or board pulse on major events.
- Floating score/combo text.
- Smooth overlay for start, pause, and game over.

## Controls

Support keyboard controls:

- Left/right: arrows or A/D.
- Rotate: up/W, optional counter-rotate Z.
- Soft drop: down/S.
- Hard drop: Space.
- Hold or reserve piece: C, if implemented.
- Use charm: X.
- Pause: P.

Include simple clickable/touch controls for smaller screens.

## UI Requirements

Show:

- Score.
- Best score persisted in `localStorage`.
- Level or speed tier.
- Tension meter.
- Current charm.
- Next piece preview.
- Skin selector.
- Brief in-game rules/controls panel.

## Acceptance Criteria

- Opening the HTML file in a browser starts a playable game without dependencies.
- The game has a clear name: `Comet Loom`.
- It is recognizably falling-piece inspired but feels creatively distinct from standard Tetris.
- It includes five skins, active charms/items, effects, scoring, pause/restart, and game-over flow.
- The implementation remains a single HTML file.
- CODER must not modify FCoP protocol files unless PLANNER creates a separate task authorizing it.

## Reporting Back

When complete, write a report to PLANNER with:

- Artifact path.
- Feature checklist.
- Verification performed.
- Any known limitations or browser assumptions.