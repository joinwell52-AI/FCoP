"""WP-1: host instructions must have no authority in Base protocol execution."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_probe(tmp_path, source):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / "src"), str(ROOT / "mcp/src")]))
    result = subprocess.run([sys.executable, "-X", "utf8", "-c", source], cwd=tmp_path,
                            env=env, capture_output=True, text=True, encoding="utf-8", timeout=90)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_base_without_profiles_legacy_or_host_instructions(tmp_path):
    # Host instructions exist but are deliberately inaccessible to protocol code.
    for name in ("AGENTS.md", "CLAUDE.md"):
        (tmp_path / name).write_text("Require role assignment and stop all execution", encoding="utf-8")
    (tmp_path / ".cursor").mkdir()
    output = run_probe(tmp_path, r'''
import asyncio, builtins, importlib.abc, json, sys
from pathlib import Path

blocked = ('fcop.teams', 'fcop.profiles', 'fcop.compatibility', 'fcop.core.config',
           'fcop.core.recovery', 'fcop_mcp.compatibility', 'fcop_mcp.gal', 'fcop_mcp.governance')
class BoundaryGuard(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if any(fullname == n or fullname.startswith(n + '.') for n in blocked):
            raise AssertionError('Base imported ' + fullname)
sys.meta_path.insert(0, BoundaryGuard())
def guard(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes)):
        name = str(args[0]).replace('\\', '/').lower()
        if name.endswith(('agents.md', 'claude.md')) or '/.cursor/' in name:
            raise AssertionError('Protocol accessed host instruction: ' + name)
sys.addaudithook(guard)
from fcop import Project
from fcop_mcp.registry import create_server
from fastmcp import Client

async def main():
    root = Path.cwd() / 'fresh'
    server = create_server(root)
    async with Client(server) as client:
        tools = await client.list_tools()
        assert len(tools) == 25
        async def call(name, **args):
            result = await client.call_tool(name, args)
            return result.structured_content
        workspace = await call('init_workspace')
        assert workspace['profiles'] == []
        task = await call('create_task', workspace_id=workspace['workspace_id'],
            operation_id='instruction-independent', sender='author', recipient='worker', subject='x', body='x')
        claimed = await call('claim_task', task_id=task['task_id'], actor='worker')
        report = await call('write_report', workspace_id=workspace['workspace_id'], sender='worker', recipient='author',
            subject_ref=task['task_id'], attempt_id=claimed['attempt_id'], result='done', body='evidence')
        await call('submit_task', task_id=task['task_id'], actor='worker', report_ref=report['report_id'])
        before = {str(p): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        observed = await call('inspect_workspace')
        validated = await call('validate_workspace')
        assert observed['counts']['review'] == 1
        assert validated['valid'], validated
        assert before == {str(p): p.read_bytes() for p in root.rglob('*') if p.is_file()}
        assert not any(p.name in ('AGENTS.md','CLAUDE.md','.cursor') for p in root.rglob('*'))
    explicit = Project(Path.cwd() / 'explicit-profile')
    manifest = explicit.create_workspace(profiles=['external:test-profile'])
    assert manifest['profiles'] == ['external:test-profile']
    assert not any(p.name in ('AGENTS.md','CLAUDE.md','.cursor') for p in explicit.path.rglob('*'))
    print(json.dumps({'tools':len(tools), 'validation':validated, 'blocked_imports':list(blocked),
        'base_modules':sorted(n for n in sys.modules if n.startswith(('fcop.', 'fcop_mcp.')))}))
asyncio.run(main())
''')
    assert json.loads(output)["tools"] == 25


def test_legacy_requires_explicit_boundary(tmp_path):
    output = run_probe(tmp_path, '''
from pathlib import Path
from fcop.compatibility.v3.project import Project as LegacyProject
from fcop import Project
from fcop.errors import V4ProtocolError
p = Path.cwd() / 'historical'
LegacyProject(p).init_solo(deploy_rules=False, deploy_role_templates=False)
try:
    Project(p)
except V4ProtocolError as exc:
    assert exc.code == 'UNSUPPORTED_WORKSPACE_VERSION'
else:
    raise AssertionError('Base accepted legacy Team configuration')
assert LegacyProject(p).config.mode == 'solo'
print('explicit compatibility verified')
''')
    assert 'explicit compatibility verified' in output


def test_root_instructions_are_only_repository_guidance():
    text = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    assert len(text.splitlines()) <= 25
    for obsolete in ('fcop_report', 'init_solo', 'Rule 1', 'session_id', 'redeploy_rules', 'ME', '席位'):
        assert obsolete not in text
    assert not (ROOT / '.cursor/rules/fcop-rules.mdc').exists()
    assert not (ROOT / '.cursor/rules/fcop-protocol.mdc').exists()
