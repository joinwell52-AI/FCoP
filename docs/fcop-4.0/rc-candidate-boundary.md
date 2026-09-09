# FCoP 4.0.0rc1: unpublished candidate boundary

This is an unpublished candidate identity, not a release announcement.

The fixed WP4D taskbook at commit
`cbdc60a92a02b9e2eb0c1c6e2e93f74c335407f9` authorizes candidate verification
only. Both distributions target `4.0.0rc1`; the MCP dependency is
`fcop>=4.0.0rc1,<4.1.0`. The candidate is Beta, not Stable.

The exact candidate package pair is admitted alongside the historical
`3.2.5 / 3.2.5` source-test pair. Stable `4.0.0 / 4.0.0` is not admitted.
The same-major.minor and pre-release lower-bound checks are development
guards, not new protocol behavior.

Registry metadata (`mcp/server.json`), published citation/DOI information,
legacy bundled rules, frozen contracts and Conformance remain unchanged.
A package version bump does not migrate or reclassify an existing workspace.

Do not install this unpublished candidate by asking a public registry for
an unverified version. Installation acceptance requires WP4D's four exact
artifact hashes and its external wheel/sdist consumer evidence.

Candidate identity is not proof of adoption, reproducibility, recovery,
cross-platform success or release readiness. The WP4D reports and Manifest
must state the actually completed checks, including any blocker. Only ADMIN
can sign `FCOP_4_RC_ACCEPTED`, which itself does not authorize publication.

No main merge, tag, PyPI upload, GitHub Release, MCP Registry update, Zenodo
update or CodeFlowMu write is authorized.
