# WP4C.6a context measurement checkpoint — NOT RUN AFTER BLOCKER

Original taskbook: dc4bd62d47c3c422c8e758b588369dd3ed089acd (SHA-256 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e).
Ruling taskbook: cd0fe4df900c3ff0b34beca957097f87a8d4b150 (9619 bytes; SHA-256 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba).
Scope: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY.

The `measure_context` incomplete request was actually executed through `Project.rule_distribution`. The unchanged ordinary fixture supplies no `historical_surfaces`. The recovered implementation raised structured `toolkit:RULE_SELECTION_INVALID` with reason `Exactly six historical surfaces required`.

The existing `call` helper at `tests/test_fcop/test_v4_rule_distribution.py:54` retains its before snapshot and `finally` snapshot equality assertion. No snapshot failure replaced the Toolkit exception. The taskbook's `pytest.raises(V4ProtocolError)` does not catch that exception, so the expected-code assertion was not reached.

This run therefore proves execution of the incomplete-input rejection path and preservation of the enclosing snapshot, but does not produce 2/2 passing alignment tests, an accepted context matrix, or a runtime-consumption claim.

The recovered measurement module, private profile/selection flags and projection helper retain exactly the eleven-file approved recovery inventory. No production fix was attempted in response to the exception-class mismatch.

```yaml
CONTEXT_MATRIX_FINAL: NOT_RUN_AFTER_ALIGNMENT_BLOCKER
DIST_28_FINAL: NOT_RUN_AFTER_ALIGNMENT_BLOCKER
CONTEXT_ESTIMATOR_CONTRACT: exact-utf8-byte-count/v1
RUNTIME_CONSUMPTION_VERIFIED: null
HOST_PROBES_PERFORMED: 0
CODEFLOWMU_FILES_MODIFIED: 0
REQUESTED_GATE: NONE
```
