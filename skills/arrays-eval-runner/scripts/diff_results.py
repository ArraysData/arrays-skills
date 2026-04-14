#!/usr/bin/env python3
"""Compare two eval result JSON files and report differences.

Usage:
    python diff_results.py old.json new.json
    python diff_results.py old.json new.json --json
"""

import argparse
import json
import sys
from pathlib import Path


def load_results(path: str) -> dict:
    return json.loads(Path(path).read_text())


def build_case_map(data: dict) -> dict:
    return {c["case_id"]: c for c in data.get("cases", [])}


def diff(old_path: str, new_path: str) -> dict:
    old_data = load_results(old_path)
    new_data = load_results(new_path)
    old_cases = build_case_map(old_data)
    new_cases = build_case_map(new_data)

    all_ids = sorted(set(old_cases) | set(new_cases))

    new_passes = []
    regressions = []
    score_changes = []

    for cid in all_ids:
        old_c = old_cases.get(cid)
        new_c = new_cases.get(cid)
        if not old_c or not new_c:
            continue

        old_pass = old_c.get("passed", False)
        new_pass = new_c.get("passed", False)
        old_score = old_c.get("overall_score", 0.0)
        new_score = new_c.get("overall_score", 0.0)

        if old_score is None or new_score is None:
            continue

        delta = round(new_score - old_score, 3)
        if delta != 0:
            score_changes.append({
                "case_id": cid,
                "old_score": old_score,
                "new_score": new_score,
                "delta": delta,
                "question": new_c.get("question", "")[:80],
            })

        if not old_pass and new_pass:
            new_passes.append(cid)
        elif old_pass and not new_pass:
            regressions.append(cid)

    # Summary metrics
    old_summary = old_data.get("summary", old_data.get("meta", {}))
    new_summary = new_data.get("summary", new_data.get("meta", {}))

    summary_delta = {}
    for key in ["tool_accuracy", "code_success_rate", "overall_pass_rate", "avg_overall_score"]:
        old_val = old_summary.get(key)
        new_val = new_summary.get(key)
        if old_val is not None and new_val is not None:
            summary_delta[key] = {
                "old": old_val,
                "new": new_val,
                "delta": round(new_val - old_val, 3),
            }

    score_changes.sort(key=lambda x: x["delta"])

    return {
        "new_passes": new_passes,
        "regressions": regressions,
        "score_changes": score_changes,
        "summary_delta": summary_delta,
    }


def print_report(result: dict):
    sd = result["summary_delta"]
    if sd:
        print("=== Summary Delta ===")
        for key, vals in sd.items():
            sign = "+" if vals["delta"] >= 0 else ""
            print(f"  {key}: {vals['old']} -> {vals['new']} ({sign}{vals['delta']})")
        print()

    if result["new_passes"]:
        print(f"=== New Passes ({len(result['new_passes'])}) ===")
        print(f"  Cases: {', '.join(result['new_passes'])}")
        print()

    if result["regressions"]:
        print(f"=== Regressions ({len(result['regressions'])}) ===")
        print(f"  Cases: {', '.join(result['regressions'])}")
        print()

    changes = result["score_changes"]
    if changes:
        print(f"=== Score Changes ({len(changes)}) ===")
        for c in changes:
            sign = "+" if c["delta"] >= 0 else ""
            print(f"  [{c['case_id']}] {c['old_score']} -> {c['new_score']} ({sign}{c['delta']})  {c['question']}")
    else:
        print("No score changes detected.")


def main():
    parser = argparse.ArgumentParser(description="Compare two eval result JSON files")
    parser.add_argument("old", help="Path to the old/baseline result JSON")
    parser.add_argument("new", help="Path to the new result JSON")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = diff(args.old, args.new)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
