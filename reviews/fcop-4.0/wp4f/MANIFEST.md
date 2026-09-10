# WP4F Stable candidate delivery Manifest

## Identity and authority

- Repository: joinwell52-AI/FCoP
- Task: taskbooks/fcop-4.0/WP4F/01-Stable-Release-and-Local-MCP-Upgrade.zh.md
- Scope: WP4F Phase A only; no Phase B before ADMIN Gate.
- Base main: `5208d8a2b37c969b0b2067c01107966bf705293c`
- Candidate content: `1e1d309a6f8219ce9cf7fa2066b80f1a5103e499`
- Reports delivery / this Manifest parent: `0f1128a1cd25936b35f19fb0e18cd54219c42e4b`
- Branch: `codex/fcop-4.0-wp4f-stable`
- Draft PR: https://github.com/joinwell52-AI/FCoP/pull/34
- Published RC preserved: `v4.0.0rc1` at `d5e851c3fa628167999a9f8b7b7b89290e7b8f06`.

## Hash contract

The following 38 files are the complete content/report delta from the fixed
main base. SHA-256 is computed over raw Git blob bytes, not Windows checkout
line-ending materialization. This Manifest is the sole change in its own
commit (39 total delivery files); its own hash and final execution HEAD are
returned by remote readback in the final PR receipt, not self-embedded.
Every listed UTF-8 blob was decoded strictly and has LF line endings.

