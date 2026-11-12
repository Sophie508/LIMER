# LIMER

**Gray-fault detection and adaptive communication recovery through network simulation.**

LIMER studies a sender using two active network paths. When one path continues
to deliver data but becomes unreliable or slow, the system detects the degraded
service, adjusts chunk allocation, and can borrow other GPUs' network paths to
relay unfinished and subsequent data. A benefit gate estimates
whether opening that relay is worthwhile for the remaining communication.

This repository is a self-contained assessment release. It includes the network
backend, source, tests, registered experiment conditions and compact results.

## Start here

| Question | Read |
| --- | --- |
| How does the combined system work? | [System and six components](docs/SYSTEM.md) |
| What are gray faults and the exact conditions? | [Conditions, controls and metrics](docs/EXPERIMENTS.md) |
| What are the experiment results? | [Results](docs/RESULTS.md) |
| How do I check or rerun it? | [Reproduction guide](docs/REPRODUCE.md) |
| Where did the code and evidence come from? | [Provenance](docs/PROVENANCE.md) and [third-party notices](THIRD_PARTY.md) |

## Experimental results

| Study | Setup | Result |
| --- | --- | --- |
| Historical detection | Blackhole, 25%-capacity slowdown, independent 0.5% loss and 80-ms delay | 60/60 trials per condition detected all affected directions within 100 ms |
| Direct relay recovery | 30 phases / 15 GiB | Healthy-normalized useful throughput: 73.88% under blackhole; 78.07% under weak loss; 76.83% on a fresh loss draw |
| Benefit gate: transient slowdown | Four phases / 2 GiB; direct recovery → benefit gate | Completion time: 80.31 → 72.68 ms |
| Benefit gate: slow helper-local links | Four phases / 2 GiB; direct recovery → benefit gate | Completion time: 109.15 → 95.44 ms |
| Benefit gate: sustained 25%-capacity slowdown | Four phases / 2 GiB; direct recovery → benefit gate | Completion time: 82.40 → 95.44 ms |
| Detection at 50% remaining capacity | Four phases / 2 GiB; 250-ms observation horizon | One affected direction missed in each of the four policy arms |

The throughput study evaluates direct recovery on a 30-phase / 15-GiB workload.
The gate study compares adaptive allocation, direct recovery, the old gate and
the new gate on a four-phase / 2-GiB workload.

## Quick check

Python 3.8+ and a C++ compiler are sufficient for source checks and tests:

```bash
git clone https://github.com/Sophie508/LIMER.git
cd LIMER
python3 verify_release.py
python3 limer.py check
```

The current local regression suite contains 216 tests, including negative
controls against the bundled pre-repair callbacks. Full native simulation builds
run on Linux and require the dependencies described in the reproduction guide.

## Repository layout

```text
src/                 Current native simulator implementation
python/              CLI, audits and independent observation/policy replay
tools/               Registered campaign runners and scoring
tests/               Unit, callback and negative-control regressions
third_party/         Included fixed network backend and upstream notices
experiments/         Presets and registered gate definitions
data/                Public compact evidence and historical tables
snapshots/           Source versions associated with historical measurements
docs/                System, experiments, results and reproduction
provenance/          Export/source mapping and original file identities
```

The default source includes the terminal helper-release repair, verified in ten
regression runs. [The data index](data/README.md) maps experiment records to
their source snapshots.

`verify_release.py` checks exported file hashes, source identities, registered
trial counts and compact result tables. Export details are in the
[provenance guide](docs/PROVENANCE.md).
