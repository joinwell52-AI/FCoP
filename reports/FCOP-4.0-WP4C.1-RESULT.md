# WP4C.1 Result — WP4C.1a completed contract work

## Previous blocked run

```yaml
PREVIOUS_STATUS: BLOCKED
PREVIOUS_STOP_CODE: TASKBOOK_RELATION_SET_CONFLICT
PREVIOUS_CONTENT_COMMIT: 741b1829283f6a7fc1023e0edd8176b58c63ded4
PREVIOUS_MANIFEST_COMMIT: d92c72620757cea455aa24b5d635cc12f1e8b16a
ADMIN_CORRECTION: WP4C.1a
```

PR #18 and both commits remain ancestors/history, unchanged. The stop was correct; WP4C.1a explicitly corrects the taskbook, not the frozen specification. Current status below supersedes the prior report's status, not its historical facts.

## Current receipt (local document validation)

```yaml
WP4C_1A_STATUS: COMPLETE
AUTHORIZED_SCOPE: WP4C_1A_ONLY
TASKBOOK_COMMIT: 7f973dc5f32bc6b9e1076184d1247c55a1349bd5
TASKBOOK_SHA256: 37d3418a7841370f0342c9de4e573bd1f4ddff12c13a3749b5d2c9516f19652a
INPUT_HEAD: 7f973dc5f32bc6b9e1076184d1247c55a1349bd5
PREVIOUS_BLOCKED_HEAD: d92c72620757cea455aa24b5d635cc12f1e8b16a
FROZEN_FCOP_CONTRACT: aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6
PARENT_GATE_COMMIT: 65ed07263de707d327e6e2c358aec2dd7c00a6df
SCOPE_CORRECTION_COMMIT: abc2dc06db227dbc81afbd554c372271c05e89da
CORE_RELATION_SET: 4/4
LEGACY_RELATION_NAMES_DISPOSITION: 3/3
SEQUENTIAL_RELATIONS_INCLUDED: PASS
SEQUENTIAL_CONVERGENCE_EXCLUDED: PASS
PARALLEL_INCREMENT: CONVERGENCE_ONLY
RELATION_CONVERGENCE_PRIMARY_OVERLAP: 0
CONTRACT_CLAUSE_PARITY: 24/24
V4_CLAUSE_PRIMARY_MAPPING: 73/73
LEGACY_RULE_DISPOSITION: 147/147
PATH_FUTURE_OWNER: 86/86
HOST_CONSUMER_MAPPING: 12/12
GENERATED_TARGETS_MAPPED: 4/4
COMMON_ROLE_BLOCK_MAPPING: 4/4
MODULE_CONTRACTS: 9/9
MANIFEST_CONTRACT: PASS
ADOPTION_RECEIPT_CONTRACT: PASS
HOST_PROFILE_CONTRACT: PASS
ASSEMBLY_PROFILES: 3/3
CODEFLOWMU_RC_EXCLUDED: PASS
P0_OPEN: 0
DOCUMENT_CHECKS: PASS
PRODUCT_TESTS: NOT_RUN
RULE_GENERATOR_RUN: false
HOST_RUNTIME_CONSUMPTION: UNVERIFIED_NOT_ASSUMED
WORKTREE: 'D:\FCoP-wp4c1a-rule-distribution-contract'
BRANCH: review/fcop-4.0-wp4c.1a-rule-distribution-contract
DELIVERY_FILES: 6
CONTENT_COMMIT: RESOLVED_IN_MANIFEST
MANIFEST_COMMIT: RESOLVED_IN_FINAL_GITHUB_RECEIPT
REMOTE_HEAD: PENDING_AT_CONTENT_CREATION
REMOTE_PUSHED: PENDING_AT_CONTENT_CREATION
REMOTE_REFETCH_VERIFIED: PENDING_AT_CONTENT_CREATION
DELIVERY_SHA256: PENDING_REMOTE_6_6
WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN: false
WP4C_2_STARTED: false
MAIN_MODIFIED: false
CODEFLOWMU_MODIFIED: false
PR18_MODIFIED: false
IMPLEMENTATION_MODIFIED: false
FROZEN_SPEC_MODIFIED: false
SCHEMA_MODIFIED: false
MCP_MODIFIED: false
TESTS_MODIFIED: false
HOST_OUTPUT_MODIFIED: false
RELEASE_CREATED: false
REQUESTED_GATE: WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN
```

