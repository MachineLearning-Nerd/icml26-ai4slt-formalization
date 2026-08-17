# Claim audit — dfqmQ9WhCP

The paper's three live claims are formal-code claims. The current audit keeps
source-era static evidence, release-build evidence, and historical provenance
separate.

## C1 — comprehensive SLT formalization

Producer path:

1. `repro/src/audit_source.py` checks the pinned `upstream/SLT` submodule,
   counts Lean files and lines, scans for `sorry`, `admit`, and `axiom`, and
   locates Efron–Stein, Gaussian Lipschitz concentration, Dudley, and the
   rank-based least-squares minimax declaration.
2. `repro/src/materialize_hf_build.py` parses the successful full-release
   terminal log rather than accepting a selected-module build.
3. `repro/src/verify_claims.py` joins those two routes into the C1 verdict.

Checker path: `repro/src/cumulative_science_gate.py`,
`repro/tests/test_source_audit.py`, and `repro/tests/test_materialize_hf_build.py`.

Recorded evidence:

- Source-era `SLT/`: 55 Lean files, 34,684 lines, zero placeholders.
- Named source declarations: `efronStein`,
  `gaussian_lipschitz_concentration`, `dudley`, and
  `linear_minimax_rate_rank`.
- Release evidence: the pinned HF log records all 8,720 targets, 65 Lean
  files, 55,867 Lean lines, zero placeholders, and `BUILD_SUCCESS`.

Status: `VERIFIED_SCOPED`. This verifies the substantive formalization and
build evidence; “first” remains a historical-priority statement.

## C2 — Dudley entropy integral

Producer path: the source audit locates `theorem dudley` in
`upstream/SLT/Dudley.lean` at line 2,517. The release-build parser separately
requires a Dudley declaration marker in the terminal output.

Checker path: the cumulative gate requires the source declaration, matching
source anchor, release marker, zero placeholders, and `BUILD_SUCCESS`.

Recorded evidence: source line 2,517 and release log markers
`DUDLEY ...`, `2517:theorem dudley ...`, and `BUILD_SUCCESS`.

Status: `VERIFIED_SCOPED`. The gate verifies the pinned theorem artifact and
recorded full-build evidence; it does not establish historical priority.

## C3 — approximately 30,000 lines of human-verified Lean

Producer path: the static source audit counts source-era lines and checks the
placeholder scan. The release parser records the larger release-build count.

Checker path: the cumulative gate requires at least 30,000 source-era lines,
zero placeholders, a successful release build, and the source/build pins.

Recorded evidence: 34,684 source-era `SLT/` lines and zero placeholders.

Status: `VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS`. The code and compilation
conditions are executable. The paper's 500-hour supervised-development claim
is retained as provenance and is not treated as a measurable runtime result.

## Non-claims

- No literature-wide priority claim is independently certified.
- No local build of the paper-era `v4.27.0-rc1` manifest is claimed after its
  parser incompatibility was observed.
- The later `v4.32.0` release build is evidence for the official release path,
  not a silently substituted source-era checkout.
