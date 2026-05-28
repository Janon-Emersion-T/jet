from __future__ import annotations

import json
from pathlib import Path


RESILIENCE_DIR = Path("storage/resilience")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def autonomous_retry_engine() -> str:
    jobs = _list_entries(RESILIENCE_DIR / "retries.json", "jobs")
    retrying = [item for item in jobs if isinstance(item, dict) and int(item.get("retries", 0) or 0) > 0]
    capped = [item for item in jobs if isinstance(item, dict) and bool(item.get("cap_reached", False))]
    return "\n".join(
        [
            "AUTONOMOUS RETRY ENGINE - PHASE 511",
            "Mode: retry-policy overview.",
            f"Tracked jobs: {len(jobs)}",
            f"Jobs with retries: {len(retrying)}",
            f"Jobs at retry cap: {len(capped)}",
            "Safety: retries should preserve idempotency, backoff, and operator visibility before running unattended.",
        ]
    )


def failure_recovery_orchestration() -> str:
    incidents = _list_entries(RESILIENCE_DIR / "recovery.json", "incidents")
    recoverable = [item for item in incidents if isinstance(item, dict) and bool(item.get("recoverable", False))]
    runbooks = [item for item in incidents if isinstance(item, dict) and item.get("runbook")]
    return "\n".join(
        [
            "FAILURE RECOVERY ORCHESTRATION - PHASE 512",
            "Mode: failure-recovery overview.",
            f"Incidents tracked: {len(incidents)}",
            f"Recoverable incidents: {len(recoverable)}",
            f"Runbook-linked incidents: {len(runbooks)}",
            "Pattern: detect, isolate, recover, verify, and escalate only when automated recovery loses confidence.",
        ]
    )


def event_sourcing_architecture() -> str:
    aggregates = _list_entries(RESILIENCE_DIR / "event_sourcing.json", "aggregates")
    streams = _list_entries(RESILIENCE_DIR / "event_sourcing.json", "streams")
    snapshots = _list_entries(RESILIENCE_DIR / "event_sourcing.json", "snapshots")
    return "\n".join(
        [
            "EVENT SOURCING ARCHITECTURE - PHASE 513",
            "Mode: event-sourcing architecture overview.",
            f"Aggregates tracked: {len(aggregates)}",
            f"Event streams: {len(streams)}",
            f"Snapshots configured: {len(snapshots)}",
            "Architecture note: command, event, snapshot, and replay boundaries should stay explicit and testable.",
        ]
    )


def immutable_operational_audit_log() -> str:
    entries = _list_entries(RESILIENCE_DIR / "audit_log.json", "entries")
    signed = [item for item in entries if isinstance(item, dict) and bool(item.get("signed", False))]
    append_only = _safe_json(RESILIENCE_DIR / "audit_log.json", {}).get("append_only", False)
    return "\n".join(
        [
            "IMMUTABLE OPERATIONAL AUDIT LOG - PHASE 514",
            "Mode: audit-log integrity overview.",
            f"Entries tracked: {len(entries)}",
            f"Signed entries: {len(signed)}",
            f"Append-only flag: {'YES' if append_only else 'NO'}",
            "Rule: audit events should be append-only, attributable, replayable, and externally inspectable.",
        ]
    )


def ai_decision_replay_engine() -> str:
    decisions = _list_entries(RESILIENCE_DIR / "decision_replay.json", "decisions")
    replayable = [item for item in decisions if isinstance(item, dict) and bool(item.get("replayable", False))]
    divergences = [item for item in decisions if isinstance(item, dict) and bool(item.get("diverged", False))]
    return "\n".join(
        [
            "AI DECISION REPLAY ENGINE - PHASE 515",
            "Mode: decision-replay overview.",
            f"Decisions tracked: {len(decisions)}",
            f"Replayable decisions: {len(replayable)}",
            f"Divergent replays: {len(divergences)}",
            "Purpose: compare original context, policy, and outcome against later replays to spot drift before it becomes policy debt.",
        ]
    )
