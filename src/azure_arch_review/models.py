from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rule:
    rule_id: str
    title: str
    description: str
    pattern: str
    file_extensions: tuple[str, ...]
    severity: str
    pillar: str
    remediation: str
    monthly_cost_delta: float = 0.0
    annual_failure_probability: float = 0.0
    failure_impact: float = 0.0


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    message: str
    path: str
    line: int
    severity: str
    pillar: str
    remediation: str
    monthly_cost_delta: float
    annual_risk_exposure: float


@dataclass
class Review:
    findings: list[Finding] = field(default_factory=list)

    @property
    def decision(self) -> str:
        return "hold" if any(f.severity in {"error", "critical"} for f in self.findings) else "pass"

    @property
    def annual_risk_exposure(self) -> float:
        return round(sum(f.annual_risk_exposure for f in self.findings), 2)

    @property
    def monthly_cost_delta(self) -> float:
        return round(sum(f.monthly_cost_delta for f in self.findings), 2)
