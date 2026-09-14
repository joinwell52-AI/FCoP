# FCoP repository development instructions

This file is repository-owned contributor guidance, not an FCoP protocol artifact.
It is not packaged or deployed to customers and does not activate a workspace.

- Follow the current ADMIN-authorized taskbook, scope and release gates.
- Preserve unrelated working trees, historical evidence and customer-owned bytes.
- Use UTF-8 and apply_patch for edits; do not edit Chinese text through PowerShell.
- Do not modify CodeFlowMu or implicitly migrate existing workspaces.
- FCoP owns protocol state under <project>/fcop/ and package rule resources,
  not project-root Host instructions. Keep Legacy compatibility isolated.
- Verify tests, generated docs and artifact identities; record real failures.
- Never merge, tag or publish without explicit task authorization.

Protocol: spec/fcop-4.0-spec.md and spec/fcop-4.0-spec.zh.md.
Current rule distribution: docs/rule-resources.md.
