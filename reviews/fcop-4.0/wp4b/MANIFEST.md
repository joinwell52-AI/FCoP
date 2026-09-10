# WP4B final implementation delivery Manifest

This delivery resumes WP4B through the fixed WP4B.3a authorization. It is not
an ADMIN Gate signature. Review only; DO NOT MERGE.

## Commit chain

```yaml
AUTHORIZED_SCOPE: WP4B_RESUME_ONLY
PARENT_GATE: WP4A_MACHINE_CONTRACT_ACCEPTED
PARENT_GATE_COMMIT: 982fcb24d9093e01c5ba4fdb87e710acd57e6d54
INPUT_HEAD: 74f0150eee88bcef754fbd5182d2eba9836a04ec
FROZEN_CONTRACT_COMMIT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
CONTENT_COMMIT: 442de2748d0d5e657bfb3c8dc844457ca43d5114
MANIFEST_COMMIT: SELF_CONTAINING_COMMIT_RESOLVED_BY_GIT
BRANCH: review/fcop-4.0-wp4b-mcp-adapter
DRAFT_PR: 15
CONTENT_FILES: 35
MANIFEST_FILES: 1
TOTAL_DELIVERY_FILES: 36
```

Manifest commit means the unique direct child of CONTENT_COMMIT whose only
changed path is `reviews/fcop-4.0/wp4b/MANIFEST.md`. Resolve the current delivery
HEAD with `git rev-parse origin/review/fcop-4.0-wp4b-mcp-adapter`, verify its
parent equals CONTENT_COMMIT and verify its one-path diff. A commit cannot embed
its own final SHA without a self-reference cycle. The final PR receipt supplies
the actual Manifest SHA and this file's own SHA-256 externally.
The Content parent is the fixed input; no local-only blocker commit was spliced
in, no delivered history was rebased, and no force push is permitted.

## Fixed taskbooks

| Scope | Commit | Path | SHA-256 |
|---|---|---|---|
| WP4B | `245d914e1f0aff48a19d8f0ba8432e6b4f008b68` | `taskbooks/fcop-4.0/WP4B/01-MCP-Thin-Adapter-and-Version-Routing-Taskbook-v1.0.zh.md` | `0a7605efba198799c3f859b68c9d225be568a57e8c591ac1097cbc2eaebebbe9` |
| WP4B.0 | `b2453202686d08bd6584302072e0be814a059be4` | `taskbooks/fcop-4.0/WP4B.0/01-Profile-Resource-Template-and-Relay-Boundary-Correction-Taskbook-v1.0.zh.md` | `10118bcc63df3b8334c9eca4137493164f1c0d329f86dd572b0c9ee9af758c59` |
| WP4B.1 | `e885135f4b074845944a7b8b799de879549fbc33` | `taskbooks/fcop-4.0/WP4B.1/01-T6-Reopen-Task-MCP-Mapping-Correction-Taskbook-v1.0.zh.md` | `0695cd68237a5a13eb438935d8741512476f977878938afd8864165345b694df` |
| WP4B.2 | `9359de1f9268dd13c8c393ee403c8837130a0960` | `taskbooks/fcop-4.0/WP4B.2/01-Public-Report-Head-Query-Boundary-and-WP4B-Resume-Taskbook-v1.0.zh.md` | `a7dc53f17d676e787ffb6b89c8305bb59e3e9b54f06f28bc75d8d737a554b060` |
| WP4B.2a | `ed8212cefeccf2e0d2a49b8802386758fd17475a` | `taskbooks/fcop-4.0/WP4B.2a/01-REPORT-Zero-Head-Error-Code-Alignment-and-WP4B-Resume-Taskbook-v1.0.zh.md` | `97a1ffe5def18d90199255adce718e00ffa22f74653ea575eb060ec4c9a33b0e` |
| WP4B.3 | `8a93129997883aa2013e4d2c412e568fe4d44e8a` | `taskbooks/fcop-4.0/WP4B.3/01-Public-Authorization-Fact-Append-Boundary-and-WP4B-Resume-Taskbook-v1.0.zh.md` | `df3f979eadc4e72469e3d658502b270c06215a4a060f18002963e218d78aa7d3` |
| WP4B.3a | `74f0150eee88bcef754fbd5182d2eba9836a04ec` | `taskbooks/fcop-4.0/WP4B.3a/01-C2-R02-Trusted-Authorization-Local-Fixture-Alignment-Taskbook-v1.0.zh.md` | `0b0aeb030b3879157b14353e5ee259d2f0ed7dd036c4561edd24c4cbade68cb3` |

WP4B.3a frontmatter contains a mistyped previous commit; its real Git parent is
8a93129997883aa2013e4d2c412e568fe4d44e8a. This metadata error remains visible in
the taskbook and reports; section 7 and the fixed Git parent governed resumption.

## Content file inventory

Hashes are SHA-256 of exact Content Commit Git blob bytes, not Windows checkout
CRLF projections. Every row must be independently fetched from GitHub at the
final Manifest HEAD and compared. They are unchanged between Content and Manifest.

