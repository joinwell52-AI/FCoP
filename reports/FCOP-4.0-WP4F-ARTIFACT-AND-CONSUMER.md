---
protocol: fcop
version: "3.0"
sender: ME
recipient: ADMIN
subject: WP4F reproducible Stable artifacts and installed-consumer evidence
---

# Stable artifacts and actual consumers

## Verified pre-delivery build

[Actions run 34451771814](https://github.com/joinwell52-AI/FCoP/actions/runs/34451771814)
built content `d5d53ead14c90c66bd1e37c7555b2382dcb517d1`.
Machine Manifest SHA-256:
`0cf9180c01946f20b6fe36f9565b2f9ef8cfaa69eaabb8a91644883a2cd1d486`.
Two independent exported source directories produced identical first/second
sets: 4/4 raw byte equalities, both sets passed Twine. Neither set was published.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `fcop-4.0.0-py3-none-any.whl` | 726220 | `6f91ea21ddd63da76b75a0dd1002825768337f0272a230b20304adaf8245b926` |
| `fcop-4.0.0.tar.gz` | 617197 | `28c82fe6dd797b46776f1923d3e156854782140e8dde362f320d25f89db322b6` |
| `fcop_mcp-4.0.0-py3-none-any.whl` | 117648 | `f04eac26f7c93e42e884f2ab42a7c9f6075d997d00e9d8e5a4117998913676cf` |
| `fcop_mcp-4.0.0.tar.gz` | 109182 | `b0266dd54dca98fe61a34c22aa6aebf238079b53c45296960194fe2268b28f41` |

Build environment: Ubuntu, Python 3.12.14; build 1.4.2, hatchling 1.32.0,
setuptools 82.0.1, wheel 0.45.1, Twine 7.0.0, packaging 26.3;
SOURCE_DATE_EPOCH 1788940367. Metadata 2.5 is retained, not downgraded.
The first-set artifact includes `candidate-manifest.json`. Build logs include
both Twine checks, exact member attribution and real-artifact dry-run JSON.

## RC-to-Stable member attribution

Comparison uses the four published RC hashes from artifact run 34442779465.
Core wheel: version module, METADATA, RECORD only. Core sdist: version module,
pyproject/PKG-INFO and CHANGELOG, README EN/ZH, Core PyPI README.
MCP wheel: version module, package-pair registration, METADATA, RECORD.
MCP sdist: version module, package-pair registration, README, pyproject/PKG-INFO.
There are no unexplained member additions/deletions, no changed business
implementation, and no changed canonical rule bytes. The archive comparison
output is `wp4f-build-logs/wp4f-artifact-delta.json`, status PASS.

## Installed consumer matrix

All 12 `wp4f-consumer-{os}-{python}` artifacts from the run were downloaded and
their `result.json` independently checked against the machine Manifest and
the four downloaded artifact bytes. Windows, Ubuntu and macOS each pass
Python 3.10, 3.11, 3.12 and 3.13: 12/12. Each cell creates separate fresh
wheel and sdist environments outside checkout: 24/24 origins, both packages
installed from the corresponding accepted origin, with site-packages import
paths and version 4.0.0 recorded. These are installed public-interface
consumers, not public PyPI downloads before publication.

Every origin proves:

- Real stdio JSON-RPC discovery: 46 Tools / 12 Resources / 4 Templates.
- `reopen_task`, T2–T7, 24 transitions; a Root with two Branches and explicit
  convergence REVIEW; final five-task states `archive,archive,done,done,inbox`.
- Two independent service processes execute real concurrent writes with one
  operation_id; one newly created result and one Existing result refer to the
  same task and digest. A changed request returns OPERATION_ID_CONFLICT with
  unchanged workspace snapshot.
- A service is killed after durable facts exist, then a new service reads the
  same tasks and family digest. Lost-response and concurrent-request retries
  remain Existing with zero additional writes: three service processes total.
- Core-only application records 19 rule artifacts, 15 transitions, disk reopen,
  exact retry and Host rollback from the installed package.
- A separate historical 3.2.5 fixture is read without workspace writes; both
  mixed-version package directions fail closed and the Stable pair is restored.

The client imports neither FCoP package; the server imports installed packages.
Its trusted educational Profile is registered at initialization, never supplied
by a business request. Source-only parity results are separate and are not
included in the 24 installed-origin count.

## Final binding requirement

This report records a real pre-delivery run, not the final review HEAD. The
subsequent strict-test type annotation and evidence/Manifest commits do not
change package members. Final review HEAD must nevertheless run the complete
CI again, reproduce these four hashes, and bind its own artifact run and machine
Manifest SHA in the final PR receipt. No readiness Gate is requested before
that verification. The publication workflow must consume the final bound run,
not silently substitute this earlier evidence run.
