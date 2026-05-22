#!/usr/bin/env python3
"""
Release sync audit — automated R1..R12 checks for FCoP releases.

This is the executable form of `docs/release-process.md` §G's six manual
`rg` commands plus inventory §4's audit-hook contract. It is a repo-side
utility (NOT shipped in the wheel) wired into `release.yml`'s `verify`
job per TASK-20260522-005.

Usage:
    py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1
    py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1 --only versions,changelog
    py -3.10 scripts/release_audit.py --new 3.0.2 --old 3.0.1 --ci

`--ci` exits 1 on any P0 finding. P1 findings are warnings only.

Bilingual output: every finding ships `zh:` + `en:` lines (per ADMIN
red line 3, "双语翻译不能错过").
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Finding model
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    check_id: str
    severity: str  # "P0" | "P1"
    status: str  # "pass" | "fail" | "skip"
    title_zh: str
    title_en: str
    detail_zh: str = ""
    detail_en: str = ""
    remediation: str = ""

    @property
    def is_failure(self) -> bool:
        return self.status == "fail"


@dataclass
class AuditReport:
    findings: list[Finding] = field(default_factory=list)

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    @property
    def p0_failures(self) -> list[Finding]:
        return [f for f in self.findings if f.is_failure and f.severity == "P0"]

    @property
    def p1_failures(self) -> list[Finding]:
        return [f for f in self.findings if f.is_failure and f.severity == "P1"]

    def render_text(self) -> str:
        lines: list[str] = []
        lines.append("=" * 72)
        lines.append("FCoP Release Sync Audit — R1..R12")
        lines.append("=" * 72)
        for f in self.findings:
            icon = {"pass": "OK ", "fail": "XX ", "skip": "-- "}[f.status]
            lines.append(f"[{icon}] {f.check_id} ({f.severity}) {f.title_zh}")
            lines.append(f"     en: {f.title_en}")
            if f.status == "fail":
                if f.detail_zh:
                    lines.append(f"     zh: {f.detail_zh}")
                if f.detail_en:
                    lines.append(f"     en: {f.detail_en}")
                if f.remediation:
                    lines.append(f"     fix: {f.remediation}")
        lines.append("-" * 72)
        lines.append(
            f"Summary: {sum(1 for f in self.findings if f.status == 'pass')} pass, "
            f"{len(self.p0_failures)} P0 fail, "
            f"{len(self.p1_failures)} P1 fail, "
            f"{sum(1 for f in self.findings if f.status == 'skip')} skip"
        )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _read_version_py(path: Path) -> str | None:
    text = _read(path)
    m = re.search(r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]', text, re.M)
    return m.group(1) if m else None


def _today_iso() -> str:
    return _dt.date.today().isoformat()


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_r1_version_source_pair(new: str) -> Finding:
    """R1 · src/fcop/_version.py 与 mcp/src/fcop_mcp/_version.py 一致 == new."""
    fcop_v = _read_version_py(REPO_ROOT / "src" / "fcop" / "_version.py")
    mcp_v = _read_version_py(REPO_ROOT / "mcp" / "src" / "fcop_mcp" / "_version.py")
    if fcop_v == new and mcp_v == new:
        return Finding(
            "R1", "P0", "pass",
            "version-source-pair 双 _version.py 已对齐",
            "version-source-pair both _version.py files aligned",
        )
    return Finding(
        "R1", "P0", "fail",
        "version-source-pair 双 _version.py 未对齐",
        "version-source-pair both _version.py files mismatch",
        detail_zh=f"fcop={fcop_v!r} mcp={mcp_v!r} 期望={new!r}",
        detail_en=f"fcop={fcop_v!r} mcp={mcp_v!r} expected={new!r}",
        remediation=(
            f'sed -i \'s/__version__ = "[^"]*"/__version__ = "{new}"/\' '
            f"src/fcop/_version.py mcp/src/fcop_mcp/_version.py"
        ),
    )


def check_r2_mcp_server_json(new: str) -> Finding:
    """R2 · mcp/server.json 顶层 version 与 packages[].version 都 == new."""
    path = REPO_ROOT / "mcp" / "server.json"
    text = _read(path)
    if not text:
        return Finding(
            "R2", "P0", "fail",
            "mcp/server.json 缺失", "mcp/server.json missing",
            remediation="检查文件是否被误删 / Verify the file exists",
        )
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return Finding(
            "R2", "P0", "fail",
            "mcp/server.json 解析失败", "mcp/server.json failed to parse",
            detail_zh=str(exc), detail_en=str(exc),
        )
    top_v = data.get("version")
    pkg_versions = [p.get("version") for p in data.get("packages") or []]
    bad: list[str] = []
    if top_v != new:
        bad.append(f"top-level version={top_v!r}")
    for i, pv in enumerate(pkg_versions):
        if pv != new:
            bad.append(f"packages[{i}].version={pv!r}")
    if not bad:
        return Finding(
            "R2", "P0", "pass",
            "mcp/server.json version 已对齐", "mcp/server.json version aligned",
        )
    return Finding(
        "R2", "P0", "fail",
        "mcp/server.json 版本未对齐", "mcp/server.json version mismatch",
        detail_zh="; ".join(bad) + f"; 期望={new!r}",
        detail_en="; ".join(bad) + f"; expected={new!r}",
        remediation=(
            f"编辑 mcp/server.json,把 top-level + packages[].version 都改成 {new}"
        ),
    )


def check_r3_changelog_block(new: str) -> Finding:
    """R3 · CHANGELOG.md 含 `## [X.Y.Z] — YYYY-MM-DD`(em-dash),日期为今日."""
    text = _read(REPO_ROOT / "CHANGELOG.md")
    today = _today_iso()
    # em-dash U+2014, NOT hyphen-minus.
    pattern = re.compile(
        r"^##\s+\[" + re.escape(new) + r"\]\s+(?:—|-+)\s+(\d{4}-\d{2}-\d{2})",
        re.M,
    )
    m = pattern.search(text)
    if not m:
        return Finding(
            "R3", "P0", "fail",
            "CHANGELOG 缺新版本 section", "CHANGELOG missing new-version section",
            detail_zh=f"未找到 `## [{new}] — YYYY-MM-DD`",
            detail_en=f"could not find `## [{new}] — YYYY-MM-DD`",
            remediation=f"在 CHANGELOG.md 顶部加 `## [{new}] — {today} (...)`",
        )
    raw = m.group(0)
    if "—" not in raw:
        return Finding(
            "R3", "P0", "fail",
            "CHANGELOG 用了普通连字符,期望 em-dash",
            "CHANGELOG uses hyphen, em-dash required",
            detail_zh=f"actual={raw!r}",
            detail_en=f"actual={raw!r}",
            remediation="把 `-` 改成 U+2014 em-dash `—`",
        )
    found_date = m.group(1)
    if found_date != today:
        return Finding(
            "R3", "P0", "fail",
            "CHANGELOG 日期不是今日", "CHANGELOG date is not today",
            detail_zh=f"actual={found_date!r} expected={today!r}",
            detail_en=f"actual={found_date!r} expected={today!r}",
            remediation=f"把 CHANGELOG 头改为 `## [{new}] — {today} (...)`",
        )
    return Finding(
        "R3", "P0", "pass",
        "CHANGELOG section 与日期已对齐", "CHANGELOG section + date aligned",
    )


# Files to scan for stale --old version literal. Excludes CHANGELOG (history).
_PUBLIC_DOCS = [
    "README.md",
    "README.zh.md",
    "mcp/README.md",
    "docs/index.html",
    "essays/README.md",
]


_HISTORICAL_HEADERS_RE = re.compile(
    r"^#+\s*(Recent releases|近期发版|Release history|发版历史)\b",
    re.I,
)


def check_r4_public_docs_stale(new: str, old: str) -> Finding:
    """R4 · 公共门面文档不再含 --old 字面量(历史段豁免)."""
    hits: list[str] = []
    pattern = re.compile(r"\b" + re.escape(old) + r"\b")
    for rel in _PUBLIC_DOCS:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        in_history = False
        for i, line in enumerate(_read(path).splitlines(), 1):
            stripped = line.lstrip()
            # Heading boundaries flip the "history section" mode.
            if stripped.startswith("#"):
                in_history = bool(_HISTORICAL_HEADERS_RE.match(stripped))
            if in_history:
                continue
            # Markdown table rows listing past releases are by construction
            # historical — skip them too.
            if stripped.startswith("|"):
                continue
            if pattern.search(line):
                # Lines that also reference --new are intentional narrative
                # ("3.0.0 / 3.0.1 bug fixed in 3.0.2") — those are not stale.
                if re.search(r"\b" + re.escape(new) + r"\b", line):
                    continue
                snippet = line.strip()[:120]
                hits.append(f"{rel}:{i}: {snippet}")
    if not hits:
        return Finding(
            "R4", "P0", "pass",
            f"公共门面文档无 {old} 残留",
            f"public docs free of stale {old}",
        )
    return Finding(
        "R4", "P0", "fail",
        f"公共门面文档仍含 {old} 字面量",
        f"public docs still mention {old}",
        detail_zh="\n          ".join(hits[:8]),
        detail_en="\n          ".join(hits[:8]),
        remediation=(
            f"逐处替换 {old} → {new},历史段(如 README 发版表)若必须保留 {old} "
            f"请改放进 CHANGELOG"
        ),
    )


def check_r5_mcp_readme_pair(new: str) -> Finding:
    """R5 · README.md / README.zh.md 的"近期发版" / Recent releases 表含 new 一行."""
    findings: list[str] = []
    for rel in ("README.md", "README.zh.md"):
        text = _read(REPO_ROOT / rel)
        if not text:
            findings.append(f"{rel}: 缺文件 / missing")
            continue
        # Look for a markdown table row whose first cell matches the new
        # version. The cell may be wrapped in backticks (`X.Y.Z`) and/or
        # bold markers (**X.Y.Z**), and may carry a trailing "(...)" annex
        # before the next pipe.
        row_re = re.compile(
            r"^\|\s*\**`?" + re.escape(new) + r"`?\**(?:[^|]*?)\|",
            re.M,
        )
        if not row_re.search(text):
            findings.append(f"{rel}: 无 {new} 表行 / no table row for {new}")
    if not findings:
        return Finding(
            "R5", "P0", "pass",
            "README 双语发版表已含新版本行",
            "README bilingual release table contains new-version row",
        )
    return Finding(
        "R5", "P0", "fail",
        "README 发版表未含新版本行",
        "README release table missing new-version row",
        detail_zh="; ".join(findings),
        detail_en="; ".join(findings),
        remediation=f"在 README.md / README.zh.md 顶部表格插入 {new} 一行",
    )


def check_r6_citation_cff(new: str) -> Finding:
    """R6 · CITATION.cff version=v{new}, date-released=今日."""
    text = _read(REPO_ROOT / "CITATION.cff")
    if not text:
        return Finding(
            "R6", "P0", "fail",
            "CITATION.cff 缺失", "CITATION.cff missing",
        )
    today = _today_iso()
    expected_v = f"v{new}"
    m_ver = re.search(r'^version:\s*["\']?([^"\'\n]+)["\']?', text, re.M)
    m_date = re.search(r'^date-released:\s*["\']?(\d{4}-\d{2}-\d{2})["\']?', text, re.M)
    actual_v = m_ver.group(1).strip() if m_ver else None
    actual_d = m_date.group(1) if m_date else None
    bad: list[str] = []
    if actual_v != expected_v:
        bad.append(f"version={actual_v!r} expected={expected_v!r}")
    if actual_d != today:
        bad.append(f"date-released={actual_d!r} expected={today!r}")
    if not bad:
        return Finding(
            "R6", "P0", "pass",
            "CITATION.cff 版本 + 日期已对齐",
            "CITATION.cff version + date aligned",
        )
    return Finding(
        "R6", "P0", "fail",
        "CITATION.cff 版本或日期未对齐",
        "CITATION.cff version or date mismatch",
        detail_zh="; ".join(bad), detail_en="; ".join(bad),
        remediation=(
            f"把 CITATION.cff 的 version 改成 \"{expected_v}\","
            f"date-released 改成 \"{today}\""
        ),
    )


_LETTER_FILES = [
    "src/fcop/rules/_data/letter-to-admin.zh.md",
    "src/fcop/rules/_data/letter-to-admin.en.md",
]


def check_r7_letter_to_admin(new: str) -> Finding:
    """R7 · letter-to-admin.{zh,en}.md 顶部摘要块含 v{new}."""
    expected_marker = f"v{new}"
    bad: list[str] = []
    found_files = 0
    for rel in _LETTER_FILES:
        path = REPO_ROOT / rel
        text = _read(path)
        if not text:
            bad.append(f"{rel}: 缺文件 / missing")
            continue
        found_files += 1
        # Inspect first 60 lines for the version marker.
        head = "\n".join(text.splitlines()[:60])
        if expected_marker not in head:
            bad.append(f"{rel}: 顶部 60 行无 {expected_marker}")
    if not bad and found_files == len(_LETTER_FILES):
        return Finding(
            "R7", "P0", "pass",
            "letter-to-admin 双语摘要已含新版",
            "letter-to-admin bilingual summary mentions new version",
        )
    return Finding(
        "R7", "P0", "fail",
        "letter-to-admin 双语摘要未对齐",
        "letter-to-admin bilingual summary not aligned",
        detail_zh="; ".join(bad), detail_en="; ".join(bad),
        remediation=(
            f"在 letter-to-admin.zh.md 与 letter-to-admin.en.md 顶部加 "
            f"`> **{expected_marker} 摘要**` 段(双份必齐)"
        ),
    )


# inventory §F lists 5 hardcoded assertion sites. Encoded literally here so
# the audit reports the *exact* line if the version literal drifts.
_HARDCODED_SITES = [
    ("mcp/src/fcop_mcp/server.py", 779),
    ("tests/test_fcop/test_rules.py", 104),
    ("tests/test_fcop_mcp/test_server.py", 163),
    ("tests/test_fcop_mcp/test_server.py", 182),
    ("tests/test_fcop_mcp/test_server.py", 196),
]


def check_r8_hardcoded_assertions(new: str) -> Finding:
    """R8 · inventory §F 5 处 vX.Y.Z 字面量 == v{new}."""
    expected = f"v{new}"
    # Match any "v<digit>.<digit>.<digit>" literal so we can detect drift.
    literal_re = re.compile(r"v\d+\.\d+\.\d+")
    drifted: list[str] = []
    missing: list[str] = []
    for rel, lineno in _HARDCODED_SITES:
        path = REPO_ROOT / rel
        if not path.exists():
            missing.append(f"{rel}: 缺文件")
            continue
        lines = _read(path).splitlines()
        if lineno > len(lines):
            missing.append(f"{rel}:{lineno} 行号越界 ({len(lines)} 行)")
            continue
        line = lines[lineno - 1]
        m = literal_re.search(line)
        if not m:
            drifted.append(f"{rel}:{lineno}: 该行不含 vX.Y.Z 字面量")
            continue
        if m.group(0) != expected:
            drifted.append(f"{rel}:{lineno}: 实际={m.group(0)} 期望={expected}")
    issues = drifted + missing
    if not issues:
        return Finding(
            "R8", "P0", "pass",
            "5 处 hardcoded vX.Y.Z 已对齐",
            "5 hardcoded vX.Y.Z literals aligned",
        )
    return Finding(
        "R8", "P0", "fail",
        "hardcoded vX.Y.Z 字面量未对齐",
        "hardcoded vX.Y.Z literals not aligned",
        detail_zh="\n          ".join(issues),
        detail_en="\n          ".join(issues),
        remediation=(
            f"逐行更新 inventory §F 列举的 5 处,把 vX.Y.Z 改成 {expected};"
            f"或更新 inventory §F 行号(若代码已重排)"
        ),
    )


def check_r9_adr_no_proposed(allow_proposed: set[str]) -> Finding:
    """R9 · adr/ADR-*.md 不含 ^Status: Proposed(白名单豁免)."""
    adr_dir = REPO_ROOT / "adr"
    if not adr_dir.exists():
        return Finding("R9", "P1", "skip",
                       "无 adr/ 目录", "no adr/ dir")
    # Match the ADR header Status line in two shapes:
    #   1) "Status: Proposed"           (plain or **bold** key)
    #   2) "| **Status** | Proposed |"  (markdown table row)
    # We require Proposed to be the *value* (followed by end-of-line,
    # whitespace, or a `|`/`)` boundary) so narrative mentions like
    # "Status: Proposed,non-binding,..." inside body prose are NOT
    # treated as the ADR's own status. Only inspect the first 80 lines
    # of each file — ADR Status fields always live in the header table.
    proposed_plain = re.compile(
        r"^\s*\*{0,2}Status\*{0,2}\s*[:：]\s*\**Proposed\**\s*$", re.M
    )
    proposed_table = re.compile(
        r"^\|\s*\*{0,2}Status\*{0,2}\s*\|\s*\**Proposed\**\s*\|", re.M
    )
    bad: list[str] = []
    for path in sorted(adr_dir.glob("ADR-*.md")):
        stem = path.stem.lower()
        if stem in allow_proposed:
            continue
        head = "\n".join(_read(path).splitlines()[:80])
        if proposed_plain.search(head) or proposed_table.search(head):
            bad.append(path.name)
    if not bad:
        return Finding("R9", "P1", "pass",
                       "无 Proposed 状态的 ADR",
                       "no ADR in Proposed state")
    return Finding(
        "R9", "P1", "fail",
        "存在 Status: Proposed 的 ADR(发版前应转 Accepted)",
        "ADRs still in Proposed state (should be Accepted before release)",
        detail_zh=", ".join(bad), detail_en=", ".join(bad),
        remediation=(
            "把对应 ADR 的 `Status: Proposed` 改成 `Accepted`,"
            "或用 --allow-proposed adr-NNNN 显式豁免"
        ),
    )


def check_r10_backup_remote() -> Finding:
    """R10 · git remote -v 含 ^backup\\s 两行(fetch + push)."""
    try:
        out = subprocess.run(
            ["git", "remote", "-v"],
            cwd=REPO_ROOT, capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return Finding("R10", "P1", "skip",
                       "git 不在 PATH", "git not on PATH")
    if out.returncode != 0:
        return Finding("R10", "P1", "skip",
                       "git remote -v 失败", "git remote -v failed",
                       detail_zh=out.stderr.strip(),
                       detail_en=out.stderr.strip())
    backup_lines = [
        l for l in out.stdout.splitlines() if re.match(r"^backup\s", l)
    ]
    if len(backup_lines) >= 2:
        return Finding("R10", "P1", "pass",
                       "backup remote 已配置(fetch + push)",
                       "backup remote configured (fetch + push)")
    return Finding(
        "R10", "P1", "fail",
        "backup remote 缺失(fetch + push 应都有)",
        "backup remote missing (fetch + push expected)",
        detail_zh=f"实际行数={len(backup_lines)}",
        detail_en=f"actual line count={len(backup_lines)}",
        remediation=(
            "git remote add backup <url>;"
            "依据 RULES-release-sync-checklist 红线 2"
        ),
    )


def check_r11_mcp_pyproject_pin(new: str) -> Finding:
    """R11 · mcp/pyproject.toml 含 fcop>=MAJOR.MINOR.0,<MAJOR.MINOR+1.0."""
    text = _read(REPO_ROOT / "mcp" / "pyproject.toml")
    if not text:
        return Finding("R11", "P1", "skip",
                       "mcp/pyproject.toml 缺失",
                       "mcp/pyproject.toml missing")
    try:
        major, minor, _ = new.split(".", 2)
        major_i = int(major)
        minor_i = int(minor)
    except (ValueError, IndexError):
        return Finding("R11", "P1", "skip",
                       f"--new 不符合 X.Y.Z: {new}",
                       f"--new is not X.Y.Z: {new}")
    # ADR-0002 §1.x: 协议 frozen 后(MAJOR>=1)允许 MINOR drift,
    # pin 形如 ``fcop>=X.<lower>,<(X+1).0``;0.x 阶段才走 ``<X.Y+1.0`` 严格 lockstep。
    if major_i >= 1:
        pin_re = re.compile(
            rf'"(fcop\s*>=\s*{major_i}\.\d+(?:\.\d+(?:rc\d+|a\d+|b\d+|c\d+|\.dev\d+)?)?'
            rf'\s*,\s*<\s*{major_i + 1}\.0)"'
        )
        m = pin_re.search(text)
        if m:
            return Finding("R11", "P1", "pass",
                           f"mcp/pyproject.toml 已 pin {m.group(1)}",
                           f"mcp/pyproject.toml pins {m.group(1)}")
        expected = f"fcop>={major_i}.0.0,<{major_i + 1}.0"
        return Finding(
            "R11", "P1", "fail",
            f"mcp/pyproject.toml 未按 ADR-0002 §1.x 规则 pin fcop",
            f"mcp/pyproject.toml does not pin fcop per ADR-0002 §1.x",
            detail_zh=f"期望形如: {expected}(MAJOR>={major_i})",
            detail_en=f"expected form: {expected} (MAJOR>={major_i})",
            remediation=(
                f"把 mcp/pyproject.toml dependencies 中 fcop 行改成 "
                f"\"fcop>={major_i}.<lower>,<{major_i + 1}.0\";per ADR-0002 §1.x"
            ),
        )

    # 0.x: 严格 lockstep,同 MINOR pin
    expected = f"fcop>={major_i}.{minor_i}.0,<{major_i}.{minor_i + 1}.0"
    if expected in text:
        return Finding("R11", "P1", "pass",
                       f"mcp/pyproject.toml 已 pin {expected}",
                       f"mcp/pyproject.toml pins {expected}")
    return Finding(
        "R11", "P1", "fail",
        f"mcp/pyproject.toml 未 pin 同 MINOR fcop",
        f"mcp/pyproject.toml does not pin same-MINOR fcop",
        detail_zh=f"期望片段: {expected}",
        detail_en=f"expected fragment: {expected}",
        remediation=(
            f"把 mcp/pyproject.toml dependencies 中 fcop 行改成 \"{expected}\";"
            f"per ADR-0002"
        ),
    )


_BILINGUAL_PAIRS = [
    ("src/fcop/rules/_data/letter-to-admin.zh.md",
     "src/fcop/rules/_data/letter-to-admin.en.md"),
    ("src/fcop/rules/_data/agent-install-prompt.zh.md",
     "src/fcop/rules/_data/agent-install-prompt.en.md"),
]


def check_r12_bilingual_pairing() -> Finding:
    """R12 · letter-to-admin / agent-install-prompt 双语配对."""
    missing: list[str] = []
    for zh, en in _BILINGUAL_PAIRS:
        zh_p = REPO_ROOT / zh
        en_p = REPO_ROOT / en
        if zh_p.exists() and not en_p.exists():
            missing.append(f"{en} 缺(zh 存在)")
        elif en_p.exists() and not zh_p.exists():
            missing.append(f"{zh} 缺(en 存在)")
        elif not zh_p.exists() and not en_p.exists():
            # Pair is fully absent — recorded as P1, may be intentional.
            missing.append(f"{zh} + {en} 双双缺失")
    # internal-readme / fcop-spec-v* discovered dynamically.
    internal_zhs = list((REPO_ROOT / "fcop" / "internal").glob("*.zh.md")) \
        if (REPO_ROOT / "fcop" / "internal").exists() else []
    for zh_p in internal_zhs:
        en_p = zh_p.with_name(zh_p.name.replace(".zh.md", ".en.md"))
        if not en_p.exists():
            missing.append(f"{en_p.relative_to(REPO_ROOT)} 缺(zh 存在)")
    if not missing:
        return Finding(
            "R12", "P1", "pass",
            "双语配对完好", "bilingual pairs intact",
        )
    return Finding(
        "R12", "P1", "fail",
        "双语配对断裂", "bilingual pairs broken",
        detail_zh="\n          ".join(missing),
        detail_en="\n          ".join(missing),
        remediation="补齐缺失的 .en.md / .zh.md 配对",
    )


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

CHECK_REGISTRY: dict[str, tuple[str, Callable[..., Finding]]] = {
    "versions": ("R1", check_r1_version_source_pair),
    "mcp-server": ("R2", check_r2_mcp_server_json),
    "changelog": ("R3", check_r3_changelog_block),
    "public-docs": ("R4", check_r4_public_docs_stale),
    "readme-pair": ("R5", check_r5_mcp_readme_pair),
    "citation": ("R6", check_r6_citation_cff),
    "letter": ("R7", check_r7_letter_to_admin),
    "hardcoded": ("R8", check_r8_hardcoded_assertions),
    "adr": ("R9", check_r9_adr_no_proposed),
    "backup-remote": ("R10", check_r10_backup_remote),
    "pin": ("R11", check_r11_mcp_pyproject_pin),
    "bilingual": ("R12", check_r12_bilingual_pairing),
}


def run_audit(new: str, old: str, only: Iterable[str] | None,
              allow_proposed: set[str]) -> AuditReport:
    report = AuditReport()
    selected = set(only) if only else set(CHECK_REGISTRY)
    if only:
        unknown = selected - set(CHECK_REGISTRY)
        if unknown:
            print(f"::warning::unknown check(s) ignored: {sorted(unknown)}",
                  file=sys.stderr)
    # Fixed order matching R1..R12.
    order = ["versions", "mcp-server", "changelog", "public-docs",
             "readme-pair", "citation", "letter", "hardcoded",
             "adr", "backup-remote", "pin", "bilingual"]
    for name in order:
        if name not in selected:
            continue
        _, fn = CHECK_REGISTRY[name]
        if name == "versions":
            report.add(fn(new))
        elif name == "mcp-server":
            report.add(fn(new))
        elif name == "changelog":
            report.add(fn(new))
        elif name == "public-docs":
            report.add(fn(new, old))
        elif name == "readme-pair":
            report.add(fn(new))
        elif name == "citation":
            report.add(fn(new))
        elif name == "letter":
            report.add(fn(new))
        elif name == "hardcoded":
            report.add(fn(new))
        elif name == "adr":
            report.add(fn(allow_proposed))
        elif name == "backup-remote":
            report.add(fn())
        elif name == "pin":
            report.add(fn(new))
        elif name == "bilingual":
            report.add(fn())
    return report


def main(argv: list[str] | None = None) -> int:
    # Windows consoles default to GBK; force UTF-8 so bilingual zh/en lines
    # render reliably both locally and in CI.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, OSError):
        pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new", required=True, help="Target version, e.g. 3.0.2")
    parser.add_argument("--old", required=True, help="Previous version, e.g. 3.0.1")
    parser.add_argument(
        "--only",
        help=("Comma-separated check names; available: "
              + ", ".join(sorted(CHECK_REGISTRY))),
    )
    parser.add_argument(
        "--allow-proposed",
        default="",
        help=("Comma-separated ADR stems to whitelist as Proposed, "
              "e.g. adr-0034,adr-0035"),
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="Exit 1 on any P0 failure (P1 stays warning).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of text.",
    )
    args = parser.parse_args(argv)
    only = [s.strip() for s in args.only.split(",")] if args.only else None
    allow = {s.strip().lower() for s in args.allow_proposed.split(",") if s.strip()}
    report = run_audit(args.new, args.old, only, allow)
    if args.json:
        payload = {
            "findings": [f.__dict__ for f in report.findings],
            "p0_failures": len(report.p0_failures),
            "p1_failures": len(report.p1_failures),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(report.render_text())
    if args.ci and report.p0_failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
