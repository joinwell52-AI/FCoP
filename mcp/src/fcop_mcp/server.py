"""Canonical server bound only by process configuration, never by a tool."""
import os
from pathlib import Path

from fcop_mcp.registry import create_server

mcp = create_server(Path(os.environ.get("FCOP_PROJECT_DIR", Path.cwd())))
