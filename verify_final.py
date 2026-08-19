#!/usr/bin/env python3
"""Verify the AI4SLT dossier and its live GitHub publication state."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORY = "icml26-ai4slt-formalization"
CANONICAL = (
    "MachineLearning-Nerd",
    "37579156+MachineLearning-Nerd@users.noreply.github.com",
)
SOURCE_COMMIT = "7b82b1323c80f0c21ca449fd12e1c24315ae9782"
SOURCE_TREE_SHA = "730c607976bf0784f3c9ca6dd76df2ba271a96c1f809d287ef3adf9a5b45e23e"
EXPECTED_CLAIM_STATUSES = [
    "verified_scoped",
    "verified_scoped",
    "verified_scoped_with_provenance_limits",
]
EXPECTED_GATE_CLAIMS = {
    "C1": "VERIFIED_SCOPED",
    "C2": "VERIFIED_SCOPED",
    "C3": "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS",
}
REQUIRED_PATHS = [
    "README.md",
    "STATUS.md",
    ".gitmodules",
    "AUTONOMOUS_STATE.json",
    "branch-audit.md",
    "BRANCH_AUDIT.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "ENVIRONMENT.md",
    "REPORT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "reproduction_verdicts.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "publication_gate.json",
    "sources.json",
    "docs/primary.pdf",
    "docs/arxiv_source.tar",
    "docs/CLAIM_AUDIT.md",
    "docs/SOURCE_AUDIT.md",
    "docs/BRANCH_AUDIT.md",
    "docs/PUBLICATION_GATE.md",
    "outputs/CUMULATIVE_SCIENCE_GATE.json",
    "outputs/claim_verification.json",
    "outputs/source_audit.json",
    "outputs/hf_build.json",
    "outputs/hf_job_build.log",
    "outputs/evidence_bundle.jsonl",
    "outputs/publication_gate.json",
    "outputs/README.md",
    "repro/src/audit_source.py",
    "repro/src/materialize_hf_build.py",
    "repro/src/verify_claims.py",
    "repro/src/cumulative_science_gate.py",
    "repro/src/publication_gate.py",
]


def fail(message: str) -> None:
    print(f"FINAL_AUDIT=FAILED {message}", file=sys.stderr)
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result.stdout


def current_bytes(path: str) -> bytes:
    local = ROOT / path
    if local.exists():
        return local.read_bytes()
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode:
        fail(f"required path is unavailable: {path}")
    return result.stdout


def current_json(path: str) -> object:
    try:
        return json.loads(current_bytes(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
    return None


def sha256(path: str) -> str:
    return hashlib.sha256(current_bytes(path)).hexdigest()


def verify_manifest() -> None:
    manifest = current_json("EVIDENCE_MANIFEST.json")
    require(isinstance(manifest, dict), "manifest is not an object")
    require(manifest.get("schema_version") == 1, "unsupported manifest schema")
    require(manifest.get("hash_algorithm") == "sha256", "manifest hash algorithm changed")
    entries = manifest.get("entries")
    require(isinstance(entries, list) and entries, "evidence manifest is empty")
    seen = set()
    for entry in entries:
        require(isinstance(entry, dict), "manifest entry is not an object")
        path = entry.get("path")
        expected = entry.get("sha256")
        require(isinstance(path, str), "manifest path is missing")
        require(
            isinstance(expected, str) and len(expected) == 64,
            f"bad manifest hash for {path}",
        )
        require(path not in seen, f"duplicate manifest path: {path}")
        seen.add(path)
        require((ROOT / path).exists(), f"manifest path is missing: {path}")
        require(sha256(path) == expected, f"manifest hash mismatch: {path}")
    require("AUTONOMOUS_STATE.json" not in seen, "state must not create a hash cycle")


def verify_git_state() -> int:
    origin = run("git", "config", "--get", "remote.origin.url").strip()
    require(
        origin in {
            f"https://github.com/MachineLearning-Nerd/{REPOSITORY}.git",
            f"git@github.com:MachineLearning-Nerd/{REPOSITORY}.git",
        },
        f"unexpected origin: {origin}",
    )
    require(
        "ref: refs/heads/main\tHEAD"
        in run("git", "ls-remote", "--symref", "origin", "HEAD"),
        "origin/HEAD is not main",
    )

    remote_lines = run("git", "ls-remote", "--heads", "origin").splitlines()
    remote_heads = {}
    for line in remote_lines:
        commit, ref = line.split("\t", 1)
        require(ref.startswith("refs/heads/"), f"unexpected remote ref: {ref}")
        remote_heads[ref.removeprefix("refs/heads/")] = commit
    require(set(remote_heads) == {"main"}, "remote branch set is not exactly main")
    require(
        remote_heads["main"] == run("git", "rev-parse", "origin/main").strip(),
        "origin/main differs from live main",
    )

    local_heads = set(
        run(
            "git",
            "for-each-ref",
            "--format=%(refname:strip=2)",
            "refs/heads",
        ).splitlines()
    )
    require(local_heads <= {"main"}, "unexpected local branch")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs").splitlines()
    require(not any("refs/original/" in ref for ref in refs), "refs/original remains")

    tree = run("git", "ls-tree", "HEAD", "upstream").strip().split()
    require(
        len(tree) == 4
        and tree[0] == "160000"
        and tree[1] == "commit"
        and tree[2] == SOURCE_COMMIT
        and tree[3] == "upstream",
        "top-level upstream gitlink changed",
    )
    require(
        run("git", "config", "-f", ".gitmodules", "--get", "submodule.upstream.url").strip()
        == "https://github.com/YuanheZ/lean-stat-learning-theory.git",
        "submodule URL changed",
    )
    require((ROOT / "upstream").is_dir(), "submodule is not initialized")
    require(
        run("git", "-C", "upstream", "rev-parse", "HEAD").strip() == SOURCE_COMMIT,
        "submodule commit changed",
    )
    require(
        run("git", "-C", "upstream", "status", "--porcelain").strip() == "",
        "submodule worktree is dirty",
    )

    identities = set()
    for line in run(
        "git", "log", "--all", "--format=%an\t%ae\t%cn\t%ce"
    ).splitlines():
        if line.strip():
            identities.add(tuple(line.split("\t")))
    require(
        identities == {(CANONICAL[0], CANONICAL[1], CANONICAL[0], CANONICAL[1])},
        f"non-canonical reachable identity: {sorted(identities)}",
    )
    require(
        "co-authored-by:" not in run("git", "log", "--all", "--format=%B").lower(),
        "co-author trailer found",
    )
    commit_count = int(run("git", "rev-list", "--count", "--all").strip())
    require(commit_count >= 5, f"unexpectedly short history: {commit_count}")
    return len(remote_heads), commit_count


def verify_artifacts() -> None:
    for path in REQUIRED_PATHS:
        require((ROOT / path).exists(), f"required path missing: {path}")

    claims = current_json("claims.json")
    require(isinstance(claims, dict), "claims.json is not an object")
    require(
        claims.get("repository") == f"MachineLearning-Nerd/{REPOSITORY}",
        "claims repository mismatch",
    )
    require(claims.get("publication_allowed") is False, "claim publication block changed")
    rows = claims.get("claims")
    require(isinstance(rows, list) and len(rows) == 3, "claims.json must contain three claims")
    statuses = [row.get("status") for row in rows]
    require(statuses == EXPECTED_CLAIM_STATUSES, f"unexpected claim statuses: {statuses}")

    verdicts = current_json("reproduction_verdicts.json")
    require(isinstance(verdicts, dict), "reproduction verdicts are not an object")
    require(
        verdicts.get("repository") == f"MachineLearning-Nerd/{REPOSITORY}",
        "reproduction verdict repository mismatch",
    )
    require(verdicts.get("overall_verdict") == "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS", "overall verdict changed")
    require(verdicts.get("gate_status") == "SCOPED_PASS", "gate status changed")
    require(verdicts.get("strict_status") == "NOT_READY", "strict status changed")
    require(verdicts.get("publication_allowed") is False, "reproduction publication block changed")
    verdict_rows = verdicts.get("claims")
    require(isinstance(verdict_rows, list) and len(verdict_rows) == 3, "reproduction verdicts must contain three claims")
    require(
        [row.get("status") for row in verdict_rows]
        == [
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED",
            "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS",
        ],
        "reproduction verdict statuses changed",
    )

    state = current_json("AUTONOMOUS_STATE.json")
    require(isinstance(state, dict), "state is not an object")
    require(state.get("phase") == "published_and_verified", "state is not final")
    require(state.get("publication_allowed") is False, "state publication block changed")
    require(state.get("last_known_git_commit"), "state has no recorded commit")

    gate = current_json("publication_gate.json")
    require(isinstance(gate, dict), "publication gate is not an object")
    require(gate.get("paper") == "dfqmQ9WhCP", "gate paper changed")
    require(gate.get("status") == "SCOPED_PASS", "gate status changed")
    require(gate.get("strict_status") == "NOT_READY", "strict gate changed")
    require(
        gate.get("overall_status") == "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS",
        "overall gate changed",
    )
    require(gate.get("claims") == EXPECTED_GATE_CLAIMS, "gate claims changed")
    require(
        gate.get("claim_count") == 3
        and gate.get("verified_claims") == 3
        and gate.get("earned_points") == 6
        and gate.get("possible_points") == 6,
        "gate scoring changed",
    )
    require(gate.get("tests_passed") is True, "recorded tests are not passing")
    require(gate.get("publication_gate_passed") is True, "publication gate is not passing")
    require(gate.get("score_forecast") is None, "score forecast was asserted")
    controls = gate.get("controls", {})
    for key in (
        "paper_pin",
        "submodule_clean",
        "source_commit_pin",
        "source_anchors",
        "source_static_audit",
        "release_build_log_hash",
        "release_build_markers",
        "claim_verification",
    ):
        require(controls.get(key) is True, f"gate control failed: {key}")
    require(controls.get("source_tree_digest") == SOURCE_TREE_SHA, "source digest changed")
    require(
        current_bytes("publication_gate.json") == current_bytes("outputs/publication_gate.json"),
        "publication gate copies differ",
    )

    sources = current_json("sources.json")
    require(isinstance(sources, dict), "sources.json is not an object")
    paper = sources.get("paper", {})
    require(paper.get("openreview_id") == "dfqmQ9WhCP", "OpenReview pin changed")
    require(paper.get("arxiv_id") == "2602.02285", "arXiv pin changed")
    require(paper.get("official_commit") == SOURCE_COMMIT, "official source pin changed")
    source_tree = sources.get("source_tree", {})
    require(
        source_tree.get("file_count") == 55
        and source_tree.get("line_count") == 34684
        and source_tree.get("sha256") == SOURCE_TREE_SHA,
        "source-tree metrics changed",
    )
    release = sources.get("release_build", {})
    require(
        release.get("job_id") == "6a5dc974bee6ee1cf4ed2118"
        and release.get("official_release") == "v4.32.0"
        and release.get("commit") == "482a1a56daf792b33afe8cf7f07f127dc0af8640"
        and release.get("lean_targets") == 8720
        and release.get("lean_files") == 65
        and release.get("lean_lines") == 55867
        and release.get("placeholder_count") == 0,
        "release-build evidence changed",
    )

    claim_verification = current_json("outputs/claim_verification.json")
    require(
        claim_verification.get("all_claims_complete") is True
        and claim_verification.get("verified_claims") == 3,
        "claim verification output changed",
    )
    require(
        all(row.get("passed") is True for row in claim_verification["claims"].values()),
        "a claim verification row is not passing",
    )
    require(
        "500-hour" in claim_verification["claims"]["C3_human_verified_codebase"]["note"],
        "C3 provenance limit disappeared",
    )
    source_audit = current_json("outputs/source_audit.json")
    require(
        source_audit.get("official_commit") == SOURCE_COMMIT
        and source_audit.get("lean_files") == 55
        and source_audit.get("lean_lines") == 34684
        and source_audit.get("placeholder_count") == 0
        and source_audit.get("all_static_checks_pass") is True,
        "source-audit output changed",
    )
    hf_build = current_json("outputs/hf_build.json")
    require(
        hf_build.get("build_success") is True
        and hf_build.get("lean_files") == 65
        and hf_build.get("lean_lines") == 55867
        and hf_build.get("placeholder_count") == 0,
        "release-build output changed",
    )
    require(
        hf_build.get("dudley_declaration") is True,
        "release-build Dudley marker changed",
    )
    require(
        sha256("docs/primary.pdf")
        == "6c98193350a5242def4ab6d918e2e6ba7a4110eeb09c63766c9e886e3731e5f2",
        "paper PDF hash changed",
    )
    require(
        sha256("docs/arxiv_source.tar")
        == "0091ed288889e3ff262a5f13174065fe51b9debbf5d18bf48b1057ff3ae2a429",
        "paper source hash changed",
    )
    require(
        sha256("outputs/hf_job_build.log")
        == "ac5873e1327209c2696eabdb4ea95a04fa672fbd13318682dd9d434834ede76f",
        "build-log hash changed",
    )
    require(
        sha256("outputs/evidence_bundle.jsonl")
        == "13ed5542a74b587232bb1ceb2316edede34aa942a518e4c1c732d6984babfd46",
        "evidence-bundle hash changed",
    )


def main() -> None:
    branches, commits = verify_git_state()
    verify_artifacts()
    verify_manifest()
    print(
        "FINAL_AUDIT=VERIFIED "
        f"branches={branches} commits={commits} "
        "claims=C1:verified_scoped,C2:verified_scoped,"
        "C3:verified_scoped_with_provenance_limits score_forecast=null"
    )


if __name__ == "__main__":
    main()
