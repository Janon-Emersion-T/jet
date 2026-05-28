from __future__ import annotations

import json
from pathlib import Path


CIVIC_JUSTICE_DIR = Path("storage/civic_justice")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CIVIC_JUSTICE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_diplomacy_coordination_ai() -> str:
    return _render("UNIVERSAL DIPLOMACY COORDINATION AI - PHASE 1141", "diplomacy-coordination overview", "diplomacy_coordination.json", "dialogues", "coordinated", "tense", "Dialogues tracked", "Coordinated dialogues", "Tense dialogues", "Guardrail: diplomacy coordination should preserve sovereign legitimacy, non-escalation, and transparent tradeoffs before action.")


def adaptive_treaty_negotiation_engine() -> str:
    return _render("ADAPTIVE TREATY NEGOTIATION ENGINE - PHASE 1142", "treaty-negotiation overview", "treaty_negotiation.json", "treaties", "negotiated", "blocked", "Treaties tracked", "Negotiated treaties", "Blocked treaties", "Guardrail: treaty negotiation should preserve informed consent, due process, and public accountability before commitment.")


def autonomous_resource_peace_framework() -> str:
    return _render("AUTONOMOUS RESOURCE PEACE FRAMEWORK - PHASE 1143", "resource-peace overview", "resource_peace.json", "compacts", "stabilized", "contested", "Compacts tracked", "Stabilized compacts", "Contested compacts", "Guardrail: resource peace frameworks should preserve fairness, ecological limits, and anti-coercive mediation before allocation.")


def infinite_scale_planetary_governance_substrate() -> str:
    return _render("INFINITE-SCALE PLANETARY GOVERNANCE SUBSTRATE - PHASE 1144", "planetary-governance overview", "planetary_governance.json", "institutions", "coordinated", "captured", "Institutions tracked", "Coordinated institutions", "Captured institutions", "Guardrail: planetary governance should preserve subsidiarity, legitimacy, and appeals before delegation.")


def recursive_constitutional_evolution_engine() -> str:
    return _render("RECURSIVE CONSTITUTIONAL EVOLUTION ENGINE - PHASE 1145", "constitutional-evolution overview", "constitutional_evolution.json", "constitutions", "evolving", "unstable", "Constitutions tracked", "Evolving constitutions", "Unstable constitutions", "Guardrail: constitutional evolution should preserve rights floors, democratic process, and public review before amendment.")


def universal_civic_intelligence_network() -> str:
    return _render("UNIVERSAL CIVIC INTELLIGENCE NETWORK - PHASE 1146", "civic-intelligence overview", "civic_intelligence.json", "civic_nodes", "informed", "disconnected", "Civic nodes tracked", "Informed civic nodes", "Disconnected civic nodes", "Guardrail: civic intelligence should preserve accessibility, plural participation, and anti-manipulation safeguards before use.")


def adaptive_democratic_participation_ai() -> str:
    return _render("ADAPTIVE DEMOCRATIC PARTICIPATION AI - PHASE 1147", "democratic-participation overview", "democratic_participation.json", "electorates", "engaged", "excluded", "Electorates tracked", "Engaged electorates", "Excluded electorates", "Guardrail: democratic participation tools should preserve equal voice, privacy, and anti-coercion safeguards before deployment.")


def autonomous_ethical_legislation_simulator() -> str:
    return _render("AUTONOMOUS ETHICAL LEGISLATION SIMULATOR - PHASE 1148", "ethical-legislation overview", "ethical_legislation.json", "bills", "simulated", "harmful", "Bills tracked", "Simulated bills", "Harmful bills", "Guardrail: legislation simulation should preserve rights review, democratic legitimacy, and contestability before recommendation.")


def infinite_scale_justice_harmonization_layer() -> str:
    return _render("INFINITE-SCALE JUSTICE HARMONIZATION LAYER - PHASE 1149", "justice-harmonization overview", "justice_harmonization.json", "jurisdictions", "harmonized", "inequitable", "Jurisdictions tracked", "Harmonized jurisdictions", "Inequitable jurisdictions", "Guardrail: justice harmonization should preserve local rights protections, due process, and anti-bias review before alignment.")


def recursive_legal_reasoning_substrate() -> str:
    return _render("RECURSIVE LEGAL REASONING SUBSTRATE - PHASE 1150", "legal-reasoning overview", "legal_reasoning.json", "cases", "reasoned", "ambiguous", "Cases tracked", "Reasoned cases", "Ambiguous cases", "Guardrail: legal reasoning should preserve jurisdictional nuance, lawyer oversight, and explicit uncertainty before advice.")
