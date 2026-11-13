from pathlib import Path
import json,os,subprocess,sys,time
root=Path('D:/codeflowmu/.cache/fcop-query-source-20261113');packet=root/'research/evidence/changes/PERF-20261113-SCOPED-REPORT-READ'
target=packet/'baseline-source/reports.py';target.parent.mkdir(exist_ok=True)
with target.open('xb') as stream:stream.write((root/'src/fcop/v4/reports.py').read_bytes())
environment=dict(os.environ,PYTHONPATH=str(root/'src')+os.pathsep+str(root))
command=[sys.executable,'-X','utf8','-m','pytest','-q','tests/test_fcop/test_v4_report_queries.py']
start=time.perf_counter();result=subprocess.run(command,cwd=root,env=environment,capture_output=True)
for suffix,data in [('stdout',result.stdout),('stderr',result.stderr)]:
    with (packet/'runs'/('baseline-01.'+suffix)).open('xb') as stream:stream.write(data)
with (packet/'runs/baseline-01.json').open('x',encoding='utf-8') as stream:json.dump(dict(command=command,exit_code=result.returncode,duration_ms=(time.perf_counter()-start)*1000,source_root=str(root),source_path_override=True),stream,indent=2)
print(json.dumps(dict(exit_code=result.returncode,stdout_tail=result.stdout.decode(errors='replace')[-500:])));raise SystemExit(result.returncode)
