#!/usr/bin/env python3
"""Generate complex Tines story JSON exports (8+ actions, branching, HTTP enrichment)."""

from __future__ import annotations

import json
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "exports" / "workflows"
PAYLOAD_DIR = ROOT / "scripts" / "payloads"
SCRIPT_DIR = ROOT / "scripts"
TENANT_CLOUD = "cloud:487706a2b146ec0742f27d378235fd1a"
RECIPIENT = "user@applyready.dev"

SCHEMA = {
    "schema_version": 30,
    "standard_lib_version": 92,
    "action_runtime_version": 83,
}


def new_guid() -> str:
    return uuid.uuid4().hex


def new_secret() -> str:
    return secrets.token_hex(16)


def agent_shell(
    agent_type: str,
    name: str,
    guid: str,
    story_guid: str,
    options: dict[str, Any],
    *,
    schedule: list | None = None,
) -> dict[str, Any]:
    origin = f"{TENANT_CLOUD}:{story_guid}"
    base: dict[str, Any] = {
        "type": agent_type,
        "name": name,
        "disabled": False,
        "description": None,
        "guid": guid,
        "origin_story_identifier": origin,
        "options": options,
        "reporting": {"time_saved_value": 0, "time_saved_unit": "minutes"},
        "monitoring": {
            "monitor_all_events": False,
            "monitor_failures": False,
            "monitor_no_events_emitted": None,
        },
        "template": {
            "created_from_template_guid": None,
            "created_from_template_version": None,
            "template_tags": [],
        },
        "width": None,
    }
    if agent_type != "Agents::WebhookAgent":
        base["schedule"] = schedule
    return base


def story_footer(story_guid: str, diagram_layout: dict[str, list[int]]) -> dict[str, Any]:
    return {
        "diagram_notes": [],
        "story_library_metadata": {},
        "monitor_failures": False,
        "synchronous_webhooks_enabled": False,
        "integrations": [],
        "sections": [],
        "parent_only_send_to_story": False,
        "send_to_story_timeout_enabled": False,
        "send_to_story_timeout_duration_seconds": None,
        "keep_events_for": 86400,
        "reporting_status": True,
        "send_to_story_enabled": False,
        "entry_agent_guid": None,
        "exit_agent_guids": [],
        "api_entry_action_guids": [],
        "api_exit_action_guids": [],
        "send_to_story_access": None,
        "send_to_story_access_source": 0,
        "send_to_story_skill_use_requires_confirmation": True,
        "pages": [],
        "tags": [],
        "time_saved_unit": "minutes",
        "time_saved_value": 0,
        "origin_story_identifier": f"{TENANT_CLOUD}:{story_guid}",
        "recipients": [RECIPIENT],
        "integration_product": None,
        "integration_vendor": None,
        "llm_product_instructions": "",
        "start_reference": None,
        "app_endpoints": [],
        "send_to_stories": [],
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "diagram_layout": json.dumps(diagram_layout),
    }


