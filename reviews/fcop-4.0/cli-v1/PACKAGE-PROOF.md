# CLI v1 candidate package proof

Versions: fcop 4.0.2 and fcop-mcp 4.0.2.
Dependency: fcop>=4.0.2,<4.1.0; exact supported pair added without removing older pairs.
No runtime dependency added to either package.

Local candidate directory:
C:/Users/Administrator/AppData/Local/Temp/fcop-402-cli-candidate.

Builds: python -m build --wheel --sdist for root and ./mcp: 4/4 generated.
Twine: python -m twine check <candidate-directory>/*: 4/4 PASSED.
These are pre-commit local evidence, NOT release-bound/tag-built artifacts.

| Candidate | Bytes | SHA-256 |
|---|---:|---|
| fcop-4.0.2-py3-none-any.whl | 743611 | c773c341a78d30d2dab89d3a611643a375e0bcb042edd79f0839f420031881f1 |
| fcop-4.0.2.tar.gz | 642698 | 4e4cc005a2461647a02d6f97e036c765025d3764dae5cb213ae85d052d2d5c1b |
| fcop_mcp-4.0.2-py3-none-any.whl | 115653 | 1bd541f248c9c2b7f1cf80aeb78c95b62f0d036e71b0c0527020a7ee71ef1792 |
| fcop_mcp-4.0.2.tar.gz | 106796 | 90a13bc53fc2aa0aefe400a287c79895e40b512f655111e3706beb8d69573dea |

These hashes precede a typing-only getattr adjustment in the observation helper;
they must never be promoted as final release artifacts. A future unblocked run
must rebuild and repeat all final release gates from its accepted source.

Core-only clean Windows wheel and sdist installs passed the real console probe:
version, spec, doctor, status, init, inspect, validate, unavailable tools.
Imports originate from site-packages and MCP is confirmed absent.
Probe: scripts/cli_v1_installed_probe.py invoked via python -I -B.

MCP wheel installed probe: PASS, actual stdio set equals all 49 declarations.
MCP sdist then reinstalled with --no-deps --force-reinstall in the same isolated
wheel-proof environment: PASS, actual stdio equality repeated. Its wheel built
from sdist has the same SHA-256 as the candidate MCP wheel above.
The Core-only sdist environment remained MCP-free.
PyPI description match: NOT_RUN; not publicly published.
Local wheel METADATA and sdist PKG-INFO descriptions match the respective
canonical source README exactly: 4/4. UTF-8 description SHA-256:
- Core: cf6a615ebe0d0163d7100ad4789d2f2c6cff657c2cec670fe817c0c3d51d55d7
- MCP: 5429133d720eeff47e3c957614449675d703b31288d65eca2f8208ded5655761
This is local metadata proof, explicitly not public PyPI page acceptance.
Tag rebuild, public reinstall and release smoke: NOT_RUN, blocked by C19.
PyPI/GitHub publish: false. Main merge: false. Tag creation: false.
Actual user-fcop environment and CodeFlowMu were not upgraded or modified.
