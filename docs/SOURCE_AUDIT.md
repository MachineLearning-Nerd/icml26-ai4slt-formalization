# Source audit — dfqmQ9WhCP

## Paper identity and source pins

- Title: *AI4SLT: Empirical Processes in Lean 4 for Formal Statistical Learning Theory*
- Authors: Yuanhe Zhang, Jason D. Lee, and Fanghui Liu
- arXiv: `2602.02285v2`
- OpenReview: `dfqmQ9WhCP`
- PDF: `docs/primary.pdf`, SHA-256 `6c98193350a5242def4ab6d918e2e6ba7a4110eeb09c63766c9e886e3731e5f2`
- arXiv source archive: `docs/arxiv_source.tar`, SHA-256 `0091ed288889e3ff262a5f13174065fe51b9debbf5d18bf48b1057ff3ae2a429`

## Source-era official tree

The `upstream/` submodule points to
`YuanheZ/lean-stat-learning-theory@7b82b1323c80f0c21ca449fd12e1c24315ae9782`.
The source-era toolchain is `leanprover/lean4:v4.27.0-rc1`.

The canonical digest covers the 55 tracked `SLT/**/*.lean` files:

```text
files: 55
lines: 34684
sha256: 730c607976bf0784f3c9ca6dd76df2ba271a96c1f809d287ef3adf9a5b45e23e
```

| Anchor | SHA-256 | Role |
| --- | --- | --- |
| `upstream/SLT/Dudley.lean` | `72ecafe31e8ad23f8373c7153dad6bb25ac940d95443a7cd5d9944a9efc7614a` | Dudley theorem and chaining infrastructure |
| `upstream/SLT/EfronStein.lean` | `5c1880799e993d938174138055fa2027f0cfb6cfe350be07bdfe61578759d179` | Efron–Stein inequality |
| `upstream/SLT/GaussianLipConcen.lean` | `117e47a301c2c962384c2abb9a6a320322ea6f5a1c90d389770d3a917deceda4` | Gaussian Lipschitz concentration |
| `upstream/SLT/LeastSquares/LinearRegression/MinimaxRate.lean` | `8a6e4c7dd86bcd83b807289f9799ef9902078f067573c00cd106437f677d4ad2` | rank-based minimax rate |
| `upstream/lean-toolchain` | `d71f508cc546aeb22c1687e8ed95fc7e371795a448134142d5e1a262fab2051e` | source-era Lean version |
| `upstream/lake-manifest.json` | `c03e3fe4e65d574f536ba3e88f83a07b37a21d0c747bdd69d2b0be54e5e8af93` | source-era dependency resolution |

## Release-build evidence

The full build evidence comes from Hugging Face Jobs `6a5dc974bee6ee1cf4ed2118`
on the `cpu-upgrade` flavor, using the official `v4.32.0` release commit
`482a1a56daf792b33afe8cf7f07f127dc0af8640`. The terminal log is retained at
`outputs/hf_job_build.log` with SHA-256
`ac5873e1327209c2696eabdb4ea95a04fa672fbd13318682dd9d434834ede76f`.

Its terminal contract records 8,720 targets, 65 Lean files, 55,867 lines, zero
placeholders, the Dudley declaration, and `BUILD_SUCCESS`.

The source-era package manifest is not accepted by the specified RC parser;
therefore the gate reports these as two separate artifacts rather than
claiming source-era/release bit-for-bit equivalence.
