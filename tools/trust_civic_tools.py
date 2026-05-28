from __future__ import annotations

import json
from pathlib import Path


TRUST_CIVIC_DIR = Path("storage/trust_civic")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def universal_archive_preservation_layer() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "archive_preservation.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    preserved = [item for item in archives if isinstance(item, dict) and bool(item.get("preserved", False))]
    fragile = [item for item in archives if isinstance(item, dict) and bool(item.get("fragile", False))]
    return _overview("UNIVERSAL ARCHIVE PRESERVATION LAYER - PHASE 901", "archive-preservation overview", [f"Archives tracked: {len(archives)}", f"Preserved archives: {len(preserved)}", f"Fragile archives: {len(fragile)}"], "Guardrail: preservation layers should preserve provenance, rights, and restoration integrity before replication.")


def autonomous_language_evolution_tracker() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "language_evolution.json", {})
    languages = payload.get("languages", []) if isinstance(payload, dict) else []
    tracked = [item for item in languages if isinstance(item, dict) and bool(item.get("tracked", False))]
    drifting = [item for item in languages if isinstance(item, dict) and bool(item.get("drifting", False))]
    return _overview("AUTONOMOUS LANGUAGE EVOLUTION TRACKER - PHASE 902", "language-evolution overview", [f"Languages tracked: {len(languages)}", f"Tracked languages: {len(tracked)}", f"Drifting languages: {len(drifting)}"], "Guardrail: language tracking should preserve community stewardship and avoid prescriptive normalization before use.")


def cross_generational_knowledge_transfer_ai() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "knowledge_transfer.json", {})
    cohorts = payload.get("cohorts", []) if isinstance(payload, dict) else []
    connected = [item for item in cohorts if isinstance(item, dict) and bool(item.get("connected", False))]
    broken = [item for item in cohorts if isinstance(item, dict) and bool(item.get("broken", False))]
    return _overview("CROSS-GENERATIONAL KNOWLEDGE TRANSFER AI - PHASE 903", "knowledge-transfer overview", [f"Cohorts tracked: {len(cohorts)}", f"Connected cohorts: {len(connected)}", f"Broken transfer paths: {len(broken)}"], "Guardrail: knowledge transfer should preserve consent, context, and elder/community authority before automation.")


def ai_guided_constitutional_ethics_engine() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "constitutional_ethics.json", {})
    clauses = payload.get("clauses", []) if isinstance(payload, dict) else []
    reviewed = [item for item in clauses if isinstance(item, dict) and bool(item.get("reviewed", False))]
    conflicted = [item for item in clauses if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("AI-GUIDED CONSTITUTIONAL ETHICS ENGINE - PHASE 904", "constitutional-ethics overview", [f"Clauses tracked: {len(clauses)}", f"Reviewed clauses: {len(reviewed)}", f"Conflicted clauses: {len(conflicted)}"], "Guardrail: constitutional ethics should remain advisory, transparent, and subordinate to legitimate democratic process.")


def planetary_empathy_simulation_framework() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "planetary_empathy.json", {})
    simulations = payload.get("simulations", []) if isinstance(payload, dict) else []
    immersive = [item for item in simulations if isinstance(item, dict) and bool(item.get("immersive", False))]
    manipulative = [item for item in simulations if isinstance(item, dict) and bool(item.get("manipulative", False))]
    return _overview("PLANETARY EMPATHY SIMULATION FRAMEWORK - PHASE 905", "planetary-empathy overview", [f"Simulations tracked: {len(simulations)}", f"Immersive simulations: {len(immersive)}", f"Manipulative simulations: {len(manipulative)}"], "Guardrail: empathy simulations should preserve emotional safety and avoid coercive persuasion before deployment.")


def collective_emotional_intelligence_layer() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "collective_emotional_intelligence.json", {})
    groups = payload.get("groups", []) if isinstance(payload, dict) else []
    attuned = [item for item in groups if isinstance(item, dict) and bool(item.get("attuned", False))]
    strained = [item for item in groups if isinstance(item, dict) and bool(item.get("strained", False))]
    return _overview("COLLECTIVE EMOTIONAL INTELLIGENCE LAYER - PHASE 906", "collective-emotional-intelligence overview", [f"Groups tracked: {len(groups)}", f"Attuned groups: {len(attuned)}", f"Strained groups: {len(strained)}"], "Guardrail: emotional intelligence layers should preserve privacy, dignity, and non-manipulative use before optimization.")


def human_conflict_de_escalation_ai() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "conflict_deescalation.json", {})
    incidents = payload.get("incidents", []) if isinstance(payload, dict) else []
    deescalated = [item for item in incidents if isinstance(item, dict) and bool(item.get("deescalated", False))]
    high_risk = [item for item in incidents if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("HUMAN CONFLICT DE-ESCALATION AI - PHASE 907", "conflict-deescalation overview", [f"Incidents tracked: {len(incidents)}", f"De-escalated incidents: {len(deescalated)}", f"High-risk incidents: {len(high_risk)}"], "Guardrail: de-escalation support should preserve human judgment, due process, and non-coercion before intervention.")


def global_trust_infrastructure() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "global_trust.json", {})
    anchors = payload.get("anchors", []) if isinstance(payload, dict) else []
    verified = [item for item in anchors if isinstance(item, dict) and bool(item.get("verified", False))]
    weak = [item for item in anchors if isinstance(item, dict) and bool(item.get("weak", False))]
    return _overview("GLOBAL TRUST INFRASTRUCTURE - PHASE 908", "global-trust overview", [f"Anchors tracked: {len(anchors)}", f"Verified anchors: {len(verified)}", f"Weak anchors: {len(weak)}"], "Guardrail: trust infrastructure should preserve decentralization, revocation, and transparent governance before dependency.")


def distributed_truth_consensus_network() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "truth_consensus.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    converged = [item for item in nodes if isinstance(item, dict) and bool(item.get("converged", False))]
    disputed = [item for item in nodes if isinstance(item, dict) and bool(item.get("disputed", False))]
    return _overview("DISTRIBUTED TRUTH CONSENSUS NETWORK - PHASE 909", "truth-consensus overview", [f"Nodes tracked: {len(nodes)}", f"Converged nodes: {len(converged)}", f"Disputed nodes: {len(disputed)}"], "Guardrail: truth consensus should preserve dissent, source provenance, and resistance to coercive convergence before adoption.")


def autonomous_misinformation_resilience_system() -> str:
    payload = _safe_json(TRUST_CIVIC_DIR / "misinformation_resilience.json", {})
    campaigns = payload.get("campaigns", []) if isinstance(payload, dict) else []
    contained = [item for item in campaigns if isinstance(item, dict) and bool(item.get("contained", False))]
    spreading = [item for item in campaigns if isinstance(item, dict) and bool(item.get("spreading", False))]
    return _overview("AUTONOMOUS MISINFORMATION RESILIENCE SYSTEM - PHASE 910", "misinformation-resilience overview", [f"Campaigns tracked: {len(campaigns)}", f"Contained campaigns: {len(contained)}", f"Spreading campaigns: {len(spreading)}"], "Guardrail: misinformation resilience should preserve civil liberties, appeals, and evidence transparency before mitigation.")
