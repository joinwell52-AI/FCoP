# MCP 4.0.3 surface and routing

Verified source full suite: 172 MCP tests passed. New real-stdio bootstrap tests: 4/4. Installed wheel behavior suite including Branch/restart: 36/36. Both clean wheel-pair and sdist-pair probes independently enumerated **49 tools / 12 resources / 4 templates**.

- Existing public names and parameter schemas retained, including create_branch, inspect_family, merge_branches and reopen_task.
- `test_branch_merge_stdio.py::test_all_46_existing_tool_signatures_unchanged` confirms the original 46 signatures and the three accepted additions; resource surface unchanged.
- redeploy_rules disposition is LEGACY_RULE_DEPLOY. On declared v4 it returns structured `toolkit:OPERATION_NOT_IMPLEMENTED` with zero writes. Legacy dispatch remains the original implementation and its existing tests remain.
- Explicit v4 init_solo/init_project route through Project.create_workspace, not legacy deploy_rules.
- Real stdio reads rules, protocol and all four sequential/parallel EN/ZH guidance URIs without Host files, both in empty and customer-populated roots.
- Both v4 spec resources return exact new ownership-source bytes; legacy payloads unchanged.
- Compatibility set adds only (4.0.3, 4.0.3), preserving all prior accepted pairs and mixed-pair rejection.
- Both packages target 4.0.3; MCP dependency is `fcop>=4.0.3,<4.1.0`.

No actual user-fcop service upgrade is claimed or performed. The probes use disposable, independently installed environments, not CodeFlowMu.
