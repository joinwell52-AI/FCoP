# FCoP — `fcop` (Python package)

**This file is the PyPI long description for the `fcop` package only** — a pure Python
library. It is **not** the MCP server; the optional IDE bridge is the **separate**
[PyPI `fcop-mcp`](https://pypi.org/project/fcop-mcp/) project.

- **FCoP protocol (what it is, no product pitch):**  
  <https://github.com/joinwell52-AI/FCoP/blob/main/docs/getting-started.en.md>
- **This repository (specs, essays, source):**  
  <https://github.com/joinwell52-AI/FCoP>

## FCoP 4.0.0 Stable

4.0.0 promotes the accepted RC without new protocol or tool business behavior.
Workspace identity, four envelopes, Branch, explicit convergence, authorization,
durable idempotency, atomic recovery and rule distribution are provided by Core.
Existing 3.x workspaces retain legacy semantics; installing does not migrate,
redeploy rules or modify other applications. Historical RC 4.0.0rc1 is retained.

## Installation

```bash
python -m pip install fcop==4.0.0
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

from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory(prefix="fcop-demo-") as directory:
    project = Project(Path(directory) / "workspace")
    workspace = project.create_workspace(protocol_version="4.0")
    print(workspace["workspace_id"])
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
