# Results and the conclusions they support

All times are simulated whole-job communication time unless explicitly labelled
as detection delay. The simulator does not execute numerical gradient reduction.
The machine-readable records under `data/` retain unfavorable and unfinished
outcomes. [Verification scope](PROVENANCE.md) explains the public export.

## Detection in the historical registered conditions

| Condition | All affected directions correct below 100 ms | P95 detection ms |
| --- | ---: | ---: |
| Blackhole | 60/60 | 8.64 |
| 25% remaining capacity, no injected loss | 60/60 | 29.82 |
| 0.5% weak loss, independent confirmation | 60/60 | 43.12 |
| 80-ms propagation delay | 60/60 | 8.66 |

These rows use `data/detection/validation-v2`, except weak loss which uses only
`validation-loss-independent-v4`. Its separately registered random streams fix
an earlier seed-derivation overlap. The two weak-loss batches are not pooled.
The completed revision has 640 valid runs across its broader matrix, not 640
independent trials of each condition. Healthy controls had 0/60 false alarms,
but deterministic repetitions do not establish broad traffic coverage.

The initial validation remains under `validation-v1`: 530 valid records and
50 infrastructure errors among 580 registrations. Its quarter-capacity primary
queue had 42/60 timely trials, with 18 missed-direction outcomes. Adding receiver
spacing evidence addressed those cases; it did not establish universal detection.

## Long-workload direct recovery

Matched 30-phase / 15-GiB workload; healthy communication time is 480.178448 ms.

| Condition | Prior integration ms | Pipelined shared-helper recovery ms | Healthy-normalized useful throughput | Fresh B-prime chunks |
| --- | ---: | ---: | ---: | ---: |
| Healthy | 480.18 | 480.18 | 100.00% | 0 |
| Blackhole | 907.90 | 649.92 | 73.88% | 10,318 |
| Weak loss | 694.96 | 615.10 | 78.07% | 7,479 |
| Weak loss, fresh matched seed | — | 624.97 | 76.83% | 7,500 |

This demonstrates usable proxy capacity for both rescued and newly assigned
work, in the stated workload. Physical pipeline overlap, bounded shared lending
and disjoint helper selection provide the revision's execution changes.
Shared lending is an extension of the earlier idle-only design.

All 24 registered throughput attempts passed execution/observation checks;
23 completed and one no-healthy-helper case remained unfinished. The seven
full-size runs include an idle-only blackhole control at 868.17 ms / 55.31% of
the original healthy reference; it has no separately registered full-size
idle-mode healthy denominator. Healthy and blackhole repeats across seeds are
deterministic. This is a small development cohort, not a statistical guarantee.

The 73.88%–78.07% rows use **direct recovery**. They do not validate the benefit
gate or establish 70%–80% retention in every fault family.

## Short-workload gate diagnostic

Matched four-phase / 2-GiB workload; healthy communication time is 63.965513 ms.
Confirmation measurements compare identical fault scene and seed within each row.

| Condition | Adaptive only ms | Direct recovery ms | New gate ms | Observation |
| --- | ---: | ---: | ---: | --- |
| Transient 25% capacity, 20 ms | 72.619 | 80.313 | 72.675 | Gate avoids an expensive replacement and stays close to adaptive-only |
| Sustained 25%, helper-local 1 Gb/s | — | 109.149 | 95.444 | Rejecting the slow alternative helps |
| Sustained 25%, ordinary helper-local links | 95.444 | 82.404 | 95.444 | Gate rejects a useful replacement |
| Weak loss, confirmation seed | — | 88.572 | 91.503 | Gate remains slower |
| No healthy helper | — | Unfinished at 249 ms | Unfinished at 249 ms | Detection does not ensure a recovery route exists |

The 20 pilot and 30 confirmation attempts contain 49 valid records: 47 completed
and two unfinished. One sustained-50% candidate failed a real terminal helper
release check. This failed run is retained, not accepted as an old performance
measurement. The separate first campaign also retains one valid and one invalid
attempt and 48 unrun registrations after an audit-model false positive.

The main gate study demonstrates why profitability matters, with both useful
rejections and harmful rejections. It does not show general superiority. The
gate's current helper/pipeline forecast is conservative in some traces. A paid
multi-chunk route measurement is a proposed follow-up, not an implemented result.

## Terminal repair and remaining detector miss

The current default source fixes terminal lease release. It has a separate
ten-case native regression: four healthy arms, two blackhole arms and four
50%-capacity arms. All ten pass execution/observation audits and complete;
20 other registered definitions are explicitly unrun.

Every selected run preserves the pre-repair completion time, policy decisions,
alarm stream and precompletion control records. Final-phase leases now release
through charged messages. The original invalid record is still invalid.

However, every repaired 50%-capacity arm alarms on path 13 after 8.726741 ms and
misses affected path 721 through the 250-ms monitor horizon. These four outcomes
remain detection misses even though their execution is valid. The broader
95%-within-100-ms target remains unresolved.

## What to accept from this release

The combined simulation and proxy execution are implemented. Selected long
blackhole/weak-loss cases retain about 74%–78% of healthy useful throughput.
The gate avoids some costly activations, but still loses in other paired cases.
Historical detector passes are bounded by their conditions; moderate slowdown
is a current counterexample. External-system comparisons, scale-out claims and
physical GPU results are not established by these measurements.

Use `python3 verify_release.py --write-tables results` to regenerate compact
review tables from the included records. See [the data index](../data/README.md)
for every campaign and its associated source snapshot.