| File | Bytes | SHA-256 |
|---|---:|---|
| `.github/workflows/rc-candidate.yml` | 6560 | `0f700041b5b32a19de68efd3639d2547b4080ea53e2b08206aa39c3a3f6f62f8` |
| `.github/workflows/release.yml` | 5133 | `0cb441d7e072e8ed06fac34a0aa34b5f82a76d65e68d6a79c5225e75875f1276` |
| `CHANGELOG.md` | 133692 | `4466578becbed21da3ea759d8c8db9d5c48a09fa58be5614f52b16b503fb1d8e` |
| `README.md` | 7303 | `831361b686c8dfa6d38458a465a0ee24f294aef7858ac8011b67aa4afd887510` |
| `README.zh.md` | 6784 | `55f7d7aceea3bb57ca1b053023cf47dfb394334628ef22128016a3098ed5fec3` |
| `docs/releases/4.0.0.md` | 2107 | `634c41fb1e564f5a26153ebb60bd23a6ac555940c84c2e71aaf71aeb536cf864` |
| `fcop-README.pypi.md` | 2290 | `d9055ab22edc90e2ac17102e60acdb43c37ef74273feace489f4ed214b7f1137` |
| `mcp/README.md` | 15486 | `35d3b7c9f3856411947850e84b8a5ddda859120164246d61a93bc554f82d1308` |
| `mcp/pyproject.toml` | 4871 | `651701fbef04b5df0b8b0238d45dffd637a98db150f9725f2708d0bcde94abdd` |
| `mcp/src/fcop_mcp/_version.py` | 607 | `746b36059a0fb1d96c3800fa90b9cca231046f1f10d00567826e3eff7fdcfd05` |
| `mcp/src/fcop_mcp/routing.py` | 3780 | `9825f3330a78d45936852c871327ef3eb2281b3cd95af005620b3a562e97b739` |
| `pyproject.toml` | 6090 | `12911755f41dff6b88f9e5fd5fea28e28e56bca659551d4eabb095f1e828f53b` |
| `reports/FCOP-4.0-WP4F-ARTIFACT-AND-CONSUMER.md` | 4575 | `3b8057ebebc8030b8ea6021889c8891ac96178bcbd306d6509226b8af801768c` |
| `reports/FCOP-4.0-WP4F-LOCAL-MCP-UPGRADE-PLAN.md` | 3259 | `a04151afce32b79f8fe5df01983311a8586ea4f7886d5bbba13755b205b72e9c` |
| `reports/FCOP-4.0-WP4F-PUBLIC-DOCS-AND-RELEASE.md` | 3773 | `8f2fcd9821654b9d2731ec3ca1425338591b30b90289dddabd71cfe6a9589f2d` |
| `reports/FCOP-4.0-WP4F-RESULT.md` | 5959 | `da318d4a1a14fb20901be2a944946e636bc7a3c71920bad8b874e46c0f221f59` |
| `reports/FCOP-4.0-WP4F-SCOPE-AND-COMPATIBILITY.md` | 3955 | `2f0b3e6154aa313bd192fb21fdb4e835cc935228e6e76122111328d65fb81f77` |
| `scripts/wp4f_artifact_delta.py` | 3978 | `a8e6608dd7bd7fb96eb572f69fdd2034d18d3a60f5c1e9914e24f4677bc5af27` |
| `scripts/wp4f_build.py` | 7122 | `6f252504226e7f4b363e7612528ea5fe9fd3fba49db45bbbabcfa93287bd7629` |
| `scripts/wp4f_candidate_ref.py` | 1164 | `8a6dcfc86b28b3e066b1826194fb998b76334cc3e7b08de7ab5ec561be50dff7` |
| `scripts/wp4f_consume.py` | 9338 | `e3e34cc019067d980928cced8f6bff207bb2b092a8e9cd1f8598327c7343b69f` |
| `scripts/wp4f_public_reinstall.py` | 3476 | `d55ce1da6e65529f897879f3297daa8f80adae0514f2991286365d52c7353bb9` |
| `scripts/wp4f_release_guard.py` | 7343 | `41c060f55d9138b6d301c8b2e4b00682f47e1dc83d03244552ddb7fe509ad95d` |
| `scripts/wp4f_source.py` | 1194 | `8590957a276c125b3cf61d842ca3e1e0c26abc2ad18c95506b20b419305908a3` |
| `scripts/wp4f_verify_scope.py` | 3692 | `efe1c2b20ecb5a87eb63c3ed967fcd4c8aeacb5c079256e9d916954bcc12d4ca` |
| `src/fcop/_version.py` | 561 | `be35666394a81397b722e083f54e51f1e32f4ddf3078ac33713698361e550e76` |
| `taskbooks/fcop-4.0/WP4F/01-Stable-Release-and-Local-MCP-Upgrade.zh.md` | 3621 | `b949fa20ab84363643b39b731b9167e5099db4726242196160428a3fae6bf50b` |
| `tests/stable/accepted-rc-fixture.json` | 35119 | `d6c868d8e92015c11905db31ec4987ee3ffb52eb2e9beab6cdd763ce85e63fd3` |
| `tests/stable/historical.py` | 1068 | `68fa423823c7563b588a0d10d97adc44733e5ce11fdcba4f37db792722d1be31` |
| `tests/stable/installed_identity.py` | 1106 | `565e65908bdd935a68883783e2a2b48a91b4f92c4e8fd91aaf83832871eb8402` |
| `tests/stable/legacy_fixture.py` | 3744 | `fb4953087103843c989b14aac03067b535a2340cd51cad7f1c3c1e360677653f` |
| `tests/stable/third-party/mcp-only/client.py` | 13686 | `83d26af6474ab50f65c46d9dd98097a237cae60f34d1d04254d83c26acc4741a` |
| `tests/stable/third-party/mcp-only/server.py` | 1192 | `a86c374839944b44d87a157bfa9aea950540a0c5dab2bc14e952057191bf1579` |
| `tests/stable/third-party/python-only/app.py` | 12977 | `2c98acdbf8db9e94d4c6eca206345237b9dbe5579406e179aa06a9d4717e00c9` |
| `tests/test_fcop/test_wp4d_rc_identity.py` | 1664 | `b9f8247d73176a6297c0f289ffa23922e4ba2b14eb127cec08eb820d6093d6ed` |
| `tests/test_fcop/test_wp4e_release_readiness.py` | 12805 | `67c73daca17a796f85b9f6a7e08d92856e5458c95c663cebc7c8b4c431da5ba8` |
| `tests/test_fcop/test_wp4f_release_readiness.py` | 14452 | `c95a8c66ee6a3047249d7bbf8a0a61a8e9e45cc49b7c6a9bdc117794543d9fcd` |
| `tests/test_fcop_mcp/test_wp4f_release_pairs.py` | 1007 | `f059e08ba1297a1ee016e3b1e1aa1e770c931a2e0b3c558f36b00a6021b6509b` |

## Final HEAD verification and Gate

The reports record the genuine pre-delivery evidence run 34451771814.
After this Manifest is committed, all three final-HEAD workflows must pass,
including both PR-only charter checks, both full source suites and all 12
installed consumers. The final binding receipt must contain:

- final Manifest HEAD and remote branch HEAD equality;
- complete CI run/job counts with no skipped job counted as PASS;
- final artifact run, machine Manifest SHA-256, four filenames/sizes/hashes;
- 12/12 matrix and 24/24 installed origins; 46/12/4 and real lifecycle,
  Branch/convergence/concurrency/idempotency/restart results;
- remote raw-blob readback for 38/38 listed files plus this Manifest (39/39);
- unchanged main, RC tag and existing local MCP environment.

Evidence-only commits do not change candidate content. The final build must
still bind its own execution HEAD and run ID, and reproduce the same four
package hashes documented in the artifact report. The publication workflow
may use only that final binding after ADMIN signs the Gate.

Sole requested Gate after verification: `FCOP_4_STABLE_RELEASE_READY`.
Gate not signed by the executor; no main merge, Stable tag, publication or
actual MCP upgrade is performed in Phase A. Stop after requesting it.
