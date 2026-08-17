# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_57804590a588", "created_at": "2026-07-20T07:09:29+00:00", "title": "AI4SLT reproduction"}
-->
# AI4SLT reproduction

OpenReview `dfqmQ9WhCP`. This logbook records a source-era static audit and a complete official-release Lean build. The claim gate is fail-closed and remains pending until the terminal build markers are materialized.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_0b6eb8afb197", "created_at": "2026-07-20T07:09:38+00:00", "title": "Pending full gate"}
-->
## Pending full gate

The source-era static audit passes. A fresh 8-core CPU full build is in progress; this page is intentionally not marked ready until all terminal markers and the independent claim verifier pass.


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_74411013244c", "created_at": "2026-07-20T07:16:01+00:00", "title": "FULLGATEREADY: dfqmQ9WhCP", "pinned": true, "pinned_at": "2026-07-20T07:16:02+00:00"}
-->
## FULL_GATE_READY: dfqmQ9WhCP

**Outcome:** all 3 live claims passed for **6/6 points**. The paper-era code audit pins 55 Lean files / 34,684 lines with zero placeholders and named empirical-process, concentration, Dudley, and minimax declarations. A fresh HF Jobs `cpu-upgrade` full build of official `v4.32.0` completed all 8,720 targets, reporting 65 Lean files / 55,867 lines, zero placeholders, and the exact `theorem dudley`. Historical priority and the reported 500-hour effort are disclosed as paper provenance, not fabricated as runtime measurements.

## Scope & cost

| Aspect | This reproduction | Full replication |
| --- | --- | --- |
| Scope | Source-era static audit plus full official-release Lean build | Same executable formalization evidence |
| Hardware | HF Jobs `cpu-upgrade` (8 vCPU) | CPU build; no GPU needed |
| Time | 339 s remote build after dependency setup | Comparable fresh build time |
| Cost | About 6 minutes of `cpu-upgrade` | Depends on provider rate |
| Outcome | All 3 claims pass, 6/6 points | Not a claim of redoing historical author labor |
