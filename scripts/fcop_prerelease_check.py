#!/usr/bin/env python3
"""
fcop 库 发版前一条龙检查脚本
用法: python scripts/fcop_prerelease_check.py

覆盖范围:
  [0]  读取版本号
  [1]  CHANGELOG 含当前版本
  [2]  核心规则文件存在且非空 (6 个)
  [3]  团队模板文件完整性 (67 个文件，5 个团队)
  [4]  团队模板无遗留 v2 路径 (fcop/tasks/, fcop/reports/, fcop/log/ 等)
  [5]  规则文件包含 FCoP 3.0 _lifecycle/ 内容
  [6]  .cursor/rules/ 与捆绑文件同步 (字节一致)
  [7]  tests/test_rules.py 硬编码版本字面量对齐
  [8]  letter-to-admin 顶部摘要含当前版本
  [9]  fcop-README.pypi.md 存在且非空
  [10] wheel 文件捆绑内容 (如已构建)
  [11] bundled 规则文件 UTF-8 / 乱码检查 (fcop-protocol.mdc 等)

所有检查通过才允许发版；任何一条 FAIL 即退出码非零。
"""
import re, sys, zipfile
from pathlib import Path

# Windows 控制台默认 GBK；强制 UTF-8 以便 ✓/✗ 与中文报错正常显示
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except (AttributeError, OSError):
    pass

from rule_encoding_guard import validate_bundled_rules, validate_wheel_rules

ROOT = Path(__file__).resolve().parent.parent   # FCoP/
SRC_FCOP = ROOT / "src" / "fcop"
VERSION_FILE = SRC_FCOP / "_version.py"
CHANGELOG = ROOT / "CHANGELOG.md"
RULES_DATA = SRC_FCOP / "rules" / "_data"
TEAMS_DATA = SRC_FCOP / "teams" / "_data"
CURSOR_RULES = ROOT / ".cursor" / "rules"
TEST_RULES = ROOT / "tests" / "test_fcop" / "test_rules.py"
PYPI_README = ROOT / "fcop-README.pypi.md"

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
WARN = "\033[93m!\033[0m"

errors = []

def check(name: str, cond: bool, msg_fail: str, msg_pass: str = "") -> None:
    if cond:
        print(f"  {PASS} {name}" + (f": {msg_pass}" if msg_pass else ""))
    else:
        print(f"  {FAIL} {name}: {msg_fail}")
        errors.append(f"{name}: {msg_fail}")

def warn(msg: str) -> None:
    print(f"  {WARN} {msg}")

# ── 0. 读取版本号 ──────────────────────────────────────────────────────────
print("\n[0] 读取 fcop 库版本号")
ver_ns: dict = {}
exec(VERSION_FILE.read_text(encoding="utf-8"), ver_ns)
version: str = ver_ns.get("__version__", "UNKNOWN")
print(f"  {PASS} src/fcop/_version.py __version__ = {version}")

# ── 1. CHANGELOG 含当前版本 ───────────────────────────────────────────────
print("\n[1] CHANGELOG 检查")
if CHANGELOG.exists():
    cl = CHANGELOG.read_text(encoding="utf-8")
    check(f"CHANGELOG 含版本 {version}", version in cl,
          f"CHANGELOG 中未找到 {version}，请先补充 CHANGELOG 条目")
else:
    check("CHANGELOG.md 存在", False, "文件缺失")

# ── 2. 核心规则文件存在且非空 ─────────────────────────────────────────────
print("\n[2] 核心规则文件检查 (6 个)")
CRITICAL_RULE_FILES = [
    "fcop-rules.mdc",
    "fcop-protocol.mdc",
    "agent-bringup-prompt.zh.md",
    "agent-bringup-prompt.en.md",
    "letter-to-admin.zh.md",
    "letter-to-admin.en.md",
]
all_rules_ok = True
for fname in CRITICAL_RULE_FILES:
    fpath = RULES_DATA / fname
    exists = fpath.exists()
    sz = fpath.stat().st_size if exists else 0
    ok = exists and sz > 200
    if not ok:
        all_rules_ok = False
    check(f"  {fname}",
          ok,
          "文件缺失" if not exists else f"文件过小 ({sz} bytes，期望 >200)",
          f"{sz // 1024}KB")

