#!/usr/bin/env python3
"""Check structured evaluator observations against the bundled behavior rubrics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", dest="case_id", help="Evaluate one case id, for example ev-02")
    parser.add_argument("--response", type=Path, help="JSON object with case_id and observed boolean criteria")
    parser.add_argument("--all", action="store_true", help="Run all bundled fixture observations")
    args = parser.parse_args()
    if args.all == (args.response is not None):
        parser.error("Use exactly one of --all or --response.")

    rubric = load_json(root / "evals" / "evals.json")
    cases = {case["id"]: case for case in rubric["cases"]}
    responses = []
    if args.all:
        responses = [load_json(path) for path in sorted((root / "evals" / "fixtures").glob("*.json"))]
    else:
        responses = [load_json(args.response)]

    failures = 0
    for response in responses:
        case_id = args.case_id or response.get("case_id")
        case = cases.get(case_id)
        if not case:
            print(f"FAIL unknown case: {case_id}")
            failures += 1
            continue
        observed = response.get("observed")
        if not isinstance(observed, dict):
            print(f"FAIL {case_id}: observed must be an object")
            failures += 1
            continue
        missing = [key for key, expected in case["expect"].items() if expected and observed.get(key) is not True]
        if missing:
            print(f"FAIL {case_id}: missing {', '.join(missing)}")
            failures += 1
        else:
            print(f"PASS {case_id}: {case['name']}")
    print(f"Checked {len(responses)} response(s), {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
