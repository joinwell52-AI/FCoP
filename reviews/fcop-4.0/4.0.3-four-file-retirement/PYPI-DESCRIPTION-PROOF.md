# PyPI description proof

Canonical sources:
- fcop: fcop-README.pypi.md
- fcop-mcp: mcp/README.md

Both wheel METADATA and sdist PKG-INFO descriptions were extracted and compared byte-for-byte with the canonical Git source. All four passed.

| Description | SHA-256 |
| --- | --- |
| fcop | 04e389fc9aff843f7b23662ed6d12e0e2ee4f1a6ececfa228627d89c96b3fa76 |
| fcop-mcp | df6b8389505855c413993f3f09e0fd5ba6edd7df2b956480577ab70978e32e2e |

Both contain a non-collapsed independent CLI chapter, all nine commands, Install & Verify examples, local/offline doctor boundaries, CLI/MCP division and customer Host ownership. MCP retains 49/12/4. Current installation guidance no longer requires four-file redeployment.

Strict Twine passed for both sets. Public PyPI page verification is **NOT PERFORMED**: publishing requires subsequent ADMIN authorization. Updating source and built metadata is not a claim that the public page has changed.
