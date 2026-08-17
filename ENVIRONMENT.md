# Environment and reproduction boundary

## Audit command

The repository audit can be run with Python 3.12 and the pinned Python
requirements:

~~~sh
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r repro/requirements.txt
.venv/bin/python repro/src/publication_gate.py
~~~

The gate performs source inspection, parses the recorded full-build log,
checks the claim contracts, runs the focused tests, rebuilds the evidence
bundle, and checks the two publication-gate copies.

## Recorded Lean build

The historical full build used Hugging Face Jobs with the <code>cpu-upgrade</code>
flavor and official Lean <code>v4.32.0</code>. Its retained log records 8,720
targets, 65 Lean files, 55,867 lines, zero placeholders, the Dudley
declaration, and <code>BUILD_SUCCESS</code>.

This is evidence that the recorded release-build contract completed. It is
not a request to rerun paid or remote compute during ordinary dossier
verification.

## Source-era boundary

The official source submodule declares Lean <code>v4.27.0-rc1</code>. Its
source-era package manifest was not accepted by that release candidate parser
in the available environment, so the repository does not claim a fresh local
build of that exact checkout. The source scan, detached commit, tree digest,
and later release build remain separately pinned.