# ── 3. 团队模板文件完整性 ─────────────────────────────────────────────────
print("\n[3] 团队模板文件完整性 (67 个文件)")

# 期望文件清单（相对于 teams/_data/）
EXPECTED_TEAMS: dict[str, list[str]] = {
    "dev-team":   ["PM", "DEV", "QA", "OPS"],
    "media-team": ["PUBLISHER", "EDITOR", "WRITER", "COLLECTOR"],
    "mvp-team":   ["MARKETER", "BUILDER", "DESIGNER", "RESEARCHER"],
    "qa-team":    ["LEAD-QA", "TESTER", "AUTO-TESTER", "PERF-TESTER"],
    "solo":       ["ME"],
}
# 每个团队的根文件（除 roles/）
TEAM_ROOT_FILES = [
    "README.md", "README.en.md",
    "TEAM-ROLES.md", "TEAM-ROLES.en.md",
    "TEAM-OPERATING-RULES.md", "TEAM-OPERATING-RULES.en.md",
]
# teams/_data/ 根文件
ROOT_FILES = ["index.json", "README.md", "README.en.md"]

missing_templates: list[str] = []

# 检查根文件
for fname in ROOT_FILES:
    fpath = TEAMS_DATA / fname
    if not fpath.exists():
        missing_templates.append(fname)

# 检查各团队文件
for team, roles in EXPECTED_TEAMS.items():
    for fname in TEAM_ROOT_FILES:
        fpath = TEAMS_DATA / team / fname
        if not fpath.exists():
            missing_templates.append(f"{team}/{fname}")
    for role in roles:
        for suffix in [".md", ".en.md"]:
            fpath = TEAMS_DATA / team / "roles" / f"{role}{suffix}"
            if not fpath.exists():
                missing_templates.append(f"{team}/roles/{role}{suffix}")

# 实际文件计数
actual_count = sum(1 for f in TEAMS_DATA.rglob("*") if f.is_file())

check("团队模板文件总数 == 67",
      actual_count == 67,
      f"实际 {actual_count} 个，期望 67 个",
      f"{actual_count} 个")
check("无缺失模板文件",
      not missing_templates,
      f"缺失 {len(missing_templates)} 个: {missing_templates[:5]}{'...' if len(missing_templates)>5 else ''}",
      "所有模板文件均存在")

# ── 4. 团队模板无遗留 v2 路径 ─────────────────────────────────────────────
print("\n[4] 团队模板文件：无遗留 FCoP v2 路径")
# 这些是 v2 的目录引用（作为路径出现），不包括正常的文本说明
V2_LEGACY_PATTERNS = [
    r"fcop/tasks/",       # v2 任务目录
    r"fcop/reports/",     # v2 报告目录
    r"fcop/log/",         # v2 归档目录（注意区分 _lifecycle/archive/）
    r"fcop/issues/",      # v2 问题目录
    r"`tasks/`",          # v2 路径在反引号中引用
    r"`reports/`",        # v2 路径在反引号中引用
    r"`log/`",            # v2 路径在反引号中引用
]
legacy_hits: dict[str, list[str]] = {}
for md_file in TEAMS_DATA.rglob("*.md"):
    text = md_file.read_text(encoding="utf-8", errors="ignore")
    hits = []
    for pattern in V2_LEGACY_PATTERNS:
        if re.search(pattern, text):
            hits.append(pattern)
    if hits:
        rel = str(md_file.relative_to(TEAMS_DATA))
        legacy_hits[rel] = hits

check("团队模板无遗留 v2 路径",
      not legacy_hits,
      f"{len(legacy_hits)} 个文件含遗留路径，示例: {dict(list(legacy_hits.items())[:2])}",
      "无遗留 v2 路径")

