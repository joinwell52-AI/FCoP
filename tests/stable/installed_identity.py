"""Read installed candidate provenance; source imports are a hard failure."""
from __future__ import annotations

import json
import socket
import sys
from importlib.metadata import requires, version
from pathlib import Path


def offline(event, args):
    if event in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto"}:
        caller = sys._getframe(1).f_code
        if caller.co_filename != socket.__file__ or caller.co_name != "_fallback_socketpair":
            raise RuntimeError("No application networking")


def main():
    sys.addaudithook(offline)
    import fcop_mcp

    import fcop
    values = {}
    for name, module in (("fcop", fcop), ("fcop-mcp", fcop_mcp)):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(Path(sys.prefix).resolve()), path
        assert "site-packages" in path.parts
        assert module.__version__ == version(name) == "4.0.0"
        values[name] = dict(version=version(name), path=str(path), requirements=requires(name))
    print(json.dumps(values, sort_keys=True))


if __name__ == "__main__":
    main()
