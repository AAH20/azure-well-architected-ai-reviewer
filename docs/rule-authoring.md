# Rule authoring

Rules are data in `rules/azure-rules.json`. Each rule must include:

- Stable identifier
- Human-readable architectural consequence
- Narrow pattern and supported extensions
- Well-Architected pillar
- Actionable remediation
- Severity
- Explicit cost and risk assumptions
- Positive detection fixture
- Negative-control fixture

Expected annual risk exposure is calculated as `annual probability × failure impact`. It is prioritization metadata, not a prediction or customer guarantee.

Regex rules are intentionally limited. Resource-aware parsing, Terraform plan analysis and Azure Resource Graph enrichment belong in later versions and must not be implied by current results.