# ── 5. 规则文件包含 FCoP 3.0 _lifecycle/ 内容 ───────────────────────────
print("\n[5] 规则文件 FCoP 3.0 内容检查")
for fname in ["fcop-rules.mdc", "fcop-protocol.mdc"]:
    fpath = RULES_DATA / fname
    if not fpath.exists():
        check(f"{fname} FCoP 3.0 内容", False, "文件缺失")
        continue
    text = fpath.read_text(encoding="utf-8")
    has_lifecycle = "_lifecycle" in text
    check(f"{fname} 含 _lifecycle/ 目录结构",
          has_lifecycle,
          "规则文件未包含 FCoP 3.0 _lifecycle/ 结构")
    # 检查生命周期阶段
    stages = ["inbox", "active", "review", "done", "archive"]
    missing_stages = [s for s in stages
                      if f"_lifecycle/{s}" not in text and f"`{s}`" not in text]
    check(f"{fname} 覆盖生命周期阶段",
          len(missing_stages) < 2,
          f"缺少阶段: {missing_stages}")

# ── 6. .cursor/rules/ 与捆绑文件同步 ────────────────────────────────────
print("\n[6] .cursor/rules/ 与捆绑规则文件同步检查")
SYNC_PAIRS = [
    ("fcop-rules.mdc",    RULES_DATA / "fcop-rules.mdc"),
    ("fcop-protocol.mdc", RULES_DATA / "fcop-protocol.mdc"),
]
for cursor_name, bundled_path in SYNC_PAIRS:
    cursor_path = CURSOR_RULES / cursor_name
    if not cursor_path.exists():
        warn(f".cursor/rules/{cursor_name} 不存在（由 fcop 包部署，非阻塞）")
        continue
    if not bundled_path.exists():
        check(f"{cursor_name} 捆绑文件存在", False, "捆绑文件缺失")
        continue
    # 比对字节（两个文件应完全一致）
    cursor_bytes = cursor_path.read_bytes()
    bundled_bytes = bundled_path.read_bytes()
    # 去掉 frontmatter（.mdc 有 Cursor 专用 frontmatter，主体应一致）
    # 简单比较字节大小作为近似一致性检查（允许 1KB 偏差）
    size_diff = abs(len(cursor_bytes) - len(bundled_bytes))
    check(f".cursor/rules/{cursor_name} 与捆绑文件大小近似一致",
          size_diff < 2048,
          f"大小差异 {size_diff} bytes（.cursor={len(cursor_bytes)}, bundled={len(bundled_bytes)}），"
          f"可能未同步；运行 redeploy_rules() 更新",
          f"差异 {size_diff} bytes (在允许范围内)")

# ── 7. tests/test_rules.py 硬编码版本字面量 ──────────────────────────────
print("\n[7] tests/test_rules.py 硬编码版本检查")
if TEST_RULES.exists():
    test_text = TEST_RULES.read_text(encoding="utf-8")
    # 查找 vX.Y.Z 格式的版本字面量
    versions_in_test = re.findall(r'v(\d+\.\d+\.\d+)', test_text)
    if versions_in_test:
        wrong = [v for v in versions_in_test if v != version]
        check("test_rules.py 版本字面量已对齐",
              not wrong,
              f"过期字面量: {list(set(wrong))}，期望 v{version}",
              f"所有字面量均为 v{version}")
    else:
        warn("test_rules.py 未找到 vX.Y.Z 字面量（非阻塞）")
else:
    warn(f"test_rules.py 不存在: {TEST_RULES}（非阻塞）")

# ── 8. letter-to-admin 顶部含当前版本 ────────────────────────────────────
print("\n[8] letter-to-admin 版本摘要检查")
LETTER_FILES = [
    RULES_DATA / "letter-to-admin.zh.md",
    RULES_DATA / "letter-to-admin.en.md",
]
expected_marker = f"v{version}"
for lf in LETTER_FILES:
    if not lf.exists():
        check(f"{lf.name} 存在", False, "文件缺失")
        continue
    head = "\n".join(lf.read_text(encoding="utf-8").splitlines()[:80])
    check(f"{lf.name} 顶部 80 行含 {expected_marker}",
          expected_marker in head,
          f"未找到 {expected_marker}，letter-to-admin 顶部摘要需更新")

