# WP4C.1 Contract Decisions — resumed by WP4C.1a

Status: contract work completed for ADMIN review; candidate freeze requested, never self-signed. Executor: ME, solo; fixed ADMIN taskbook is the decision carrier. No dogfood initialization or out-of-scope task/archive writes.

## Previous blocked run

```yaml
PREVIOUS_STATUS: BLOCKED
PREVIOUS_STOP_CODE: TASKBOOK_RELATION_SET_CONFLICT
PREVIOUS_CONTENT_COMMIT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
PREVIOUS_MANIFEST_COMMIT: d92c72620757cea455aa24b5d635cc12f1e8b16a
ADMIN_CORRECTION: WP4C.1a
```

PR #18 and both commits remain ancestors/history, unchanged. The stop was correct; WP4C.1a explicitly corrects the taskbook, not the frozen specification. Current status below supersedes the prior report's status, not its historical facts.

## Fixed inputs and scope

Input/taskbook commit: `7f973dc5f32bc6b9e1076184d1247c55a1349bd5`; taskbook SHA-256: `37d3418a7841370f0342c9de4e573bd1f4ddff12c13a3749b5d2c9516f19652a`.
[Current authority](https://github.com/joinwell52-AI/FCoP/blob/7f973dc5f32bc6b9e1076184d1247c55a1349bd5/taskbooks/fcop-4.0/WP4C.1a/01-Core-Relation-Set-and-Sequential-Assembly-Correction-Taskbook-v1.0.zh.md) supersedes only the specified relation/assembly statements in the [original taskbook](../taskbooks/fcop-4.0/WP4C.1/01-Rule-Package-Manifest-and-Host-Projection-Contract-Freeze-Taskbook-v1.0.zh.md).

The required blocked Content/Manifest, prior taskbook, Gate `65ed07263de707d327e6e2c358aec2dd7c00a6df`, scope correction `abc2dc06db227dbc81afbd554c372271c05e89da`, audit HEAD `59a6654dbb5387201056004c06068f8afcafb9ed` and frozen Core are ancestors. Frozen EN/ZH blobs are identical to `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`. GitHub taskbook bytes match the expected hash and local Git object. All four prior blocker files match d92c726. Both taskbooks, both complete specs, six baseline inputs, Gate, scope correction and four blocker files were read completely this run. Old source-policy statements are evidence, not competing execution instructions.

Integral contract: [EN](../docs/fcop-4.0/rule-distribution-contract.md), [ZH](../docs/fcop-4.0/rule-distribution-contract.zh.md). Schedules here are unique ownership/disposition decisions for that candidate contract, not rule bodies or executable implementation.

## Resolved relation blocker — 3/3 legacy names

Bounded exact-name scan at input: 83 tracked files under src/fcop/rules/_data, src/fcop/teams/_data, src/fcop/templates/roles plus spec/fcop-v3-spec.md. Regex word matches and anchored YAML-field matches were inspected separately; natural-language verbs are not protocol fields. No CodeFlowMu repository or excluded RC body was read.

| Name | Current disposition | Actual source evidence | v4 consequence |
| --- | --- | --- | --- |
| blocks | DOCUMENTARY | 42 word-hit lines in bounded set, zero anchored field lines; internal-readme.en.md:97 says never blocks; TEAM-OPERATING-RULES.en.md:93 describes a dependency blocking a plan. Neither canonical mdc declares this relation. | Not a Base name, alias or gate encoding. Ordinary English may remain nonnormative documentary prose. |
| relates_to | NOT_PRESENT | Zero word-hit and zero field lines in the bounded 83 files; erroneous WP4C.1 table is not a 3.x source. Existing commentary P:1116/1134/1148 uses related, not this name. | No fabricated legacy provenance, Profile or migration mapping. |
| supersedes | LEGACY_V3_ONLY | 170 word-hit lines, 69 anchored field lines; canonical commentary P:1117/1134/1149–1158, source units P-1104/P-1402/P-2339; frozen v3 spec:230; role templates retain examples. | Historical correction link only; v4 append/correction uses frozen references semantics, not alias conversion. |

R = [canonical legacy rules](../src/fcop/rules/_data/fcop-rules.mdc); P = [canonical legacy commentary](../src/fcop/rules/_data/fcop-protocol.mdc). Paths/line anchors refer to fixed input Git blobs, not mutable workspace text. The exact v4 set is parent, branch_of, subject_ref, references. Sequential includes relations and excludes convergence; parallel adds ONLY convergence. F4.5.1/2/5 belong to relations; F4.5.3/4 belong to convergence. No clause split, renamed relation, changed Core cardinality or frozen-spec edit is needed.

## Primary clause mapping — 73/73

Every row is the entire numbered clause including attached tables/examples in both [EN](../spec/fcop-4.0-spec.md) and [ZH](../spec/fcop-4.0-spec.zh.md). Secondary references do not count as another owner. The candidate audit's semantic addresses are consolidated into the nine RD-04 domains. F4.6.1–4 remain common lifecycle/evidence, NOT optional convergence; F4.9.5 remains recovery even when cited by convergence. Authority, errors and conformance/version limits fit compatibility without importing a development manual. F4.12.1 is common workspace security. This is a guidance ownership map, not removal of any applicable obligation.

| Clause ID | Primary module |
| --- | --- |
| F4.0.1 | compatibility |
| F4.0.2 | compatibility |
| F4.0.3 | compatibility |
| F4.1.1 | workspace |
| F4.1.2 | compatibility |
| F4.1.3 | compatibility |
| F4.1.4 | compatibility |
| F4.2.1 | workspace |
| F4.2.2 | workspace |
| F4.2.3 | workspace |
| F4.2.4 | workspace |
| F4.2.5 | workspace |
| F4.2.6 | workspace |
| F4.3.1 | envelopes |
| F4.3.2 | envelopes |
| F4.3.3 | envelopes |
| F4.3.4 | envelopes |
| F4.3.5 | envelopes |
| F4.4.1 | lifecycle |
| F4.4.2 | lifecycle |
| F4.4.3 | lifecycle |
| F4.4.4 | lifecycle |
| F4.4.5 | lifecycle |
| F4.4.6 | lifecycle |
| F4.4.7 | lifecycle |
| F4.5.1 | relations |
| F4.5.2 | relations |
| F4.5.3 | convergence |
| F4.5.4 | convergence |
| F4.5.5 | relations |
| F4.6.1 | lifecycle |
| F4.6.2 | lifecycle |
| F4.6.3 | lifecycle |
| F4.6.4 | lifecycle |
| F4.6.5 | convergence |
| F4.6.6 | convergence |
| F4.6.7 | convergence |
| F4.6.8 | convergence |
| F4.7.1 | authorization |
| F4.7.2 | authorization |
| F4.7.3 | authorization |
| F4.7.4 | authorization |
| F4.7.5 | authorization |
| F4.7.6 | authorization |
| F4.7.7 | authorization |
| F4.8.1 | idempotency |
| F4.8.2 | idempotency |
| F4.8.3 | idempotency |
| F4.8.4 | idempotency |
| F4.8.5 | idempotency |
| F4.9.1 | recovery |
| F4.9.2 | recovery |
| F4.9.3 | recovery |
| F4.9.4 | recovery |
| F4.9.5 | recovery |
| F4.9.6 | recovery |
| F4.9.7 | recovery |
| F4.9.8 | recovery |
| F4.9.9 | recovery |
| F4.9.10 | recovery |
| F4.9.11 | recovery |
| F4.10.1 | compatibility |
| F4.10.2 | compatibility |
| F4.10.3 | compatibility |
| F4.11.1 | compatibility |
| F4.11.2 | compatibility |
| F4.11.3 | compatibility |
| F4.11.4 | compatibility |
| F4.11.5 | compatibility |
| F4.12.1 | workspace |
| F4.12.2 | compatibility |
| F4.12.3 | compatibility |
| F4.12.4 | compatibility |

## Legacy disposition decision method

Source of all 147 IDs, exact intervals and previous semantic findings: [accepted reverse audit](FCOP-4.0-WP4C.0-RULE-DISPOSITION.md), fixed at 59a6654. R and P partition the two canonical texts (51 + 96); bilingual repeats and container headings remain units, not invented atomic requirements. The audit's source/authority/normative/Host/downstream flags and notes remain supporting evidence. Below every unit receives a final candidate action and one future owning stage. Nothing is copied verbatim into v4 because a legacy row said retained.

Actions:
- REPROJECT: WP4C.3 authors guidance ONLY from the owning frozen clauses, never mechanically promotes the old paragraph; conflicting examples are excluded. The target module is an eligibility address, not primary ownership of additional Core clauses.
- PROFILE_ONLY: WP4C.5 maintains explicitly adopted application policy outside Base and ordinary minimum package; unresolved legacy internal policy contradictions stay legacy, not active v4 Profile instructions.
- DOCUMENTARY_ONLY: WP4C.5 retains optional explanatory material outside minimum package, without importing old normative authority.
- LEGACY_V3_ONLY: WP4C.5 preserves/version-scopes old semantics and tests exclusion from v4; no alias or silent migration.
- DEVELOPMENT_REFERENCE_ONLY: WP4C.3 isolates the repository development reference boundary; old development advice is not an adopted constitution or business rule.
- HOST_CONTRACT_REPLACEMENT: WP4C.4 uses RD-11–16 instead of old metadata/deployment wording; no in-place legacy rewrite.
- EXCLUDE_PLACEHOLDER: WP4C.3 excludes the literal TBD from active artifacts and preserves history.

| Unit / fixed source interval | Audit category | Candidate action | Future target | Sole owner |
| --- | --- | --- | --- | --- |
| R-0001 R:1–21 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| R-0022 R:22–40 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-0041 R:41–42 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-0043 R:43–74 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-0075 R:75–99 | LEGACY | LEGACY_V3_ONLY | legacy.architecture | WP4C.5 |
| R-0100 R:100–229 | CATEGORY_MODULE | DOCUMENTARY_ONLY | architecture.evolution | WP4C.5 |
| R-0230 R:230–231 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-0232 R:232–243 | CORE | REPROJECT | envelopes | WP4C.3 |
| R-0244 R:244–306 | CORE | REPROJECT | lifecycle | WP4C.3 |
| R-0307 R:307–323 | CATEGORY_MODULE | PROFILE_ONLY | profile.work-planning | WP4C.5 |
| R-0324 R:324–336 | CORE | REPROJECT | lifecycle | WP4C.3 |
| R-0337 R:337–347 | CATEGORY_MODULE | PROFILE_ONLY | profile.work-planning | WP4C.5 |
| R-0348 R:348–359 | CORE | REPROJECT | authorization | WP4C.3 |
| R-0360 R:360–370 | CORE | REPROJECT | lifecycle | WP4C.3 |
| R-0371 R:371–388 | CATEGORY_MODULE | PROFILE_ONLY | profile.review-separation | WP4C.5 |
| R-0389 R:389–421 | CORE | REPROJECT | lifecycle | WP4C.3 |
| R-0422 R:422–427 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| R-0428 R:428–453 | LEGACY | LEGACY_V3_ONLY | legacy.initialization | WP4C.5 |
| R-0454 R:454–463 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| R-0464 R:464–501 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| R-0502 R:502–532 | LEGACY | LEGACY_V3_ONLY | legacy.initialization | WP4C.5 |
| R-0533 R:533–540 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| R-0541 R:541–584 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| R-0585 R:585–614 | CORE | REPROJECT | lifecycle | WP4C.3 |
| R-0615 R:615–628 | CORE | REPROJECT | envelopes | WP4C.3 |
| R-0629 R:629–652 | CATEGORY_MODULE | PROFILE_ONLY | profile.role-routing | WP4C.5 |
| R-0653 R:653–695 | CATEGORY_MODULE | PROFILE_ONLY | profile.team-documents | WP4C.5 |
| R-0696 R:696–745 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| R-0746 R:746–770 | CORE | REPROJECT | envelopes | WP4C.3 |
| R-0771 R:771–781 | CATEGORY_MODULE | PROFILE_ONLY | profile.reply-routing | WP4C.5 |
| R-0782 R:782–798 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| R-0799 R:799–847 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| R-0848 R:848–856 | LEGACY | LEGACY_V3_ONLY | legacy.lifecycle | WP4C.5 |
| R-0857 R:857–872 | LEGACY | LEGACY_V3_ONLY | legacy.layout | WP4C.5 |
| R-0873 R:873–892 | LEGACY | LEGACY_V3_ONLY | legacy.lifecycle | WP4C.5 |
| R-0893 R:893–904 | LEGACY | LEGACY_V3_ONLY | legacy.compatibility | WP4C.5 |
| R-0905 R:905–915 | LEGACY | LEGACY_V3_ONLY | legacy.capabilities | WP4C.5 |
| R-0916 R:916–948 | CORE | REPROJECT | envelopes | WP4C.3 |
| R-0949 R:949–971 | CATEGORY_MODULE | PROFILE_ONLY | profile.capabilities | WP4C.5 |
| R-0972 R:972–994 | LEGACY | LEGACY_V3_ONLY | legacy.failure | WP4C.5 |
| R-0995 R:995–1015 | LEGACY | LEGACY_V3_ONLY | legacy.events | WP4C.5 |
| R-1016 R:1016–1020 | CATEGORY_MODULE | DOCUMENTARY_ONLY | profile.risk | WP4C.5 |
| R-1021 R:1021–1038 | CATEGORY_MODULE | PROFILE_ONLY | profile.risk | WP4C.5 |
| R-1039 R:1039–1042 | LEGACY | LEGACY_V3_ONLY | legacy.approval | WP4C.5 |
| R-1043 R:1043–1057 | CATEGORY_MODULE | PROFILE_ONLY | profile.skills | WP4C.5 |
| R-1058 R:1058–1100 | LEGACY | LEGACY_V3_ONLY | legacy.inspection | WP4C.5 |
| R-1101 R:1101–1140 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| R-1141 R:1141–1158 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-1159 R:1159–1169 | CORE | REPROJECT | compatibility | WP4C.3 |
| R-1170 R:1170–1336 | LEGACY | LEGACY_V3_ONLY | legacy.rule-history | WP4C.5 |
| R-1337 R:1337–1359 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-0001 P:1–39 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-0040 P:40–78 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0079 P:79–101 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0102 P:102–123 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0124 P:124–136 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0137 P:137–147 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0148 P:148–165 | CORE | REPROJECT | compatibility | WP4C.3 |
| P-0166 P:166–179 | CATEGORY_MODULE | DOCUMENTARY_ONLY | architecture.evolution | WP4C.5 |
| P-0180 P:180–199 | CATEGORY_MODULE | DOCUMENTARY_ONLY | architecture.evolution | WP4C.5 |
| P-0200 P:200–227 | CATEGORY_MODULE | DOCUMENTARY_ONLY | architecture.evolution | WP4C.5 |
| P-0228 P:228–243 | CATEGORY_MODULE | DOCUMENTARY_ONLY | architecture.evolution | WP4C.5 |
| P-0244 P:244–256 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-0257 P:257–285 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-0286 P:286–336 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-0337 P:337–364 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-0365 P:365–383 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-0384 P:384–391 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0392 P:392–411 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0412 P:412–439 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0440 P:440–460 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0461 P:461–466 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0467 P:467–479 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0480 P:480–486 | CATEGORY_MODULE | PROFILE_ONLY | profile.work-planning | WP4C.5 |
| P-0487 P:487–492 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0493 P:493–497 | CORE | REPROJECT | authorization | WP4C.3 |
| P-0498 P:498–502 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0503 P:503–530 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-0531 P:531–557 | CORE | REPROJECT | lifecycle | WP4C.3 |
| P-0558 P:558–639 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0640 P:640–649 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0650 P:650–659 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0660 P:660–686 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0687 P:687–732 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0733 P:733–780 | CATEGORY_MODULE | PROFILE_ONLY | profile.identity | WP4C.5 |
| P-0781 P:781–792 | LEGACY | LEGACY_V3_ONLY | legacy.team-migration | WP4C.5 |
| P-0793 P:793–850 | LEGACY | LEGACY_V3_ONLY | legacy.team-migration | WP4C.5 |
| P-0851 P:851–924 | LEGACY | LEGACY_V3_ONLY | legacy.team-migration | WP4C.5 |
| P-0925 P:925–935 | LEGACY | LEGACY_V3_ONLY | legacy.team-migration | WP4C.5 |
| P-0936 P:936–943 | LEGACY | LEGACY_V3_ONLY | legacy.layout | WP4C.5 |
| P-0944 P:944–972 | LEGACY | LEGACY_V3_ONLY | legacy.layout | WP4C.5 |
| P-0973 P:973–994 | LEGACY | LEGACY_V3_ONLY | legacy.layout | WP4C.5 |
| P-0995 P:995–1008 | LEGACY | LEGACY_V3_ONLY | legacy.naming | WP4C.5 |
| P-1009 P:1009–1030 | LEGACY | LEGACY_V3_ONLY | legacy.naming | WP4C.5 |
| P-1031 P:1031–1103 | LEGACY | LEGACY_V3_ONLY | legacy.naming | WP4C.5 |
| P-1104 P:1104–1159 | CORE | REPROJECT | envelopes | WP4C.3 |
| P-1160 P:1160–1175 | CORE | REPROJECT | envelopes | WP4C.3 |
| P-1176 P:1176–1200 | CATEGORY_MODULE | PROFILE_ONLY | profile.work-planning | WP4C.5 |
| P-1201 P:1201–1222 | CATEGORY_MODULE | DOCUMENTARY_ONLY | knowledge.organization | WP4C.5 |
| P-1223 P:1223–1230 | CATEGORY_MODULE | PROFILE_ONLY | profile.cross-scope | WP4C.5 |
| P-1231 P:1231–1259 | CATEGORY_MODULE | PROFILE_ONLY | profile.cross-scope | WP4C.5 |
| P-1260 P:1260–1282 | CATEGORY_MODULE | PROFILE_ONLY | profile.cross-scope | WP4C.5 |
| P-1283 P:1283–1307 | CATEGORY_MODULE | PROFILE_ONLY | profile.reply-routing | WP4C.5 |
| P-1308 P:1308–1312 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-1313 P:1313–1338 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-1339 P:1339–1342 | REMOVE | EXCLUDE_PLACEHOLDER | history-only | WP4C.3 |
| P-1343 P:1343–1355 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-1356 P:1356–1367 | LEGACY | LEGACY_V3_ONLY | legacy.query | WP4C.5 |
| P-1368 P:1368–1401 | CATEGORY_MODULE | PROFILE_ONLY | profile.autonomy | WP4C.5 |
| P-1402 P:1402–1814 | LEGACY | LEGACY_V3_ONLY | legacy.protocol-history | WP4C.5 |
| P-1815 P:1815–1821 | CATEGORY_MODULE | PROFILE_ONLY | profile.patrol | WP4C.5 |
| P-1822 P:1822–1829 | CATEGORY_MODULE | PROFILE_ONLY | profile.patrol | WP4C.5 |
| P-1830 P:1830–1847 | CATEGORY_MODULE | PROFILE_ONLY | profile.patrol | WP4C.5 |
| P-1848 P:1848–1856 | CATEGORY_MODULE | PROFILE_ONLY | profile.patrol | WP4C.5 |
| P-1857 P:1857–1867 | CATEGORY_MODULE | PROFILE_ONLY | profile.patrol | WP4C.5 |
| P-1868 P:1868–1876 | LEGACY | LEGACY_V3_ONLY | legacy.capabilities | WP4C.5 |
| P-1877 P:1877–1934 | CORE | REPROJECT | envelopes | WP4C.3 |
| P-1935 P:1935–1975 | CATEGORY_MODULE | PROFILE_ONLY | profile.capabilities | WP4C.5 |
| P-1976 P:1976–2006 | LEGACY | LEGACY_V3_ONLY | legacy.failure | WP4C.5 |
| P-2007 P:2007–2042 | LEGACY | LEGACY_V3_ONLY | legacy.events | WP4C.5 |
| P-2043 P:2043–2044 | CATEGORY_MODULE | PROFILE_ONLY | profile.risk | WP4C.5 |
| P-2045 P:2045–2069 | CATEGORY_MODULE | PROFILE_ONLY | profile.risk | WP4C.5 |
| P-2070 P:2070–2087 | LEGACY | LEGACY_V3_ONLY | legacy.approval | WP4C.5 |
| P-2088 P:2088–2107 | CATEGORY_MODULE | PROFILE_ONLY | profile.risk | WP4C.5 |
| P-2108 P:2108–2111 | LEGACY | LEGACY_V3_ONLY | legacy.inspection | WP4C.5 |
| P-2112 P:2112–2122 | LEGACY | LEGACY_V3_ONLY | legacy.inspection | WP4C.5 |
| P-2123 P:2123–2140 | LEGACY | LEGACY_V3_ONLY | legacy.inspection | WP4C.5 |
| P-2141 P:2141–2151 | LEGACY | LEGACY_V3_ONLY | legacy.inspection | WP4C.5 |
| P-2152 P:2152–2157 | CATEGORY_MODULE | PROFILE_ONLY | profile.audit-response | WP4C.5 |
| P-2158 P:2158–2167 | CATEGORY_MODULE | PROFILE_ONLY | profile.audit-response | WP4C.5 |
| P-2168 P:2168–2171 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| P-2172 P:2172–2180 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| P-2181 P:2181–2188 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| P-2189 P:2189–2197 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| P-2198 P:2198–2211 | CATEGORY_MODULE | PROFILE_ONLY | profile.governance-alerts | WP4C.5 |
| P-2212 P:2212–2216 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-2217 P:2217–2222 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-2223 P:2223–2243 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-2244 P:2244–2253 | DEVELOPMENT_CONSTITUTION | DEVELOPMENT_REFERENCE_ONLY | repository-development | WP4C.3 |
| P-2254 P:2254–2259 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-2260 P:2260–2282 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-2283 P:2283–2294 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-2295 P:2295–2306 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-2307 P:2307–2324 | HOST_ADAPTER | HOST_CONTRACT_REPLACEMENT | RD-11–16 | WP4C.4 |
| P-2325 P:2325–2336 | LEGACY | LEGACY_V3_ONLY | legacy.tool-history | WP4C.5 |
| P-2337 P:2337–2338 | LEGACY | LEGACY_V3_ONLY | legacy.protocol-history | WP4C.5 |
| P-2339 P:2339–2356 | LEGACY | LEGACY_V3_ONLY | legacy.protocol-history | WP4C.5 |

No 3.x field or role claim can supply v4 trust. R-0746/P-1104/P-1877 use frozen append facts and do not promote old supersedes or human_approval. R-1141's rule-file priority is replaced by frozen authority. R-0799 and P-0503/P-1308 are development-only, not downstream workspace restrictions. Role binding/parent waiting/GAL/INSPECTION stay out of Base; ordinary parent children or ISSUE state do not acquire T7 gates.

### Four common injection variants

| Variant | Source anchor | Decision | Sole owner |
| --- | --- | --- | --- |
| COMMON-TEAM-ZH | _COMMON-FCOP-3.2.5.md BEGIN_TEAM_ZH | Profile-only, no v4 Core copying; adopted trust/evidence remain required | WP4C.5 |
| COMMON-TEAM-EN | _COMMON-FCOP-3.2.5.md BEGIN_TEAM_EN | Same; optional Q&A exception cannot silently bypass applicable contract | WP4C.5 |
| COMMON-SOLO-ZH | _COMMON-FCOP-3.2.5.md BEGIN_SOLO_ZH | Solo seat/reread policy not issuer proof; no automatic archive | WP4C.5 |
| COMMON-SOLO-EN | _COMMON-FCOP-3.2.5.md BEGIN_SOLO_EN | Same; ordinary-child waits never become hidden Base gates | WP4C.5 |

All 34 injected role copies inherit this classification; none becomes another editable v4 canonical source.

## Path future ownership — 86/86

Source/byte identities are in [Distribution Baseline](FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md), accepted 59a6654. Each input path below has one future owner and exact destination policy. Legacy owner means preserving and testing its boundary, NOT authorization to edit it now. New canonical artifacts belong exclusively in v4 namespace (RD-04); no automatic rename/migration is implied.

| Input path | Future policy | Sole owner |
| --- | --- | --- |
| .cursor/rules/fcop-protocol.mdc | Preserve legacy output; future selected thin profile uses ownership checks, not whole-file overwrite | WP4C.4 |
| .cursor/rules/fcop-rules.mdc | Preserve legacy output; future selected thin profile uses ownership checks, not whole-file overwrite | WP4C.4 |
| AGENTS.md | Preserve legacy output; future selected thin profile uses ownership checks, not whole-file overwrite | WP4C.4 |
| CLAUDE.md | Preserve legacy output; future selected thin profile uses ownership checks, not whole-file overwrite | WP4C.4 |
| src/fcop/rules/_data/agent-bringup-prompt.en.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/agent-bringup-prompt.zh.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/agent-install-prompt.en.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/agent-install-prompt.zh.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-protocol.mdc | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-rules.mdc | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-spec-v1.0.en.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-spec-v1.0.zh.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-spec-v1.1.en.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/fcop-spec-v1.1.zh.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/internal-readme.en.md | Optional knowledge explanation outside minimal v4 package; no automatic inclusion | WP4C.5 |
| src/fcop/rules/_data/internal-readme.zh.md | Optional knowledge explanation outside minimal v4 package; no automatic inclusion | WP4C.5 |
| src/fcop/rules/_data/letter-to-admin.en.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/rules/_data/letter-to-admin.zh.md | Retain legacy namespace; explicit v3-only consumer, no default v4 loading | WP4C.5 |
| src/fcop/teams/_data/dev-team/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/DEV.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/DEV.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/OPS.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/OPS.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/PM.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/PM.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/QA.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/roles/QA.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/TEAM-OPERATING-RULES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/TEAM-OPERATING-RULES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/TEAM-ROLES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/dev-team/TEAM-ROLES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/index.json | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/COLLECTOR.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/COLLECTOR.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/EDITOR.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/EDITOR.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/PUBLISHER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/PUBLISHER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/WRITER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/roles/WRITER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/TEAM-OPERATING-RULES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/TEAM-OPERATING-RULES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/TEAM-ROLES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/media-team/TEAM-ROLES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/BUILDER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/BUILDER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/DESIGNER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/DESIGNER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/MARKETER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/MARKETER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/RESEARCHER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/roles/RESEARCHER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/TEAM-OPERATING-RULES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/TEAM-OPERATING-RULES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/TEAM-ROLES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/mvp-team/TEAM-ROLES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/AUTO-TESTER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/AUTO-TESTER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/LEAD-QA.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/LEAD-QA.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/PERF-TESTER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/PERF-TESTER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/TESTER.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/roles/TESTER.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/TEAM-OPERATING-RULES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/TEAM-OPERATING-RULES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/TEAM-ROLES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/qa-team/TEAM-ROLES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/README.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/README.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/roles/ME.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/roles/ME.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/TEAM-OPERATING-RULES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/TEAM-OPERATING-RULES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/TEAM-ROLES.en.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/teams/_data/solo/TEAM-ROLES.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |
| src/fcop/templates/roles/_COMMON-FCOP-3.2.5.md | Retain legacy Profile/template input; explicit adoption only, no Core authority | WP4C.5 |

## Host / consumer policy — 12/12

[Accepted consumer audit](FCOP-4.0-WP4C.0-HOST-CONSUMER-MATRIX.md) supplies inventory and evidence anchors. This contract does not upgrade unknown Runtime/reference evidence to PASS. All current runtime_consumption_verified and v4 adapter support remain unverified/not implemented; ADMIN adoption is not assumed.

| Consumer ID | Frozen candidate generation/read policy | Sole owner |
| --- | --- | --- |
| Codex | Selected static codex profile only; bounded embed by default; references require separate evidence; AGENTS managed entry | WP4C.4 |
| Cursor | Selected cursor profile only; single fcop-v4.mdc, not dual AGENTS load; references unverified | WP4C.4 |
| Claude Code | Selected claude-code profile only; CLAUDE managed entry; references unverified | WP4C.4 |
| Devin | No v4 static profile; typed unavailable, no inferred support from AGENTS filename | WP4C.4 |
| Claude Desktop | Version-selected read-only MCP resource access only; no file-profile generation or consumption claim | WP4C.5 |
| PulseMCP | Discovery mention, unsupported generation; no runtime claim | WP4C.4 |
| Doubao | Portability mention, unsupported generation; no runtime claim | WP4C.4 |
| CLI / raw LLM API / generic SDK | Can read public files; no distinct automatic Host profile or consumption proof | WP4C.5 |
| Gemini SDK / Gemini | No FCoP GEMINI projection; typed unavailable; downstream adapters are not inherited | WP4C.4 |
| Copilot | Tutorial audience only; unsupported generation | WP4C.4 |
| ChatGPT | Tutorial audience only; unsupported generation | WP4C.4 |
| CodeFlow / CodeFlowMu | Existing fixed shadow evidence only; future read-only version/ownership shadow, no generated/deployed files or RC authority | WP4C.5 |

### Four existing outputs

| Existing target | Existing source | Future disposition | Sole owner |
| --- | --- | --- | --- |
| .cursor/rules/fcop-rules.mdc | legacy canonical rules | Preserve legacy bytes; no silent v4 substitution | WP4C.4 |
| .cursor/rules/fcop-protocol.mdc | legacy canonical commentary | Preserve legacy bytes; no silent v4 substitution | WP4C.4 |
| AGENTS.md | combined legacy rules/commentary | Separate repository-development and ordinary adopted usage; ownership conflict stops | WP4C.4 |
| CLAUDE.md | combined legacy rules/commentary | Same; never assume identical file means identical adoption/consumption | WP4C.4 |

## Remaining decisions and acceptance owners

Each row specifies one lead owner; other stages may consume its evidence, not become competing owners. Historical problems are not repaired in this contract-only task.

| Finding / required decision | Contract disposition | Sole owner | Acceptance evidence required |
| --- | --- | --- | --- |
| Nine modules, 73 obligations, common evidence vs Branch | RD-04–08; no catch-all; unique owners above | WP4C.3 | 18 artifact identities/parity, dependency graph, all 73 coverage |
| 147 legacy units and common role blocks | Unit schedule; no old normative promotion | WP4C.5 | Version/audience negative loading checks against each disposition |
| Package inventory vs workspace receipt | RD-07/09; immutable byte identity vs explicit adoption | WP4C.3 | Loader rejects runtime fields, duplicate keys, cycles and digest drift |
| Three minimal assemblies | RD-17–19; 8 common, +convergence, separate development reference bundle | WP4C.3 | Exact sets, no dev/RC in ordinary assemblies; explicit task/Gate references |
| AGENTS/CLAUDE 192003-byte duplication; Cursor 192014 combined | One selected Host/language, no default alternative duplication | WP4C.6 | Per-assembly full byte and token-estimator report; no inferred session load |
| Six context measurements | Retain raw byte/4 heuristic and LF-vs-splitlines distinction | WP4C.6 | Reproducible six baseline and new assembly measurements with denominators |
| Cursor rules same-version history drift | Hash not version label; preserve historical difference | WP4C.5 | Old/new version routing and drift negatives; no claim current copies equal |
| Cursor commentary missing 28-line checklist | Development-only isolation, not business injection | WP4C.5 | Diff attribution and exclusion tests, separate development reference |
| 50 leading BOM, embedded BOM, U+000C/control hazards | RD-06/13 raw strict validation, preserve legacy bytes | WP4C.3 | v4 invalid UTF8/BOM/CR/control rejection with zero writes |
| getter cache | Immutable artifact reads keyed by manifest/hash, never stale version-only acceptance | WP4C.3 | Changed bytes with same label reject, cache keyed to identity |
| team index cache | Legacy Profile catalog stays separate, package upgrade not adoption | WP4C.5 | Index/profile compatibility and no implicit authorization adoption |
| process lifetime | Package update cannot update live process state automatically | WP4C.5 | Explicit restart/read comparison; no background refresh guarantee |
| deployment persistence | RD-09/10/16 adoption/output hashes and receipts | WP4C.4 | No file-existence inference, drift detection, partial-failure evidence |
| Host consumption lifetime | Four facts separate; never infer consume from deploy/restart | WP4C.4 | Authorized isolated exact-byte/reference/load-order evidence or explicit unavailable |
| COL-01 downstream prefixes/suffix | RD-13/16 exact ownership and diff before write | WP4C.4 | Unmarked/custom/edited regions survive; conflict gives zero writes |
| COL-02 archive-before-write partial window | RD-16 same-directory stage, replace, no group-atomic claim | WP4C.4 | Failure injection at preparation/replace/receipt boundary, preserve evidence |
| COL-03 seconds-only archive collision/archive=False | RD-10 immutable hashed backups, no silent destructive rollback | WP4C.4 | Repeat/rollback/missing-backup/modified-target rejection |
| COL-04 digest not version | RD-08 raw identities | WP4C.3 | Same version different bytes rejection |
| COL-05/06 encoding hazards | RD-06; v4 rejects, no v3 byte repair by backflow | WP4C.3 | Strict byte negatives, v3 unchanged |
| COL-07 role/Host masquerading as authorization | RD-03/11/17; trust not installed by text | WP4C.3 | Negative assembly/authority checks; no evaluator in manifest/profile |
| COL-08 legacy finish/history/fifth-envelope | RD-20 and frozen Core only | WP4C.5 | Legacy stays v3, v4 rejects semantic fallback |
| COL-09 history/language/dev bulk | RD-03/12/17 | WP4C.6 | Explicit selection/size evidence, no silent truncation |
| COL-10 broken/relocated references | RD-14/15 explicit base and immutable in-workspace snapshot | WP4C.4 | Resolve all pointers or reject; traversal/symlink/stale target tests |
| COL-11 manual copy/release prose | Source-only future generation; legacy SOP recorded, not executed | WP4C.6 | Source-to-package/Host proof, no hand-maintained second authority |
| COL-12 unresolved constitution | Exclude RC and drafts; absent general constitution allowed under fixed ADMIN correction | WP4C.3 | Development/business separation; no payload/dependency/bundle reference to excluded source |
| wheel/sdist CRLF-only differences (fcop 131/144; MCP 11/21) | Diagnostic normalization never raw-byte acceptance | WP4C.6 | Fresh authorized cross-platform artifacts match raw v4 source/Manifest bytes |
| Old guides, missing spec path, MCP wheel ownership/release drift | Version-scoped docs; fcop owns modules, adapter delegates | WP4C.5 | Correct version-selected references/ownership with 3.x compatibility evidence |
| MCP six unavailable guidance surfaces / 11 resources / 3 templates | RD-21 future read-only mapping; no WP4B change now | WP4C.5 | Typed/version/resource parity, reads cause zero writes/evaluator adoption |
| Relay | Transport only; no parser/authority duplicate/updater | WP4C.5 | Delegation/no-write/no-network-rule-fetch checks |
| CodeFlowMu fixed local shadow | Prior c008d9d evidence only, no new access this round | WP4C.5 | Separate authorized read-only snapshot; preserve product regions/pins, no mutation |
| First-failing test contract | Observable postconditions not method/parameter probes | WP4C.2 | Red tests for fields, bytes, selection, ownership, races and rollback before implementation |
| Cross-platform complete closure | RD-23/24; individually authorized stages | WP4C.6 | Full applicable CI/artifacts/consumption limits and final Gate package |

## Judgment register

- Original 15 questions are resolved by RD-04 (namespace), RD-07/09 (inventory/adoption), RD-07/08 (selection), RD-06 (bytes), RD-11/12 (Host), RD-13–15 (reference/embed), RD-03/19 (audience), RD-03 (constitution excluded/absent), RD-20 (legacy), RD-16 (ownership), RD-10/16 (writes/rollback), RD-21 (MCP), RD-02/22 (layers) and this P0 closure.
- Candidate caps 65536 embed/8192 reference are explicit safety choices, not measured Host limits; overflow rejects. WP4C.6 measures actual context; only reviewed profile revisions can change caps, never truncate.
- 24 EN/ZH contract clauses define fields, bytes and failure behavior. Three candidate Host profiles do not establish current runtime support.
- Declared Toolkit distribution error categories are explicitly namespaced, not additions to the 31 Base errors. Receipt schemas here are documentation, not JSON Schema files or code.
- Future stage Gate names in RD-24 are candidate contract identifiers requiring ADMIN freeze and separate taskbooks, not previously signed approvals.
- Prior generic-constitution entry blocker was removed by original WP4C.1 §5.3 and its scope correction; no substitute source was adopted. CodeFlowMu RC exclusion is unconditional.
- P0_OPEN: 0 in this completed contract review. This is not implementation conformance, Host adoption or repaired baseline. The only requested Gate is WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN.
