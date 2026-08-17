"""Convert terminal HF Job evidence into a fail-closed build record."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def one(pattern: str, text: str, label: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        raise SystemExit(f"missing required HF build marker: {label}")
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    text = args.log.read_text(errors="replace")
    commit = one(r"^COMMIT ([0-9a-f]{40})$", text, "COMMIT")
    lean_files = int(one(r"^LEAN_FILES\s+(\d+)$", text, "LEAN_FILES"))
    lean_lines = int(one(r"^LEAN_LINES\s+(\d+)(?:\s+total)?$", text, "LEAN_LINES"))
    placeholders = int(one(r"^PLACEHOLDERS\s+(\d+)$", text, "PLACEHOLDERS"))
    dudley = "DUDLEY " in text and bool(
        re.search(r"^\d+:(?:theorem|def)\s+dudley\b", text, re.MULTILINE)
    )
    if "BUILD_SUCCESS" not in text or placeholders != 0 or not dudley:
        raise SystemExit("remote build did not satisfy the complete evidence contract")
    record = {
        "status": "COMPLETED",
        "job_id": args.job_id,
        "flavor": "cpu-upgrade",
        "official_release": "v4.32.0",
        "commit": commit,
        "build_success": True,
        "lean_files": lean_files,
        "lean_lines": lean_lines,
        "placeholder_count": placeholders,
        "dudley_declaration": dudley,
        "log_file": str(args.log.resolve().relative_to(ROOT)),
    }
    destination = ROOT / "outputs" / "hf_build.json"
    destination.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
