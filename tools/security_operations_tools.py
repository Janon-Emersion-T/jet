from __future__ import annotations

import json
from pathlib import Path


SECURITY_OPS_DIR = Path("storage/security_ops")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_forensic_investigation_assistant() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "forensics.json", {})
    cases = payload.get("cases", []) if isinstance(payload, dict) else []
    preserved = [item for item in cases if isinstance(item, dict) and bool(item.get("evidence_preserved", False))]
    active = [item for item in cases if isinstance(item, dict) and item.get("status") == "active"]
    return _overview(
        "AI FORENSIC INVESTIGATION ASSISTANT - PHASE 536",
        "forensic-investigation overview",
        [
            f"Cases tracked: {len(cases)}",
            f"Active cases: {len(active)}",
            f"Evidence-preserved cases: {len(preserved)}",
        ],
        "Guardrail: forensic automation should preserve chain of custody, evidence integrity, and investigator review before drawing conclusions.",
    )


def autonomous_incident_containment() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "incident_containment.json", {})
    actions = payload.get("actions", []) if isinstance(payload, dict) else []
    automatic = [item for item in actions if isinstance(item, dict) and item.get("mode") == "automatic"]
    isolated = [item for item in actions if isinstance(item, dict) and item.get("result") == "isolated"]
    return _overview(
        "AUTONOMOUS INCIDENT CONTAINMENT - PHASE 537",
        "incident-containment overview",
        [
            f"Containment actions: {len(actions)}",
            f"Automatic actions: {len(automatic)}",
            f"Isolated assets: {len(isolated)}",
        ],
        "Guardrail: containment should prefer reversible isolation, narrow blast-radius reduction, and operator confirmation for high-impact actions.",
    )


def predictive_infrastructure_maintenance() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "predictive_maintenance.json", {})
    assets = payload.get("assets", []) if isinstance(payload, dict) else []
    at_risk = [item for item in assets if isinstance(item, dict) and item.get("risk") == "high"]
    scheduled = [item for item in assets if isinstance(item, dict) and bool(item.get("maintenance_scheduled", False))]
    return _overview(
        "PREDICTIVE INFRASTRUCTURE MAINTENANCE - PHASE 538",
        "predictive-maintenance overview",
        [
            f"Assets tracked: {len(assets)}",
            f"High-risk assets: {len(at_risk)}",
            f"Scheduled interventions: {len(scheduled)}",
        ],
        "Guardrail: maintenance prediction should favor service continuity, clear evidence, and planned windows before forcing disruption.",
    )


def ai_soc_dashboard() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "soc_dashboard.json", {})
    alerts = payload.get("alerts", []) if isinstance(payload, dict) else []
    open_alerts = [item for item in alerts if isinstance(item, dict) and item.get("status") == "open"]
    critical = [item for item in alerts if isinstance(item, dict) and item.get("severity") == "critical"]
    return _overview(
        "AI SOC DASHBOARD - PHASE 539",
        "soc-dashboard overview",
        [
            f"Alerts tracked: {len(alerts)}",
            f"Open alerts: {len(open_alerts)}",
            f"Critical alerts: {len(critical)}",
        ],
        "Guardrail: SOC summaries should elevate high-confidence threats, operational context, and response state before escalating urgency.",
    )


def ai_penetration_testing_sandbox() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "pentest_sandbox.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    safe = [item for item in scenarios if isinstance(item, dict) and bool(item.get("isolated", False))]
    completed = [item for item in scenarios if isinstance(item, dict) and item.get("status") == "completed"]
    return _overview(
        "AI PENETRATION TESTING SANDBOX - PHASE 540",
        "penetration-sandbox overview",
        [
            f"Scenarios tracked: {len(scenarios)}",
            f"Isolated scenarios: {len(safe)}",
            f"Completed scenarios: {len(completed)}",
        ],
        "Guardrail: penetration testing should stay isolated, scoped, and non-production before offensive automation is permitted.",
    )


def red_team_simulation_engine() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "red_team.json", {})
    exercises = payload.get("exercises", []) if isinstance(payload, dict) else []
    adversarial = [item for item in exercises if isinstance(item, dict) and bool(item.get("adversarial_chain", False))]
    validated = [item for item in exercises if isinstance(item, dict) and item.get("status") == "validated"]
    return _overview(
        "RED-TEAM SIMULATION ENGINE - PHASE 541",
        "red-team overview",
        [
            f"Exercises tracked: {len(exercises)}",
            f"Adversarial-chain exercises: {len(adversarial)}",
            f"Validated exercises: {len(validated)}",
        ],
        "Guardrail: red-team simulations should remain permissioned, evidence-backed, and clearly separated from live production operations.",
    )


def blue_team_defense_assistant() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "blue_team.json", {})
    playbooks = payload.get("playbooks", []) if isinstance(payload, dict) else []
    tuned = [item for item in playbooks if isinstance(item, dict) and bool(item.get("tuned", False))]
    automated = [item for item in playbooks if isinstance(item, dict) and bool(item.get("automated", False))]
    return _overview(
        "BLUE-TEAM DEFENSE ASSISTANT - PHASE 542",
        "blue-team overview",
        [
            f"Playbooks tracked: {len(playbooks)}",
            f"Tuned playbooks: {len(tuned)}",
            f"Automated playbooks: {len(automated)}",
        ],
        "Guardrail: defensive automation should reinforce detection quality, reviewability, and containment safety before expanding authority.",
    )


def compliance_monitoring_framework() -> str:
    payload = _safe_json(SECURITY_OPS_DIR / "compliance_monitoring.json", {})
    checks = payload.get("checks", []) if isinstance(payload, dict) else []
    failing = [item for item in checks if isinstance(item, dict) and item.get("status") == "failing"]
    continuous = [item for item in checks if isinstance(item, dict) and bool(item.get("continuous", False))]
    return _overview(
        "COMPLIANCE MONITORING FRAMEWORK - PHASE 543",
        "compliance-monitoring overview",
        [
            f"Checks tracked: {len(checks)}",
            f"Failing checks: {len(failing)}",
            f"Continuous checks: {len(continuous)}",
        ],
        "Guardrail: compliance monitoring should prefer durable evidence, change awareness, and reviewable exceptions before marking systems compliant.",
    )
