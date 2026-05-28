from __future__ import annotations

import json
from pathlib import Path


RUNTIME_SECURITY_DIR = Path("storage/runtime_security")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def runtime_threat_analysis() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "runtime_threats.json", {})
    findings = payload.get("findings", []) if isinstance(payload, dict) else []
    critical = [item for item in findings if isinstance(item, dict) and item.get("severity") == "critical"]
    mitigated = [item for item in findings if isinstance(item, dict) and item.get("status") == "mitigated"]
    return "\n".join(
        [
            "RUNTIME THREAT ANALYSIS - PHASE 531",
            "Mode: runtime-threat overview.",
            f"Threat findings: {len(findings)}",
            f"Critical findings: {len(critical)}",
            f"Mitigated findings: {len(mitigated)}",
            "Guardrail: runtime threat scoring should privilege high-confidence behavior, blast radius, and containment state over noisy heuristics.",
        ]
    )


def ai_intrusion_detection() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "intrusion_detection.json", {})
    detections = payload.get("detections", []) if isinstance(payload, dict) else []
    confirmed = [item for item in detections if isinstance(item, dict) and item.get("confidence") == "high"]
    lateral = [item for item in detections if isinstance(item, dict) and bool(item.get("lateral_movement", False))]
    return "\n".join(
        [
            "AI INTRUSION DETECTION - PHASE 532",
            "Mode: intrusion-detection overview.",
            f"Detections tracked: {len(detections)}",
            f"High-confidence detections: {len(confirmed)}",
            f"Lateral-movement detections: {len(lateral)}",
            "Guardrail: intrusion detection should correlate privilege shifts, movement patterns, and confidence signals before triggering escalation.",
        ]
    )


def real_time_anomaly_detection() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "anomaly_detection.json", {})
    anomalies = payload.get("anomalies", []) if isinstance(payload, dict) else []
    active = [item for item in anomalies if isinstance(item, dict) and item.get("status") == "active"]
    high = [item for item in anomalies if isinstance(item, dict) and item.get("severity") == "high"]
    return "\n".join(
        [
            "REAL-TIME ANOMALY DETECTION - PHASE 533",
            "Mode: anomaly-detection overview.",
            f"Anomalies tracked: {len(anomalies)}",
            f"Active anomalies: {len(active)}",
            f"High-severity anomalies: {len(high)}",
            "Guardrail: anomaly detection should separate baseline drift from dangerous deviations before disrupting healthy systems.",
        ]
    )


def ai_malware_behavior_analyzer() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "malware_behavior.json", {})
    samples = payload.get("samples", []) if isinstance(payload, dict) else []
    malicious = [item for item in samples if isinstance(item, dict) and item.get("classification") == "malicious"]
    stealthy = [item for item in samples if isinstance(item, dict) and bool(item.get("stealthy", False))]
    return "\n".join(
        [
            "AI MALWARE BEHAVIOR ANALYZER - PHASE 534",
            "Mode: malware-behavior overview.",
            f"Behavior samples: {len(samples)}",
            f"Malicious samples: {len(malicious)}",
            f"Stealthy samples: {len(stealthy)}",
            "Guardrail: malware analysis should prioritize execution behavior, persistence signals, and stealth characteristics before recommending action.",
        ]
    )


def behavioral_firewall_system() -> str:
    payload = _safe_json(RUNTIME_SECURITY_DIR / "behavioral_firewall.json", {})
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    events = payload.get("events", []) if isinstance(payload, dict) else []
    blocked = [item for item in events if isinstance(item, dict) and item.get("action") == "blocked"]
    learning = [item for item in policies if isinstance(item, dict) and item.get("mode") == "learning"]
    return "\n".join(
        [
            "BEHAVIORAL FIREWALL SYSTEM - PHASE 535",
            "Mode: behavioral-firewall overview.",
            f"Firewall policies: {len(policies)}",
            f"Learning-mode policies: {len(learning)}",
            f"Behavior events: {len(events)}",
            f"Blocked behavior events: {len(blocked)}",
            "Guardrail: behavioral firewalls should prefer explainable blocks, adaptive learning boundaries, and low false-positive impact before tightening controls.",
        ]
    )
