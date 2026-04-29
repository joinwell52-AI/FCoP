---
protocol: fcop
version: 1
sender: ME
recipient: ADMIN
priority: P2
references:
- TASK-20260429-001
status: done
---

Completed the requested single-file Tetris-style game.

Artifact:
- `workspace/nebula-stack/index.html`

What it includes:
- Game name: Nebula Stack.
- Single HTML file, no external dependencies.
- Playable falling-block mechanics with move, rotate, soft drop, hard drop, hold, next preview, scoring, levels, combos, pause, restart, and persistent best score.
- Power items: Bomb, Stasis, and Prism, collected from glowing item blocks when lines clear.
- Skins: Aurora Candy, Ember Arcade, and Moonstone Mono, selectable in-game and saved locally.
- Effects: animated starfield background, glowing blocks, ghost piece, line-clear particles, floating score text, combo messaging, and screen shake.
- Touch controls for smaller screens.

Verification:
- Re-read the generated artifact start/end to confirm it is a complete HTML document.
- Checked editor diagnostics for `workspace/nebula-stack/index.html`; no linter errors were reported.