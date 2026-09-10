# WP4E publication controls / 发布控制

Phase A is a dry-run only. No publication credential is used, no environment is
created or weakened, and no tag or Release is created. Existing repository
configuration currently has only `github-pages`; a publishing environment must
be independently configured and reviewed before Phase B. Missing protection
causes `publish-preflight` to fail before the environment job can start.

The release workflow has no tag-push trigger. A manual dry-run requires the
accepted head, content commit, RC artifact run ID and candidate Manifest SHA-256.
It downloads and verifies the same four artifacts, never rebuilds on upload.
Only `publish-preflight` can consider publication, and it additionally requires:

1. An OWNER-authored GitHub comment in this repository with one JSON block.
2. `gate=FCOP_4_RC_RELEASE_READY`, `status=SIGNED`, repository, version, tag,
   accepted head, content commit, artifact run ID, Manifest SHA-256 and all four
   artifact hashes matching exactly.
3. Separate true booleans for `phase_b_authorized`, `tag_authorized`,
   `pypi_publish_authorized`, `github_release_authorized`; stable publication false.
4. A pre-existing `fcop-pypi` environment with required reviewers,
   self-review prevention and a branch/tag deployment policy.
5. A successful RC workflow run at the accepted head, and an existing tag
   resolving to that head. Creating a tag remains an independently authorized act.
6. Reverification after environment approval, then upload without rebuilding,
   public PyPI four-file SHA verification, fresh installed identity verification,
   and GitHub Pre-release creation with `--verify-tag --prerelease`.

The two project-scoped PyPI secrets are referenced only by the protected publish
job. No token is requested, read or used by the Phase A dry-run. Workflow
permissions default to read; contents write is restricted to that publish job.
RC acceptance, a tool caller's declaration, this document, a generated report,
and successful CI are not substitutes for the explicit ADMIN publication grant.

中文摘要：Phase A 仅 dry-run，不使用发布凭据、不创建发布 environment、不创建
tag、不上传。将来 Phase B 必须另有 OWNER 的结构化授权，绑定候选 HEAD、内容提交、
制品 run、Manifest 与四个哈希，并明确允许不可逆动作。还需预先配置独立人工审核的
`fcop-pypi` environment 和分支/tag 策略；缺失时默认拒绝。上传只使用已验收制品，
之后从公开 PyPI 回装并核验，RC 必须为 Pre-release，不能写成 stable。

Neither this documentation nor any unit-test authorization fixture is a signed Gate.
部分上传不可逆；若 Phase B 途中失败必须保留结果，由 ADMIN 决定续作，不删除发布历史。
