# CLI v1 package proof

## Final restriction-preserving pre-merge build

Source identity: 81d3229ee602341063879fe9100ab7db92417ffe.
Directory: C:/Users/Administrator/AppData/Local/Temp/fcop-402-cli-final-candidate.
Build / Twine / descriptions / packaged source identities: **4/4 PASS**.
Current source descriptors remain the canonical README hashes listed below.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| fcop-4.0.2-py3-none-any.whl | 743898 | 741955544fe3cf55fe5edb30d63580ff373945db30a70d7717027c9fd37f02c2 |
| fcop-4.0.2.tar.gz | 643201 | de14624fcd66ddc201be87c3a37cbf4ac69a1564eee8bbbf8ed08e1c95e88f42 |
| fcop_mcp-4.0.2-py3-none-any.whl | 115992 | 911c2d30c129b4568b8b0004e7c758cf26d6e963e04d1c88222189e2b61d0b6d |
| fcop_mcp-4.0.2.tar.gz | 107102 | 63e9a65df803ba86be30d7a6b1be2396c8edd2d1ee7c14fc2a5de67cac77d7cd |

These final candidate files still must NOT replace the mandatory tag build.
Final-HEAD and tag-built installed probes are bound in the PR completion receipt.

## Intermediate Stable-identity pre-merge build (superseded)

Directory: C:/Users/Administrator/AppData/Local/Temp/fcop-402-cli-stable-identity-candidate.
Both builds: python -m build --wheel --sdist; Hatchling 1.32.0.
Four artifacts built; Twine check **4/4 PASS**. All four METADATA/PKG-INFO
descriptions exactly equal their current canonical README source.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| fcop-4.0.2-py3-none-any.whl | 743920 | 6808c6b662aa66aa084e48523fe0b72d6a4e089d4acd2a995e500a21953d543d |
| fcop-4.0.2.tar.gz | 643066 | d43f99223529b07e82bc720a637393a7a8e539d05b39778559676d0ddc5ea203 |
| fcop_mcp-4.0.2-py3-none-any.whl | 115997 | 7366be253654f72493666a65cd80e45de92dd38f9879acbbda800e3f79ccf338 |
| fcop_mcp-4.0.2.tar.gz | 107109 | ff76a140306a9c4db2b04046e5a239e14d03b5416df12cb0483fed1ad3a92567 |

Core description SHA-256: ca0931e849bd37101e9bd51745f38af09d84ffb8771e67857a620fa89a0dce2b.
MCP description SHA-256: 8aa7e299211fb3c7bda5c94592e2932f73122d3f3427a62e459f850ebd11e16c.
These are pre-merge evidence, not permission to upload these local files.
After all final-HEAD gates pass, build from exact merged v4.0.2 tag and verify
the four artifacts again. Public no-cache installs and public descriptions must
then be verified independently; actual results/hashes belong to the PR receipt.
No actual user-fcop Host upgrade or CodeFlowMu change is part of this CLI task.

Fresh native Windows environment: fcop-402-cli-stable-identity-clean.
Core wheel without MCP: PASS; MCP wheel: PASS. Both use python -I -B and actual
installed `fcop` entrypoints, with
site-packages import provenance. The probe verifies --help, all eleven JSON
calls, explicit init, read-only snapshots, and the exact Stable Core identity.
The MCP run additionally verifies actual stdio 49 tools / 12 resources / 4
templates and exact full EN/ZH spec Resource text and SHA-256.

## Historical initial candidate proof (superseded, not reused)

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
