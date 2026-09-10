# FCoP 4.0 — relations

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): workspace, envelopes.

## F4.5.1

Use exactly parent, branch_of, subject_ref and references. parent is strong TASK hierarchy, not parallel work; branch_of is a strong single Root link; subject_ref is one strong TASK/workspace subject (workspace ISSUE: workspace:<workspace_id>); references are weak existing-envelope citations, mandatory when consumed by a gate.

## F4.5.2

Fail closed with RELATION_INVALID for missing, dangling, cross-workspace, cyclic or non-unique strong relations. Ordinary unresolved weak references yield REFERENCE_UNRESOLVED; gate-used references must resolve or reject the operation.

## F4.5.5

Treat thread_key as Profile/Legacy metadata only. It cannot add, rename or change a Core relation. Branch depth and active-Root requirements are owned by the convergence module.
