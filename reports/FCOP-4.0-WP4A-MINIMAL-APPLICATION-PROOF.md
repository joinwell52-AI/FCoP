# WP4A.1 minimal application proof

Source: `examples/v4/application.py`. No test driver or private lifecycle API is imported. Both modes use real `Project` initialization, explicit trusted Profile adoption, TASK creation, transition, current-attempt REPORT, acceptance and archive APIs. The demonstration evaluator is not a production identity-security scheme.

## Sequential

T1 -> T2 -> REPORT -> T3 -> acceptance REVIEW -> T4 -> separate authorization REVIEW -> T7. A fresh Python interpreter opens the workspace, reads its one archived TASK path and five transition events, and hashes complete file bytes. It does not recover NOW from mtime or events.

## Family

Root enters active. Two ordinary Branch TASKs are created and each executes T2/T3/T4 with its own REPORT and trusted authorization. Root completes its own T3/T4. `Project.family_digest` computes the canonical family input; convergence references both current Branch REPORTs. A separate archive authorization binds the digest; Root T7 succeeds. This demonstrates protocol-level parallel family membership, not simultaneous Agent execution or a new scheduler. No Git branch/merge participates.

## Execution isolation

The command-line examples always use a fresh TemporaryDirectory, never a repository/dogfood/home workspace. Tests also run them from an external working directory. The restart reader is another interpreter. The artifact smoke proof imports fcop from clean-venv site-packages and launches both modes outside the checkout; the explicit offline guard rejects socket connects and DNS calls in it and child interpreters. Installation uses a prepared wheelhouse and `--no-index`, not the network.

The source run completed both examples with archive state and five root events. The final wheel run and exact artifact hashes are recorded in PACKAGE-PROOF. Example temporary workspaces are removed automatically; no user workspace was migrated or cleaned.
