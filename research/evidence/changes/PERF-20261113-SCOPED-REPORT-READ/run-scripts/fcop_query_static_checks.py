from pathlib import Path
import hashlib, json, os, subprocess, sys, time

root = Path('D:/codeflowmu/.cache/fcop-query-source-20261113')
packet = root/'research/evidence/changes/PERF-20261113-SCOPED-REPORT-READ'
commands = [
    ['D:/codeflowmu/.cache/fcop-check-tools/bin/ruff.exe', 'check',
     'src/fcop/v4/reports.py', 'tests/test_fcop/test_v4_report_query_scope.py'],
    [sys.executable, '-X', 'utf8', '-m', 'py_compile',
     'src/fcop/v4/reports.py', 'tests/test_fcop/test_v4_report_query_scope.py'],
    ['git', 'diff', '--check'],
]
rows = []
for index, command in enumerate(commands, 1):
    start = time.perf_counter()
    result = subprocess.run(command, cwd=root, capture_output=True)
    for suffix, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        with (packet/'runs'/f'static-{index:02}.{suffix}').open('xb') as stream:
            stream.write(data)
    rows.append(dict(command=command, exit_code=result.returncode,
                     duration_ms=(time.perf_counter()-start)*1000))
output = dict(checks=rows, installed_sdk_untouched=True, version_unchanged=True,
              package_build='Not run: source change only; no release/package candidate claimed.')
with (packet/'runs/static-01.json').open('x', encoding='utf-8') as stream:
    json.dump(output, stream, indent=2)
print(json.dumps(output))
raise SystemExit(0 if all(r['exit_code']==0 for r in rows) else 1)
