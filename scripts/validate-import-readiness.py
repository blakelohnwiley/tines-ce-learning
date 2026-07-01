#!/usr/bin/env python3
"""Validate generated Tines story JSON exports for import readiness."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "exports" / "workflows"
GENERATED = ROOT / "exports" / "generated-workflows.json"

REFERENCE_EXPORTS = (
    "alert-triage-advanced.json",
    "manual-playbook-runner.json",
    "dedup-alerts.json",
    "throttle-demo.json",
    "delay-retry.json",
    "ip-enrichment.json",
)

KNOWN_AGENT_TYPES = {
    "Agents::WebhookAgent",
    "Agents::EventTransformationAgent",
    "Agents::TriggerAgent",
    "Agents::HTTPRequestAgent",
}

MODE_OPTIONS: dict[str, set[str]] = {
    "message_only": {"mode", "loop", "payload"},
    "deduplicate": {"mode", "loop", "payload", "path", "period"},
    "throttle": {"mode", "loop", "payload", "capacity", "interval"},
    "delay": {"mode", "loop", "payload", "seconds"},
}

LIQUID_REF = re.compile(r"<<([a-zA-Z0-9_]+)\.")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def link_signature(links: list[dict]) -> list[tuple]:
    return sorted((l["source"], l["receiver"], l.get("link_type")) for l in links)


def agent_type_sequence(agents: list[dict]) -> list[str]:
    return [a["type"].replace("Agents::", "") for a in agents]


def validate_generated_workflow(
    wf_id: str,
    data: dict,
    *,
    ref_adv: dict,
    ref_pipe: dict,
    refs: dict[str, dict],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    required_top = set()
    for ref in refs.values():
        required_top |= set(ref.keys())
    required_top -= {"icon", "description"}

    missing_top = required_top - set(data.keys())
    if missing_top:
        errors.append(f"missing top-level keys: {sorted(missing_top)}")

    agents = data.get("agents", [])
    if not agents:
        errors.append("no agents")
        return errors, warnings

    names = {a["name"] for a in agents}
    n = len(agents)

    if agents[0]["type"] != "Agents::WebhookAgent":
        errors.append("first agent is not WebhookAgent")

    wh_path = agents[0].get("options", {}).get("path")
    if wh_path != wf_id:
        errors.append(f"webhook path {wh_path!r} != workflow id {wf_id!r}")

    if len(data.get("guid", "")) != 32:
        errors.append("story guid is not 32 hex chars")

    slug = data.get("slug", "")
    if not re.fullmatch(r"[a-z0-9_]+", slug):
        errors.append(f"invalid slug {slug!r}")

    story_guid = data["guid"]
    for i, agent in enumerate(agents):
        if agent["type"] not in KNOWN_AGENT_TYPES:
            errors.append(f"agent[{i}] unknown type {agent['type']!r}")
        if len(agent.get("guid", "")) != 32:
            errors.append(f"agent[{i}] guid is not 32 hex chars")

        expected_origin = f"cloud:487706a2b146ec0742f27d378235fd1a:{story_guid}"
        if agent.get("origin_story_identifier") != expected_origin:
            errors.append(f"agent[{i}] origin_story_identifier mismatch")

        ref_same = next(
            (a for ref in refs.values() for a in ref["agents"] if a["type"] == agent["type"]),
            None,
        )
        if ref_same:
            missing_keys = set(ref_same.keys()) - set(agent.keys())
            if missing_keys:
                errors.append(f"{agent['name']}: missing agent keys {sorted(missing_keys)}")

        options = agent.get("options", {})
        if agent["type"] == "Agents::EventTransformationAgent":
            mode = options.get("mode")
            required = MODE_OPTIONS.get(mode or "")
            if not required:
                errors.append(f"{agent['name']}: unknown mode {mode!r}")
            else:
                missing_opts = required - set(options.keys())
                if missing_opts:
                    errors.append(
                        f"{agent['name']}: mode {mode} missing options {sorted(missing_opts)}"
                    )
        elif agent["type"] == "Agents::TriggerAgent":
            rules = options.get("rules", [])
            if not rules:
                errors.append(f"{agent['name']}: trigger has no rules")
            for rule in rules:
                if rule.get("type") != "field==value":
                    errors.append(f"{agent['name']}: unsupported rule type {rule.get('type')!r}")
            if len(rules) > 1 and "must_match" not in options:
                warnings.append(f"{agent['name']}: multi-rule trigger without must_match")
        elif agent["type"] == "Agents::HTTPRequestAgent":
            for key in ("url", "method", "content_type", "payload"):
                if key not in options:
                    errors.append(f"{agent['name']}: missing options.{key}")

        for match in LIQUID_REF.findall(json.dumps(agent)):
            if match not in names:
                errors.append(f"{agent['name']}: liquid reference to unknown agent {match!r}")

    links = data.get("links", [])
    for j, link in enumerate(links):
        source, receiver = link.get("source"), link.get("receiver")
        if source is None or receiver is None:
            errors.append(f"link[{j}] missing source/receiver")
            continue
        if not (0 <= source < n and 0 <= receiver < n):
            errors.append(f"link[{j}] index out of range (agents={n})")
        link_type = link.get("link_type")
        if link_type is not None and link_type not in ("primary", "secondary"):
            errors.append(f"link[{j}] invalid link_type {link_type!r}")

    graph: dict[int, list[int]] = defaultdict(list)
    for link in links:
        graph[link["source"]].append(link["receiver"])
    seen: set[int] = set()
    stack = [0]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(graph[node])
    unreachable = set(range(n)) - seen
    if unreachable:
        errors.append(f"unreachable agents from webhook: {sorted(unreachable)}")

    try:
        layout = json.loads(data.get("diagram_layout", "{}"))
    except json.JSONDecodeError:
        errors.append("diagram_layout is not valid JSON")
    else:
        if set(layout) != {a["guid"] for a in agents}:
            errors.append("diagram_layout guids do not match agent guids")

    if n == 11:
        if link_signature(links) != link_signature(ref_adv["links"]):
            errors.append("link topology differs from alert-triage-advanced reference")
        if agent_type_sequence(agents) != agent_type_sequence(ref_adv["agents"]):
            errors.append("agent type sequence differs from alert-triage-advanced reference")
    elif n == 10:
        if link_signature(links) != link_signature(ref_pipe["links"]):
            errors.append("link topology differs from manual-playbook-runner reference")
    elif n < 8:
        errors.append(f"only {n} actions (expected >= 8)")

    return errors, warnings


def validate_uniqueness(all_workflows: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    slugs: dict[str, str] = {}
    story_guids: dict[str, str] = {}
    paths: dict[str, str] = {}
    agent_guids: dict[str, str] = {}

    for wf_id, data in all_workflows.items():
        slug = data["slug"]
        if slug in slugs:
            errors.append(f"{wf_id}: duplicate slug {slug!r} (also {slugs[slug]})")
        slugs[slug] = wf_id

        story_guid = data["guid"]
        if story_guid in story_guids:
            errors.append(
                f"{wf_id}: duplicate story guid (also {story_guids[story_guid]})"
            )
        story_guids[story_guid] = wf_id

        if data["agents"][0]["type"] == "Agents::WebhookAgent":
            path = data["agents"][0]["options"]["path"]
            if path in paths:
                errors.append(
                    f"{wf_id}: duplicate webhook path {path!r} (also {paths[path]})"
                )
            paths[path] = wf_id

        for agent in data["agents"]:
            guid = agent["guid"]
            if guid in agent_guids:
                errors.append(
                    f"{wf_id}: duplicate agent guid {guid} (also {agent_guids[guid]})"
                )
            agent_guids[guid] = wf_id

    return errors


def main() -> int:
    generated_ids = {entry["id"] for entry in load_json(GENERATED)}
    refs = {name: load_json(WORKFLOWS / name) for name in REFERENCE_EXPORTS}
    ref_adv = refs["alert-triage-advanced.json"]
    ref_pipe = refs["manual-playbook-runner.json"]

    all_workflows = {
        path.stem: load_json(path) for path in sorted(WORKFLOWS.glob("*.json"))
    }

    total_errors = 0
    total_warnings = 0
    passed: list[str] = []

    for wf_id in sorted(generated_ids):
        path = WORKFLOWS / f"{wf_id}.json"
        if not path.exists():
            print(f"FAIL: missing {path}", file=sys.stderr)
            total_errors += 1
            continue

        errors, warnings = validate_generated_workflow(
            wf_id,
            all_workflows[wf_id],
            ref_adv=ref_adv,
            ref_pipe=ref_pipe,
            refs=refs,
        )
        for message in errors:
            print(f"FAIL: {wf_id}: {message}", file=sys.stderr)
        for message in warnings:
            print(f"WARN: {wf_id}: {message}", file=sys.stderr)

        total_errors += len(errors)
        total_warnings += len(warnings)
        if not errors:
            passed.append(wf_id)

    for message in validate_uniqueness(all_workflows):
        print(f"FAIL: {message}", file=sys.stderr)
        total_errors += 1

    adv_count = sum(1 for wf_id in generated_ids if len(all_workflows[wf_id]["agents"]) == 11)
    pipe_count = sum(1 for wf_id in generated_ids if len(all_workflows[wf_id]["agents"]) == 10)

    print(f"Import readiness: {len(passed)}/{len(generated_ids)} generated workflows passed")
    print(f"Patterns: {adv_count} advanced-triage (11 actions), {pipe_count} enriched-pipeline (10 actions)")
    print(f"Errors: {total_errors}, Warnings: {total_warnings}")

    if total_errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
