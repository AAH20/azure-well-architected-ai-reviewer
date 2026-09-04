from __future__ import annotations

import re
from pathlib import Path

from .models import Finding, Review, Rule


IGNORED_PARTS = {".git", ".terraform", ".venv", "node_modules", "vendor"}


def discover(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and not IGNORED_PARTS.intersection(path.parts)
    )


def review_path(root: Path, rules: list[Rule]) -> Review:
    findings: list[Finding] = []
    for path in discover(root):
        applicable = [rule for rule in rules if path.suffix.lower() in rule.file_extensions]
        if not applicable:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(lines, start=1):
            for rule in applicable:
                if re.search(rule.pattern, line, flags=re.IGNORECASE):
                    risk = rule.annual_failure_probability * rule.failure_impact
                    findings.append(Finding(
                        rule_id=rule.rule_id,
                        title=rule.title,
                        message=rule.description,
                        path=path.name if root.is_file() else str(path.relative_to(root)),
                        line=number,
                        severity=rule.severity,
                        pillar=rule.pillar,
                        remediation=rule.remediation,
                        monthly_cost_delta=rule.monthly_cost_delta,
                        annual_risk_exposure=round(risk, 2),
                    ))
    return Review(findings=findings)
