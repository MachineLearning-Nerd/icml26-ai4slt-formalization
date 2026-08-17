# Independent formalization audit

The active contract has three claims. Unlike an empirical paper, its primary
evidence is executable proof code. The audit therefore requires both a pinned
source-era static scan and a complete fresh Lean build; a file listing alone
cannot establish formal verification.

## Pinned artifact

The paper points to `YuanheZ/lean-stat-learning-theory`. The source-era revision
is `7b82b1323c80f0c21ca449fd12e1c24315ae9782` (2026-02-09), using Lean
`v4.27.0-rc1`, rather than the repository's later expanded main branch. The
static audit finds 55 Lean files and 34,684 lines under `SLT/`, with zero
occurrences of `sorry`, `admit`, or `axiom`. That source-era manifest is no
longer accepted by the specified RC's package parser, so the executable gate is
a complete build of the official `v4.32.0` release while preserving the
source-era audit as provenance. The two revisions are never conflated.

## C1 — comprehensive SLT formalization

The audit requires a successful full `lake build` of the official release, not selected imports. It
also finds source-era declarations for Efron--Stein, Gaussian Lipschitz
concentration, Dudley, and the rank-based least-squares minimax rate. Together
these span the paper’s foundations, concentration, empirical-process, and
least-squares layers.

## C2 — Dudley entropy integral

The source-era `SLT/Dudley.lean` declares theorem `dudley` at line 2517. The
gate accepts this claim only if that declaration is present in the pinned source
and the fresh full Lean build completes successfully.

## C3 — 30,000-line verified code claim

The source-era `SLT/` count is 34,684 lines, exceeding the claimed approximate
30,000. No proof placeholders occur. A code build can independently establish
the source, line count, no-placeholder condition, and compilation; the stated
500 hours of supervised human development is historical provenance reported by
the paper and is not falsely represented as an independently measurable runtime
quantity.
