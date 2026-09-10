# WP3A.1 compatibility decision — option B, locally verified

Final local verification passes; ADMIN's implementation Gate is still pending.
The early candidate findings below are preserved as history. The appended ADMIN
clarification and final decision supersede those findings. See CORRECTION-RESULT
for final test evidence; remote delivery is attested only after push/refetch.

## Historical pre-clarification classification (superseded below)

| Declaration | Current candidate behavior |
|---|---|
| Absent | Original empty/legacy detection |
| Strictly parsed legacy object without v4 declaration | Original legacy route |
| Exact supported v4 | v4 binding |
| Unsupported declared v4 protocol/version/encoding | Structured rejection |
| Duplicate keys, bad UTF-8/BOM/CRLF/JSON | Invalid-declaration binding; writes rejected |
| Business protocol_version parameter | Cannot alter binding |

The last invalid-encoding row conflicts with Windows legacy CRLF fixtures and
successful REVIEW expectations. No legacy CRLF exception has been installed.
This remains an ADMIN policy question, not a reason to edit frozen contracts.

## Workspace publication

Validate request and destination, reject retained earlier staging if canonical
is absent, create unpredictable sibling staging, publish manifest inside it,
create/sync all minimal directories, then no-replace rename to canonical fcop/.
On failure, retain staging; after publication/response loss canonical is complete.
Already-existing canonical paths are never merged, deleted or overwritten.
Concurrent contenders are arbitrated by the OS publication, not a cached scan.

Platform primitives:

