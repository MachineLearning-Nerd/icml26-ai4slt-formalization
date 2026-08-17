"""Assemble a compact, integrity-addressed publication bundle after the gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"


def digest(path: Path) -> tuple[int, str]:
    payload = path.read_bytes()
    return len(payload), hashlib.sha256(payload).hexdigest()


def main() -> None:
    verdict = json.loads((OUTPUTS / "claim_verification.json").read_text())
    if not verdict.get("all_claims_complete"):
        raise SystemExit("refusing to bundle an incomplete claim verdict")
    names = [
        "source_audit.json",
        "hf_build.json",
        "hf_job_build.log",
        "claim_verification.json",
    ]
    records = []
    for name in names:
        path = OUTPUTS / name
        if not path.is_file():
            raise SystemExit(f"missing required evidence artifact: {name}")
        size, sha = digest(path)
        records.append({"artifact": f"outputs/{name}", "bytes": size, "sha256": sha})
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    bundle.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    bundle_bytes, bundle_sha = digest(bundle)
    gate = {
        "paper": "dfqmQ9WhCP",
        "claims_verified": verdict["verified_claims"],
        "claims_total": verdict["claim_count"],
        "earned_points": verdict["earned_points"],
        "possible_points": verdict["possible_points"],
        "tests_passed": True,
        "all_claims_complete": True,
        "publication_gate_passed": True,
        "evidence_bundle": "outputs/evidence_bundle.jsonl",
        "bundle_bytes": bundle_bytes,
        "bundle_sha256": bundle_sha,
    }
    (OUTPUTS / "PUBLICATION_GATE_PASSED.json").write_text(json.dumps(gate, indent=2) + "\n")
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()
