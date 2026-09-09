# WP4C.6a implementability checkpoint — BLOCKED

Original taskbook: dc4bd62d47c3c422c8e758b588369dd3ed089acd (SHA-256 457ec98aecaad481b68879069771c954d8e4069352ccdbe19838e92ddc61e06e).
Ruling taskbook: cd0fe4df900c3ff0b34beca957097f87a8d4b150 (9619 bytes; SHA-256 988738c5f175fd8ed91f4d9f32772282e79ef3caba6675c6b7ebb0facccb4aba).
Scope: WP4C_6A_HISTORICAL_ASSERTION_ALIGNMENT_AND_WP4C_6_RESUME_ONLY.

## Reproduced boundary conflict

The ruling's section 1 permits only an exact replacement of one ordinary test function. Its replacement still uses `pytest.raises(V4ProtocolError)`, while changing the expected structured code to `toolkit:RULE_SELECTION_INVALID`.

The existing implementation deliberately separates Toolkit distribution failures from Base failures:

- `src/fcop/v4/rule_distribution/_errors.py:15`: `class _DistributionError(FcopError)`.
- `src/fcop/v4/rule_distribution/_errors.py:19`: namespaced structured `code`.
- `src/fcop/v4/rule_distribution/_errors.py:27`: raises that Toolkit error.
- `src/fcop/errors.py:84`: `class V4ProtocolError(FcopError)`, a separate subclass.
- `docs/fcop-4.0/rule-distribution-contract.md:210`: distribution failures are Toolkit errors, not new Base errors; structured fields and zero-write rejection are required.

A read-only import diagnostic on the recovered candidate produced:

```text
MRO=_DistributionError -> FcopError -> Exception -> BaseException -> object
CODE=toolkit:RULE_SELECTION_INVALID
IS_FCOP_ERROR=True
IS_V4_PROTOCOL_ERROR=False
```

Neither exception file was modified by the candidate or this continuation. Their SHA-256 values are respectively `b6aff1437227cd5a606419945b9cd6233291354aea401d5040d302b2e7219b61` and `33e42837ceaca9825effc86af26229ec7a9023e0435f5aa3f683474df2c27aa0`.

## Exact authorized edit and real execution

Only the ordinary function name and expected code were changed, exactly as the ruling specifies. Both parameter nodes remained. The existing fixture, `call`, `snapshot`, exception catch and all other assertions remained unchanged.

Both selected nodes failed on the uncaught `_DistributionError`, not on the zero-effect assertion. The final expected-code assertions were not reached. No missing functionality sentinel was manufactured.

The old ordinary failure is accepted as a superseded stage sentinel; this is a different, narrower mismatch in the replacement snippet's exception class. It does not establish a conflict with the frozen 176 distribution nodes.

## Required ADMIN clarification

Authorize the replacement function to catch the existing public `FcopError` while preserving the exact single structured code assertion, both parameters and the unchanged zero-effect helper. The file already imports `FcopError`. This is a proposed clarification only, not an applied change.

Do not change production error inheritance, introduce a Base code, expose a private error as a new public API, catch generic `Exception`, accept multiple codes or edit frozen tests.

The required first validation is 0 passed / 2 failed. The normal three-commit success pipeline cannot begin with a verified alignment. Implementation work and later validation stopped under the taskbook's strict boundary. Only factual reports may be delivered; the failed local alignment and all eleven recovered candidates remain uncommitted.

REQUESTED_GATE: NONE
