# WP4B packaging and Relay result

Reporter: ME. Local Windows / CPython 3.12.9. No package was published or
installed into CodeFlowMu or the original dogfood workspace.

## Final artifact verification

Both packages built wheel from sdist successfully using `python -m build`.
Versions remain 3.2.5; these are review artifacts, not a FCoP 4.0 release.

| Package | Artifact | SHA-256 |
|---|---|---|
| fcop | wheel | `418e352fff133b1e58471da16d6bde7e6f79f8420419f5b82618ed46dad4a4bc` |
| fcop | sdist | `471ff35398f306fb0a01c8ce0abf821c057d83e77e553904cc0da564a54e69ad` |
| fcop-mcp | wheel | `bd80cbbfe3446d5df4e0f2b0ab75807b2dcba5500281b2783b266b0a31670a89` |
| fcop-mcp | sdist | `3b23b3b871c791abb59967e3613d79869ce78655797972fa2ae0ec2d1a733973` |

Byte comparison: 144 fcop package payload files and
21 MCP payload files match source, wheel and sdist.
Four bundled specification payloads match current Git source bytes and recorded
SHA-256. All 24 v4 Schema JSON files remain unchanged against the fixed input,
both Git blobs and checkout bytes. Frozen EN/ZH specs match aec4c2b.

## Dependency boundary

| Item | Before | Review implementation |
|---|---|---|
| fcop requirement | >=3.2.5,<4.0 | unchanged metadata; runtime exact pair table |
| FastMCP | >=3.2.0 | ==3.2.4, tested SDK API |
| FCoP direct websockets | base dependency | relay extra only, >=12.0 |
| Runtime dependency names added | — | 0 |
| New distribution/version/release | — | 0 |

The immutable compatibility table permits only fcop 3.2.5 / fcop-mcp 3.2.5.
Malformed, missing or unsupported pairs fail before capability registration.
Clean resolution installed 69 distributions, including FastMCP 3.2.4,
mcp 1.29.1 and websockets 17.1. The latter is an upstream transitive dependency,
not proof that FCoP Relay is enabled. No --no-deps, uninstall, vendor or upstream
metadata changes were used.

## Reproducible clean-install probes

Artifact root used locally: `D:/FCoP-wp4b3-artifact-proof`.
Final fcop distribution directory: `final-dist-fcop`; final MCP directory:
`accepted-dist-mcp` (a local folder name, not an ADMIN acceptance).
Two new, independent uv venvs: `verified-base-env` and `verified-relay-env`.
Each installed both locally built wheels with full dependency resolution;
the second explicitly selected the MCP wheel's [relay] extra.

Checked-in reproducer: `tests/test_fcop_mcp/artifact_probe.py`.

```text
python -m build --outdir <fcop-dist>
python -m build mcp --outdir <mcp-dist>
uv venv <clean-base>
uv pip install --python <clean-base-python> <fcop-wheel> <mcp-wheel>
<clean-base-python> -I -B tests/test_fcop_mcp/artifact_probe.py base
uv venv <clean-relay>
uv pip install --python <clean-relay-python> <fcop-wheel> <mcp-wheel>[relay]
<clean-relay-python> -I -B tests/test_fcop_mcp/artifact_probe.py relay
```

Both probes passed on the final artifacts. Imports were verified inside their
own site-packages, never the checkout. Real stdio subprocess completed MCP
initialize, list 46/11/3, explicit v4 bootstrap, TASK creation, same-operation
retry with existing=true, correct v4 specification read and structured legacy
rejection. Relay performed real loopback WebSocket MCP initialization and
46-tool listing against the same server implementation. Simulated missing
Relay import produced the explicit install-fcop-mcp[relay] diagnostic; installed
dependencies were never removed.

## Offline stdio and diagnostic corrections

The SDK's default banner may query PyPI. The CLI now passes show_banner=False,
so ordinary startup does not invoke that update-check path. A fake Relay URL in
the environment is ignored. The real subprocess probe uses Python's audit hook
to reject socket.connect; the only exception is the identified Python stdlib
socket._fallback_socketpair call used to construct Windows' asyncio self-pipe.
It is not a Relay endpoint or arbitrary loopback exception. The first indiscriminate
hook rejected that self-pipe and was corrected; it was not a product failure.

On this Windows host, initial fresh-venv imports were slow in importlib's
atomic .pyc writes (faulthandler located the stack). -B disables only bytecode
cache writes; -I isolates the interpreter. It does not alter package behavior,
dependency resolution, network rules or assertions. The later real installed
transport probes, not the earlier import-only count, establish this result.

```yaml
FCOP_DIRECT_BASE_RELAY_DEPENDENCY: ABSENT
FASTMCP_TRANSITIVE_WEBSOCKETS: 17.1
BASE_STDIO_NO_RELAY_ACTIVATION: PASS
BASE_STDIO_NO_NETWORK_CONNECT: PASS
RELAY_REQUIRES_EXPLICIT_ENABLEMENT: PASS
RELAY_OPTIONAL_EXTRA_METADATA: PASS
PACKAGE_COMPATIBILITY_FAIL_CLOSED: PASS
SPEC_PROJECTION_PARITY: 4/4
SCHEMA_JSON_UNCHANGED: 24/24
RELEASE_CREATED: false
```

Final-Manifest GitHub CI is a separate required delivery check; these local
artifact results do not claim remote CI has already passed.
