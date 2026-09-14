# 4.0.3 candidate package proof

Build/content identity: `d1abaa6dba73be829450c108719c50506e82be29`; implementation commit `009d6abdadcde1fc97c440e04970434e2e0c9459`. Evidence-only later commits do not replace this build identity.

Command: `python scripts/fcop_403_package_proof.py <fresh-output> --commit d1abaa6dba73be829450c108719c50506e82be29`.

Two independent Git source exports, fixed SOURCE_DATE_EPOCH, no build isolation, no publication. Git export explicitly disables the local autocrlf transformation, so source files are canonical Git bytes. Four raw archives match in both builds: **4/4**. Strict Twine: **8/8**. Tool versions and exact file hashes are in package-proof.json.

Both Core archives include 18 bilingual rule artifacts and one manifest, all per-artifact sizes/hashes verified. No consumer-target AGENTS.md, CLAUDE.md or fcop-v4.mdc in any archive. Legacy package data remains for v1-v3 compatibility. Both packages are 4.0.3 Production/Stable; MCP requires fcop>=4.0.3,<4.1.0.

Clean installs: Core wheel, Core sdist, pair wheel, pair sdist: **4/4** CLI/identity probes passed with runtime imports proven to originate in site-packages. Both pair probes verify real MCP stdio 49/12/4 and bilingual spec payload hashes. Core source/archive/installed 19-member parity and public rule export passed. Installed wheel pair additionally passed 36 actual ownership/Branch/stdio/restart checks.

The first build verification failed because local Git archive conversion materialized README CRLF while metadata used LF. Its outputs are preserved as failed evidence and are not candidates. The build-only fix does not normalize or weaken comparison: the second build verifies exact source-to-metadata bytes.

These artifacts are local candidates, not public PyPI downloads or released binaries.
