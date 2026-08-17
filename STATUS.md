# Status

- Paper: `dfqmQ9WhCP` — *AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory*
- Owner: `codex-ai4slt-formalization-three-claims`
- State: `in_progress`
- Effective contract: 3 anchored claims / 6 possible points
- Primary source: arXiv `2602.02285`, PDF SHA-256 `6c98193350a5242def4ab6d918e2e6ba7a4110eeb09c63766c9e886e3731e5f2`
- Official source: `YuanheZ/lean-stat-learning-theory@7b82b1323c80f0c21ca449fd12e1c24315ae9782`

## Current step

HF Jobs `cpu-upgrade` full Lean build of the official `v4.32.0` release is
running as `DineshAI/6a5dc974bee6ee1cf4ed2118`. The source-era checkout is
statically audited; its pinned v4.27.0-rc1 manifest is not parser-compatible
with that RC, so the release-build and source-era provenance are recorded
separately. Gate evidence requires a successful full `lake build`, an exact
source-era declaration audit, no-placeholder scan, and source-era Lean-line-
count evidence.

## Attempts

- `6a5dc7dbbee6ee1cf4ed2101`: compiled all 8,720 Lean targets, then its
  post-build `rg` zero-match scan exited 1 under `pipefail`; it is not counted
  as a successful evidence run.
- `6a5dc974bee6ee1cf4ed2118`: same full release build with the zero-match scan
  explicitly normalized to a count of zero; terminal markers will be retained
  before the claim gate is evaluated.

## Blockers

None. This is a full formal-code compilation, not a partial module build.
