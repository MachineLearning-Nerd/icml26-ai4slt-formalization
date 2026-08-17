"""Static independent audit of the source-era Lean formalization."""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
UPSTREAM=ROOT/"upstream"
PIN="7b82b1323c80f0c21ca449fd12e1c24315ae9782"
DECLARATIONS={
    "dudley": "SLT/Dudley.lean",
    "efronStein": "SLT/EfronStein.lean",
    "gaussian_lipschitz_concentration": "SLT/GaussianLipConcen.lean",
    "linear_minimax_rate_rank": "SLT/LeastSquares/LinearRegression/MinimaxRate.lean",
}


def main()->None:
    commit=subprocess.check_output(["git","-C",str(UPSTREAM),"rev-parse","HEAD"],text=True).strip()
    files=sorted((UPSTREAM/"SLT").rglob("*.lean"))
    text={path.relative_to(UPSTREAM).as_posix():path.read_text(errors="replace") for path in files}
    placeholders=[]
    for filename,contents in text.items():
        for match in re.finditer(r"\b(sorry|admit|axiom)\b",contents):
            placeholders.append({"file":filename,"token":match.group(1)})
    declarations={}
    declaration_locations={}
    for name,path in DECLARATIONS.items():
        match=re.search(rf"^theorem\s+{re.escape(name)}\b",text[path],re.M)
        declarations[name]=bool(match)
        if match:
            declaration_locations[name]={"file":path,"line":text[path][:match.start()].count("\n")+1}
    line_count=sum(value.count("\n")+1 for value in text.values())
    report={"official_commit":commit,"commit_matches_pin":commit==PIN,"lean_files":len(files),"lean_lines":line_count,"placeholder_count":len(placeholders),"declarations":declarations,"declaration_locations":declaration_locations,"all_static_checks_pass":commit==PIN and len(files)>=50 and line_count>=30000 and not placeholders and all(declarations.values())}
    (ROOT/"outputs"/"source_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if not report["all_static_checks_pass"]:raise SystemExit("static source audit failed")


if __name__=="__main__":main()
