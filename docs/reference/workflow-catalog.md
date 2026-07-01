# Reference: Workflow catalog

Index of all workflow exports. Machine-readable source: [`exports/catalog.yaml`](../../exports/catalog.yaml).

## Library summary

| Metric | Count |
|---|---|
| Total workflow JSON exports | 29 |
| Active in CE tenant | 2 |
| Standard exported-only | 7 |
| Complex imported (disabled) | 20 |
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

## Complex imported (20)

All imported to the CE tenant on 2026-07-01; **disabled** to preserve the 2/3 flow budget. Enable one at a time via [swap workflow](../how-to/swap-workflows-on-ce.md), copy its webhook URL, then run the matching test script.

| ID | Story ID | Name | Actions | Webhook env var | Test script |
|---|---|---|---|---|---|
| phishing-analyzer | 121699 | Phishing Analyzer | 11 | `WEBHOOK_URL_PHISHING_ANALYZER` | scripts/test-phishing-analyzer.sh |
| email-ticket-router | 121700 | Email Ticket Router | 11 | `WEBHOOK_URL_EMAIL_TICKET_ROUTER` | scripts/test-email-ticket-router.sh |
| manual-playbook-runner | 121701 | Manual Playbook Runner | 10 | `WEBHOOK_URL_MANUAL_PLAYBOOK_RUNNER` | scripts/test-manual-playbook-runner.sh |
| batch-etl-pipeline | 121702 | Batch ETL Pipeline | 10 | `WEBHOOK_URL_BATCH_ETL_PIPELINE` | scripts/test-batch-etl-pipeline.sh |
| case-management-stub | 121703 | Case Management Stub | 11 | `WEBHOOK_URL_CASE_MANAGEMENT_STUB` | scripts/test-case-management-stub.sh |
| slack-notify-stub | 121704 | Slack Notify Stub | 11 | `WEBHOOK_URL_SLACK_NOTIFY_STUB` | scripts/test-slack-notify-stub.sh |
| servicenow-incident-stub | 121705 | ServiceNow Incident Stub | 11 | `WEBHOOK_URL_SERVICENOW_INCIDENT_STUB` | scripts/test-servicenow-incident-stub.sh |
| ai-summary-stub | 121706 | AI Summary Stub | 10 | `WEBHOOK_URL_AI_SUMMARY_STUB` | scripts/test-ai-summary-stub.sh |
| malware-hash-triage | 121707 | Malware Hash Triage | 10 | `WEBHOOK_URL_MALWARE_HASH_TRIAGE` | scripts/test-malware-hash-triage.sh |
| user-risk-engine | 121708 | User Risk Engine | 11 | `WEBHOOK_URL_USER_RISK_ENGINE` | scripts/test-user-risk-engine.sh |
| incident-correlator | 121709 | Incident Correlator | 10 | `WEBHOOK_URL_INCIDENT_CORRELATOR` | scripts/test-incident-correlator.sh |
| vulnerability-scorer | 121710 | Vulnerability Scorer | 11 | `WEBHOOK_URL_VULNERABILITY_SCORER` | scripts/test-vulnerability-scorer.sh |
| auth-anomaly-detector | 121711 | Auth Anomaly Detector | 10 | `WEBHOOK_URL_AUTH_ANOMALY_DETECTOR` | scripts/test-auth-anomaly-detector.sh |
| exfil-monitor | 121712 | Exfil Monitor | 11 | `WEBHOOK_URL_EXFIL_MONITOR` | scripts/test-exfil-monitor.sh |
| compliance-audit-chain | 121713 | Compliance Audit Chain | 10 | `WEBHOOK_URL_COMPLIANCE_AUDIT_CHAIN` | scripts/test-compliance-audit-chain.sh |
| threat-intel-pipeline | 121714 | Threat Intel Pipeline | 11 | `WEBHOOK_URL_THREAT_INTEL_PIPELINE` | scripts/test-threat-intel-pipeline.sh |
| ransomware-response | 121715 | Ransomware Response | 10 | `WEBHOOK_URL_RANSOMWARE_RESPONSE` | scripts/test-ransomware-response.sh |
| insider-threat-analyzer | 121716 | Insider Threat Analyzer | 11 | `WEBHOOK_URL_INSIDER_THREAT_ANALYZER` | scripts/test-insider-threat-analyzer.sh |
| cloud-misconfig-triage | 121717 | Cloud Misconfig Triage | 10 | `WEBHOOK_URL_CLOUD_MISCONFIG_TRIAGE` | scripts/test-cloud-misconfig-triage.sh |
| supply-chain-scanner | 121719 | Supply Chain Scanner | 11 | `WEBHOOK_URL_SUPPLY_CHAIN_SCANNER` | scripts/test-supply-chain-scanner.sh |

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
