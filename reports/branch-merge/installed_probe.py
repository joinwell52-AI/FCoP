"""Run with -I in a fresh wheel-installed environment (pytest is test-only)."""
from __future__ import annotations

import sys
import tempfile
from importlib.metadata import version
from pathlib import Path


def main() -> None:
    import fcop
    import fcop_mcp

    for name, module in (("fcop", fcop), ("fcop-mcp", fcop_mcp)):
        assert version(name) == "4.0.1"
        assert Path(module.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
        print(name, version(name), module.__file__, flush=True)
    # Only test support is loaded from the checkout. Core/MCP remain installed.
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from tests.test_fcop.test_branch_merge import test_process_death_and_restart, test_real_cross_process_merge
    from tests.test_fcop_mcp.test_branch_merge_stdio import test_real_stdio_branch_merge_and_restart

    with tempfile.TemporaryDirectory(prefix="fcop-401-installed-") as directory:
        root = Path(directory)
        test_real_stdio_branch_merge_and_restart(root / "stdio")
        for mode in ("same-operation", "different-operation", "legacy", "different-content"):
            test_real_cross_process_merge(root / mode, mode)
        for stage in ("PREPARED", "TARGET_DURABLE", "COMMITTED", "RESPONSE_LOST"):
            test_process_death_and_restart(root / stage, stage)
    print("INSTALLED_WHEEL: 49/12/4; stdio 3 tools; 4 races; 4 crash/restart boundaries PASS", flush=True)


if __name__ == "__main__":
    main()
