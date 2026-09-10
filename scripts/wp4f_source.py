"""Source-only parity smoke; explicitly not a clean-room installation proof."""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from wp4f_consume import execute, python_reopen


def main():
    repo = Path.cwd()
    work = Path(tempfile.mkdtemp(prefix="wp4f-source-"))
    applications, logs = work / "applications", work / "logs"
    shutil.copytree(repo / "tests/stable/third-party", applications)
    logs.mkdir()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
           "PYTHONPATH": os.pathsep.join(str(p) for p in (repo, repo / "src", repo / "mcp/src"))}
    python = python_reopen(sys.executable, applications / "python-only/app.py",
                           work / "python-project", logs, env, source=True)
    mcp = execute([sys.executable, "-B", str(applications / "mcp-only/client.py"),
                   str(work / "mcp-project"), "--source"],
                  logs / "mcp-source.log", cwd=work, env=env)
    print(json.dumps({"proof_class": "SOURCE_ONLY", "python": python, "mcp": mcp,
                      "evidence": str(logs)}, sort_keys=True))


if __name__ == "__main__":
    main()
