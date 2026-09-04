#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_dir"

PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m azure_arch_review.cli tests/fixtures/safe.bicep \
  --rules rules/azure-rules.json --format sarif --output evidence/safe-results.sarif
python3 scripts/run-benchmark.py
python3 -m json.tool evidence/safe-results.sarif >/dev/null
