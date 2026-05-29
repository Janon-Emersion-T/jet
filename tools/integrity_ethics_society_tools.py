from __future__ import annotations

import json
from pathlib import Path


INTEGRITY_ETHICS_DIR = Path("storage/integrity_ethics_society")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_intelligence_analysis() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "intelligence_analysis.json", {})
    briefs = payload.get("briefs", []) if isinstance(payload, dict) else []
    corroborated = [item for item in briefs if isinstance(item, dict) and bool(item.get("corroborated", False))]
    flagged = [item for item in briefs if isinstance(item, dict) and bool(item.get("flagged", False))]
    return _overview("AUTONOMOUS INTELLIGENCE ANALYSIS - PHASE 761", "intelligence-analysis overview", [f"Briefs tracked: {len(briefs)}", f"Corroborated briefs: {len(corroborated)}", f"Flagged briefs: {len(flagged)}"], "Guardrail: intelligence analysis should preserve source scrutiny, uncertainty, and human review before decisions.")


def multi_source_truth_validation() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "truth_validation.json", {})
    claims = payload.get("claims", []) if isinstance(payload, dict) else []
    validated = [item for item in claims if isinstance(item, dict) and bool(item.get("validated", False))]
    conflicted = [item for item in claims if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("MULTI-SOURCE TRUTH VALIDATION - PHASE 762", "truth-validation overview", [f"Claims tracked: {len(claims)}", f"Validated claims: {len(validated)}", f"Conflicted claims: {len(conflicted)}"], "Guardrail: truth validation should preserve source provenance and avoid overstating certainty where evidence is mixed.")


def propaganda_detection_engine() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "propaganda_detection.json", {})
    signals = payload.get("signals", []) if isinstance(payload, dict) else []
    escalated = [item for item in signals if isinstance(item, dict) and bool(item.get("escalated", False))]
    manipulative = [item for item in signals if isinstance(item, dict) and bool(item.get("manipulative", False))]
    return _overview("PROPAGANDA DETECTION ENGINE - PHASE 763", "propaganda-detection overview", [f"Signals tracked: {len(signals)}", f"Escalated signals: {len(escalated)}", f"Manipulative signals: {len(manipulative)}"], "Guardrail: propaganda detection should remain bias-aware, appealable, and grounded in transparent criteria.")


def information_authenticity_scoring() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "authenticity_scoring.json", {})
    documents = payload.get("documents", []) if isinstance(payload, dict) else []
    trusted = [item for item in documents if isinstance(item, dict) and bool(item.get("trusted", False))]
    uncertain = [item for item in documents if isinstance(item, dict) and item.get("score") == "uncertain"]
    return _overview("INFORMATION AUTHENTICITY SCORING - PHASE 764", "authenticity-scoring overview", [f"Documents tracked: {len(documents)}", f"Trusted documents: {len(trusted)}", f"Uncertain documents: {len(uncertain)}"], "Guardrail: authenticity scores should remain interpretable and should not replace direct source review where stakes are high.")


def deepfake_detection_framework() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "deepfake_detection.json", {})
    media = payload.get("media", []) if isinstance(payload, dict) else []
    screened = [item for item in media if isinstance(item, dict) and bool(item.get("screened", False))]
    suspicious = [item for item in media if isinstance(item, dict) and bool(item.get("suspicious", False))]
    return _overview("DEEPFAKE DETECTION FRAMEWORK - PHASE 765", "deepfake-detection overview", [f"Media assets tracked: {len(media)}", f"Screened assets: {len(screened)}", f"Suspicious assets: {len(suspicious)}"], "Guardrail: deepfake detection should preserve evidence trails and avoid definitive claims without supporting review.")


def ai_media_integrity_system() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "media_integrity.json", {})
    assets = payload.get("assets", []) if isinstance(payload, dict) else []
    signed = [item for item in assets if isinstance(item, dict) and bool(item.get("signed", False))]
    tampered = [item for item in assets if isinstance(item, dict) and bool(item.get("tampered", False))]
    return _overview("AI MEDIA INTEGRITY SYSTEM - PHASE 766", "media-integrity overview", [f"Assets tracked: {len(assets)}", f"Signed assets: {len(signed)}", f"Tampered assets: {len(tampered)}"], "Guardrail: media integrity systems should preserve provenance, revocation, and transparent verification paths.")


def trustworthy_ai_certification_layer() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "trustworthy_ai.json", {})
    systems = payload.get("systems", []) if isinstance(payload, dict) else []
    audited = [item for item in systems if isinstance(item, dict) and bool(item.get("audited", False))]
    certified = [item for item in systems if isinstance(item, dict) and bool(item.get("certified", False))]
    return _overview("TRUSTWORTHY AI CERTIFICATION LAYER - PHASE 767", "trustworthy-ai overview", [f"Systems tracked: {len(systems)}", f"Audited systems: {len(audited)}", f"Certified systems: {len(certified)}"], "Guardrail: certification layers should preserve independent review, scope clarity, and renewal discipline before trust claims.")


def autonomous_ethics_review_board() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "ethics_review.json", {})
    cases = payload.get("cases", []) if isinstance(payload, dict) else []
    reviewed = [item for item in cases if isinstance(item, dict) and bool(item.get("reviewed", False))]
    blocked = [item for item in cases if isinstance(item, dict) and item.get("decision") == "blocked"]
    return _overview("AUTONOMOUS ETHICS REVIEW BOARD - PHASE 768", "ethics-review overview", [f"Cases tracked: {len(cases)}", f"Reviewed cases: {len(reviewed)}", f"Blocked cases: {len(blocked)}"], "Guardrail: ethics review should remain plural, documented, and subordinate to human governance in contested cases.")


def ai_rights_governance_sandbox() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "ai_rights_governance.json", {})
    frameworks = payload.get("frameworks", []) if isinstance(payload, dict) else []
    debated = [item for item in frameworks if isinstance(item, dict) and bool(item.get("debated", False))]
    provisional = [item for item in frameworks if isinstance(item, dict) and bool(item.get("provisional", False))]
    return _overview("AI RIGHTS GOVERNANCE SANDBOX - PHASE 769", "ai-rights-governance overview", [f"Frameworks tracked: {len(frameworks)}", f"Debated frameworks: {len(debated)}", f"Provisional frameworks: {len(provisional)}"], "Guardrail: rights-governance exploration should preserve humility, legal context, and clear separation between simulation and policy.")


def human_ai_coexistence_framework() -> str:
    payload = _safe_json(INTEGRITY_ETHICS_DIR / "human_ai_coexistence.json", {})
    domains = payload.get("domains", []) if isinstance(payload, dict) else []
    coordinated = [item for item in domains if isinstance(item, dict) and bool(item.get("coordinated", False))]
    tensioned = [item for item in domains if isinstance(item, dict) and bool(item.get("tensioned", False))]
    return _overview("HUMAN-AI COEXISTENCE FRAMEWORK - PHASE 770", "human-ai-coexistence overview", [f"Domains tracked: {len(domains)}", f"Coordinated domains: {len(coordinated)}", f"Tension-marked domains: {len(tensioned)}"], "Guardrail: coexistence planning should preserve human dignity, labor fairness, and participatory governance before scaling.")
