# 4.0.3 candidate package proof

Build/content identity: `b767e8f46ede33d405a96ba568dc38b4e733b3ec`; implementation commit `009d6abdadcde1fc97c440e04970434e2e0c9459`. Later test/evidence-only commits do not replace this build identity. After preserving newly merged upstream handoff documentation, both builds and all four installed-consumer probes were repeated. This candidate supersedes the earlier d1abaa6 build, whose evidence remains in history.

Command: `python scripts/fcop_403_package_proof.py <fresh-output> --commit b767e8f46ede33d405a96ba568dc38b4e733b3ec`. Current local output: C:/Users/Administrator/.codex/tmp/fcop-403-package-proof-3.

Two independent Git source exports, fixed SOURCE_DATE_EPOCH, no build isolation, no publication. Git export explicitly disables the local autocrlf transformation, so source files are canonical Git bytes. Four raw archives match in both builds: **4/4**. Strict Twine: **8/8**. Tool versions and exact file hashes are in package-proof.json.

Both Core archives include 18 bilingual rule artifacts and one manifest, all per-artifact sizes/hashes verified. No consumer-target AGENTS.md, CLAUDE.md or fcop-v4.mdc in any archive. Legacy package data remains for v1-v3 compatibility. Both packages are 4.0.3 Production/Stable; MCP requires fcop>=4.0.3,<4.1.0.

Clean installs: Core wheel, Core sdist, pair wheel, pair sdist: **4/4** CLI/identity probes passed with runtime imports proven to originate in site-packages. Both pair probes verify real MCP stdio 49/12/4 and bilingual spec payload hashes. Core source/archive/installed 19-member parity and public rule export passed. Installed wheel pair additionally passed 36 actual ownership/Branch/stdio/restart checks.

The first build verification failed because local Git archive conversion materialized README CRLF while metadata used LF. Its outputs are preserved as failed evidence and are not candidates. The build-only fix does not normalize or weaken comparison: the second build verifies exact source-to-metadata bytes.

During reinstallation, using --no-build-isolation in consumer-only sdist environments failed because they did not contain hatchling. Repeating normal pip sdist installation with its isolated build environment passed for both. No package or dependency policy was changed to bypass the failure.

These artifacts are local candidates, not public PyPI downloads or released binaries.