def build_advanced_triage_story(spec: dict[str, Any]) -> dict[str, Any]:
    """11-action nested triage pattern (mirrors alert-triage-advanced topology)."""
    story_guid = new_guid()
    webhook_name = spec["webhook_name"]
    path = spec["path"]
    entity = spec.get("entity", "alert")
    source_token = spec.get("source_token", "firewall")
    http_url = spec.get("http_url", "https://httpbin.org/post")

    g = [new_guid() for _ in range(11)]

    agents = [
        agent_shell(
            "Agents::WebhookAgent",
            webhook_name,
            g[0],
            story_guid,
            {"path": path, "secret": new_secret(), "verbs": "get,post"},
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "normalize_event",
            g[1],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    f"{entity}_id": f"<<{webhook_name}.body.{entity}_id>>-<<{webhook_name}.id>>",
                    "severity": f"<<{webhook_name}.body.severity>>",
                    "source": f"<<{webhook_name}.body.source>>",
                    "received_at": f"<<{webhook_name}.date>>",
                    "workflow": path,
                    "normalized": True,
                },
            },
        ),
        agent_shell(
            "Agents::TriggerAgent",
            "check_severity",
            g[2],
            story_guid,
            {
                "rules": [
                    {"type": "field==value", "value": "high", "path": "<<normalize_event.severity>>"},
                    {"type": "field==value", "value": "critical", "path": "<<normalize_event.severity>>"},
                ],
                "must_match": 1,
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "escalate_high",
            g[3],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "escalate",
                    "priority": "P1",
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "severity": "<<normalize_event.severity>>",
                    "source": "<<normalize_event.source>>",
                },
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "log_standard",
            g[4],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "log",
                    "priority": "P4",
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "severity": "<<normalize_event.severity>>",
                },
            },
        ),
        agent_shell(
            "Agents::TriggerAgent",
            "check_critical",
            g[5],
            story_guid,
            {
                "rules": [
                    {"type": "field==value", "value": "critical", "path": "<<normalize_event.severity>>"},
                ],
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "escalate_critical",
            g[6],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "escalate",
                    "priority": "P0",
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "severity": "critical",
                },
            },
        ),
        agent_shell(
            "Agents::TriggerAgent",
            "check_source",
            g[7],
            story_guid,
            {
                "rules": [
                    {
                        "type": "field==value",
                        "value": source_token,
                        "path": "<<normalize_event.source>>",
                    },
                ],
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "audit_source_log",
            g[8],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "audit",
                    "source": source_token,
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "priority": "P3",
                },
            },
        ),
        agent_shell(
            "Agents::HTTPRequestAgent",
            "enrich_critical",
            g[9],
            story_guid,
            {
                "url": http_url,
                "content_type": "application_json",
                "method": "post",
                "payload": {
                    "priority": "P0",
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "stage": "critical_enrichment",
                },
                "emit_failure_event": False,
            },
        ),
        agent_shell(
            "Agents::HTTPRequestAgent",
            "enrich_high",
            g[10],
            story_guid,
            {
                "url": http_url,
                "content_type": "application_json",
                "method": "post",
                "payload": {
                    "priority": "P1",
                    f"{entity}_id": f"<<normalize_event.{entity}_id>>",
                    "stage": "high_enrichment",
                },
                "emit_failure_event": False,
            },
        ),
    ]

    links = [
        {"source": 0, "receiver": 1},
        {"source": 1, "receiver": 2},
        {"source": 2, "receiver": 5},
        {"source": 2, "receiver": 7, "link_type": "secondary"},
        {"source": 3, "receiver": 10},
        {"source": 5, "receiver": 3, "link_type": "secondary"},
        {"source": 5, "receiver": 6},
        {"source": 6, "receiver": 9},
        {"source": 7, "receiver": 4, "link_type": "secondary"},
        {"source": 7, "receiver": 8},
    ]

    layout = {guid: [105 + (i % 3) * 345, 105 + (i // 3) * 180] for i, guid in enumerate(g)}

    story = {
        **SCHEMA,
        "name": spec["name"],
        "description": spec.get("description"),
        "guid": story_guid,
        "slug": spec["slug"],
        "agents": agents,
        "links": links,
        **story_footer(story_guid, layout),
    }
    return story


def build_enriched_pipeline_story(spec: dict[str, Any]) -> dict[str, Any]:
    """10-action pipeline: webhook → normalize → dedup → throttle → HTTP → condition → branches."""
    story_guid = new_guid()
    webhook_name = spec["webhook_name"]
    path = spec["path"]
    http_url = spec.get("http_url", "https://httpbin.org/post")
    dedup_key = spec.get("dedup_key", "event_id")

    g = [new_guid() for _ in range(10)]

    agents = [
        agent_shell(
            "Agents::WebhookAgent",
            webhook_name,
            g[0],
            story_guid,
            {"path": path, "secret": new_secret(), "verbs": "get,post"},
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "normalize_input",
            g[1],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "event_id": f"<<{webhook_name}.body.{dedup_key}>>",
                    "severity": f"<<{webhook_name}.body.severity>>",
                    "category": f"<<{webhook_name}.body.category>>",
                    "received_at": f"<<{webhook_name}.date>>",
                },
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "dedupe_window",
            g[2],
            story_guid,
            {
                "mode": "deduplicate",
                "loop": False,
                "payload": {},
                "path": "<<normalize_input.event_id>>",
                "period": 300,
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "rate_limit",
            g[3],
            story_guid,
            {"mode": "throttle", "loop": False, "payload": {}, "capacity": 5, "interval": "minute"},
        ),
        agent_shell(
            "Agents::HTTPRequestAgent",
            "external_lookup",
            g[4],
            story_guid,
            {
                "url": http_url,
                "content_type": "application_json",
                "method": "post",
                "payload": {
                    "event_id": "<<normalize_input.event_id>>",
                    "category": "<<normalize_input.category>>",
                },
                "emit_failure_event": False,
            },
        ),
        agent_shell(
            "Agents::TriggerAgent",
            "check_severity",
            g[5],
            story_guid,
            {
                "rules": [
                    {"type": "field==value", "value": "high", "path": "<<normalize_input.severity>>"},
                    {"type": "field==value", "value": "critical", "path": "<<normalize_input.severity>>"},
                ],
                "must_match": 1,
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "delay_processing",
            g[6],
            story_guid,
            {"mode": "delay", "loop": False, "payload": {}, "seconds": 3},
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "escalate",
            g[7],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "escalate",
                    "event_id": "<<normalize_input.event_id>>",
                    "http_status": "<<external_lookup.status>>",
                },
            },
        ),
        agent_shell(
            "Agents::EventTransformationAgent",
            "standard_log",
            g[8],
            story_guid,
            {
                "mode": "message_only",
                "loop": False,
                "payload": {
                    "action": "log",
                    "event_id": "<<normalize_input.event_id>>",
                    "http_status": "<<external_lookup.status>>",
                },
            },
        ),
        agent_shell(
            "Agents::TriggerAgent",
            "check_http_ok",
            g[9],
            story_guid,
            {
                "rules": [{"type": "field==value", "value": "200", "path": "<<external_lookup.status>>"}],
            },
        ),
    ]

    links = [
        {"source": 0, "receiver": 1},
        {"source": 1, "receiver": 2},
        {"source": 2, "receiver": 3},
        {"source": 3, "receiver": 4},
        {"source": 4, "receiver": 5},
        {"source": 5, "receiver": 6},
        {"source": 6, "receiver": 9},
        {"source": 9, "receiver": 7},
        {"source": 9, "receiver": 8, "link_type": "secondary"},
    ]

    layout = {guid: [105 + (i % 4) * 270, 105 + (i // 4) * 165] for i, guid in enumerate(g)}

    return {
        **SCHEMA,
        "name": spec["name"],
        "description": spec.get("description"),
        "guid": story_guid,
        "slug": spec["slug"],
        "agents": agents,
        "links": links,
        **story_footer(story_guid, layout),
    }


WORKFLOWS: list[dict[str, Any]] = [
    {
        "id": "email-ticket-router",
        "pattern": "advanced",
        "name": "Email Ticket Router",
        "slug": "email_ticket_router",
        "webhook_name": "inbound_email",
        "path": "email-ticket-router",
        "entity": "ticket",
        "source_token": "urgent",
        "description": "Email-shaped webhook ingress with priority routing and enrichment.",
    },
    {
        "id": "manual-playbook-runner",
        "pattern": "pipeline",
        "name": "Manual Playbook Runner",
        "slug": "manual_playbook_runner",
        "webhook_name": "run_playbook",
        "path": "manual-playbook-runner",
        "dedup_key": "playbook_id",
        "description": "Simulated manual playbook with dedup, throttle, HTTP, and retry branch.",
    },
    {
        "id": "batch-etl-pipeline",
        "pattern": "pipeline",
        "name": "Batch ETL Pipeline",
        "slug": "batch_etl_pipeline",
        "webhook_name": "receive_batch",
        "path": "batch-etl-pipeline",
        "dedup_key": "batch_id",
        "description": "Batch ingest with rate limiting and enrichment gate.",
    },
    {
        "id": "case-management-stub",
        "pattern": "advanced",
        "name": "Case Management Stub",
        "slug": "case_management_stub",
        "webhook_name": "open_case",
        "path": "case-management-stub",
        "entity": "case",
        "source_token": "legal",
        "description": "Case record triage with nested severity and audit paths.",
    },
    {
        "id": "slack-notify-stub",
        "pattern": "advanced",
        "name": "Slack Notify Stub",
        "slug": "slack_notify_stub",
        "webhook_name": "receive_alert",
        "path": "slack-notify-stub",
        "entity": "alert",
        "source_token": "slack",
        "http_url": "https://httpbin.org/post",
        "description": "Slack-shaped notification stub with HTTP post placeholder.",
    },
    {
        "id": "servicenow-incident-stub",
        "pattern": "advanced",
        "name": "ServiceNow Incident Stub",
        "slug": "servicenow_incident_stub",
        "webhook_name": "receive_incident",
        "path": "servicenow-incident-stub",
        "entity": "incident",
        "source_token": "servicenow",
        "description": "ITSM incident mapping with P0/P1 routing and enrichment.",
    },
    {
        "id": "ai-summary-stub",
        "pattern": "pipeline",
        "name": "AI Summary Stub",
        "slug": "ai_summary_stub",
        "webhook_name": "receive_alert",
        "path": "ai-summary-stub",
        "dedup_key": "alert_id",
        "description": "AI summarizer placeholder pipeline with throttle and HTTP echo.",
    },
    {
        "id": "phishing-analyzer",
        "pattern": "advanced",
        "name": "Phishing Analyzer",
        "slug": "phishing_analyzer",
        "webhook_name": "receive_email",
        "path": "phishing-analyzer",
        "entity": "message",
        "source_token": "phishing",
        "description": "Phishing email analysis with URL reputation branch.",
    },
    {
        "id": "malware-hash-triage",
        "pattern": "pipeline",
        "name": "Malware Hash Triage",
        "slug": "malware_hash_triage",
        "webhook_name": "submit_hash",
        "path": "malware-hash-triage",
        "dedup_key": "hash",
        "description": "Hash submission with dedup, lookup, and escalation.",
    },
    {
        "id": "user-risk-engine",
        "pattern": "advanced",
        "name": "User Risk Engine",
        "slug": "user_risk_engine",
        "webhook_name": "user_event",
        "path": "user-risk-engine",
        "entity": "user",
        "source_token": "vpn",
        "description": "User risk scoring with geo and severity gates.",
    },
    {
        "id": "incident-correlator",
        "pattern": "pipeline",
        "name": "Incident Correlator",
        "slug": "incident_correlator",
        "webhook_name": "correlate_signal",
        "path": "incident-correlator",
        "dedup_key": "correlation_id",
        "description": "Multi-signal correlation with dedup and enrichment.",
    },
    {
        "id": "vulnerability-scorer",
        "pattern": "advanced",
        "name": "Vulnerability Scorer",
        "slug": "vulnerability_scorer",
        "webhook_name": "receive_finding",
        "path": "vulnerability-scorer",
        "entity": "finding",
        "source_token": "scanner",
        "description": "CVSS-style finding triage with critical path.",
    },
    {
        "id": "auth-anomaly-detector",
        "pattern": "pipeline",
        "name": "Auth Anomaly Detector",
        "slug": "auth_anomaly_detector",
        "webhook_name": "auth_event",
        "path": "auth-anomaly-detector",
        "dedup_key": "session_id",
        "description": "Authentication anomaly pipeline with delay and HTTP verify.",
    },
    {
        "id": "exfil-monitor",
        "pattern": "advanced",
        "name": "Exfil Monitor",
        "slug": "exfil_monitor",
        "webhook_name": "data_transfer",
        "path": "exfil-monitor",
        "entity": "transfer",
        "source_token": "sensitive",
        "description": "Data exfiltration volume and severity routing.",
    },
    {
        "id": "compliance-audit-chain",
        "pattern": "pipeline",
        "name": "Compliance Audit Chain",
        "slug": "compliance_audit_chain",
        "webhook_name": "audit_event",
        "path": "compliance-audit-chain",
        "dedup_key": "audit_id",
        "description": "Compliance event chain with throttle and HTTP audit log.",
    },
    {
        "id": "threat-intel-pipeline",
        "pattern": "advanced",
        "name": "Threat Intel Pipeline",
        "slug": "threat_intel_pipeline",
        "webhook_name": "intel_indicator",
        "path": "threat-intel-pipeline",
        "entity": "indicator",
        "source_token": "feed",
        "description": "IOC enrichment with nested severity routing.",
    },
    {
        "id": "ransomware-response",
        "pattern": "pipeline",
        "name": "Ransomware Response",
        "slug": "ransomware_response",
        "webhook_name": "ransomware_signal",
        "path": "ransomware-response",
        "dedup_key": "signal_id",
        "description": "Ransomware indicator response with immediate escalation path.",
    },
    {
        "id": "insider-threat-analyzer",
        "pattern": "advanced",
        "name": "Insider Threat Analyzer",
        "slug": "insider_threat_analyzer",
        "webhook_name": "insider_event",
        "path": "insider-threat-analyzer",
        "entity": "event",
        "source_token": "hr",
        "description": "Insider threat behavior scoring and audit branches.",
    },
    {
        "id": "cloud-misconfig-triage",
        "pattern": "pipeline",
        "name": "Cloud Misconfig Triage",
        "slug": "cloud_misconfig_triage",
        "webhook_name": "misconfig_alert",
        "path": "cloud-misconfig-triage",
        "dedup_key": "resource_id",
        "description": "Cloud misconfiguration finding pipeline with remediation gate.",
    },
    {
        "id": "supply-chain-scanner",
        "pattern": "advanced",
        "name": "Supply Chain Scanner",
        "slug": "supply_chain_scanner",
        "webhook_name": "package_alert",
        "path": "supply-chain-scanner",
        "entity": "package",
        "source_token": "registry",
        "description": "Supply chain package alert with CVE-style routing.",
    },
]


def env_var_name(workflow_id: str) -> str:
    return "WEBHOOK_URL_" + workflow_id.upper().replace("-", "_")


def default_payload(spec: dict[str, Any]) -> dict[str, Any]:
    wid = spec["id"]
    if spec.get("pattern") == "pipeline":
        key = spec.get("dedup_key", "event_id")
        return {
            key: f"demo-{wid}-001",
            "severity": "high",
            "category": wid,
        }
    entity = spec.get("entity", "alert")
    return {
        f"{entity}_id": f"demo-{wid}-001",
        "severity": "high",
        "source": spec.get("source_token", "firewall"),
        "note": f"Test payload for {wid}",
    }


def write_test_script(workflow_id: str, env_var: str) -> None:
    script_path = SCRIPT_DIR / f"test-{workflow_id}.sh"
    content = f"""#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
exec "$SCRIPT_DIR/send-test-webhook-env.sh" {env_var} "$SCRIPT_DIR/payloads/{workflow_id}.json"
"""
    script_path.write_text(content)
    script_path.chmod(0o755)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PAYLOAD_DIR.mkdir(parents=True, exist_ok=True)

    catalog_entries: list[dict[str, str]] = []

    for spec in WORKFLOWS:
        wf_id = spec["id"]
        if spec["pattern"] == "advanced":
            story = build_advanced_triage_story(spec)
        else:
            story = build_enriched_pipeline_story(spec)

        out_file = OUT_DIR / f"{wf_id}.json"
        out_file.write_text(json.dumps(story, indent=2) + "\n")

        payload_file = PAYLOAD_DIR / f"{wf_id}.json"
        payload_file.write_text(json.dumps(default_payload(spec), indent=2) + "\n")

        env_var = env_var_name(wf_id)
        write_test_script(wf_id, env_var)

        action_count = len(story["agents"])
        catalog_entries.append(
            {
                "id": wf_id,
                "name": spec["name"],
                "file": f"workflows/{wf_id}.json",
                "actions": str(action_count),
                "env": env_var,
            }
        )
        print(f"  {wf_id}: {action_count} actions -> {out_file.name}")

    manifest = ROOT / "exports" / "generated-workflows.json"
    manifest.write_text(json.dumps(catalog_entries, indent=2) + "\n")
    print(f"\nWrote {len(WORKFLOWS)} workflows. Manifest: {manifest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