| Path | SHA-256 |
|---|---|
| `CHANGELOG.md` | `2b1bd4284deb517c30067d35a3097405cbdba817108605d68b38ebc0d08fb178` |
| `docs/mcp-tools.md` | `06344b365a7f2780c16266aab5ae89f1a3902bea0cd8c4f9f956a19af17cc453` |
| `mcp/README.md` | `f3f1950d6eac34ba6a1197e86c1b7b15580640465a36db33c8748f8797d9d8d0` |
| `mcp/pyproject.toml` | `7efbe568496abe034e80bcee258e90da1ba8606a78487def294899d57e1cf17b` |
| `mcp/src/fcop_mcp/__main__.py` | `6d14642bdb1de2587d0298ebe23474c84fef8de67713e9c93ae3fcdd80cd534f` |
| `mcp/src/fcop_mcp/_specs.json` | `2e832fa4d238a4e8875d44b5b86cbf3435bdb4d3cc0272442ca2cf73394b324d` |
| `mcp/src/fcop_mcp/adapter.py` | `9a29787af675f244e56458e2a41382fc25c64ca89460963d11af1ba74bd98f63` |
| `mcp/src/fcop_mcp/disposition.py` | `cc23bf927953c6b1168924d05020bf02bd895b7dfa58e9932096702f6771a5d8` |
| `mcp/src/fcop_mcp/governance/interceptor.py` | `50a561b329905aca6a5a83b841d4321ba577de6e984f97608005731d15c06dec` |
| `mcp/src/fcop_mcp/projection.py` | `a106ce8ede0637b8661aa38e444da96a010e6bdb87f804f157d737cfb23ceabe` |
| `mcp/src/fcop_mcp/relay.py` | `e27dd523d0aee60dd81b70e27ef98af8793643382d09aad87feae21493a84042` |
| `mcp/src/fcop_mcp/resources.py` | `d6b6ae7fdd73b64eafa8c5525c2838816b423213fbe669234c53022ecdcf5ef3` |
| `mcp/src/fcop_mcp/routing.py` | `914e1ad38cdbc11be14ffbb41b6dc1cc9c27e6d80cdb47152c91269467e04223` |
| `mcp/src/fcop_mcp/server.py` | `e9849a6bb761a047a3637541b240d1d953f644042028e88c30fec42f8290bb71` |
| `reports/FCOP-4.0-WP4B-45-11-3-DISPOSITION-RESULT.md` | `585c2ffc39bc7bf79db501848df32e3ff8858b27a725bf9bc6be4bb8aeb83899` |
| `reports/FCOP-4.0-WP4B-IMPLEMENTATION-PLAN.md` | `06836ff625d85acdf8ce63d8c1349bdb843941b5fe0ff3c8dc2b52c30dc6bf42` |
| `reports/FCOP-4.0-WP4B-PACKAGING-AND-RELAY-RESULT.md` | `18ae8660ef1fc4207c4d515d2fb0656129ac58faf7786450f337cbcea8d53677` |
| `reports/FCOP-4.0-WP4B-RESULT.md` | `a18bfd6d1209ec9a179445b11b4c0d8813a833993a5f3494a4b54cd481238b45` |
| `reports/FCOP-4.0-WP4B-VERSION-ROUTING-AND-TRUST-BOUNDARY.md` | `ae94ccba67469fed9ddc8443980ba61b0576fbd3422705882dd00055dd56b0c2` |
| `src/fcop/v4/authorization.py` | `7af855f2bd8e1b0f4d3af8ba89e8b2b8be7f0481631bae90ae6a680cf5ee5d17` |
| `src/fcop/v4/boundary.py` | `dc7a8f0785c66010e3625e8fb22ffaf76f49d7e3840723b5940085829c9f1dfe` |
| `src/fcop/v4/creation.py` | `8c76be19b73a75db58523aa9b626dcb9f99d9e968113e210d74220f98b2c96b7` |
| `src/fcop/v4/lifecycle.py` | `c9c3511e05240d7f869c29c664a3134b31d33bda9cc9fb92d7696c51755e4a1d` |
| `src/fcop/v4/reports.py` | `5f854b4708443fc3c10137efd175c258f74ea9fb6c78349a8ce16673c42ee70b` |
| `tests/conformance/v4/test_c2_envelopes.py` | `b76a59071fb8d178888c223cd3588db6c578a22cf7e52558f81e79365971b215` |
| `tests/test_fcop/test_v4_authorization_append.py` | `5baf758f5d6a6424d7f344ffbb6b3253d5b8215c65f988b4907f0012fb8c5883` |
| `tests/test_fcop/test_v4_creation.py` | `1397e4aaf9b0158c3491c4821fc13eb6dd38a608f9c88af4c68e2f7c15417012` |
| `tests/test_fcop/test_v4_report_queries.py` | `d05c327d623d916589da484b6cdd84637a0274e3373e2b16d70c8668cca8b5e1` |
| `tests/test_fcop_mcp/artifact_probe.py` | `6bd6c2d4ad75090e7502618a45768c3d1b02cdff1478f6f80d974ef337a4eb6f` |
| `tests/test_fcop_mcp/snapshots/tool_surface_v4.json` | `a0ec12e2cfd9125535b5a49d78de65e4b4e955da0c0f5273e4029fbbe91b79e0` |
| `tests/test_fcop_mcp/test_tool_surface.py` | `f48fc41d875ad2d76d7c4a91562940120c0529ef3f35462afd4d38648d8ee795` |
| `tests/test_fcop_mcp/test_wp4b_authorization_append.py` | `25d7c166eae1cd4ca51e1826541bd76dfdb90af43780b7fb87afe3d8cb964f98` |
| `tests/test_fcop_mcp/test_wp4b_delivery.py` | `e3d68de1b8be0b8699a796dcd3e48e984efd0eb4df8ffa67306fa00fa72e3bd1` |
| `tests/test_fcop_mcp/test_wp4b_races.py` | `2f713b7a93b12d0649c863761fa5f4865eac8639fcc6ae5de0a9f11c260f19e6` |
| `tests/test_fcop_mcp/test_wp4b_resume.py` | `87e35839fe54358370bcbcfa7320558849bd39005d6cd0685ff59073a4255b51` |

