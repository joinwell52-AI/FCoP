from pathlib import Path
from tempfile import TemporaryDirectory
from statistics import median
import hashlib, json, os, sys, time

ROOT = Path('D:/codeflowmu/.cache/fcop-query-source-20261113')
PACKET = ROOT/'research/evidence/changes/PERF-20261113-SCOPED-REPORT-READ'
sys.path[:0] = [str(ROOT/'src'), str(ROOT)]
from examples.v4.application import Application
from fcop.v4 import reports

candidate = reports.ReportQueries
old_namespace = {'__name__': 'fcop.v4.reports_baseline'}
exec(compile((PACKET/'baseline-source/reports.py').read_bytes(), 'baseline-reports.py', 'exec'), old_namespace)
baseline = old_namespace['ReportQueries']

def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}

rows = []
with TemporaryDirectory(prefix='fcop-scope-bench-') as directory:
    root = Path(directory)
    app = Application(root)
    tasks = []
    for index in range(6):
        task = app.task('Fixed task '+str(index))
        attempt = app.project.inspect_state(task_id=task)['current_attempt_id']
        report = app.project.write_report(
            workspace_id=app.workspace_id, sender='ME', recipient='ME', subject_ref=task,
            body='Evidence '+str(index)+'\n'+'x'*8192, attempt_id=attempt,
            report_kind='final', result='done')
        tasks.append((task, attempt, report))
    task, attempt, first = tasks[0]
    app.project.write_report(
        workspace_id=app.workspace_id, sender='ME', recipient='ME', subject_ref=task,
        body='Replacement\n'+'y'*8192, attempt_id=attempt,
        report_kind='replacement', result='done', references=[first['report_id']])
    before = snapshot(root)
    original_resolver = reports.report_head
    for operation in ('read_report', 'scoped_heads', 'all_heads'):
        expected = None
        for pair, order in enumerate(('AB', 'BA', 'AB'), 1):
            for label in order:
                query_class = baseline if label == 'A' else candidate
                counts = dict(head_resolutions=0, inventory_scans=0)
                original_scan = query_class._scan
                def scan(self):
                    counts['inventory_scans'] += 1
                    return original_scan(self)
                def resolve(*args, **kwargs):
                    counts['head_resolutions'] += 1
                    return original_resolver(*args, **kwargs)
                reports.ReportQueries = query_class
                query_class._scan = scan
                reports.report_head = resolve
                old_namespace['report_head'] = resolve
                try:
                    start = time.perf_counter()
                    if operation == 'read_report':
                        result = app.project.read_report(first['report_id'])
                    elif operation == 'scoped_heads':
                        result = app.project.list_reports(subject_ref=task, attempt_id=attempt, head_only=True)
                    else:
                        result = app.project.list_reports(head_only=True)
                    elapsed = (time.perf_counter()-start)*1000
                finally:
                    query_class._scan = original_scan
                    reports.ReportQueries = candidate
                    reports.report_head = original_resolver
                    old_namespace['report_head'] = original_resolver
                normalized = json.dumps(result, sort_keys=True, ensure_ascii=False).encode()
                result_digest = hashlib.sha256(normalized).hexdigest()
                if expected is None:
                    expected = result_digest
                assert result_digest == expected, (operation, label, 'result drift')
                assert snapshot(root) == before, 'Persisted files changed'
                rows.append(dict(operation=operation, pair=pair, order=order, variant=label,
                                 elapsed_ms=elapsed, result_sha256=result_digest, **counts))
                print(json.dumps(rows[-1]), flush=True)
    summaries = []
    for operation in ('read_report', 'scoped_heads', 'all_heads'):
        variants = {v: median(r['elapsed_ms'] for r in rows if r['operation']==operation and r['variant']==v) for v in 'AB'}
        summaries.append(dict(operation=operation, baseline_median_ms=variants['A'],
                              candidate_median_ms=variants['B'], reduction_percent=(1-variants['B']/variants['A'])*100))
    output = dict(source_origin=reports.__file__, fixture_groups=6, fixture_reports=7,
                  unchanged_files=True, paired_result_parity=True, rows=rows, summaries=summaries)
    with (PACKET/'runs/benchmark-01.json').open('x', encoding='utf-8') as stream:
        json.dump(output, stream, indent=2)
    print(json.dumps(dict(completed=True, summaries=summaries)), flush=True)
