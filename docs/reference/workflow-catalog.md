# Reference: Workflow catalog

Index of all workflow exports. Machine-readable source: [`exports/catalog.yaml`](../../exports/catalog.yaml).

## Library summary

| Metric | Count |
|---|---|
| Total workflow JSON exports | 29 |
| Active in CE tenant | 2 |
| Standard exported-only | 7 |
| Complex generated-only | 20 |
| Story library imports | 1 |

![Workflow library overview](../diagrams/workflow-library-overview.drawio.png)

## Active in tenant

| ID | Name | Actions | Webhook path | Test script |
|---|---|---|---|---|
| alert-triage | Your first story | 5 | your-first-story | scripts/test-both-branches.sh |
| alert-triage-advanced | Alert Triage Advanced | 11 | alert-triage-advanced | scripts/test-advanced-branches.sh |

## Standard exported-only

| ID | Trigger | Test script |
|---|---|---|
| scheduled-heartbeat | Schedule */15 | — |
| ip-enrichment | Webhook | scripts/test-ip-enrichment.sh |
| url-reputation-check | Webhook | scripts/test-url-reputation.sh |
| dedup-alerts | Webhook | scripts/test-dedup-alerts.sh |
| throttle-demo | Webhook | scripts/test-throttle-demo.sh |
| delay-retry | Webhook | scripts/test-delay-retry.sh |
| geo-block-gate | Webhook | scripts/test-geo-block-gate.sh |

## Complex generated-only (20)

Import JSON from `exports/workflows/` to run. Each has 8–11 actions, nested conditions, and HTTP enrichment (httpbin). Regenerate with `python3 scripts/generate-complex-workflows.py`.

| ID | Name | Actions | Webhook env var | Test script |
|---|---|---|---|---|
| email-ticket-router | Email Ticket Router | 11 | `WEBHOOK_URL_EMAIL_TICKET_ROUTER` | scripts/test-email-ticket-router.sh |
| manual-playbook-runner | Manual Playbook Runner | 10 | `WEBHOOK_URL_MANUAL_PLAYBOOK_RUNNER` | scripts/test-manual-playbook-runner.sh |
| batch-etl-pipeline | Batch ETL Pipeline | 10 | `WEBHOOK_URL_BATCH_ETL_PIPELINE` | scripts/test-batch-etl-pipeline.sh |
| case-management-stub | Case Management Stub | 11 | `WEBHOOK_URL_CASE_MANAGEMENT_STUB` | scripts/test-case-management-stub.sh |
| slack-notify-stub | Slack Notify Stub | 11 | `WEBHOOK_URL_SLACK_NOTIFY_STUB` | scripts/test-slack-notify-stub.sh |
| servicenow-incident-stub | ServiceNow Incident Stub | 11 | `WEBHOOK_URL_SERVICENOW_INCIDENT_STUB` | scripts/test-servicenow-incident-stub.sh |
| ai-summary-stub | AI Summary Stub | 10 | `WEBHOOK_URL_AI_SUMMARY_STUB` | scripts/test-ai-summary-stub.sh |
| phishing-analyzer | Phishing Analyzer | 11 | `WEBHOOK_URL_PHISHING_ANALYZER` | scripts/test-phishing-analyzer.sh |
| malware-hash-triage | Malware Hash Triage | 10 | `WEBHOOK_URL_MALWARE_HASH_TRIAGE` | scripts/test-malware-hash-triage.sh |
| user-risk-engine | User Risk Engine | 11 | `WEBHOOK_URL_USER_RISK_ENGINE` | scripts/test-user-risk-engine.sh |
| incident-correlator | Incident Correlator | 10 | `WEBHOOK_URL_INCIDENT_CORRELATOR` | scripts/test-incident-correlator.sh |
| vulnerability-scorer | Vulnerability Scorer | 11 | `WEBHOOK_URL_VULNERABILITY_SCORER` | scripts/test-vulnerability-scorer.sh |
| auth-anomaly-detector | Auth Anomaly Detector | 10 | `WEBHOOK_URL_AUTH_ANOMALY_DETECTOR` | scripts/test-auth-anomaly-detector.sh |
| exfil-monitor | Exfil Monitor | 11 | `WEBHOOK_URL_EXFIL_MONITOR` | scripts/test-exfil-monitor.sh |
| compliance-audit-chain | Compliance Audit Chain | 10 | `WEBHOOK_URL_COMPLIANCE_AUDIT_CHAIN` | scripts/test-compliance-audit-chain.sh |
| threat-intel-pipeline | Threat Intel Pipeline | 11 | `WEBHOOK_URL_THREAT_INTEL_PIPELINE` | scripts/test-threat-intel-pipeline.sh |
| ransomware-response | Ransomware Response | 10 | `WEBHOOK_URL_RANSOMWARE_RESPONSE` | scripts/test-ransomware-response.sh |
| insider-threat-analyzer | Insider Threat Analyzer | 11 | `WEBHOOK_URL_INSIDER_THREAT_ANALYZER` | scripts/test-insider-threat-analyzer.sh |
| cloud-misconfig-triage | Cloud Misconfig Triage | 10 | `WEBHOOK_URL_CLOUD_MISCONFIG_TRIAGE` | scripts/test-cloud-misconfig-triage.sh |
| supply-chain-scanner | Supply Chain Scanner | 11 | `WEBHOOK_URL_SUPPLY_CHAIN_SCANNER` | scripts/test-supply-chain-scanner.sh |

## Story library

| ID | Source |
|---|---|
| analyze-urls-fraud-abuse | [Tines Library #87699](https://www.tines.com/library/stories/87699/) |

## Complexity tiers

| Tier | Pattern | Actions | Examples |
|---|---|---|---|
| Standard | Linear or single branch | 3–6 | ip-enrichment, dedup-alerts |
| Complex (triage) | Nested conditions + HTTP | 11 | alert-triage-advanced, phishing-analyzer |
| Complex (pipeline) | Dedup + throttle + HTTP + branch | 10 | manual-playbook-runner, ransomware-response |

## Related

- [How-to: Swap workflows on CE](../how-to/swap-workflows-on-ce.md)
- [Reference: CE limits](ce-limits.md)
- [Explanation: Alert triage pipelines](../explanation/alert-triage-pipelines.md)
