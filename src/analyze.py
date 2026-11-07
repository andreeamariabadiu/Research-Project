import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
GEN_DIR = ROOT / "data" / "generated"
RES_DIR = ROOT / "data" / "results"
RAW_JSON = RES_DIR / "bandit_raw.json"


def run_bandit():
    RES_DIR.mkdir(parents=True, exist_ok=True)
    # Bandit exits with code 1 when it finds issues, so no check=True here
    subprocess.run([
        sys.executable, "-m", "bandit", "-r", str(GEN_DIR),
        "-f", "json", "-o", str(RAW_JSON), "-q",
    ])


def parse_name(path):
    """model_condition_functionId_run.py -> (model, condition, id, run)"""
    model, condition, fid, run = Path(path).stem.rsplit("_", 3)
    return model, condition, int(fid), int(run)


def main():
    if not any(GEN_DIR.rglob("*.py")):
        print("No generated files found in", GEN_DIR, "- run generate.py first.")
        return

    run_bandit()
    raw = json.loads(RAW_JSON.read_text(encoding="utf-8"))

    bad_files = {Path(e["filename"]).name for e in raw.get("errors", [])}

    columns = ["file", "model", "condition", "function_id", "run", "test_id",
               "test_name", "severity", "confidence", "cwe", "line", "text"]
    rows = []
    for r in raw["results"]:
        model, condition, fid, run = parse_name(r["filename"])
        cwe = r.get("issue_cwe") or {}
        rows.append({
            "file": Path(r["filename"]).name,
            "model": model,
            "condition": condition,
            "function_id": fid,
            "run": run,
            "test_id": r["test_id"],
            "test_name": r["test_name"],
            "severity": r["issue_severity"],
            "confidence": r["issue_confidence"],
            "cwe": f"CWE-{cwe['id']}" if cwe.get("id") else "",
            "line": r["line_number"],
            "text": r["issue_text"],
        })
    findings = pd.DataFrame(rows, columns=columns)
    findings.to_csv(RES_DIR / "findings.csv", index=False)

    files = []
    excluded = []
    for p in sorted(GEN_DIR.rglob("*.py")):
        if p.name in bad_files or p.stat().st_size <= 1:
            excluded.append(p.name)
            continue
        model, condition, fid, run = parse_name(p)
        sub = findings[findings["file"] == p.name]
        files.append({
            "file": p.name,
            "model": model,
            "condition": condition,
            "function_id": fid,
            "run": run,
            "n_findings": len(sub),
            "n_high": int((sub["severity"] == "HIGH").sum()),
            "n_medium": int((sub["severity"] == "MEDIUM").sum()),
            "n_low": int((sub["severity"] == "LOW").sum()),
        })

    if not files:
        print("All files were excluded (empty or unparsable).")
        return

    summary = pd.DataFrame(files)
    summary["has_finding"] = summary["n_findings"] > 0
    summary.to_csv(RES_DIR / "summary_per_file.csv", index=False)

    print(summary.groupby(["model", "condition"])[
        ["n_findings", "n_high", "n_medium", "n_low", "has_finding"]
    ].mean().round(2))
    print("\nFiles analysed:", len(summary))
    print("Files excluded (unparsable or empty):", len(excluded))
    for name in excluded:
        print("  -", name)


if __name__ == "__main__":
    main()