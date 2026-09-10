# Static GitHub Pages maintenance

GitHub Pages serves `main:/docs`. `docs/.nojekyll` keeps this an ordinary static site.
Markdown files are not converted by the host.

- Homepage source: `scripts/pages/index.template.html`.
- Python example source: `README.zh.md` (first Python fence).
- Article sources: `docs/fcop-architecture-series/*.md` and `manifest.json`.
- Shared styles and language/copy controls: `docs/site-assets/site.css` and `site.js`.
- Diagram sources: `assets/fcop-*.svg`; the builder copies the six selected diagrams.

Install build-only dependencies in a virtual environment:

```text
python -m pip install -r scripts/pages/requirements.txt
python scripts/pages/build.py --write
python scripts/pages/build.py --check
```

Commit generated HTML with the sources. The builder rewrites article links to
local HTML; other repository documents link to GitHub. It preserves the full
article body and generates a table of contents. `--check` reads files only and
detects drift. For patch-based editing environments, `--list` and `--json PATH`
emit the output without writing any file; apply the emitted content using the
approved editor instead of `--write`.

Release numbers in the homepage, installed packages, the MCP Registry, and DOI
archives have distinct meanings. Check their primary sources before updating.
Client setup examples were checked against official Codex/Cursor/uv docs on
2026-09-10. Installing an MCP package does not migrate workspaces or AGENTS.md.
