# Security policy

Report vulnerabilities with a private GitHub security advisory. Do not submit customer IaC, cloud identifiers, secrets, plans or state files in a public issue.

The reviewer processes repository content locally in v0.1. The GitHub Action requests read-only contents permission. SARIF upload, if enabled by a consuming repository, should use the minimum `security-events: write` permission.
