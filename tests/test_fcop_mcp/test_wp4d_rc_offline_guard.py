"""Exercise the example's real audit hook only in an isolated subprocess."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_wp4d_rc_offline_guard_stdlib_identity_and_network_denials():
    server = Path(__file__).resolve().parents[2] / "examples/v4/third-party/mcp-only/server.py"
    code = r'''
import json
import runpy
import socket
import sys

sample = runpy.run_path(sys.argv[1], run_name="wp4d_guard_test")
allowed = sample["_SOCKETPAIR_CODES"]
assert isinstance(allowed, frozenset)
expected = [fn.__code__ for name in ("socketpair", "_fallback_socketpair")
            if (fn := getattr(socket, name, None)) is not None and hasattr(fn, "__code__")]
assert len(allowed) == len({id(code) for code in expected})
assert all(any(code is original for original in expected) for code in allowed)
sys.addaudithook(sample["offline"])

left, right = socket.socketpair()
left.close()
right.close()

denials = []
def rejected(action, event, label):
    try:
        action()
    except RuntimeError as exc:
        assert str(exc) == "WP4D server network access forbidden: " + event, str(exc)
        denials.append(label)
    else:
        raise AssertionError("Network operation unexpectedly allowed: " + label)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    rejected(lambda: sock.bind(("127.0.0.1", 0)), "socket.bind", "direct-bind")
    rejected(lambda: sock.connect(("127.0.0.1", 9)), "socket.connect", "direct-connect")
rejected(lambda: socket.getaddrinfo("localhost", 9), "socket.getaddrinfo", "direct-dns")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    rejected(lambda: sock.sendto(b"denied", ("127.0.0.1", 9)), "socket.sendto", "direct-sendto")

# Spoof both the legacy/new function names and the genuine stdlib filename.
# No guard state, audit event or result is patched.
for name in ("socketpair", "_fallback_socketpair"):
    namespace = {"socket": socket}
    source = ("def " + name + "():\n"
              "    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:\n"
              "        sock.bind(('127.0.0.1', 0))\n")
    exec(compile(source, socket.__file__, "exec"), namespace)
    fake = namespace[name]
    assert not any(fake.__code__ is original for original in allowed)
    rejected(fake, "socket.bind", "spoof-" + name)

# Supplement the executable spoof probes: runtime guard lookup must not
# depend on code filename/name strings.
original = sample["offline"].__code__
assert original.co_names.count("co_filename") == 0
assert original.co_names.count("co_name") == 0
print(json.dumps({"socketpair": "PASS", "network_denials": denials,
                  "allowance": "STDLIB_CODE_OBJECT_IDENTITY_ONLY"}))
'''
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", code, str(server)],
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
    assert '"socketpair": "PASS"' in result.stdout
    assert '"spoof-_fallback_socketpair"' in result.stdout
