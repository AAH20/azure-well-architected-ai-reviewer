import json
import tempfile
import unittest
from pathlib import Path

from azure_arch_review.engine import review_path
from azure_arch_review.benchmark import run
from azure_arch_review.reporters import as_json, as_sarif
from azure_arch_review.rules import load_rules


ROOT = Path(__file__).parents[1]
RULES = load_rules(ROOT / "rules/azure-rules.json")


class ReviewerTests(unittest.TestCase):
    def test_unsafe_fixture_is_held(self):
        review = review_path(ROOT / "tests/fixtures", RULES)
        ids = {finding.rule_id for finding in review.findings}
        self.assertEqual(review.decision, "hold")
        self.assertTrue({"AZR-NET-001", "AZR-STO-001", "AZR-TLS-001", "AZR-K8S-001"}.issubset(ids))

    def test_safe_bicep_has_no_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "safe.bicep"
            target.write_text((ROOT / "tests/fixtures/safe.bicep").read_text())
            self.assertEqual(review_path(Path(directory), RULES).findings, [])

    def test_risk_math_is_reproducible(self):
        review = review_path(ROOT / "tests/fixtures", RULES)
        storage = next(f for f in review.findings if f.rule_id == "AZR-STO-001")
        self.assertEqual(storage.annual_risk_exposure, 6000)

    def test_sarif_has_physical_locations(self):
        sarif = json.loads(as_sarif(review_path(ROOT / "tests/fixtures", RULES)))
        location = sarif["runs"][0]["results"][0]["locations"][0]["physicalLocation"]
        self.assertGreater(location["region"]["startLine"], 0)

    def test_json_declares_evidence_boundary(self):
        result = json.loads(as_json(review_path(ROOT / "tests/fixtures", RULES)))
        self.assertIn("Static analysis", result["evidence_boundary"])

    def test_benchmark_manifest(self):
        result = run(ROOT / "benchmarks/manifest.json", ROOT / "rules/azure-rules.json")
        self.assertEqual(result["pass_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