- Windows MoveFileExW WRITE_THROUGH with no replace/copy flags, as described
  in [Microsoft's directory-move documentation](https://learn.microsoft.com/en-us/windows/win32/fileio/moving-directories).
- Linux renameat2 RENAME_NOREPLACE; unavailable support fails closed. See
  [Linux rename documentation](https://man7.org/linux/man-pages/man2/rename.2.html).
- macOS renamex_np RENAME_EXCL; see Apple's
  [exclusive rename capability](https://developer.apple.com/documentation/foundation/urlresourcevalues/volumesupportsexclusiverenaming)
  and [exclusive flag value](https://developer.apple.com/documentation/kernel/1646220-anonymous/vfs_rename_excl).

Only Windows was executed natively. Native Linux/macOS publication verification
remains required before merge/release. Type checks do not discharge that gate.

## Durable operation identity and path

The fact stores `fcop/_lifecycle/inbox/<task_id>.md`, with slash separators,
no drive, absolute root, empty/dot/dot-dot segments or alternate workspace.
The current root is applied through safe_path only at read/commit time.
API results remain absolute paths; initial and Existing results in the same
location match exactly. Relocation changes only the derived API absolute path,
not task_id, request digest, operation fact or TASK bytes.

workspace_id + operation_kind + operation_id identify the operation key;
task_id and the echoed normalized request digest identify its result.
Initial inbox path and content_digest are a **creation snapshot**, not a second
NOW authority. WP3B must later prove legitimate transitions by task_id and
transition evidence without rewriting this fact. Until that is implemented,
unprovable moved/changed TASK content returns RECOVERY_REQUIRED; no second TASK
is created. Moving the whole Project directory preserves the relative snapshot
and is already covered. This is not a lifecycle migration implementation.

## Historical wrapper candidate and defect (resolved below)

Provisional option B replaces the custom descriptor with explicit policies and
ordinary function wrappers. COMMON_SAFE validate_team is a staticmethod and is
left untouched. V4_HANDLER dispatches the existing creation handlers;
V4_MUTATION_REJECTED, V4_READ_UNAVAILABLE and LEGACY_ONLY preserve refusal of
unsupported v4 surfaces. All 44 public methods are classified. Unknown future
public methods cause a class-construction error rather than silently inheriting
the catch-all strategy. Subclass overrides are ordinary Python extension behavior,
not an isolation/security mechanism.

The compatibility test verifies original 38 method discovery, __name__/__doc__,
signature/binding, real legacy instance/class calls, autospec/patch, inheritance,
and override-with-super on legacy and v4. Unsupported mutator class and instance
calls preserve the filesystem. Project source and public snapshot are unchanged.

However, full conformance exposed that the wrapper's __wrapped__ advertises
legacy signatures on **v4-bound instances**. The frozen driver correctly refuses
these incomplete surfaces, causing four new failures. Therefore the wrapper
candidate is not proven compatible and is not a final decision. This must be
fixed in allowed implementation files, never by weakening driver inspection or
adding tests that bypass it. No additional production edit was made after the
separate taskbook-policy blocker was confirmed.

No new public API, dependency, store, background component or WP3B behavior is
introduced. No commit/push/Gate acceptance is claimed for this partial work.

## ADMIN clarification — supersedes the interim CRLF blocker

ADMIN_CLARIFICATION: WP3A_1_MANIFEST_LINE_ENDING_COMPATIBILITY.
DECISION: APPROVED. AUTHORIZED_SCOPE: WP3A_1_ONLY.
LEGACY_MANIFEST_CRLF: ALLOWED. V4_MANIFEST_CRLF: REJECTED.
V4_MANIFEST_LF: REQUIRED. DUPLICATE_JSON_KEYS: REJECTED_FOR_ALL_VERSION_CLASSIFICATION.
INVALID_UTF8: REJECTED. VERSION_FAIL_OPEN: PROHIBITED.
WP3A_IMPLEMENTATION_ACCEPTED: false. WP3B_AUTHORIZED: false.

Classification must strictly decode UTF-8 and reject duplicate JSON keys before
choosing a version; CRLF is not rejected in that first phase. Confirmed legacy
keeps legacy Encoding; exact v4 applies its strict no-BOM/LF Encoding. Unknown,
conflicting or unclassifiable versions fail closed. The current taskbook's CRLF
blanket is corrected by this explicit ruling, not by silently changing v3.

Required signature contract: legacy instance = old v3; v4 instance = selected
handler; class public surface = unchanged. A minimal private binding connection
in Project initialization/create_workspace is now planned. The former blocker
and candidate defect above are retained as history, not erased. Final results
will be appended after full validation; there is still no WP3B authorization.

## Final classification and compatibility decision

| Input | Final behavior |
|---|---|
| No canonical manifest | Preserve original empty/legacy detection |
| Strict UTF-8 JSON, any repeated key (also nested/escaped) | Reject classification, no writer fallback |
| Invalid UTF-8, BOM, invalid JSON, NaN constants, non-object | Reject classification; diagnostic construction may remain |
| Recognized v1/v2/v3 declaration, LF or CRLF | Original legacy path; no rewriting or migration |
| Historical legacy `version: "2.0.0"` | Original legacy writer, not forced through newer integer config parsing |
| Exact v4 declaration | Apply strict no-BOM/LF Encoding, then validate manifest |
| Exact v4 with CRLF | INVALID_ENVELOPE, zero writes |
| Unknown/malformed version, unsupported protocol/Encoding | Fail Closed with structured code |
| No declared version and not a valid legacy declaration | Invalid binding, no fallback writer |
| Request carries a version | Cannot switch the bound instance |

Both phases use one captured byte sequence: parse_json(classification=True)
enforces UTF-8/unique keys before routing; strict_text applies v4 Encoding only
after selection. Formal v4 reads use the same parse_json unique-key semantics
with the Encoding guard enabled. No last-key-wins probe exists.

Option B is implemented with an explicit immutable 44-method policy table:
COMMON_SAFE / V4_HANDLER / V4_READ_UNAVAILABLE / V4_MUTATION_REJECTED /
LEGACY_ONLY. There is no catch-all installation for future public methods;
class definition rejects an unclassified addition. validate_team remains the
unwrapped safe staticmethod. All other classified methods retain one centralized
version wrapper; no scattered legacy method bodies are changed.

At trusted Project initialization and successful create_workspace, only supported
V4_HANDLER instance slots receive callables wrapped around their bound v4 handler.
They route actual calls through the same class wrapper, preserving validation and
structured errors. inspect.signature therefore sees the handler on v4, the old
method on legacy, and the old class surface for class-level integration. No v3
__signature__ is installed on a v4 instance callable. Subclass overrides are not
shadowed; inherited methods and explicit super calls remain tested.

| Compatibility evidence | Final result |
|---|---|
| Original v3 method AST bodies, parameters and docstrings vs ffbfa008 | 38/38 identical |
| Class public function discovery | 44 methods visible, including static validate_team |
| Original public surface snapshot | Unchanged; snapshot regression passes |
| Legacy instance signatures and binding | PASS |
| Class-style actual legacy calls | PASS |
| Class and legacy-object autospec, patch.object autospec | PASS |
| Freshly created and reopened v4 bound handler signatures | PASS |
| v4 bound-method autospec | PASS |
| Inheritance, overrides and super on v3/v4 | PASS |
| Unsupported mutator instance/class calls | Structured refusal, unchanged tree |
| Unknown future public method policy | Definition rejected, no guessed strategy |
| Original 11 Windows v3 boundary failures | Restored |
| C2-N01/C2-R02/C4-N01/AT-04 wrapper regressions | Restored |

Observable limits: wrappers are normal functions but not identical objects to
their unwrapped implementation; v4 supported instance callables are bound closures,
not native MethodType objects. Signatures and actual calls are tested, not Python
object identity. Whole-object autospec of a v4 Project still encounters its
pre-existing unsupported legacy config property; use the class or v4 bound-method
autospec. This does not change v3 compatibility and no config API was added.

Project edits are limited to the import, two private binding calls and preserving
the invalid-declaration diagnostic under explicit workspace_dir. No source change
to any original 38 legacy method body is present. Relative creation facts and
workspace staging retain the publication/identity behavior documented above.
No T2-T7, new public API, Runtime, dependency, migration or MCP work is included.
The final receipt resolves delivery commits after remote verification; ADMIN
alone may sign WP3A_IMPLEMENTATION_ACCEPTED.
