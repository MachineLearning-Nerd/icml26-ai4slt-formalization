# Branch audit — dfqmQ9WhCP

## Original top-level state

The reproduction repository originally had exactly one top-level branch,
`main`, with two reachable commits:

| Commit | Role |
| --- | --- |
| `a5c6197153631f83f09cc708b13217153881eea3` | source audit, full-build evidence, and claim gate |
| `1decf8986627129edc01b7c6c32725b1ac90e71b` | publication queue handoff |

There were no `orx/*`, experiment, or hidden evidence branches. The official
Lean project is represented by the detached `upstream/` submodule at its
explicit commit; that detached state is intentional and is not a publication
branch.

## Published state

The cleaned repository keeps exactly one top-level branch:

- `main` — paper source, pinned submodule, static audit, release-build
  evidence, claim ledger, and publication gate.

All reachable top-level commits are normalized to:

```text
MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>
```

The branch name is intentionally plain and stable. No queue, temporary
experiment, or `orx/*` branch is part of the public repository.
