# FCoP 4.0 machine contract (WP4A.1)

Authority: frozen F4 contract `aec4c2b21b2ac74f1ffcf99cf06ac14137ba3fc6`, effective Core `1d94b881e38cc0b98ca41c47d25c605431d5f9a7`, and ADMIN Schema Binding taskbook `6ddf6a35235c6aedff6807e5e7aba3f7d515e2ff`. This directory does not revise that contract or declare a release.

`generate.py` is the single declarative source. `python spec/schemas/v4/generate.py` deterministically produces the readable and package-data copies; `--check` verifies every byte. Twelve Draft 2020-12 documents use unique absolute v4 IDs and revision 4.0.0. Their URLs are identifiers, not download requirements. Existing eight schemas above this directory remain historical/3.x artifacts, including their historical version/$id discrepancies.

| Document | Scope |
|---|---|
| workspace | F4.2 declaration and closed encoding object |
| task, report, issue, review | F4.3 four frontmatter shapes, typed identities, known fields |
| transition | F4.4.5 historical event shape and evidence fields |
| authorization-binding | F4.7 from/to binding object |
| family-canonical | F4.6.6 canonical digest input shape |
| create-request-canonical | F4.8.4 exact normalized request input shape |
| create-operation | Stable Toolkit create fact, not a fifth envelope |
| lifecycle-receipt | Stable Toolkit durable receipt including authorized-edge fields |
| recovery-observation | Existing compact recovery observation, not a new receipt protocol |

Only workspace and the four envelope roots are open for opaque Profile values. Fully defined nested Core objects are closed. No new prefix, container, registry or Profile protocol is defined. Optional absent/null authorization context on non-authorizing REVIEWs does not grant authority. Authorization REVIEW conditional structure requires its non-null binding and profile; expiry/attempt/family nullability and effective applicability remain subject to Core gates. Arbitrary root fields do not imply arbitrary public API kwargs.

Strict UTF-8/no-BOM/LF and duplicate JSON/YAML key rejection happen **before** schema evaluation. YAML timestamp objects are normalized to ISO strings for schema evaluation; all fields, including opaque roots, are retained, not projected away. The internal loader in `fcop.v4.schema` uses only bundled data and refuses remote references. It does not add a Project method.

## What a successful validation does NOT prove

Schema validation cannot establish unique authoritative path/NOW, valid T1–T7 execution, issuer trust, freshness or consumption, REPORT head uniqueness, family coverage/digest equality, operation races, crash-recovery classification, or supported filesystem guarantees. Core and behavioral Conformance remain authoritative for these. Historical event `from/to/tool` are strings, not proof of a legal edge; the existing reader intentionally selects the last **valid** active-entry event, not the last arbitrary event. Receipt/binding stage names are closed enumerations. Neither events nor their schema derive NOW.

Root extensions do not enter normalized create request inputs. Full-file evidence hashing still covers extension bytes, and family canonical inputs include the REPORT's complete byte digest. Lifecycle movement retains unknown values semantically while reserializing YAML; it does not promise byte preservation of the original header.

Consumers may load these JSON documents using `importlib.resources.files('fcop').joinpath('_data/schemas/v4')` and an offline `jsonschema` store. Resolve every absolute `$ref` from those bundled documents. Apply Base validation before any local adopted Profile restrictions; a Profile cannot waive Base requirements. The internal validator is implementation detail, not a new supported public API.
