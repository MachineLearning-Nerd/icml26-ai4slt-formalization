import json
from pathlib import Path


def test_source_audit_is_source_era_and_sorry_free():
    report=json.loads((Path(__file__).resolve().parents[2]/"outputs"/"source_audit.json").read_text())
    assert report["commit_matches_pin"]
    assert report["lean_files"] >= 50
    assert report["lean_lines"] >= 30_000
    assert report["placeholder_count"] == 0
    assert all(report["declarations"].values())
