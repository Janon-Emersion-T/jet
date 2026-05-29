from __future__ import annotations

import json
from pathlib import Path


HEALTHCARE_DIR = Path("storage/healthcare_ai")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_healthcare_assistant() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "healthcare_assistant.json", {})
    cases = payload.get("cases", []) if isinstance(payload, dict) else []
    triaged = [item for item in cases if isinstance(item, dict) and bool(item.get("triaged", False))]
    reviewed = [item for item in cases if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI HEALTHCARE ASSISTANT - PHASE 629", "healthcare-assistant overview", [f"Cases tracked: {len(cases)}", f"Triaged cases: {len(triaged)}", f"Reviewed cases: {len(reviewed)}"], "Guardrail: healthcare assistance should remain clinician-supervised, evidence-aware, and explicit about uncertainty.")


def medical_imaging_analysis() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "medical_imaging.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    flagged = [item for item in studies if isinstance(item, dict) and bool(item.get("flagged", False))]
    validated = [item for item in studies if isinstance(item, dict) and bool(item.get("validated", False))]
    return _overview("MEDICAL IMAGING ANALYSIS - PHASE 630", "medical-imaging overview", [f"Studies tracked: {len(studies)}", f"Flagged studies: {len(flagged)}", f"Validated studies: {len(validated)}"], "Guardrail: imaging analysis should remain radiologist-reviewable, calibration-aware, and non-diagnostic without human confirmation.")


def ai_triage_assistant() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "triage.json", {})
    patients = payload.get("patients", []) if isinstance(payload, dict) else []
    urgent = [item for item in patients if isinstance(item, dict) and item.get("priority") == "urgent"]
    monitored = [item for item in patients if isinstance(item, dict) and bool(item.get("monitored", False))]
    return _overview("AI TRIAGE ASSISTANT - PHASE 631", "triage overview", [f"Patients tracked: {len(patients)}", f"Urgent patients: {len(urgent)}", f"Monitored patients: {len(monitored)}"], "Guardrail: triage support should remain clinician-supervised and should prioritize safety over throughput.")


def clinical_decision_support() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "clinical_decision_support.json", {})
    recommendations = payload.get("recommendations", []) if isinstance(payload, dict) else []
    accepted = [item for item in recommendations if isinstance(item, dict) and item.get("status") == "accepted"]
    risky = [item for item in recommendations if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("CLINICAL DECISION SUPPORT - PHASE 632", "clinical-decision overview", [f"Recommendations tracked: {len(recommendations)}", f"Accepted recommendations: {len(accepted)}", f"High-risk recommendations: {len(risky)}"], "Guardrail: decision support should remain explainable, guideline-aware, and subordinate to licensed judgment.")


def patient_monitoring_intelligence() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "patient_monitoring.json", {})
    monitors = payload.get("monitors", []) if isinstance(payload, dict) else []
    alerting = [item for item in monitors if isinstance(item, dict) and bool(item.get("alert", False))]
    stable = [item for item in monitors if isinstance(item, dict) and item.get("status") == "stable"]
    return _overview("PATIENT MONITORING INTELLIGENCE - PHASE 633", "patient-monitoring overview", [f"Monitors tracked: {len(monitors)}", f"Alerting monitors: {len(alerting)}", f"Stable monitors: {len(stable)}"], "Guardrail: patient monitoring should reduce alarm fatigue, preserve traceability, and escalate safely.")


def drug_interaction_analyzer() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "drug_interactions.json", {})
    checks = payload.get("checks", []) if isinstance(payload, dict) else []
    interactions = [item for item in checks if isinstance(item, dict) and bool(item.get("interaction", False))]
    severe = [item for item in checks if isinstance(item, dict) and item.get("severity") == "severe"]
    return _overview("DRUG INTERACTION ANALYZER - PHASE 634", "drug-interaction overview", [f"Checks tracked: {len(checks)}", f"Detected interactions: {len(interactions)}", f"Severe interactions: {len(severe)}"], "Guardrail: drug interaction guidance should remain pharmacist/clinician-reviewable and prioritize patient safety over automation.")


def autonomous_health_risk_scoring() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "health_risk_scoring.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    high = [item for item in profiles if isinstance(item, dict) and item.get("risk") == "high"]
    reviewed = [item for item in profiles if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AUTONOMOUS HEALTH RISK SCORING - PHASE 635", "health-risk overview", [f"Profiles tracked: {len(profiles)}", f"High-risk profiles: {len(high)}", f"Reviewed profiles: {len(reviewed)}"], "Guardrail: health risk scores should be fairness-aware, clinically contextualized, and not used as standalone decisions.")


def genomics_research_assistant() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "genomics.json", {})
    samples = payload.get("samples", []) if isinstance(payload, dict) else []
    annotated = [item for item in samples if isinstance(item, dict) and bool(item.get("annotated", False))]
    uncertain = [item for item in samples if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("GENOMICS RESEARCH ASSISTANT - PHASE 636", "genomics overview", [f"Samples tracked: {len(samples)}", f"Annotated samples: {len(annotated)}", f"Uncertain samples: {len(uncertain)}"], "Guardrail: genomics assistance should preserve scientific uncertainty, privacy, and specialist review before interpretation.")


def ai_pharmaceutical_simulation() -> str:
    payload = _safe_json(HEALTHCARE_DIR / "pharma_simulation.json", {})
    runs = payload.get("runs", []) if isinstance(payload, dict) else []
    completed = [item for item in runs if isinstance(item, dict) and item.get("status") == "completed"]
    promising = [item for item in runs if isinstance(item, dict) and bool(item.get("promising", False))]
    return _overview("AI PHARMACEUTICAL SIMULATION - PHASE 637", "pharma-simulation overview", [f"Simulation runs: {len(runs)}", f"Completed runs: {len(completed)}", f"Promising runs: {len(promising)}"], "Guardrail: pharmaceutical simulation should remain hypothesis-driven, evidence-bounded, and expert-reviewed before research decisions.")
