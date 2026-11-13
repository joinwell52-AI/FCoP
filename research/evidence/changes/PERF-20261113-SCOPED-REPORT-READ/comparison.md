# Comparison

Public Project API, three paired runs per operation, AB/BA/AB order. All paired result hashes match; persisted fixture/ledger files remain unchanged. Both real-ledger variants use the same existing request-local YAML reuse.

| Dataset | Operation | Baseline median seconds | Candidate median seconds | Reduction |
|---|---|---:|---:|---:|
| Fixture | read_report | 1.061 | 0.275 | 74.06% |
| Fixture | scoped_heads | 0.955 | 0.254 | 73.39% |
| Fixture | all_heads | 0.955 | 0.944 | 1.17% |
| Real ledger | read_report | 28.075 | 2.253 | 91.97% |
| Real ledger | scoped_heads | 30.454 | 2.435 | 92.00% |

Fixture target queries resolve 1 graph instead of 6; query inventory scans fall from 14 to 4. Unscoped all-heads still resolves 6 graphs with 14 inventory scans. The canonical lifecycle/writer report_head resolver is unchanged. Directory reads remain; this is not an indexed lookup.

The earlier live HTTP observations (92.147 ms file view, 36.060 s read_report, 84.251 s report_heads) are different routes/samples, not the paired experiment above. Three pairs are engineering observations, not a research distribution or whole-task/model-time speedup.
