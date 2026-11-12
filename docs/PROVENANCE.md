# Source and evidence provenance

## Release origin

This is a fresh assessment repository exported from LIMER research revision
`1377d17aa79f0b06d79ab3626305c9df35b0a5fe`. It contains no imported private Git
history. [The source/export index](../provenance/public-export.json) identifies
upstream relative files, original hashes and source snapshots.

The current root source is the terminal helper-release repair. Historical
snapshots retain the implementation used by each study. The network backend is
included once under `third_party/`; snapshot links resolve to that same tree
inside a complete clone. Native scientific code and backend hashes must match
the associated historical registrations.

## Packaging changes

Private local-home paths, research-host paths and host identifiers were redacted
from public copies. Numerical values, fault definitions, seeds, trial names,
validity, alarms, negative results and unrun denominators were not changed.
One inherited report's descriptive host reference was redacted. The current
terminal regression's reference-directory lookup was adapted to the bundled
`snapshots/gate-original` location. No detector, policy, transport, capacity or
fault-injection algorithm was changed for public packaging.

Reader-facing documentation, ignore rules and the public verifier are new.
The original development worktree and original evidence remain unchanged.

## Hash meanings and verification scope

`release-manifest.json` describes the actual bytes in this public export.
Run `python3 verify_release.py` to check it and cross-check source identities,
registered cases, compact outcomes and table derivations.

Historical `COMPACT_MANIFEST.json`, archive receipts, build hashes and their
embedded file hashes describe the **original** research records. Metadata
redaction changes some public JSON/text bytes, so those original manifests must
not be passed to the old compact verifier as if they described this export.
The public index records each original file's hash and whether it was redacted;
the release manifest records each public file's hash. Metadata-redacted copies
are not newly executed registrations or new raw-audit receipts.

Source hash checks include the bundled backend. Recorded operating-system
resource-fork entries (`._*`) are excluded because they are not scientific source.
The failed historical detector v1 retains its registration and trial tables but
does not have a separately certified old detector source snapshot here.

The public export contains gate and throughput compact run records, plus
historical detector tables and registrations. It does not include original
packet archives or compiled binaries. It therefore supports inspection and
fresh source builds, but checking public integrity does not replay the original
raw packet audits. Historical build/audit receipts retain that distinction.

## Attribution

See [THIRD_PARTY.md](../THIRD_PARTY.md), the inherited [LICENSE](../LICENSE),
and the component licenses in `third_party/`. Existing upstream notices remain
attached to the source. This repository does not claim external simulator,
transport or collaborator code as newly original work.
