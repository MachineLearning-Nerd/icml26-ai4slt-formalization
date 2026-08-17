# Negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8d47bfaa472a", "created_at": "2026-07-20T07:09:36+00:00", "title": "Negative controls"}
-->
## Negative controls

The audit fails if the source commit differs, the code is below 30,000 lines, a required theorem declaration is absent, a proof placeholder is present, or the remote build is incomplete.


---
<!-- trackio-cell
{"type": "code", "id": "cell_14113700d23e", "created_at": "2026-07-20T07:10:58+00:00", "title": "Run: python (exit 0)", "command": [".venv/bin/python", "-m", "pytest", "-q"], "exit_code": 0, "duration_s": 0.407}
-->
````bash
$ .venv/bin/python -m pytest -q
````

exit 0 · 0.4s


````output
...                                                                      [100%]
3 passed in 0.13s

````