COMPLETE refers to the candidate contract work and local validation recorded here, not a prospective claim that GitHub delivery already succeeded when Content was created. Manifest fixes Content SHA; after push/refetch the final Draft PR receipt records actual Manifest/remote HEAD, six hashes and CLEAN status without a self-referential hash or a third commit. This candidate is not frozen until ADMIN signs its Gate.

## What changed

Two language contracts with 24 identical numbered clauses define nine modules/18 future language artifacts, exact four relations, distinct package Manifest/adoption receipt/Host profile contracts, deterministic reference/bounded_embed, dry-run/ownership/partial-failure/rollback evidence, three isolated assemblies, version isolation, thin read-only MCP and single-owner subsequent phases. The decision report individually resolves all 73 clause, 147 source-section, 86 path and 12 consumer entries. It keeps ordinary REPORT/attempt evidence common and Branch convergence optional; this applies ADMIN's correction rather than rewriting frozen F4.5.

The prior BLOCKED delivery is a fixed ancestor and explicitly recorded in all three reports and Manifest. New review branch and Draft PR are used; PR #18 is not changed or merged. Existing dirty D:\FCoP and historical/dogfood files are untouched. No CodeFlowMu repository or RC body was read, copied, rewritten, translated, adopted, bundled or projected. The old constitution source-decision report was read as required historical evidence, not used as a new authority.

## Verification actually performed

1. Read and base64-decode the taskbook through GitHub contents API at the fixed commit; exact SHA-256 matched expected and local Git blob. Initial console decoding was corrected by setting Python output to UTF-8 and re-reading the complete taskbook; no source bytes were rewritten.
2. Verify all required ancestry and both frozen specification full byte identities. Four previous blocker files match their accepted historical HEAD. All required documents were completely read, including the six prior audit inputs and both languages; source searches do not substitute for that reading.
3. Inspect exact old-name occurrences in 83 bounded 3.x sources: blocks 42 prose matches / zero anchored fields; relates_to zero; supersedes 170 word matches / 69 anchored fields. The decision schedule distinguishes documentary prose from formal relation fields and preserves v3-only supersedes semantics.
4. Recheck 86 baseline inventory Git blob SHA-256 values, not Windows checkout text after line normalization. All matched the accepted baseline.
5. Validate 24/24 bilingual clause IDs, module/field-table structures, declared errors/Gates, exact relation and assembly JSON arrays, dependency closure/order, 73 unique primary rows, 147 identical contiguous intervals, 86 exact path rows, 12 consumer rows, four common variants and four targets. Explicit per-unit review supplies semantics beyond machine counting.
6. Review EN/ZH obligation equivalence paragraph-by-paragraph. Unknown Host/reference/runtime evidence remains unknown. Candidate profile caps are not claimed measured Host limits. Deployment receipts do not confer Core lifecycle authority and multi-file atomicity is not claimed.
7. Validate strict UTF-8/LF/no BOM, consistent table columns, resolvable concrete Markdown relative links, and git diff --check before content delivery. Final six-file scope, Manifest-only child and remote identities are checked after their respective files/commits exist.

Observed primary-module counts: compatibility 17, workspace 8, envelopes 5, lifecycle 11, relations 3, convergence 6, authorization 7, idempotency 5, recovery 11; total 73. Table data-row counts: EN and ZH each [9,4,11,13,11,3,5]; Decisions [3,73,147,4,86,12,4,32]; Matrix [30,15]. These are documentation counts, not executed behavioral test counts.

No product regression, generator, Host deployment/probe, fresh wheel/sdist build or CodeFlowMu shadow was run. The original 47 tests, artifact parity numbers and downstream snapshot are cited only as accepted baseline evidence; they are not current results. The 30 future behavioral matrix rows are design obligations, not new executable tests. Actual implementation work remains for independently authorized WP4C.2–6.

