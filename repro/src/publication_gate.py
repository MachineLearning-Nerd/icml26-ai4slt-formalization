"""Run and publish the deterministic paper-scoped reproduction gate."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"


def run(*args: str) -> None:
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_bundle() -> tuple[int, str]:
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    records = [json.loads(line) for line in bundle.read_text().splitlines()]
    if not records:
        raise SystemExit("evidence bundle is empty")
    for record in records:
        path = ROOT / record["artifact"]
        if not path.is_file():
            raise SystemExit(f"evidence artifact is missing: {record['artifact']}")
        if path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            raise SystemExit(f"evidence artifact is stale: {record['artifact']}")
    return bundle.stat().st_size, sha256(bundle)


def main() -> None:
    sources = json.loads((ROOT / "sources.json").read_text())
    release = sources["release_build"]
    run("repro/src/audit_source.py")
    run(
        "repro/src/materialize_hf_build.py",
        "--job-id",
        release["job_id"],
        "--log",
        release["log_path"],
    )
    run("repro/src/verify_claims.py")
    run("repro/src/cumulative_science_gate.py")
    subprocess.run([sys.executable, "-m", "pytest", "-q", "repro/tests"], cwd=ROOT, check=True)
    run("repro/src/cumulative_science_gate.py")
    run("repro/src/build_evidence_bundle.py")
    bundle_bytes, bundle_sha = validate_bundle()

    cumulative = json.loads((OUTPUTS / "CUMULATIVE_SCIENCE_GATE.json").read_text())
    claims = json.loads((OUTPUTS / "claim_verification.json").read_text())
    gate = {
        "paper": cumulative["paper"],
        "gate_version": "publication-v3",
        "status": cumulative["status"],
        "strict_status": cumulative["strict_status"],
        "overall_status": cumulative["overall_status"],
        "claims": cumulative["claims"],
        "claim_count": claims["claim_count"],
        "verified_claims": claims["verified_claims"],
        "earned_points": claims["earned_points"],
        "possible_points": claims["possible_points"],
        "tests_passed": True,
        "tests": ["pytest -q repro/tests: passed"],
        "publication_gate_passed": True,
        "controls": cumulative["controls"],
        "source_tree": cumulative["source_tree"],
        "release_build": cumulative["release_build"],
        "evidence_bundle": {
            "path": "outputs/evidence_bundle.jsonl",
            "bytes": bundle_bytes,
            "sha256": bundle_sha,
        },
        "score_forecast": None,
        "limitations": cumulative["limitations"],
    }
    payload = json.dumps(gate, indent=2) + "\n"
    (ROOT / "publication_gate.json").write_text(payload)
    (OUTPUTS / "publication_gate.json").write_text(payload)
    if (ROOT / "publication_gate.json").read_bytes() != (OUTPUTS / "publication_gate.json").read_bytes():
        raise SystemExit("publication gate copies differ")
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()
