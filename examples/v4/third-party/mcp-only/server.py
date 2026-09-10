"""Trusted startup configuration, never a caller-supplied authorization judge."""
from __future__ import annotations

import socket
import sys
from pathlib import Path

PROFILE = "profile:wp4d-offline-demo"

_SOCKETPAIR_CODES = frozenset(
    fn.__code__
    for name in ("socketpair", "_fallback_socketpair")
    if (fn := getattr(socket, name, None)) is not None
    and hasattr(fn, "__code__")
)


def offline(event, args):
    if event not in {"socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto"}:
        return
    caller = sys._getframe(1).f_code
    if any(caller is code for code in _SOCKETPAIR_CODES):
        return
    raise RuntimeError("WP4D server network access forbidden: " + event)


def evaluator(*, profile_ref, issuer, proof):
    # Educational fixed Profile; not a production credential validation scheme.
    return "AUTHORIZED" if (profile_ref, issuer, proof) == (PROFILE, "ME", "demo-only") else "DENIED"


if __name__ == "__main__":
    sys.addaudithook(offline)
    from fcop_mcp.server import create_server
    server = create_server(Path(sys.argv[1]), trusted_profiles={PROFILE: evaluator})
    server.run(transport="stdio", show_banner=False)
