import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "repro" / "src" / "materialize_hf_build.py"


def test_rejects_incomplete_log(tmp_path: Path) -> None:
    log = tmp_path / "incomplete.log"
    log.write_text("COMMIT " + "a" * 40 + "\nBUILD_SUCCESS\n")
    destination = ROOT / "outputs" / "hf_build.json"
    before = destination.read_bytes() if destination.exists() else None
    result = subprocess.run([sys.executable, str(SCRIPT), "--job-id", "test", "--log", str(log)], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    if before is None:
        assert not destination.exists()
    else:
        assert destination.read_bytes() == before
