# Reproduction: AI4SLT

This repository independently audits the executable evidence behind
*AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory*
(OpenReview `dfqmQ9WhCP`; arXiv `2602.02285`).

## Contract

The live challenge contract contains three scored claims (six points total):

1. A comprehensive Lean 4 formalization of statistical learning theory rooted
   in empirical processes.
2. A formalized Dudley entropy-integral result for sub-Gaussian processes.
3. Approximately 30,000 lines of human-verified Lean code.

The gate is fail-closed: every claim needs the pinned source-era audit and a
full fresh build of the official release. `outputs/claim_verification.json` is
created only after all three pass.

## Evidence model

`upstream/` pins the paper-era repository revision
`7b82b1323c80f0c21ca449fd12e1c24315ae9782`. Its `SLT/` tree is scanned for
file/line counts, named declarations, and proof placeholders. The source-era
Lean v4.27.0-rc1 manifest is no longer accepted by that RC's package parser;
therefore a fresh, full compilation runs against the official `v4.32.0`
release on Hugging Face Jobs `cpu-upgrade` (8 vCPU). The two revisions remain
explicitly separate in the artifacts.

## Run locally

```bash
.venv/bin/python repro/src/audit_source.py
.venv/bin/python -m pytest -q
```

After downloading terminal output from the successful HF build to
`outputs/hf_job_build.log`, materialize and gate it with:

```bash
.venv/bin/python repro/src/materialize_hf_build.py --job-id <job-id> --log outputs/hf_job_build.log
.venv/bin/python repro/src/verify_claims.py
```

See [the independent audit](docs/independent_proof_audit.md) for scope and the
source-era compatibility limitation.
