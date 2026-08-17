# Output contract

| File | Producer | Meaning |
| --- | --- | --- |
| `source_audit.json` | `repro/src/audit_source.py` | Source-era Lean file/line, placeholder, and declaration evidence |
| `hf_build.json` | `repro/src/materialize_hf_build.py` | Parsed full-release build contract |
| `hf_job_build.log` | recorded HF job | Terminal evidence for the full `v4.32.0` build |
| `claim_verification.json` | `repro/src/verify_claims.py` | Three-claim executable verdict |
| `CUMULATIVE_SCIENCE_GATE.json` | `repro/src/cumulative_science_gate.py` | Current source, release, claim, and control status |
| `evidence_bundle.jsonl` | `repro/src/build_evidence_bundle.py` | Relative-path size/hash manifest for public evidence |
| `publication_gate.json` | `repro/src/publication_gate.py` | Canonical scoped publication status |
| `PUBLICATION_GATE_PASSED.json` | historical | Retired pre-audit marker; never used by the current gate |

The root and `outputs/` publication-gate JSON files must be byte-identical.
The evidence bundle includes the source/build manifests, paper provenance,
claim docs, scripts, and the retained build log, but excludes the two
self-referential gate copies.
