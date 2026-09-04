from __future__ import annotations

import json
from dataclasses import asdict

from .models import Review


LEVELS = {"critical": "error", "error": "error", "warning": "warning", "note": "note"}


def as_json(review: Review) -> str:
    return json.dumps({
        "schema_version": "1.0",
        "decision": review.decision,
        "summary": {
            "findings": len(review.findings),
            "monthly_cost_delta": review.monthly_cost_delta,
            "annual_risk_exposure": review.annual_risk_exposure,
        },
        "findings": [asdict(finding) for finding in review.findings],
        "evidence_boundary": "Static analysis of repository text; validate estimates and runtime behavior independently.",
    }, indent=2, sort_keys=True) + "\n"


def as_sarif(review: Review) -> str:
    rule_index = {}
    rules = []
    for finding in review.findings:
        if finding.rule_id not in rule_index:
            rule_index[finding.rule_id] = len(rules)
            rules.append({
                "id": finding.rule_id,
                "name": finding.title,
                "shortDescription": {"text": finding.title},
                "help": {"text": finding.remediation},
            })
    results = [{
        "ruleId": f.rule_id,
        "ruleIndex": rule_index[f.rule_id],
        "level": LEVELS[f.severity],
        "message": {"text": f"{f.message} Remediation: {f.remediation}"},
        "locations": [{"physicalLocation": {
            "artifactLocation": {"uri": f.path},
            "region": {"startLine": f.line},
        }}],
        "properties": {
            "pillar": f.pillar,
            "monthlyCostDelta": f.monthly_cost_delta,
            "annualRiskExposure": f.annual_risk_exposure,
        },
    } for f in review.findings]
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{"tool": {"driver": {
            "name": "Azure Well-Architected AI Reviewer",
            "informationUri": "https://github.com/AAH20/azure-well-architected-ai-reviewer",
            "rules": rules,
        }}, "results": results}],
    }
    return json.dumps(sarif, indent=2, sort_keys=True) + "\n"


def as_markdown(review: Review) -> str:
    lines = [
        "# Azure architecture review",
        "",
        f"**Decision:** `{review.decision.upper()}`",
        f"**Findings:** {len(review.findings)}",
        f"**Modeled monthly cost delta:** ${review.monthly_cost_delta:,.2f}",
        f"**Modeled annual risk exposure:** ${review.annual_risk_exposure:,.2f}",
        "",
    ]
    for f in review.findings:
        lines.extend([
            f"## {f.severity.upper()}: {f.title}", "",
            f"- Location: `{f.path}:{f.line}`",
            f"- Pillar: {f.pillar}",
            f"- Impact: {f.message}",
            f"- Remediation: {f.remediation}", "",
        ])
    lines.append("> Estimates are declared rule assumptions, not guaranteed losses or savings.")
    return "\n".join(lines) + "\n"
