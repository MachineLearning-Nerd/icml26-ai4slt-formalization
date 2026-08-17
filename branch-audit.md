# Complete branch and history map

This file is the detailed branch map for the normalized collection
repository.

## Top-level Git refs

| Ref | Kind | Purpose | Publication status |
| --- | --- | --- | --- |
| <code>main</code> | Top-level branch | Single canonical collection history | Published |
| <code>origin/main</code> | Remote-tracking ref | Local view of the GitHub <code>main</code> branch | Must equal live <code>main</code> |
| <code>origin/HEAD</code> | Symbolic remote default | Points to <code>main</code> | Required |

The final remote branch set is exactly {main}. No <code>orx/*</code>,
<code>work/*</code>, <code>master</code>, scratch, or experiment branch is
part of this repository.

## History roles

The main history contains the original scoped reproduction work followed by
the publication dossier and final-state record:

1. The reproduction commit records the source-pinned AI4SLT claim audit.
2. The publication-queue handoff preserves the scoped gate and its limits.
3. The scoped claim-audit commit records the source, declaration, and
   full-release build evidence.
4. The dossier commit adds the standardized claim, source, environment,
   report, citation, and author-thank-you records.
5. The state commit records publication and verification as the current
   checkpoint.

The exact live tip is intentionally read from GitHub by
<code>verify_final.py</code> rather than copied into this static map.

## Detached official source

| Path | Pinned object | Role |
| --- | --- | --- |
| <code>upstream/</code> | <code>7b82b1323c80f0c21ca449fd12e1c24315ae9782</code> | Official source-era Lean tree |

The submodule is initialized in a detached state and must be clean. It is
not an editable branch of this collection and its history is not included in
the top-level branch count.

## Naming and attribution policy

- Repository: <code>MachineLearning-Nerd/icml26-ai4slt-formalization</code>
- Published branch: <code>main</code>
- Commit author and committer: <code>MachineLearning-Nerd</code>
- No co-author trailers
- No branch names containing <code>orx</code>, <code>work</code>, or temporary experiment labels

The final-state verifier checks these invariants, the remote branch set, and
the absence of stale <code>refs/original/</code> references.
