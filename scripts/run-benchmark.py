#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from azure_arch_review.benchmark import run  # noqa: E402

result = run(ROOT / "benchmarks/manifest.json", ROOT / "rules/azure-rules.json")
output = json.dumps(result, indent=2, sort_keys=True) + "\n"
(ROOT / "evidence/benchmark-results.json").write_text(output)
print(output, end="")
raise SystemExit(0 if result["pass_rate"] == 1.0 else 1)