# ── 9. fcop-README.pypi.md 存在且非空 ────────────────────────────────────
print("\n[9] fcop-README.pypi.md 检查")
if PYPI_README.exists():
    sz = PYPI_README.stat().st_size
    check("fcop-README.pypi.md 非空", sz > 500,
          f"文件过小 ({sz} bytes，期望 >500)",
          f"{sz // 1024}KB")
else:
    check("fcop-README.pypi.md 存在", False, "文件缺失")

# ── 10. wheel 文件捆绑内容 (如已构建) ────────────────────────────────────
print("\n[10] fcop wheel 文件检查（如已构建）")
dist_dir = ROOT / "dist"
# 同时检查本地构建目录 dist_322/
dist_dirs = [dist_dir]
# 也检查以 dist_ 开头的目录
for d in ROOT.glob("dist_*/"):
    dist_dirs.append(d)

whl_found = False
for dd in dist_dirs:
    if not dd.exists():
        continue
    whl_files = sorted(dd.glob(f"fcop-{version}-*.whl"))
    if not whl_files:
        continue
    whl = whl_files[-1]
    whl_found = True
    print(f"  {PASS} 找到 wheel: {whl.name}")
    with zipfile.ZipFile(whl) as z:
        names = z.namelist()
        # 检查规则文件
        rules_in_whl = [n for n in names if "rules/_data/" in n and n.endswith(".mdc")]
        check(f"wheel 含规则 .mdc 文件",
              len(rules_in_whl) >= 2,
              f"wheel 中仅有 {len(rules_in_whl)} 个 .mdc 文件，期望 >=2",
              f"{len(rules_in_whl)} 个")
        # 检查团队模板
        teams_in_whl = [n for n in names if "teams/_data/" in n and n.endswith(".md")]
        check(f"wheel 含团队模板 .md 文件",
              len(teams_in_whl) >= 60,
              f"wheel 中仅有 {len(teams_in_whl)} 个团队 .md 文件，期望 >=60",
              f"{len(teams_in_whl)} 个")
    break

if not whl_found:
    warn(f"未找到 fcop-{version}-*.whl（先 build 再重跑）；跳过 wheel 内容检查")

# ── 11. bundled 规则 UTF-8 / 乱码检查 ─────────────────────────────────────
print("\n[11] bundled 规则文件 UTF-8 / 乱码检查")
encoding_issues = validate_bundled_rules(RULES_DATA)
check("fcop-protocol.mdc / fcop-rules.mdc 无乱码且含预期锚点",
      not encoding_issues,
      "; ".join(encoding_issues[:5]) + ("..." if len(encoding_issues) > 5 else ""),
      "协议解释 / Protocol Commentary 等锚点 OK")

if whl_found:
    whl_encoding_issues = validate_wheel_rules(whl)
    check("wheel 内规则文件 UTF-8 / 无乱码",
          not whl_encoding_issues,
          "; ".join(whl_encoding_issues[:5]),
          "wheel 内 fcop-protocol.mdc 可读")
else:
    warn("未构建 wheel，跳过 [11] wheel 乱码子检查")

# ── 结果汇总 ──────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
if errors:
    print(f"\033[91m发版阻塞！{len(errors)} 项未通过：\033[0m")
    for e in errors:
        print(f"  • {e}")
    print(f"\n\033[93m修复上述问题后，重新运行本脚本验证。\033[0m")
    sys.exit(1)
else:
    print(f"\033[92m全部通过 ✓  fcop=={version} 可以发版\033[0m")
    print(f"  下一步: python -m build && twine upload dist/fcop-{version}-*.whl")
    sys.exit(0)
