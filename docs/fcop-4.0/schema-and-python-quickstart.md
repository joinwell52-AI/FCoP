# FCoP 4.0 Schema and Python quickstart

This is review-stage documentation, not a release or migration instruction. Use the locally built WP4A.1 wheel, not a claimed published FCoP 4.0 package. Package version remains unchanged. Existing v3 workspaces and the eight historical schemas are not modified.

## Run an application

In an environment containing the review wheel and its existing dependencies, run:

```sh
python /path/to/examples/v4/application.py sequential
python /path/to/examples/v4/application.py family
```

Both commands create and remove their own temporary workspace, print an archived TASK ID, event count and SHA-256, and reopen disk state in a fresh interpreter. No CodeFlowMu, MCP, Git branch/merge, network, database, or background Runtime participates. The family example creates two ordinary Branch TASKs under an active Root, completes both, computes family digest, appends convergence, and uses a separate authorization for Root T7.

`Project(root, trusted_profiles={profile_id: evaluator})` registers the local trusted evaluator **at initialization**, before any business request. `create_workspace(protocol_version='4.0', encoding='fcop-filesystem/4.0', profiles=[profile_id])` explicitly adopts it. Business transitions carry references, never evaluator logic. The demo evaluator checks a fixed demonstration proof and is **not a production authentication scheme**; real adopters must supply their own issuer verification at the trusted boundary.

## Discover the machine contract offline

```python
import json
from importlib.resources import files
from jsonschema import Draft202012Validator, FormatChecker, RefResolver

directory = files('fcop').joinpath('_data/schemas/v4')
documents = [json.loads(p.read_bytes()) for p in directory.iterdir()
             if p.name.endswith('.schema.json')]
store = {doc['$id']: doc for doc in documents}
schema = next(doc for doc in documents if doc['$id'].endswith('/workspace.schema.json'))
def offline(uri):
    raise ValueError('Unbundled reference: ' + uri)
validator = Draft202012Validator(schema, format_checker=FormatChecker(),
    resolver=RefResolver.from_schema(schema, store=store,
                                    handlers={'https': offline, 'http': offline}))
```

`RefResolver` is used for compatibility with the project's existing `jsonschema>=4,<5` range; newer jsonschema versions emit a deprecation warning. No new dependency or online registry is required. Identifiers do not require fetching fcop.dev.

Use the existing Project APIs for actual strict byte reads/writes. A consumer validating untrusted raw input independently must reject invalid UTF-8, BOM, CRLF, and duplicate JSON/YAML keys before passing the **entire parsed object** to a validator. Ordinary `json.loads` or `yaml.safe_load` alone does not reject duplicate keys. Schema validation cannot retroactively discover overwritten duplicates.

Base accepts opaque fields only at the workspace and four frontmatter roots. Encoding, binding, event and fixed receipt/family substructures stay closed. Local Profile rules may tighten their own fields but cannot override Base. Passing Schema does not authorize a transition or prove a path, digest binding, REPORT head, convergence coverage, idempotent race, recovery state, or filesystem support. Those remain Core checks.

Generate/check source/package parity with `python spec/schemas/v4/generate.py --check`. See the Schema README and WP4A evidence reports for tested boundaries, exact artifact hashes, and CI limitations. Never infer an accepted Gate from a successful local example.
