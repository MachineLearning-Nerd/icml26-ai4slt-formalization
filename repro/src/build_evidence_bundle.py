"""Assemble a hash-bound public evidence bundle after the cumulative gate."""
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
        ".gitmodules",
        "README.md",
        "STATUS.md",
        "sources.json",
        "docs/BRANCH_AUDIT.md",
        "docs/CLAIM_AUDIT.md",
        "docs/PUBLICATION_GATE.md",
        "docs/SOURCE_AUDIT.md",
        "docs/arxiv_source.tar",
        "docs/primary.pdf",
        "docs/hf_job_protocol.md",
        "docs/independent_proof_audit.md",
        "outputs/CUMULATIVE_SCIENCE_GATE.json",
        "outputs/README.md",
        "outputs/claim_verification.json",
        "outputs/hf_build.json",
        "outputs/hf_job_build.log",
        "outputs/source_audit.json",
        "repro/configs/live_claims.json",
        "repro/requirements.txt",
        "repro/src/audit_source.py",
        "repro/src/build_evidence_bundle.py",
        "repro/src/cumulative_science_gate.py",
        "repro/src/materialize_hf_build.py",
        "repro/src/publication_gate.py",
        "repro/src/verify_claims.py",
        "repro/tests/test_build_evidence_bundle.py",
        "repro/tests/test_materialize_hf_build.py",
        "repro/tests/test_source_audit.py",
    ]
    records = []
    for name in sorted(names):
        path = ROOT / name
        if not path.is_file():
            raise SystemExit(f"missing required evidence artifact: {name}")
        size, sha = digest(path)
        records.append({"artifact": name, "bytes": size, "sha256": sha})
    bundle = OUTPUTS / "evidence_bundle.jsonl"
    bundle.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    bundle_bytes, bundle_sha = digest(bundle)
    report = {
        "paper": "dfqmQ9WhCP",
        "records": len(records),
        "bytes": bundle_bytes,
        "sha256": bundle_sha,
        "claim_verification": {
            "verified_claims": verdict["verified_claims"],
            "claim_count": verdict["claim_count"],
            "earned_points": verdict["earned_points"],
            "possible_points": verdict["possible_points"],
        },
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
