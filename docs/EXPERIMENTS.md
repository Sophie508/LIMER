# Conditions, controls and metrics

## What is a gray fault?

A gray fault leaves the connection alive but degrades useful delivery. Examples
are persistent weak loss repaired by retransmission, or sustained capacity
reduction without packet loss. Blackhole is a complete delivery failure used as
a hard-fault control. Severe delay is also eligible for a delivery-service alarm.
A single ordinary packet loss is not by itself a demonstrated gray-fault episode.

These are deliberately designed simulation injections, not samples from a
production incident dataset or a universal benchmark. Healthy, quarter-capacity,
weak-loss and blackhole families originate in the collaborator's experiments;
delay, duration, moderate slowdown and slow/no-helper cases probe specific limits.

| Condition | Actual injection | Purpose |
| --- | --- | --- |
| Healthy | No fault | False alarms and matched completion denominator |
| Blackhole | 100% loss on one GPU's B access link, both directions | Detection and recovery from no delivery |
| Weak loss | Independent per-packet loss probability 0.005, normal configured service rate | Delivery degradation despite transport repair |
| 25%-capacity slowdown | 0.25 remaining service fraction, zero injected loss | Slow-but-live path |
| 50%-capacity slowdown | 0.50 remaining service fraction, zero injected loss | Moderate degradation; retained missed-path case |
| Transient slowdown | 25% capacity for 20 ms, then recovery | Whether replacement can cost more than waiting |
| Delay | Single-direction propagation delay set to 80 ms on the affected access channel | Severe delay without artificial loss |
| Slow helper-local links | Local relay links set to 1 Gb/s instead of 2400 Gb/s | Expensive alternatives |
| No healthy helper | All four B links in one server blackholed | Detectable fault without a usable local B helper |

The `quarter` name means **25% remaining capacity**, not a 25% reduction.
Exact scenes and seeds in each exported registration override table shorthand.

## Three study families

All use 16 logical GPUs, four per server, two 10-Gb/s access paths, and 64-KiB
chunks. Ordinary helper-local capacity is 2400 Gb/s, a model parameter.

| Study | Workload and timing | Question |
| --- | --- | --- |
| Historical detector validation | Usually 60 phases, 64 chunks/rank/phase, 400-ms horizon; fault time sampled 35–55 ms. The slow-helper boundary uses a separate longer workload/horizon. | Detection in registered fault conditions |
| Direct-recovery throughput | 30 phases, 512 chunks/rank/phase, 15 GiB, fault at 40 ms, 2-s horizon | Useful throughput retained after recovery |
| Current gate diagnostic | Four phases, 512 chunks/rank/phase, 2 GiB, fault at 24 or 40 ms, 250-ms horizon | Profitability of initial relay activation |

The gate transient lasts 20 ms. The pilot uses seed 111213001; confirmation uses
111213033. Plans fix 20 pilot and 30 confirmation cases before execution.
Changing seeds does not create independent samples for deterministic faults.

## Internal ablations

| Method | Allocation | Proxy recovery |
| --- | --- | --- |
| G00 | Fixed A/B ownership | Disabled |
| G10 | Adaptive | Disabled |
| G01 | Fixed A/B ownership | Enabled |
| G11 | Adaptive | Enabled |

The recent gate diagnostic compares G10/always, G11/always, G11/benefit and
G11/benefit_v2. `always` means direct recovery after valid preparation, not free
or instantaneous switching. The detector runs in shadow in non-recovery arms
to preserve its observation cost. These are LIMER ablations, not external-system
reproductions. The current candidate changes estimates, paid helper observations
and temporary-loan lifecycle together; it is not an estimator-only ablation.

## Acceptance and reporting

- Detection delay is delivered controller alarm time minus injection onset.
  Every affected direction must be correctly localized below 100 ms. Missing
  directions, late/wrong alarms and unrun/invalid trials are not removed from
  denominators. Healthy false alarms are reported separately.
- The intended detection target is at least 95% timely correct trials in each
  agreed condition. A small paired diagnostic cannot establish a population
  guarantee; the new 50%-capacity condition currently fails all-path detection.
- Completion time is whole-job communication time after the common 1-ms launch
  offset. It includes modeled helper contention and recovery costs.
- Healthy-normalized useful throughput is `T_healthy / T_fault` for equal payload
  and matched workload. With healthy time 480.178448 ms, at least 70% requires
  at most about 685.97 ms; 80% corresponds to about 600.22 ms.
- A valid unfinished run remains a negative communication outcome. Its horizon
  cap is not an observed finish. Invalid or unrun records have no finish value.
- Do not pool workload families or attribute the long direct-recovery result
  to the new gate. The 100-ms detection deadline is not a job-completion limit.

Registered inputs are under [data](../data/) and
[gate plan definitions](../experiments/registered/). The exported registration
is a metadata-redacted view of the frozen original, not a newly run experiment.
