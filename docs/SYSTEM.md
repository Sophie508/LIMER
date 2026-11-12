# How the combined system works

## One concrete transfer

A source GPU and destination GPU communicate over two active paths, A and B.
The scheduler assigns 64-KiB chunks to these paths. If B slows down, adaptive
allocation gives faster paths more future work. This alone cannot rescue every
chunk already assigned to B or restore the original two-path capacity.

The recovery mechanism builds an alternative route:

```text
source GPU -> local helper GPU -> remote helper GPU -> destination GPU
              local transfer     healthy network      local transfer
```

We call this complete route B-prime. It borrows the helpers' existing resources;
it is not a free backup link and does not repair the original B link.

## Six components

| Component | Role |
| --- | --- |
| Splitting | Assigns future chunks according to observed delivery rates; this fast loop continues during recovery. |
| Detection | Looks for abnormal canary service, stalled business ACK progress or sustained receiver-spacing changes. |
| Alarm | Delivers the affected-path warning to the controller through a charged control message. |
| Prepare a helper route | Acquires bounded helper resources and sends a full 64-KiB probe over all three legs; health reports have delivery costs. |
| Benefit gate | Optionally compares predicted completion with and without initial relay activation, including remaining source work and the two helpers' outgoing work. |
| Switch | Coordinates PREPARE/READY/COMMIT and migrates unfinished data; later allocations may also use the relay. |

Direct recovery still requires a validated route and coordination. It simply
does not apply the benefit gate's additional profitability rejection.

## Detection signals

The detector uses observed transport events and receiver samples, never the
injected fault's location, rate, onset or future recovery time.

1. Each original path receives a 64-KiB canary every 2 ms. The first 20 ms
   calibrate a healthy reference. The deadline is
   `max(100 us, 2 * calibrated maximum completion time + 100 us)`.
   Three anomalous canaries within 40 ms, spanning at least 4 ms of submissions,
   can trigger an alarm. Retransmission is also an anomaly; repeated repairs of
   the same canary do not create independent samples.
2. An active, unfinished original business chunk can trigger an alarm after
   40 ms without actual ACK-prefix progress. Idle or unallocated work cannot.
3. Whole-path full-packet receiver gaps are summarized in nonoverlapping 10-ms
   windows. Each window needs 64 samples. Its 10th-percentile gap must exceed
   twice the calibrated reference plus 100 ns in two consecutive windows.

The first satisfied rule produces the path's alarm. A charged 96-byte message
then carries it to the controller. Detection latency ends at delivered alarm
time, not at the internal rule decision.

The goal is detecting abnormal delivery service. Severe delay qualifies even
when a delayed packet is eventually delivered. The fixed canary payload load is
about 2.62% of each 10-Gb/s path before headers and retransmissions.

## Resource sharing and correctness

The current shared-helper extension can lend one of four B-NIC admission
credits before a helper finishes its own workload. Existing transfers drain
normally; forwarded and original traffic share bandwidth and physical limits.
Different simultaneous recoveries select disjoint helpers. This extends the
collaborator's earlier idle-only helper assumption.

Physical data resources can release after the last relay data leg, while
logical completion still waits for the charged final source notification.
A bounded 32-chunk source confirmation window permits overlap. It does not
raise the four physical NIC/helper limits.

Bindings end at each communication phase. The next phase reopens original A/B
eligibility; stale callbacks cannot overwrite a new binding. This reset does
not heal an impaired physical link or erase an already received alarm.

Confirmed prefixes are retained during migration. A logical chunk is complete
only after modeled destination delivery and final notification. Every worker's
declared chunks must complete before the phase barrier advances. The terminal
repair also completes charged helper releases after the final phase transition.

## Contribution being investigated

The combined system connects delivery-service detection, adaptive chunk
allocation, shared-helper recovery and an observation-driven activation choice.
The narrower research question is whether remaining current-phase work and
helper burden can distinguish worthwhile relays from costly ones under gray
degradation. Proxy forwarding and performance-based strategy selection already
exist in prior work; this release does not claim worldwide priority for them.

The gate is a local heuristic for initial activation in each phase, not a
continuous optimizer or a predictor of every worker's critical path. It has
both favorable and unfavorable paired results.
