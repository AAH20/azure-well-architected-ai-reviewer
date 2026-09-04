from __future__ import annotations

import json
from pathlib import Path

from .engine import review_path
from .rules import load_rules


def run(manifest_path: Path, rules_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text())
    rules = load_rules(rules_path)
    outcomes = []
    for case in manifest["cases"]:
        target = manifest_path.parent / case["path"]
        actual = sorted({finding.rule_id for finding in review_path(target, rules).findings})
        expected = sorted(case["expected_rule_ids"])
        outcomes.append({
            "id": case["id"],
            "passed": actual == expected,
            "expected": expected,
            "actual": actual,
        })
    passed = sum(outcome["passed"] for outcome in outcomes)
    return {
        "cases": outcomes,
        "passed": passed,
        "total": len(outcomes),
        "pass_rate": round(passed / len(outcomes), 4) if outcomes else 0,
    }
