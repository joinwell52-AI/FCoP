# Test retirement disposition

Authority: 4.0.3 taskbook section 5 explicitly retires Host-only conformance. This is not a blanket weakening of Core or rule-resource requirements.

DIST-08–20 and DIST-28 (14 IDs) describe retired Host profiles, adoption, projection bytes, replacement/rollback or projection context. They are removed rather than marked skip/xfail. Retained DIST IDs: 01–07, 21–27, 29–30 (16). Current rule-distribution suite: 101 nodes, all passing. Frozen Core Conformance: unchanged 18-file tree, 60 IDs / 119 nodes, all passing.

## Removed functions (recoverable in the taskbook parent history)

### tests/conformance/rule_distribution_v4/test_dist_07_12_profiles.py

- test_dist_08
- test_dist_09
- test_dist_10
- test_dist_11
- test_dist_12

### tests/conformance/rule_distribution_v4/test_dist_13_20_projection.py

- test_dist_13
- test_dist_14
- test_dist_15
- test_dist_16
- test_dist_17
- test_dist_18
- test_dist_19
- test_dist_20

### tests/conformance/rule_distribution_v4/test_dist_25_30_failures_artifacts_context_gates.py

- test_dist_28

### tests/test_fcop/test_v4_rule_distribution.py

- test_adoption_still_requires_explicit_authority
- test_hash_matching_receipt_is_not_trusted
- test_readonly_host_capability_has_no_effects

### tests/test_fcop/test_v4_rule_distribution_closeout.py

- test_measure_18_real_projection_bytes
- test_measure_changed_historical_identity
- test_measure_invalid_history_zero_effect
- test_measurement_reuses_pure_projection_not_host_runtime
- test_real_indirect_history

### tests/test_fcop/test_v4_rule_distribution_host.py

- test_adopt_only_receipt_and_exact_retry
- test_adoption_identity_and_chain_cannot_be_substituted
- test_fault_with_owned_target_preserves_original_and_recovers
- test_invalid_batch_item_is_not_ignored
- test_invalid_rollback_time_precedes_all_writes
- test_lost_apply_response_and_complete_plan_retry
- test_manifest_unc_is_rejected_before_loader_io
- test_owned_plan_rechecks_historical_evidence
- test_plan_revalidates_each_input_before_effect
- test_profile_byte_contract_is_strict
- test_real_process_exit_after_replace_is_explicitly_recoverable
- test_rollback_keeps_user_bytes_added_between_deployments
- test_rollback_lost_response_does_not_toggle_history
- test_rollback_receipt_interruption_has_a_recoverable_intent

Total removed function definitions: 36. Parameterized-node counts are not conflated with functions.

## Mixed checks retained or redirected

- DIST-23: legacy cases unchanged; v4 redeploy now exact OPERATION_NOT_IMPLEMENTED with full zero-write snapshot.
- DIST-25: retain manifest, artifact, selection and executable-input errors. Four projection/adoption/deployment-only error scenarios are retired with their operations.
- DIST-26: retain disk/index drift, reopened reads, customer Host byte preservation and unknown Runtime consumption; do not assert retired deployment receipts.
- Generic path traversal, junction and executable-input rejection checks remain. The removed UNC test specifically intercepted the retired receipt/plan loader; retained artifact/path tests still cover their active boundaries.
- Current release version/spec-resource bindings updated to 4.0.3. Historical Gate/RC fixtures remain pinned and are not rewritten.
- Eight new CLI entry tests and 34 ownership/stdio tests validate the new public boundary; no empty-success implementation or generic skip substitutes for behavior.

No removal or change to lifecycle, authorization, merge, family digest, idempotency, atomic recovery, Schema or frozen Core behavioral expectations.
