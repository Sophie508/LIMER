# Inspect and reproduce

## Check the public release

Use a full clone or the complete repository archive. `third_party/` is included.
Snapshot dependency links point inside this repository, not into another checkout.

```bash
python3 verify_release.py
python3 limer.py check
python3 verify_release.py --write-tables results
```

The verifier checks public file hashes, source identities, registered denominators,
case identities, completion times, paired ratios and retained miss/unfinished
outcomes. It does not rerun native simulations or raw packet-archive audits.
The callback tests require a C++ compiler. Full tests must run outside Python's
optimized mode, because the inherited simulator/auditor code uses assertions.

Use this public verifier instead of the historical `limer.py verify` and
`verify-reference` commands, which refer to earlier delivery/reference packages.

## Build and run on Linux

Install GCC/G++, CMake, Python 3.8+, pkg-config, Boost headers, GSL, SQLite and
libxml2 development headers. The Dockerfile records the Ubuntu package names.
Build and run outputs must use new directories on a volume with enough quota.

```bash
python3 limer.py build --out /work/limer-build --jobs 2
python3 limer.py run --build /work/limer-build --out /work/limer-healthy \
  --method G11 --scenario healthy --rounds 1 --phases-per-round 4 \
  --chunks 512 --horizon-ms 250 --fault-ms 24 --seed 111213033 \
  --detector service --policy benefit_v2 --replacement-lifetime phase \
  --relay-completion pipelined --helper-mode shared
```

For the exact registered 50%-capacity counterexample, run its included case:

```bash
python3 limer.py run --build /work/limer-build --out /work/limer-half-capacity \
  --case data/gate/evidence-terminal-fix/confirmation-terminal-fix/cases/sustained_50_early-candidate_gate-s111213033.json
```

The default source is the terminal repair. Repeating a historical original
measurement requires its [source snapshot](../data/README.md), rather than
silently using the repaired source or changing parameters.

## Docker

```bash
docker build -t limer:assessment .
mkdir -p outputs
docker run --rm -v "$PWD/outputs:/work" limer:assessment \
  build --out /work/build --jobs 2
docker run --rm -v "$PWD/outputs:/work" limer:assessment \
  run --build /work/build --out /work/healthy \
  --method G11 --scenario healthy --rounds 1 --phases-per-round 4 \
  --chunks 512 --horizon-ms 250 --fault-ms 24 --seed 111213033 \
  --detector service --policy benefit_v2 --replacement-lifetime phase \
  --relay-completion pipelined --helper-mode shared
```

The image provides the simulation environment. Its entry point is `limer.py`.
Local unit checks run directly from the clone because the Docker build context
excludes historical snapshots needed by the negative-control tests.

## Run a newly registered gate campaign

After building the chosen source, register both plans before inspecting outcomes:

```bash
python3 tools/gray_gate_campaign.py register --preset pilot \
  --build /work/limer-build --out /work/limer-pilot
python3 tools/gray_gate_campaign.py register --preset confirmation \
  --build /work/limer-build --out /work/limer-confirmation
python3 /work/limer-pilot/tooling/tools/gray_gate_campaign.py execute \
  --out /work/limer-pilot --workers 1
python3 /work/limer-confirmation/tooling/tools/gray_gate_campaign.py execute \
  --out /work/limer-confirmation --workers 1
```

These commands create new runs on the current source. They do not relabel
historical results or reproduce the original source identity automatically.
For exact original studies, use `snapshots/gate-original` or
`snapshots/throughput` with the corresponding registered cases.

The runner freezes source, binary, build, conditions and tooling. Run the frozen
tooling path when resuming. Never overwrite an existing experiment directory.
Failures and unfinished outcomes must remain in the denominator. Repeating a
deterministic scene or an existing random seed is a reproduction check, not
new independent validation.

Before large campaigns, measure one run's wall time and storage. The original
gate study used roughly 520 MiB raw working data and a 91-MiB archive for one
measured case, not a guaranteed bound. Use one worker initially; packet archives
can be substantially larger than the compact public evidence.
