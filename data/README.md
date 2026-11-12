# Evidence index

All paths are repository-local. Private host/path metadata is redacted; scientific
numbers and outcomes remain unchanged. See [provenance](../docs/PROVENANCE.md)
for original versus public hash meanings and what is not included.

| Evidence | Associated source | Scope |
| --- | --- | --- |
| `detection/validation-v2` | `snapshots/detection` | 580 historical detector/strategy records |
| `detection/validation-loss-independent-v4` | `snapshots/detection` | 60 separately registered independent weak-loss confirmation records |
| `detection/validation-v1` | Old failed detector source not certified in this export | First failed 580-case registration and outcome tables |
| `throughput/evidence/pilot-v1` | `snapshots/throughput-first` | 12 first-candidate attempts, including an unfinished boundary |
| `throughput/evidence/pilot-v2` | `snapshots/throughput` | Three updated-pilot attempts |
| `throughput/evidence/full-v2` | `snapshots/throughput` | Seven full-size direct-recovery cases |
| `throughput/evidence/policy-pilot-v2` | `snapshots/throughput` | Two short old-gate compatibility diagnostics |
| `gate/evidence-v1` | `snapshots/gate-first` | Two initial attempts; one invalid; 48 registered cases unrun |
| `gate/evidence` | `snapshots/gate-original` | 50 attempts: 47 completed, two unfinished, one invalid |
| `gate/evidence-terminal-fix` | Current root source | Ten selected repair regressions; 20 definitions intentionally unrun |

Throughput reports and per-attempt CSVs are in `throughput/results`. Each gate
campaign has `registration.json`, cases, attempts, compact run records and its
`gray_gate_summary.json`. Historical detector exports contain registrations,
trial tables and summaries, not their original raw packet traces.

Only the independent confirmation's weak-loss detection row is used for the
historical headline. Do not pool overlapping random streams, policy arms or
deterministic repetitions into an independent detection sample.

Registrations and raw-audit receipts are historical records. To create new
measurements, use new output directories and the matched source snapshot.
