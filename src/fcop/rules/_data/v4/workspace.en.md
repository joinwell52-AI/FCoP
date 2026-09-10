# FCoP 4.0 — workspace

Audience: business-agent. Package: 4.0.0-candidate.1. Language: en.
Primary authority: frozen Core aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6, spec/fcop-4.0-spec.md.
This derived guidance grants no execution, adoption, Host or release authority.
Dependencies (explicit selection): none.

## F4.1.1

Use landed protocol files for coordination, paths for current state, and recorded events for history; never substitute an in-memory status for an authoritative file.

## F4.2.1

Before any 4.0 operation, read fcop/fcop.json: protocol=fcop, protocol_version=4.0, workspace_id, encoding={name:fcop-filesystem,version:4.0}, and profiles must declare the workspace. A rule package is not this declaration.

## F4.2.2

Keep the canonical lowercase UUID URN stable. Require every envelope to match that workspace_id; reject mismatch with WORKSPACE_ID_MISMATCH.

## F4.2.3

Treat profiles as a set of explicitly adopted identifiers, not precedence by array order. An empty array permits ungated Base operations. Team, role and leader extensions never change Core semantics.

## F4.2.4

A backup or read-only mirror may retain identity. An explicit independent writable fork must receive a new ID before writing; forced retention must reject with WORKSPACE_ID_CLONE_CONFLICT or become explicitly read-only. A tool observing conflicting writable copies may fail closed.

## F4.2.5

Reject unsupported protocol, version or Encoding using UNSUPPORTED_PROTOCOL, UNSUPPORTED_WORKSPACE_VERSION or UNSUPPORTED_ENCODING, respectively; do not downgrade an ambiguous declaration.

## F4.2.6

Do not claim that offline inspection detects invisible clones. Single-writer deployment, replication and network discovery belong outside Core.

## F4.12.1

Validate workspace containment and raw UTF-8/LF before use. Reject traversal, preserve unknown or failed evidence, and never disclose Profile or Runtime credentials.
