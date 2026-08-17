# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_0e64c345b51b", "created_at": "2026-07-20T07:09:35+00:00", "title": "Methods"}
-->
## Methods

Pinned paper source and official code are hashed locally. A recorded
CPU-upgrade Hugging Face Job performed a complete Lean build of the official
v4.32.0 release; no subset compilation is accepted. The source-era
v4.27.0-rc1 checkout is audited statically because its package manifest is not
accepted by that release candidate's current parser.


---
<!-- trackio-cell
{"type": "code", "id": "cell_5b66763e9fce", "created_at": "2026-07-20T07:10:57+00:00", "title": "Run: python audit_source.py (exit 0)", "command": [".venv/bin/python", "repro/src/audit_source.py"], "exit_code": 0, "duration_s": 0.117}
-->
````bash
$ .venv/bin/python repro/src/audit_source.py
````

exit 0 · 0.1s


````python title=audit_source.py
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
    declarations={name:bool(re.search(rf"^theorem\s+{re.escape(name)}\b",text[path],re.M)) for name,path in DECLARATIONS.items()}
    report={"official_commit":commit,"commit_matches_pin":commit==PIN,"lean_files":len(files),"lean_lines":sum(value.count("\n")+1 for value in text.values()),"placeholder_count":len(placeholders),"declarations":declarations,"all_static_checks_pass":commit==PIN and len(files)>=50 and sum(value.count("\n")+1 for value in text.values())>=30000 and not placeholders and all(declarations.values())}
    (ROOT/"outputs"/"source_audit.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if not report["all_static_checks_pass"]:raise SystemExit("static source audit failed")


if __name__=="__main__":main()

````


````output
{
  "official_commit": "7b82b1323c80f0c21ca449fd12e1c24315ae9782",
  "commit_matches_pin": true,
  "lean_files": 55,
  "lean_lines": 34684,
  "placeholder_count": 0,
  "declarations": {
    "dudley": true,
    "efronStein": true,
    "gaussian_lipschitz_concentration": true,
    "linear_minimax_rate_rank": true
  },
  "all_static_checks_pass": true
}

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_ecbfd868b37c", "created_at": "2026-07-20T07:11:57+00:00", "title": "Run: python audit_source.py (exit 0)", "command": [".venv/bin/python", "repro/src/audit_source.py"], "exit_code": 0, "duration_s": 0.119}
-->
````bash
$ .venv/bin/python repro/src/audit_source.py
````

exit 0 · 0.1s


````python title=audit_source.py
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

````


````output
{
  "official_commit": "7b82b1323c80f0c21ca449fd12e1c24315ae9782",
  "commit_matches_pin": true,
  "lean_files": 55,
  "lean_lines": 34684,
  "placeholder_count": 0,
  "declarations": {
    "dudley": true,
    "efronStein": true,
    "gaussian_lipschitz_concentration": true,
    "linear_minimax_rate_rank": true
  },
  "declaration_locations": {
    "dudley": {
      "file": "SLT/Dudley.lean",
      "line": 2517
    },
    "efronStein": {
      "file": "SLT/EfronStein.lean",
      "line": 1212
    },
    "gaussian_lipschitz_concentration": {
      "file": "SLT/GaussianLipConcen.lean",
      "line": 1301
    },
    "linear_minimax_rate_rank": {
      "file": "SLT/LeastSquares/LinearRegression/MinimaxRate.lean",
      "line": 592
    }
  },
  "all_static_checks_pass": true
}

````
