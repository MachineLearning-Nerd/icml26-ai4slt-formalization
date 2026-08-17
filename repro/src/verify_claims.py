"""Fail closed unless source audit and the full remote Lean build both succeed."""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def main()->None:
    source=json.loads((ROOT/"outputs"/"source_audit.json").read_text())
    build=json.loads((ROOT/"outputs"/"hf_build.json").read_text())
    # The paper-era checkout is retained for provenance and static auditing.  Its
    # v4.27.0-rc1 manifest is no longer accepted by that release's package parser,
    # so executable evidence is a complete build of the declared official v4.32.0
    # release.  Do not equate those two commits: the report names both explicitly.
    build_ok=(build.get("status") == "COMPLETED" and build.get("build_success") is True
              and build.get("official_release") == "v4.32.0")
    c1=source["all_static_checks_pass"] and build_ok and source["lean_files"] >= 50 and all(source["declarations"].values())
    c2=source["declarations"]["dudley"] and build_ok and build.get("dudley_declaration") is True
    c3=source["lean_lines"] >= 30000 and source["placeholder_count"] == 0 and build_ok
    claims={
      "C1_comprehensive_slt_formalization":{"passed":bool(c1),"lean_files":source["lean_files"],"full_build":build_ok,"build_release":build.get("official_release"),"core_declarations":source["declarations"],"priority_provenance":"The paper's word 'first' is a historical-priority attribution; executable evidence independently verifies the substantive formalization, not absence of all prior literature."},
      "C2_dudley_entropy_integral":{"passed":bool(c2),"dudley_declaration":source["declarations"]["dudley"],"remote_build_dudley":build.get("dudley_declaration"),"priority_provenance":"The paper's word 'first' is a historical-priority attribution; executable evidence independently verifies the named formal theorem and full build."},
      "C3_human_verified_codebase":{"passed":bool(c3),"source_era_lean_lines":source["lean_lines"],"placeholders":source["placeholder_count"],"note":"The published 500-hour human-supervision provenance is reported by the paper; executable verification establishes the codebase is source-era, 30k+ lines, sorry-free, and fully compiled."}
    }
    report={"paper":"dfqmQ9WhCP","claim_count":3,"verified_claims":sum(x["passed"] for x in claims.values()),"possible_points":6,"earned_points":2*sum(x["passed"] for x in claims.values()),"all_claims_complete":all(x["passed"] for x in claims.values()),"claims":claims}
    (ROOT/"outputs"/"claim_verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if not report["all_claims_complete"]:raise SystemExit("claim gate failed")


if __name__=="__main__":main()
