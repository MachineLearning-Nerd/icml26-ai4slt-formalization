# Claim-to-evidence audit

This dossier separates executable formalization evidence from historical
priority and human-supervision statements. The source-era Lean tree and the
later release build are pinned as distinct artifacts.

## Claim ledger

| Claim | Production path | Result | Boundary |
| --- | --- | --- | --- |
| C1 — comprehensive SLT formalization grounded in empirical processes | <code>repro/src/audit_source.py</code> scans the pinned <code>upstream/SLT</code>; <code>repro/src/materialize_hf_build.py</code> parses the full release log; <code>repro/src/verify_claims.py</code> joins them; <code>repro/src/cumulative_science_gate.py</code> checks the contract. | VERIFIED_SCOPED | Verifies the substantive formalization and full-build evidence; not the historical word “first”. |
| C2 — Dudley entropy-integral theorem for sub-Gaussian processes | Source audit locates <code>theorem dudley</code>; build parser requires the Dudley marker and <code>BUILD_SUCCESS</code>. | VERIFIED_SCOPED | Verifies the pinned theorem artifact and recorded build; not historical priority. |
| C3 — approximately 30,000 lines of human-verified Lean code | Source audit counts source-era Lean lines and placeholders; release parser records the full-build counts. | VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS | 34,684 source-era lines and zero placeholders are executable facts; 500 hours of supervised development is paper-reported provenance. |

## C1 — comprehensive formalization

The source-era tree contains 55 Lean files and 34,684 Lean lines, with zero
<code>sorry</code>, <code>admit</code>, or <code>axiom</code> placeholders. The
static audit locates Efron–Stein, Gaussian Lipschitz concentration, Dudley,
and the rank-based linear-regression minimax declaration. The recorded full
release build contains 8,720 targets, 65 Lean files, 55,867 Lean lines, zero
placeholders, and <code>BUILD_SUCCESS</code>.

This verifies the substantive formalization contract. It does not establish
that the authors were first in the literature.

## C2 — Dudley theorem

The source audit identifies <code>theorem dudley</code> in
<code>upstream/SLT/Dudley.lean</code> at line 2,517. The independent build-log
parser requires the Dudley declaration marker and successful completion of all
8,720 targets. Both source and release evidence are hash-bound by the current
publication gate.

The claim is verified at the pinned artifact/build scope, not as a
literature-wide priority result.

## C3 — human-verified codebase

The source-era count exceeds 30,000 lines and the placeholder scan is clean.
The full release build independently records 55,867 Lean lines and zero
placeholders. The paper's 500-hour supervised-development statement is
retained as provenance; code inspection and compilation cannot measure the
human labor history or prove the phrase “human-verified” in its historical
sense.

## Gate and controls

The canonical <code>publication_gate.json</code> reports
<code>SCOPED_PASS</code>, <code>VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS</code>,
3/3 executable claims, 6/6 possible points, and null score forecast. Its
controls require the paper pin, submodule cleanliness, source commit and tree
digest, source anchors, static audit, release-log hash/markers, and claim
verification. The root and <code>outputs/</code> gate copies must be byte
identical.

## Non-claims

- No literature-wide “first” claim is independently certified.
- No local source-era <code>v4.27.0-rc1</code> build is claimed after the old package manifest was found incompatible with that parser.
- The later <code>v4.32.0</code> build is not silently substituted for the source-era checkout.
- No external evaluator score or author endorsement is claimed.
