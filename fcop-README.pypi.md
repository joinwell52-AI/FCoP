# FCoP — `fcop` (Python package)

**This file is the PyPI long description for the `fcop` package only** — a pure Python
library. It is **not** the MCP server; the optional IDE bridge is the **separate**
[PyPI `fcop-mcp`](https://pypi.org/project/fcop-mcp/) project.

- **FCoP protocol (what it is, no product pitch):**  
  <https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md>
- **This repository (specs, essays, source):**  
  <https://github.com/joinwell52-AI/FCoP>

## Unpublished 4.0.0rc1 candidate

This review tree targets `fcop==4.0.0rc1`, classified Beta, not Stable.
It has not been published to PyPI, merged to main, or registered as a release.
Candidate verification installs only the four fixed GitHub Actions artifacts
identified by the WP4D Manifest; do not request this candidate from an index
or upgrade an existing workspace. The copied Python-only sample under
`examples/v4/third-party/python-only/` explicitly creates a fresh 4.0 workspace.
Legacy workspace reads do not migrate or relabel files. Acceptance evidence
and any unresolved checks are recorded in `reports/FCOP-4.0-WP4D-*.md`.

## Published 3.x installation (not candidate installation)

```bash
pip install fcop
```

Runtime: **Python 3.10+**, **PyYAML** and **jsonschema** — no `fastmcp`, no `websockets`, no LLM SDK.

`fcop` gives you a **`Project` API** for creating and maintaining
`fcop/` (tasks, reports, issues, `fcop.json`, team templates) and
reading/writing the protocol’s Markdown+YAML files. The normative **rules
files** for agents (`fcop-rules.mdc`, `fcop-protocol.mdc`) ship inside the
package and can be written into a repo by `init` / `deploy` flows.

## Minimal example

```python
from fcop import Project

Project(".").init()  # e.g. dev-team; or .init_solo() for single role
```

## 0.5.x → 0.6.x

The MCP **server** moved to **`fcop-mcp`**; this wheel keeps the **library** and a
`fcop` **compat CLI** that only prints a migration message if someone still
expects the old 0.5 `fcop` command. See:  
<https://github.com/joinwell52-AI/FCoP/blob/main/docs/MIGRATION-0.6.md>

## License

MIT — <https://github.com/joinwell52-AI/FCoP/blob/main/LICENSE>

---

*Full monorepo README, essays, and the optional MCP install guide: same GitHub
repository, not the PyPI `fcop` long description.*
