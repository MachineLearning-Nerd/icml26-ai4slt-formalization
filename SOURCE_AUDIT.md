# Source and provenance audit

## Paper identity

- Title: **AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory**
- Authors: Yuanhe Zhang, Jason D. Lee, and Fanghui Liu
- arXiv: [2602.02285v2](https://arxiv.org/abs/2602.02285v2)
- OpenReview: [dfqmQ9WhCP](https://openreview.net/forum?id=dfqmQ9WhCP)
- Former repository: <code>icml26-repro-dfqmQ9WhCP-ai4slt-formalization</code>
- Current repository: <code>icml26-ai4slt-formalization</code>

## Paper artifacts

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| Paper PDF | <code>docs/primary.pdf</code> | <code>6c98193350a5242def4ab6d918e2e6ba7a4110eeb09c63766c9e886e3731e5f2</code> |
| arXiv source | <code>docs/arxiv_source.tar</code> | <code>0091ed288889e3ff262a5f13174065fe51b9debbf5d18bf48b1057ff3ae2a429</code> |

## Source-era official tree

The detached <code>upstream</code> submodule points to
<code>YuanheZ/lean-stat-learning-theory</code> commit
<code>7b82b1323c80f0c21ca449fd12e1c24315ae9782</code>. Its declared toolchain
is <code>leanprover/lean4:v4.27.0-rc1</code>. The source-era digest covers 55
Lean files and 34,684 lines:

    730c607976bf0784f3c9ca6dd76df2ba271a96c1f809d287ef3adf9a5b45e23e

The pinned source anchors cover Dudley, Efron–Stein, Gaussian Lipschitz
concentration, and the rank-based minimax rate. Their individual hashes and
locations remain in <code>sources.json</code> and
<code>docs/SOURCE_AUDIT.md</code>.

## Release-build evidence

The recorded full build is a separate artifact from the source-era checkout:

- Hugging Face job: <code>6a5dc974bee6ee1cf4ed2118</code>
- Flavor: <code>cpu-upgrade</code>
- Official release: <code>v4.32.0</code>
- Build commit: <code>482a1a56daf792b33afe8cf7f07f127dc0af8640</code>
- Log SHA-256: <code>ac5873e1327209c2696eabdb4ea95a04fa672fbd13318682dd9d434834ede76f</code>
- Targets/files/lines: 8,720 / 65 / 55,867
- Placeholders: 0

The source-era package manifest is no longer accepted by the specified
release-candidate parser. The gate therefore reports source-era static
evidence and later release-build evidence separately; it does not claim
bit-for-bit compilation of the former with the latter.

## Provenance limits

The paper's “first” language requires literature-wide evidence. The 500-hour
human-supervision statement is historical provenance. Neither is converted
into a machine-checked fact by the source scan or build log.
