import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "repro" / "src" / "build_evidence_bundle.py"


def test_refuses_without_complete_verdict() -> None:
    verdict = ROOT / "outputs" / "claim_verification.json"
    before = verdict.read_bytes() if verdict.exists() else None
    verdict.write_text('{"all_claims_complete": false}\n')
    try:
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], cwd=ROOT, capture_output=True, text=True
        )
    finally:
        if before is None:
            verdict.unlink()
        else:
            verdict.write_bytes(before)
    assert result.returncode != 0
    assert "refusing to bundle" in result.stderr
