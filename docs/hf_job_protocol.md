# Full-build protocol

The reproducibility gate uses a fresh Hugging Face Jobs `cpu-upgrade` worker
(8 vCPU) to compile the entire official `v4.32.0` release. It performs:

1. `lake exe cache get` for the release dependencies;
2. `LEAN_NUM_THREADS=8 lake build` with no selected-module restriction;
3. a commit, Lean-file, Lean-line, zero-placeholder, and Dudley-declaration
   terminal audit.

The job must finish with `BUILD_SUCCESS`. `materialize_hf_build.py` rejects
missing terminal fields, nonzero placeholder counts, or a missing Dudley
declaration. The preceding attempt that reached the end of compilation but
failed its shell wrapper is preserved in `STATUS.md` and is not gate evidence.

This is a release-build compatibility route: the paper-era tree remains pinned
and statically audited at `7b82b1323c80f0c21ca449fd12e1c24315ae9782`; its
specified 4.27.0-rc1 parser rejects the source-era manifest before resolution.
