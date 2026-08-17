# AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory

Source-pinned ICML 2026 audit for:

- Paper: [*AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory*](https://arxiv.org/abs/2602.02285v2)
- OpenReview: [`dfqmQ9WhCP`](https://openreview.net/forum?id=dfqmQ9WhCP)
- Authors: Yuanhe Zhang, Jason D. Lee, and Fanghui Liu
- Official code: [`YuanheZ/lean-stat-learning-theory`](https://github.com/YuanheZ/lean-stat-learning-theory) at source-era commit `7b82b1323c80f0c21ca449fd12e1c24315ae9782`

The target collection repository is [`MachineLearning-Nerd/icml26-ai4slt-formalization`](https://github.com/MachineLearning-Nerd/icml26-ai4slt-formalization).

## Status

`SCOPED_PASS` — `VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS`

The source-era Lean library passes its static declaration, line-count, and
placeholder audit. A recorded Hugging Face Jobs run also completed a full
`v4.32.0` release build of the official code path: 8,720 targets, 65 Lean
files, 55,867 Lean lines, zero placeholders, and the Dudley declaration.

The strict paper-level status is `NOT_READY` for two reasons that the gate
keeps explicit: historical priority words such as “first” cannot be proved by
this repository, and the paper-reported 500 hours of supervised development is
provenance rather than a reproducible runtime measurement. The source-era
`v4.27.0-rc1` tree and the release-build `v4.32.0` evidence are never silently
treated as the same checkout.

The canonical gate is [`publication_gate.json`](publication_gate.json), with an
identical copy at [`outputs/publication_gate.json`](outputs/publication_gate.json).
The claim reasoning is in [`docs/CLAIM_AUDIT.md`](docs/CLAIM_AUDIT.md).

## What the paper formalizes

AI4SLT builds a machine-checked Lean 4 foundation for statistical learning
theory from empirical-process ingredients. Its paper-era core includes:

- Gaussian Lipschitz concentration and supporting Efron–Stein, Poincaré, and
  log-Sobolev infrastructure;
- Dudley’s entropy-integral theorem for sub-Gaussian processes; and
- a localized least-squares development with a rank-based minimax rate.

The paper also explains a human–AI formalization workflow. The executable
audit checks the Lean artifacts and build evidence; it does not infer human
authorship or historical priority from the code alone.

## Claim-to-evidence ledger

| Claim | Status | Producer path | Checker path | Evidence |
| --- | --- | --- | --- | --- |
| C1 — comprehensive SLT formalization grounded in empirical processes | `VERIFIED_SCOPED` | `repro/src/audit_source.py` scans the pinned `upstream/SLT` tree; `repro/src/materialize_hf_build.py` parses the full release-build log | `repro/src/cumulative_science_gate.py`, `repro/src/verify_claims.py`, and focused tests | Source-era tree: 55 Lean files, 34,684 lines, zero `sorry`/`admit`/`axiom` placeholders, with Efron–Stein, Gaussian Lipschitz, Dudley, and rank-minimax declarations; release build: all 8,720 targets completed |
| C2 — Dudley entropy-integral theorem for sub-Gaussian processes | `VERIFIED_SCOPED` | Source scan locates `theorem dudley` in `upstream/SLT/Dudley.lean`; release log records the compiled declaration | `cumulative_science_gate.py`, `verify_claims.py`, and `test_source_audit.py` | Source-era declaration at line 2,517; release-build log contains both Dudley markers and `BUILD_SUCCESS` |
| C3 — approximately 30,000 lines of human-verified Lean code | `VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS` | `audit_source.py` counts source-era Lean lines and checks placeholders; `materialize_hf_build.py` records release-build counts | `cumulative_science_gate.py`, `verify_claims.py`, and focused tests | 34,684 source-era `SLT/` lines exceed 30,000, with zero placeholders; the 500-hour human-supervision statement remains paper-reported provenance, not an independently measurable claim |

The gate verifies substantive executable conditions. It does not turn the
words “first” or “human-verified” into automatically decidable facts.

## Repository and branch map

The top-level repository has one published branch: `main`. The `upstream/`
directory is a deliberately detached Git submodule pinned to the source-era
official commit; it is not a second top-level publication branch.

| Path | Role | How it is used |
| --- | --- | --- |
| `upstream/` | Pinned official Lean source at `7b82b132…` | Source-era static audit; initialize with `--recurse-submodules` |
| `docs/primary.pdf` | Vendored arXiv v2 paper PDF | Paper identity and claim anchors |
| `docs/arxiv_source.tar` | Vendored arXiv source archive | Source provenance |
| `repro/src/audit_source.py` | Static Lean source producer | Counts files/lines, checks placeholders, and locates declarations |
| `repro/src/materialize_hf_build.py` | Build-log producer | Converts terminal evidence into `outputs/hf_build.json` |
| `repro/src/verify_claims.py` | Claim producer | Combines source and release evidence into `outputs/claim_verification.json` |
| `repro/src/cumulative_science_gate.py` | Fail-closed checker | Validates pins, log markers, claim statuses, and submodule cleanliness |
| `repro/src/publication_gate.py` | End-to-end gate | Runs the audit/tests and writes both canonical gate copies |
| `outputs/` | Hash-bound evidence | Build log, source audit, claim verdict, and manifests; see [`outputs/README.md`](outputs/README.md) |

See [`docs/BRANCH_AUDIT.md`](docs/BRANCH_AUDIT.md) and
[`docs/SOURCE_AUDIT.md`](docs/SOURCE_AUDIT.md) for exact boundaries.

## Reproduce the audit

Clone the repository with its pinned official submodule:

```bash
git clone --recurse-submodules \
  https://github.com/MachineLearning-Nerd/icml26-ai4slt-formalization.git
cd icml26-ai4slt-formalization
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/publication_gate.py
```

The gate performs the source-era static audit, validates the recorded full
release-build markers, runs the three focused tests, rebuilds the evidence
bundle, and writes identical root/output gate files. It does not require a
Hugging Face token and does not read Trackio metadata, private paths, or queue
state.

The paper-era submodule declares Lean `v4.27.0-rc1`. Its package manifest is no
longer accepted by that release candidate's current parser, so the repository
does not claim a fresh local build of that exact source-era checkout. The
recorded full build uses the official `v4.32.0` release and is documented in
[`docs/hf_job_protocol.md`](docs/hf_job_protocol.md). Re-running a comparable
full Lean build is intentionally a separate, compute-heavy operation.

## Citation

```bibtex
@inproceedings{zhang2026ai4slt,
  title     = {AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory},
  author    = {Zhang, Yuanhe and Lee, Jason D. and Liu, Fanghui},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year      = {2026},
  eprint    = {2602.02285},
  archivePrefix = {arXiv}
}
```

## Thank you

Thank you to Yuanhe Zhang, Jason D. Lee, and Fanghui Liu for making a large
formal learning-theory development public, for exposing the proof structure
behind the headline results, and for releasing an artifact that can be
audited at the source, declaration, and full-build levels.

## Scope limits

- Historical “first” claims require literature-wide evidence and are recorded
  as author/paper provenance, not independently established here.
- The 500-hour human-supervision claim is reported by the paper; executable
  checks verify source size, absence of placeholders, and build evidence only.
- The source-era tree and the later `v4.32.0` build are separate pinned
  artifacts. The gate does not claim bit-for-bit compilation of the former on
  the latter toolchain.
- The gate does not forecast an external evaluator score; `score_forecast` is
  intentionally `null`.
