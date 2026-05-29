from __future__ import annotations

import json
from pathlib import Path


SERVER_OPS_GOVERNANCE_DIR = Path("storage/server_ops_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(SERVER_OPS_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def multi_app_server_inventory() -> str:
    return _render("MULTI-APP SERVER INVENTORY - PHASE 1611", "multi-app-inventory overview", "multi_app_server_inventory.json", "app_nodes", "tracked", "unknown", "App nodes tracked", "Tracked nodes", "Unknown nodes", "Guardrail: server inventory should preserve environment boundaries, source timestamps, and avoid assuming completeness from partial scans.")


def domain_to_server_mapping_brain() -> str:
    return _render("DOMAIN-TO-SERVER MAPPING BRAIN - PHASE 1612", "domain-server-mapping overview", "domain_server_mapping.json", "domain_maps", "mapped", "orphaned", "Domain maps tracked", "Mapped domains", "Orphaned domains", "Guardrail: mapping analysis should preserve DNS/hosting uncertainty and verify stale references before recommending changes.")


def ssl_renewal_intelligence() -> str:
    return _render("SSL RENEWAL INTELLIGENCE - PHASE 1613", "ssl-renewal overview", "ssl_renewal_intelligence.json", "certificate_paths", "covered", "expiring", "Certificate paths tracked", "Covered certificates", "Expiring certificates", "Guardrail: SSL renewal guidance should preserve exact expiry evidence, provider context, and safe renewal sequencing.")


def dns_propagation_monitor() -> str:
    return _render("DNS PROPAGATION MONITOR - PHASE 1614", "dns-propagation overview", "dns_propagation_monitor.json", "dns_checks", "settled", "lagging", "DNS checks tracked", "Settled checks", "Lagging checks", "Guardrail: DNS monitoring should preserve TTL awareness, resolver variance, and avoid premature conclusions from partial propagation.")


def mail_deliverability_command_center() -> str:
    return _render("MAIL DELIVERABILITY COMMAND CENTER - PHASE 1615", "mail-deliverability overview", "mail_deliverability_command.json", "deliverability_signals", "healthy", "failing", "Deliverability signals tracked", "Healthy signals", "Failing signals", "Guardrail: deliverability analysis should preserve header evidence, mailbox-provider nuance, and avoid overstating root cause from one signal.")


def queue_failure_analyst() -> str:
    return _render("QUEUE FAILURE ANALYST - PHASE 1616", "queue-failure overview", "queue_failure_analyst.json", "queue_events", "healthy", "failing", "Queue events tracked", "Healthy events", "Failing events", "Guardrail: queue analysis should preserve error provenance, retry-context nuance, and separate symptom from root cause.")


def cron_job_governor() -> str:
    return _render("CRON JOB GOVERNOR - PHASE 1617", "cron-job overview", "cron_job_governor.json", "cron_jobs", "tracked", "misfiring", "Cron jobs tracked", "Tracked jobs", "Misfiring jobs", "Guardrail: cron governance should preserve host-specific schedules, time-zone context, and safe change-control for critical jobs.")


def storage_permission_fixer() -> str:
    return _render("STORAGE PERMISSION FIXER - PHASE 1618", "storage-permission overview", "storage_permission_fixer.json", "permission_paths", "correct", "broken", "Permission paths tracked", "Correct paths", "Broken paths", "Guardrail: permission guidance should preserve least privilege and avoid blanket chmod/chown recommendations without scope context.")


def laravel_route_health_monitor() -> str:
    return _render("LARAVEL ROUTE-HEALTH MONITOR - PHASE 1619", "route-health overview", "laravel_route_health.json", "route_checks", "healthy", "broken", "Route checks tracked", "Healthy routes", "Broken routes", "Guardrail: route-health analysis should preserve environment differences and show exact failing endpoints or mismatches before inference.")


def cache_invalidation_advisor() -> str:
    return _render("CACHE INVALIDATION ADVISOR - PHASE 1620", "cache-invalidation overview", "cache_invalidation_advisor.json", "cache_paths", "clear", "stale", "Cache paths tracked", "Clear paths", "Stale paths", "Guardrail: cache advice should preserve blast-radius awareness and avoid broad invalidation without evidence of stale state.")