## Verification recorded at content freeze

| Scope | Result |
|---|---|
| Full tests/test_fcop | 1256 passed |
| Independently expanded test_v4*.py | 348 passed |
| Frozen Conformance | 119 passed / 119 collected / 60 contract IDs |
| MCP full suite | 134 passed |
| Authorization + REPORT/lifecycle directed | 114 passed |
| Canonical tool surface/disposition | 46/46 (45 historical + only reopen_task) |
| Static resources/disposition | 11/11, actual v3/v4 reads |
| Profile templates/disposition | 3/3 read-only, no authorization effect |
| Real MCP races | 5/5; actual operations, two cross-process create scenarios |
| C2-R02 | 6 original assertions preserved + 14 added; local trusted evaluator |
| Global driver / other frozen tests | Unchanged |
| Ruff / mypy | PASS; Core 41 files; MCP source/tests 28 files |
| Wheel/sdist and clean base/Relay | PASS; real installed protocol probes |
| Spec payload parity | 4/4 |
| Frozen specs / Schema JSON | 2/2 and 24/24 unchanged |
| Local unexpected failures | 0 on final verification |

Commands, artifact hashes, resolved dependencies and earlier failures are in
the five result reports above. Plain surface counting is not represented as
independent behavior coverage. Optional v4 Profile/governance capabilities have
explicit unavailable dispositions; state snapshots are not a new global audit.

## Dependency and complexity disclosure

- Version numbers remain 3.2.5; no publication.
- fcop requirement metadata remains >=3.2.5,<4.0; runtime exact accepted pair
  is (3.2.5, 3.2.5), unsupported pairs fail before registration.
- FastMCP is fixed to tested 3.2.4; FCoP direct websockets moves to [relay].
  Clean installs resolve upstream transitive websockets 17.1; it grants no Relay
  activation. No new runtime dependency names.
- New Project public names: 0. Existing list_reports/read_report and
  mark_human_approved are the explicitly authorized v4 handler completions.
- New MCP canonical tools: 1, only reopen_task, per WP4B.1.
- New private production modules: 7 (six MCP, one Core REPORT query module).
- New background components / authoritative stores / state machines: 0/0/0.
- Frozen-spec / Schema / bundled-rule / version / workflow changes: 0.
- Frozen Conformance exception: only the authorized C2-R02 local function.
- Original D:/FCoP dogfood and CodeFlowMu: not modified or migrated.
- Main remains 68dbeb15f4e7f84e1d03f907be9fa66c2265843e; no merge/release.

## Remote acceptance protocol

At Manifest creation, future CI cannot be asserted as green:

```yaml
GITHUB_CI_AT_FINAL_HEAD: PENDING_REMOTE_EXECUTION
REMOTE_READBACK: REQUIRED_AFTER_PUSH
WP4B_MCP_ADAPTER_ACCEPTED: false
REQUESTED_GATE: NONE_UNTIL_REMOTE_VERIFIED_AND_CI_GREEN
```

[Draft PR #15](https://github.com/joinwell52-AI/FCoP/pull/15) is the review entry.
After pushing this exact head: refetch, verify PR head and ancestry, independently
read every content blob plus this Manifest from GitHub, and verify all hashes.
Then wait for BOTH test-fcop and test-fcop-mcp workflows at that exact head.
All matrix, coverage, charter and package jobs must succeed; skipped package
jobs or older taskbook-only green CI do not count. Record the exact Actions run
URLs, Manifest SHA and 36/36 remote hash result in a final PR receipt.
No post-Manifest evidence commit is needed to pretend future results were known.

Only then request WP4B_MCP_ADAPTER_ACCEPTED and stop. Never sign it, enter WP4C/
WP4D, merge main, migrate a workspace or publish any artifact.
