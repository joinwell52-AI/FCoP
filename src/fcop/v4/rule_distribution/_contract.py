"""Private frozen RD-04/07/08 identities; no Runtime registry."""

MODULES = ["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility","convergence"]
DEPS = {"workspace":[],"envelopes":["workspace"],"relations":["workspace","envelopes"],"authorization":["workspace","envelopes","relations"],"idempotency":["workspace"],"recovery":["workspace"],"lifecycle":["workspace","envelopes","relations","authorization","idempotency","recovery"],"compatibility":["workspace"],"convergence":["workspace","envelopes","relations","authorization","idempotency","recovery","lifecycle","compatibility"]}
OWNED = {"workspace":["F4.1.1","F4.2.1","F4.2.2","F4.2.3","F4.2.4","F4.2.5","F4.2.6","F4.12.1"],"envelopes":["F4.3.1","F4.3.2","F4.3.3","F4.3.4","F4.3.5"],"relations":["F4.5.1","F4.5.2","F4.5.5"],"authorization":["F4.7.1","F4.7.2","F4.7.3","F4.7.4","F4.7.5","F4.7.6","F4.7.7"],"idempotency":["F4.8.1","F4.8.2","F4.8.3","F4.8.4","F4.8.5"],"recovery":["F4.9.1","F4.9.2","F4.9.3","F4.9.4","F4.9.5","F4.9.6","F4.9.7","F4.9.8","F4.9.9","F4.9.10","F4.9.11"],"lifecycle":["F4.4.1","F4.4.2","F4.4.3","F4.4.4","F4.4.5","F4.4.6","F4.4.7","F4.6.1","F4.6.2","F4.6.3","F4.6.4"],"compatibility":["F4.0.1","F4.0.2","F4.0.3","F4.1.2","F4.1.3","F4.1.4","F4.10.1","F4.10.2","F4.10.3","F4.11.1","F4.11.2","F4.11.3","F4.11.4","F4.11.5","F4.12.2","F4.12.3","F4.12.4"],"convergence":["F4.5.3","F4.5.4","F4.6.5","F4.6.6","F4.6.7","F4.6.8"]}
RELATIONS = ["parent", "branch_of", "subject_ref", "references"]
ARTIFACT_FIELDS = {
    "module_id", "source_path", "language", "sha256", "size_bytes",
    "normative_clause_refs", "depends_on", "load_order", "audience",
    "required_when", "conflicts_with",
}
