# Status — dfqmQ9WhCP

## Identity

- Paper: *AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory*
- Authors: Yuanhe Zhang, Jason D. Lee, and Fanghui Liu
- arXiv: `2602.02285v2`
- OpenReview: `dfqmQ9WhCP`
- Repository: `https://github.com/MachineLearning-Nerd/icml26-ai4slt-formalization`
- Official source-era submodule: `YuanheZ/lean-stat-learning-theory@7b82b1323c80f0c21ca449fd12e1c24315ae9782`

## Gate state

`SCOPED_PASS` / `VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS`

The source-era audit and recorded full `v4.32.0` Lean build support all three
declared executable contracts. The strict paper-level status is `NOT_READY`
only for historical-priority and human-supervision provenance that cannot be
established from code and logs alone.

## Evidence

- Source-era: 55 Lean files, 34,684 lines, zero placeholders, and four core
  declarations including `dudley` at line 2,517.
- Full release build: Hugging Face Jobs `6a5dc974bee6ee1cf4ed2118`, all 8,720
  targets, 65 Lean files, 55,867 lines, zero placeholders, and `BUILD_SUCCESS`.
- Claim verdict: 3/3 claims and 6/6 executable points pass.
- Focused tests: `repro/tests/`.
- Canonical gate: `publication_gate.json` and `outputs/publication_gate.json`.

## Provenance and branches

Paper PDF/source hashes, source-tree digest, release-build markers, and
submodule boundaries are recorded in `sources.json` and `docs/SOURCE_AUDIT.md`.
The public top-level repository keeps only `main`; `upstream/` remains a
detached pinned submodule. Current gates do not depend on Trackio metadata,
private paths, or queue state.
