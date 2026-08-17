# Normalized branch audit

## Published collection branches

The collection repository has exactly one published branch: <code>main</code>.

| Branch | Role | Evidence boundary |
| --- | --- | --- |
| <code>main</code> | Canonical README, pinned paper/source artifacts, claim ledger, audit outputs, and final-state verifier | The live remote branch set and <code>origin/HEAD</code> are checked by <code>verify_final.py</code> |

There are no <code>master</code>, <code>orx/*</code>, <code>work/*</code>,
experiment, or temporary branches in the collection repository. The
<code>upstream/</code> directory is a detached Git submodule, not a second
collection branch.

## Submodule boundary

<code>upstream/</code> points to the official
<code>YuanheZ/lean-stat-learning-theory</code> repository at commit
<code>7b82b1323c80f0c21ca449fd12e1c24315ae9782</code>. Its detached state is
deliberate: the collection pins the source-era artifact instead of publishing
a mutable copy of the authors' history. The submodule's own branch or tag
state is provenance and is not renamed by this repository.

## Branch policy

All collection changes land on <code>main</code>. A future change should
preserve the main-only policy, update the dossier and manifest together, and
pass the lightweight final-state verifier before publication. Historical
author branches and the official repository's workflow are not claimed as
collection branches.

## Attribution

All reachable collection commits are required to use:

    MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>

The verifier also rejects co-author trailers and unexpected Git references.
