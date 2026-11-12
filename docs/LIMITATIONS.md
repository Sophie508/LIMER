# Current limitations

- This is network simulation of logical GPU communication. Numerical tensor
  reduction, GPU/HBM activity, computation overlap and physical hardware are not
  validated. Phase/chunk accounting is the implemented correctness boundary.
- The first 20 ms are assumed suitable for healthy calibration. Startup faults,
  arbitrary background congestion and timestamp noise are not qualified.
- Endpoint events and receiver summaries feed a shared detector with ideal
  simulated timestamps. Raw observation/summary exchange and observation processing
  latency are not independently modeled. Alarm, probe, report and recovery
  control transport are charged.
- The fixed topology has 16 logical GPUs and modeled 10-Gb/s access links.
  Published timing does not establish training-scale or scale-out performance.
- All-path detection still misses one direction at 50% remaining capacity.
  Historical four-condition passes do not establish universal gray-fault coverage.
- No healthy helper means recovery may remain unfinished. No validated fallback
  automatically moves every outstanding B chunk onto A in that boundary case.
- Shared helpers extend the original idle-only assumption. Their own work and
  link contention affect actual completion and must remain in comparisons.
- The gate decides initial activation per phase. It does not continuously search
  helper pairs, know future fault duration, or optimize every rank's critical path.
- Helper estimates cover outgoing work; separate incoming contention and tensor
  computation are not fully predicted. Tail persistence and equal-byte helper
  opportunity cost are heuristics. Some useful relays are rejected.
- Proxy re-failure, explicit recovery of the physical B link, arbitrary repeated
  faults and production distributed helper discovery remain unqualified.
- The long direct-recovery study and short gate diagnostic use different payloads
  and phase counts. Their normalized ratios cannot be pooled. The direct recovery
  70%–80% result is not a gate result or a guarantee across all conditions.
- These are internal ablations. Proxy forwarding and performance-based policy
  selection exist in prior work. A complete external-system comparison is not
  part of the reported evidence.
- Original raw packet archives and native binaries are not in this public export.
  Public checks validate the export and included compact records; original
  audit receipts are retained historical evidence, not newly repeated audits.
