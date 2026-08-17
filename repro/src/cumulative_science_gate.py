"""Validate the source, build, and claim contracts as one fail-closed gate."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream"
SOURCES = ROOT / "sources.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(list(args), cwd=cwd, text=True).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def source_tree_digest() -> tuple[int, int, str]:
    names = [
        name
        for name in command("git", "-C", str(UPSTREAM), "ls-files", "SLT").splitlines()
        if name.endswith(".lean")
    ]
    rows = []
    line_count = 0
    for name in sorted(names):
        file_path = UPSTREAM / name
        rows.append(f"{sha256(file_path)}  upstream/{name}\n")
        line_count += file_path.read_text(errors="replace").count("\n") + 1
    digest = hashlib.sha256("".join(rows).encode()).hexdigest()
    return len(names), line_count, digest


def main() -> None:
    sources = json.loads(SOURCES.read_text())
    paper = sources["paper"]
    source_spec = sources["source_tree"]
    release_spec = sources["release_build"]
    require(paper["openreview_id"] == "dfqmQ9WhCP", "unexpected paper identity")
    require(UPSTREAM.is_dir(), "missing upstream submodule")

    dirty = command("git", "-C", str(UPSTREAM), "status", "--porcelain")
    commit = command("git", "-C", str(UPSTREAM), "rev-parse", "HEAD")
    require(not dirty, "upstream submodule is dirty")
    require(commit == paper["official_commit"], "upstream commit does not match the source pin")

    lean_files, lean_lines, tree_digest = source_tree_digest()
    require(lean_files == source_spec["file_count"], "source Lean file count changed")
    require(lean_lines == source_spec["line_count"], "source Lean line count changed")
    require(tree_digest == source_spec["sha256"], "source tree digest changed")
    for relative, expected in sources["anchors"].items():
        require(sha256(ROOT / relative) == expected, f"source anchor changed: {relative}")

    source_audit = json.loads((ROOT / "outputs/source_audit.json").read_text())
    require(source_audit["official_commit"] == paper["official_commit"], "source audit pin mismatch")
    require(source_audit["commit_matches_pin"] is True, "source audit pin check failed")
    require(source_audit["lean_files"] == source_spec["file_count"], "source audit file count mismatch")
    require(source_audit["lean_lines"] == source_spec["line_count"], "source audit line count mismatch")
    require(source_audit["placeholder_count"] == 0, "source placeholders found")
    require(source_audit["all_static_checks_pass"] is True, "source static audit failed")
    require(all(source_audit["declarations"].values()), "required source declaration missing")

    build = json.loads((ROOT / "outputs/hf_build.json").read_text())
    for key in ("job_id", "flavor", "official_release", "commit"):
        require(build[key] == release_spec[key], f"release build {key} mismatch")
    require(build["status"] == "COMPLETED", "release build is not completed")
    require(build["build_success"] is True, "release build did not succeed")
    require(release_spec["lean_targets"] == 8720, "release target count changed")
    require(build["lean_files"] == release_spec["lean_files"], "release Lean file count mismatch")
    require(build["lean_lines"] == release_spec["lean_lines"], "release Lean line count mismatch")
    require(build["placeholder_count"] == 0, "release placeholders found")
    require(build["dudley_declaration"] is True, "release Dudley declaration missing")
    log = ROOT / release_spec["log_path"]
    require(sha256(log) == release_spec["log_sha256"], "release build log changed")
    log_text = log.read_text(errors="replace")
    require("BUILD_SUCCESS" in log_text, "release success marker missing")
    require(re.search(r"^COMMIT " + re.escape(release_spec["commit"]) + r"$", log_text, re.MULTILINE), "release commit marker missing")
    require(re.search(r"^LEAN_FILES\s+65$", log_text, re.MULTILINE), "release file marker missing")
    require(re.search(r"^LEAN_LINES\s+55867(?:\s+total)?$", log_text, re.MULTILINE), "release line marker missing")
    require(re.search(r"^PLACEHOLDERS\s+0$", log_text, re.MULTILINE), "release placeholder marker missing")
    require(re.search(r"^\d+:(?:theorem|def)\s+dudley\b", log_text, re.MULTILINE), "release Dudley marker missing")

    claims = json.loads((ROOT / "outputs/claim_verification.json").read_text())
    require(claims["paper"] == paper["openreview_id"], "claim paper identity mismatch")
    require(claims["claim_count"] == 3, "claim count changed")
    require(claims["verified_claims"] == 3, "not all claims passed")
    require(claims["possible_points"] == 6 and claims["earned_points"] == 6, "claim score changed")
    require(claims["all_claims_complete"] is True, "claim verdict is incomplete")
    require(all(claim["passed"] for claim in claims["claims"].values()), "a claim failed")

    report = {
        "paper": paper["openreview_id"],
        "gate_version": "scoped-v3",
        "status": "SCOPED_PASS",
        "strict_status": "NOT_READY",
        "overall_status": "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS",
        "claims": {
            "C1": "VERIFIED_SCOPED",
            "C2": "VERIFIED_SCOPED",
            "C3": "VERIFIED_SCOPED_WITH_PROVENANCE_LIMITS",
        },
        "claim_count": claims["claim_count"],
        "verified_claims": claims["verified_claims"],
        "earned_points": claims["earned_points"],
        "possible_points": claims["possible_points"],
        "controls": {
            "paper_pin": True,
            "submodule_clean": True,
            "source_commit_pin": True,
            "source_tree_digest": tree_digest,
            "source_anchors": True,
            "source_static_audit": True,
            "release_build_log_hash": True,
            "release_build_markers": True,
            "claim_verification": True,
        },
        "source_tree": {
            "commit": commit,
            "file_count": lean_files,
            "line_count": lean_lines,
            "sha256": tree_digest,
        },
        "release_build": {
            "job_id": build["job_id"],
            "official_release": build["official_release"],
            "commit": build["commit"],
            "lean_targets": release_spec["lean_targets"],
            "lean_files": build["lean_files"],
            "lean_lines": build["lean_lines"],
            "placeholder_count": build["placeholder_count"],
        },
        "score_forecast": None,
        "limitations": [
            "Historical priority claims are not literature-wide executable facts.",
            "The paper-reported 500 hours of supervised development is provenance, not a runtime measurement.",
            "The source-era v4.27.0-rc1 tree and later v4.32.0 release build are separate artifacts.",
        ],
    }
    destination = ROOT / "outputs/CUMULATIVE_SCIENCE_GATE.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
