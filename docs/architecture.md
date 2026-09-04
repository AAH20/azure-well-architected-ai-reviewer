# Architecture

## Execution path

1. Discover supported IaC files.
2. Apply versioned deterministic rules.
3. Calculate declared cost and expected-loss metadata.
4. Produce Markdown, JSON or SARIF.
5. Return `hold` only for error or critical findings.
6. Preserve evidence that can be independently reproduced.

The GitHub Action executes this path without requiring an external account, model key or Azure subscription. A future hosted control plane can retain organizational history and architecture graphs, but it is not required for OSS adoption.

## Planned advisory plane

Model integrations are deliberately not implemented in v0.1. Future Azure-hosted, NVIDIA NIM, OpenAI, Anthropic, OpenRouter-compatible and local adapters must all implement the same advisory interface. Their recommendations cannot change deterministic rule results or gain production mutation authority.

The evaluation loop will measure exact finding accuracy, remediation compilation, cost, latency and human acceptance by model and scenario. A model is promoted only against a versioned benchmark.

## Context graph

The target graph connects IaC lines, Azure resources, networks, application dependencies, SLOs, cost centres, controls, incidents and architecture decisions. This permits impact analysis across technical and business boundaries while retaining provenance.

## Azure hosted profile

The default `azd` profile provisions Log Analytics only. The optional Container Apps environment provides a future hosted API boundary and remains disabled to minimize spend. No hosted application is claimed in this release.
