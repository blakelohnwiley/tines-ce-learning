# Remaining catalog workflows — Workbench build prompts

**Status:** The 20 complex workflows in `exports/workflows/` are **generated JSON** (8–11 actions each). Import them directly — no Workbench build required.

Regenerate: `python3 scripts/generate-complex-workflows.py` then `python3 scripts/update-catalog-from-generated.py`.

---

## Already generated (import from JSON)

| ID | Actions | File |
|---|---|---|
| email-ticket-router | 11 | workflows/email-ticket-router.json |
| manual-playbook-runner | 10 | workflows/manual-playbook-runner.json |
| batch-etl-pipeline | 10 | workflows/batch-etl-pipeline.json |
| case-management-stub | 11 | workflows/case-management-stub.json |
| slack-notify-stub | 11 | workflows/slack-notify-stub.json |
| servicenow-incident-stub | 11 | workflows/servicenow-incident-stub.json |
| ai-summary-stub | 10 | workflows/ai-summary-stub.json |
| phishing-analyzer | 11 | workflows/phishing-analyzer.json |
| malware-hash-triage | 10 | workflows/malware-hash-triage.json |
| user-risk-engine | 11 | workflows/user-risk-engine.json |
| incident-correlator | 10 | workflows/incident-correlator.json |
| vulnerability-scorer | 11 | workflows/vulnerability-scorer.json |
| auth-anomaly-detector | 10 | workflows/auth-anomaly-detector.json |
| exfil-monitor | 11 | workflows/exfil-monitor.json |
| compliance-audit-chain | 10 | workflows/compliance-audit-chain.json |
| threat-intel-pipeline | 11 | workflows/threat-intel-pipeline.json |
| ransomware-response | 10 | workflows/ransomware-response.json |
| insider-threat-analyzer | 11 | workflows/insider-threat-analyzer.json |
| cloud-misconfig-triage | 10 | workflows/cloud-misconfig-triage.json |
| supply-chain-scanner | 11 | workflows/supply-chain-scanner.json |

---

## Optional future builds (not yet in library)

Use Workbench prompts below if you prefer tenant-native builds over generated JSON.

### Okta user suspend path

```
Build Okta user suspend stub with webhook, condition on risk score, and HTTP placeholder for Okta API.
Requires Okta credential when going live.
```

### AWS EC2 inventory

```
Build AWS EC2 list stub: webhook → transform → HTTP AWS API placeholder.
Requires AWS credential.
```

---

## Import path (Story Library)

For templates not yet exported, use **Stories → New → Story library** in the tenant, search, import, export to `exports/story-library/`, then disable.

Recommended next imports:
- Write and improve AI prompts with an AI chatbot
- List EC2 instances in AWS (needs AWS cred)
- Report inactive Okta accounts (needs Okta cred)
