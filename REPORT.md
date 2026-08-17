# Scoped reproduction report

## Final verdict

| Claim | Verdict | Evidence boundary |
| --- | --- | --- |
| C1 | VERIFIED_SCOPED | Source-era 55-file static audit plus recorded full release build. |
| C2 | VERIFIED_SCOPED | Pinned Dudley declaration plus independent full-build marker. |
| C3 | VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS | Source/build counts and zero placeholders; human-supervision history remains provenance. |

The repository status is
<code>VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS</code> with gate state
<code>SCOPED_PASS</code> and strict status <code>NOT_READY</code> for the
non-executable historical claims.

## What is established

The pinned source-era Lean tree contains the declared empirical-process
formalization, named theorem declarations, more than 30,000 Lean lines, and no
placeholder declarations. A separate recorded full release build completed all
8,720 targets with zero placeholders. The current gate checks these facts,
source pins, markers, controls, and claim evidence.

## What is not established

The formal gate cannot prove literature-wide priority or measure the paper's
500 hours of supervised development. It also does not claim a fresh build of
the source-era <code>v4.27.0-rc1</code> checkout using the later
<code>v4.32.0</code> release.

## Publication policy

The dossier is published for transparent review. A complete paper-level
conclusion remains blocked by the explicit provenance limits, and
<code>publication_allowed</code> remains false for a new score or priority
claim.
