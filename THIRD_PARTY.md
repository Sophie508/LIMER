# Sources and third-party notices

This assessment release preserves upstream source notices and the inherited
license files. Component licenses continue to apply to their respective files.

| Component | Recorded origin | Role |
| --- | --- | --- |
| ns-3/RDMA backend | ns-3 revision `7e3cb5b88c99abcb582c5abc3919484a4805111b`, with the previously integrated RDMA modifications | Fixed packet/network simulator under `third_party/ns3` |
| Network initialization | SimAI revision `f5efb5a93ea9be7db25a8843f9f7ff54044f6062` | Adapted topology, routing and NIC initialization |
| Original integrated splitting/relay implementation | `ZjianJ/simai-limer` revision `7c372d6f7e4e49ac2ccd0d2c923636c6324128b3` | Source lineage for feedback, path binding, ACK handling and relay execution |
| Original M13 detection lineage | `Sophie508/LIMER_draft` revision `1447bc48689802662f0571feaf0d3e03cace1475` | Earlier observer and replay components retained in the source lineage |
| Current combined research revision | `Sophie508/LIMER_draft` revision `1377d17aa79f0b06d79ab3626305c9df35b0a5fe` | Service detector, phase-scoped integration, throughput and benefit-gate studies |

The ns-3 license is included at `third_party/ns3/LICENSE` and
`third_party/LICENSE.ns3`. The SimAI license is included at
`third_party/LICENSE.SimAI`. The inherited project LICENSE is preserved; this
export does not newly relicense collaborator material. Additional fixed-source
records are in `provenance/original_sources.json` and
`provenance/public-export.json`.
