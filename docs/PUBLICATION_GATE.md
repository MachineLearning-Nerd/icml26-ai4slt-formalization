# Publication gate

The current gate is a self-contained `SCOPED_PASS` for the source-era static
audit and the recorded full `v4.32.0` release-build evidence. It is not a
literature-priority checker and not a score forecast.

## Gate sequence

[`repro/src/publication_gate.py`](../repro/src/publication_gate.py):

1. runs `audit_source.py` and checks the source submodule commit, tree digest,
   file/line counts, placeholders, and named declarations;
2. materializes the pinned HF terminal log and checks the release/build
   markers;
3. verifies all three claim contracts;
4. runs the focused pytest suite;
5. rebuilds and validates the hash-bound evidence bundle; and
6. writes identical JSON summaries to `publication_gate.json` and
   `outputs/publication_gate.json`.

The gate fails closed if the submodule is missing/dirty, a source anchor or
tree digest changes, the release log hash or markers change, a claim fails,
the tests fail, an evidence row is stale, or the gate copies differ.

## Status semantics

- `SCOPED_PASS` means the executable source/build contracts passed.
- `VERIFIED_SCOPED` means the substantive formal artifact or named theorem
  contract passed.
- `VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS` records the C3 provenance boundary
  and the overall limits around priority and human-supervision claims.
- `NOT_READY` is the strict paper-level status for those non-executable
  historical claims.
- `score_forecast: null` is intentional.

The old `outputs/PUBLICATION_GATE_PASSED.json` is retained only as a labeled
historical artifact; the current gate does not read it.