## Reproducible core document-check recipe

Run the following read-only Python through standard input in this independent worktree with UTF-8 output. It creates no files and runs no rule generator. Final Result/Manifest format/scope/remote checks supplement this content check; no validation helper file was added outside the allowlist.

```python
import pathlib,re,json,subprocess,hashlib,collections
root=pathlib.Path('.')
def read(p):return pathlib.Path(p).read_text(encoding='utf-8')
def git(*a):return subprocess.check_output(['git',*a])
base='7f973dc5f32bc6b9e1076184d1247c55a1349bd5'
frozen='aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6'
specs=[read('spec/fcop-4.0-spec'+s+'.md') for s in ['', '.zh']]
ids=lambda t:re.findall(r'^\*\*(F4\.\d+\.\d+)\*\*',t,re.M)
assert ids(specs[0])==ids(specs[1]) and len(ids(specs[0]))==73
for p in ['spec/fcop-4.0-spec.md','spec/fcop-4.0-spec.zh.md']:
 assert git('show',base+':'+p)==git('show',frozen+':'+p)
def tables(t):
 result=[];cur=[]
 for l in t.splitlines()+['']:
  if l.startswith('|'):cur.append([c.strip() for c in l.strip().strip('|').split('|')])
  elif cur:
   assert len({len(r) for r in cur})==1,cur[:2]
   result.append(cur);cur=[]
 return result
en=read('docs/fcop-4.0/rule-distribution-contract.md')
zh=read('docs/fcop-4.0/rule-distribution-contract.zh.md')
rids=lambda t:re.findall(r'^### (RD-\d\d)',t,re.M)
assert rids(en)==rids(zh)==['RD-%02d'%i for i in range(1,25)]
arrays=lambda t:[json.loads(x) for x in re.findall(r'\x60\x60\x60json\n(.*?)\n\x60\x60\x60',t,re.S)]
a=arrays(en);assert a==arrays(zh)
assert a[0]==['parent','branch_of','subject_ref','references']
assert 'relations' in a[1] and 'convergence' not in a[1] and a[2]==a[1]+['convergence']
et,zt=tables(en),tables(zh)
assert [len(t) for t in et]==[len(t) for t in zt]
mods={r[0]:r for r in et[0][2:]};assert len(mods)==9
for module,r in mods.items():
 assert not any(x in ' '.join(r) for x in ['blocks','relates_to','supersedes'])
 deps=[s for s in r[2].strip('[]').split(',') if s]
 assert all(d in mods and int(mods[d][3])<int(r[3]) for d in deps)
 for selection in a[1:]:
  if module in selection:assert set(deps)<=set(selection)
assert [(r[0],r[2:]) for r in et[0][2:]]==[(r[0],r[2:]) for r in zt[0][2:]]
# Field/table structural parity is independent of prose translation.
for i in range(1,len(et)):
 assert [r[0] for r in et[i][2:]]==[r[0] for r in zt[i][2:]]
assert set(re.findall(r'toolkit:[A-Z_]+',en))==set(re.findall(r'toolkit:[A-Z_]+',zh))
assert set(re.findall(r'WP4C_[A-Z0-9_]+',en))==set(re.findall(r'WP4C_[A-Z0-9_]+',zh))
d=read('reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md')
mapping=re.findall(r'^\| (F4\.\d+\.\d+) \| ([a-z]+) \|$',d,re.M)
assert [r[0] for r in mapping]==ids(specs[0])
assert len(mapping)==len(set(r[0] for r in mapping))==73
assert set(r[1] for r in mapping)==set(mods)
rel={i for i,m in mapping if m=='relations'}
conv={i for i,m in mapping if m=='convergence'}
assert rel=={'F4.5.1','F4.5.2','F4.5.5'} and not rel&conv
audit=read('reports/FCOP-4.0-WP4C.0-RULE-DISPOSITION.md')
unitpattern=r'^\| ([RP]-\d{4} [RP]:\d+\u2013\d+) \|'
oldunits=re.findall(unitpattern,audit,re.M);units=re.findall(unitpattern,d,re.M)
assert units==oldunits and len(units)==147 and len(set(units))==147
b=read('reports/FCOP-4.0-WP4C.0-DISTRIBUTION-BASELINE.md')
inventory=[]
for l in b.splitlines():
 if re.search(r'\| [0-9a-f]{64} \|$',l):
  c=[s.strip() for s in l.strip('|').split('|')];inventory.append((c[0],c[-1]))
assert len(inventory)==86
for p,h in inventory:
 assert len(re.findall(r'^\| '+re.escape(p)+r' \|',d,re.M))>=1
 assert hashlib.sha256(git('show',base+':'+p)).hexdigest()==h,p
pt=next(t for t in tables(d) if t[0][0]=='Input path')
assert [r[0] for r in pt[2:]]==[p for p,h in inventory]
ht=next(t for t in tables(d) if t[0][0]=='Consumer ID')
assert len(ht[2:])==12
assert len(next(t for t in tables(d) if t[0][0]=='Existing target')[2:])==4
assert len(next(t for t in tables(d) if t[0][0]=='Variant')[2:])==4
assert len(next(t for t in tables(d) if t[0][0]=='Name')[2:])==3
for t in tables(d):
 if 'Sole owner' in t[0]:
  col=t[0].index('Sole owner')
  assert all(re.fullmatch(r'WP4C\.[2-6]',r[col]) for r in t[2:])
paths=['docs/fcop-4.0/rule-distribution-contract.md','docs/fcop-4.0/rule-distribution-contract.zh.md','reports/FCOP-4.0-WP4C.1-CONTRACT-DECISIONS.md','reports/FCOP-4.0-WP4C.1-CONFORMANCE-MATRIX.md']
for p in paths:
 raw=pathlib.Path(p).read_bytes();t=raw.decode('utf-8')
 assert b'\r' not in raw and '\ufeff' not in t
 assert all(ord(c)>=32 or c in '\n\t' for c in t) and '\x7f' not in t
 tables(t)
 # Restrict link scan to real Markdown links, excluding templates inside inline code.
 for target in re.findall(r'\]\(([^)\n]+)\)',t):
  if target.startswith('<') or '<' in target:continue
  if target.startswith('https://'):continue
  assert (pathlib.Path(p).parent/target.split('#')[0]).exists(),(p,target)
for p in paths[2:]:
 t=read(p)
 for token in ['Previous blocked run','741b1829283f6a7fc1023e0edd8176b58c63ded4','d92c72620757cea455aa24b5d635cc12f1e8b16a','ADMIN_CORRECTION: WP4C.1a']:assert token in t
print('PASS: 24/24 bilingual IDs; 9/9 modules; 4/4 relations; 3/3 legacy dispositions')
print('PASS: sequential eight; parallel sole increment convergence; acyclic dependency closure')
print('PASS: 73/73 primary clauses; 147/147 intervals; 86/86 paths and input Git hashes; 12/12 consumers; 4/4 outputs/common')
print('PASS: bilingual field/error/Gate parity; formatting/table/link resolution; blocked history')
print('PRIMARY_COUNTS',dict(collections.Counter(m for i,m in mapping)))
print('TABLE_COUNTS',{p:[len(t)-2 for t in tables(read(p))] for p in paths})
```

## Delivery and stop

Content commit modifies exactly the two contracts and three reports. Its direct parent is 7f973dc5f32bc6b9e1076184d1247c55a1349bd5. Manifest-only direct child records five content hashes and all fixed authorities/history. Push only the new review branch, refetch, verify HEAD and both direct parents, read six files from GitHub at the fixed Manifest HEAD and compare full raw bytes/SHA-256. Create a new Draft PR stacked on the fixed taskbook branch, and leave the complete final receipt.

After verified delivery stop and request only WP4C_1_RULE_DISTRIBUTION_CONTRACT_FROZEN. No self-signature, next stage, main merge, workspace migration or release.
