from __future__ import annotations

import json
from pathlib import Path


COLLECTIVE_CIV_DIR = Path("storage/collective_civilization")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_democracy_simulation() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "democracy_simulation.json", {})
    constituencies = payload.get("constituencies", []) if isinstance(payload, dict) else []
    represented = [item for item in constituencies if isinstance(item, dict) and bool(item.get("represented", False))]
    contested = [item for item in constituencies if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("AI DEMOCRACY SIMULATION - PHASE 701", "democracy-simulation overview", [f"Constituencies tracked: {len(constituencies)}", f"Represented constituencies: {len(represented)}", f"Contested constituencies: {len(contested)}"], "Guardrail: democracy simulations should remain pluralistic, transparent, and clearly non-prescriptive before informing governance ideas.")


def collective_intelligence_network() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "collective_intelligence.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    connected = [item for item in nodes if isinstance(item, dict) and item.get("status") == "connected"]
    curated = [item for item in nodes if isinstance(item, dict) and bool(item.get("curated", False))]
    return _overview("COLLECTIVE INTELLIGENCE NETWORK - PHASE 702", "collective-intelligence overview", [f"Nodes tracked: {len(nodes)}", f"Connected nodes: {len(connected)}", f"Curated nodes: {len(curated)}"], "Guardrail: collective intelligence should preserve source diversity, attribution, and review before synthesis.")


def distributed_human_ai_governance() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "distributed_governance.json", {})
    councils = payload.get("councils", []) if isinstance(payload, dict) else []
    delegated = [item for item in councils if isinstance(item, dict) and bool(item.get("delegated", False))]
    audited = [item for item in councils if isinstance(item, dict) and bool(item.get("audited", False))]
    return _overview("DISTRIBUTED HUMAN-AI GOVERNANCE - PHASE 703", "distributed-governance overview", [f"Councils tracked: {len(councils)}", f"Delegated councils: {len(delegated)}", f"Audited councils: {len(audited)}"], "Guardrail: distributed governance should preserve human accountability, auditability, and override authority before autonomy expands.")


def ai_assisted_scientific_council() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "scientific_council.json", {})
    briefs = payload.get("briefs", []) if isinstance(payload, dict) else []
    reviewed = [item for item in briefs if isinstance(item, dict) and bool(item.get("reviewed", False))]
    consensus = [item for item in briefs if isinstance(item, dict) and bool(item.get("consensus", False))]
    return _overview("AI-ASSISTED SCIENTIFIC COUNCIL - PHASE 704", "scientific-council overview", [f"Briefs tracked: {len(briefs)}", f"Reviewed briefs: {len(reviewed)}", f"Consensus briefs: {len(consensus)}"], "Guardrail: scientific councils should preserve dissent, evidence grading, and expert review before consensus claims.")


def autonomous_innovation_ecosystem() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "innovation_ecosystem.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    active = [item for item in programs if isinstance(item, dict) and item.get("status") == "active"]
    funded = [item for item in programs if isinstance(item, dict) and bool(item.get("funded", False))]
    return _overview("AUTONOMOUS INNOVATION ECOSYSTEM - PHASE 705", "innovation-ecosystem overview", [f"Programs tracked: {len(programs)}", f"Active programs: {len(active)}", f"Funded programs: {len(funded)}"], "Guardrail: innovation ecosystems should preserve explicit funding logic, accountability, and inclusive access before automation steers portfolios.")


def global_knowledge_synchronization() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "knowledge_sync.json", {})
    sources = payload.get("sources", []) if isinstance(payload, dict) else []
    synchronized = [item for item in sources if isinstance(item, dict) and bool(item.get("synchronized", False))]
    lagging = [item for item in sources if isinstance(item, dict) and item.get("status") == "lagging"]
    return _overview("GLOBAL KNOWLEDGE SYNCHRONIZATION - PHASE 706", "knowledge-synchronization overview", [f"Sources tracked: {len(sources)}", f"Synchronized sources: {len(synchronized)}", f"Lagging sources: {len(lagging)}"], "Guardrail: knowledge synchronization should preserve provenance, recency, and conflict visibility before merging perspectives.")


def planet_scale_semantic_index() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "planet_scale_index.json", {})
    corpora = payload.get("corpora", []) if isinstance(payload, dict) else []
    indexed = [item for item in corpora if isinstance(item, dict) and bool(item.get("indexed", False))]
    multilingual = [item for item in corpora if isinstance(item, dict) and bool(item.get("multilingual", False))]
    return _overview("PLANET-SCALE SEMANTIC INDEX - PHASE 707", "planet-scale-index overview", [f"Corpora tracked: {len(corpora)}", f"Indexed corpora: {len(indexed)}", f"Multilingual corpora: {len(multilingual)}"], "Guardrail: global semantic indexing should preserve source rights, privacy, and retrieval transparency before broad deployment.")


def universal_translation_framework() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "universal_translation.json", {})
    language_pairs = payload.get("language_pairs", []) if isinstance(payload, dict) else []
    supported = [item for item in language_pairs if isinstance(item, dict) and bool(item.get("supported", False))]
    nuanced = [item for item in language_pairs if isinstance(item, dict) and bool(item.get("nuance_checked", False))]
    return _overview("UNIVERSAL TRANSLATION FRAMEWORK - PHASE 708", "universal-translation overview", [f"Language pairs tracked: {len(language_pairs)}", f"Supported pairs: {len(supported)}", f"Nuance-checked pairs: {len(nuanced)}"], "Guardrail: translation at scale should preserve meaning, cultural nuance, and clear fallback when confidence is low.")


def human_cultural_preservation_ai() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "cultural_preservation.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    digitized = [item for item in archives if isinstance(item, dict) and bool(item.get("digitized", False))]
    at_risk = [item for item in archives if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("HUMAN CULTURAL PRESERVATION AI - PHASE 709", "cultural-preservation overview", [f"Archives tracked: {len(archives)}", f"Digitized archives: {len(digitized)}", f"High-risk archives: {len(at_risk)}"], "Guardrail: cultural preservation should respect stewardship, consent, and contextual integrity before replication or remix.")


def historical_reconstruction_engine() -> str:
    payload = _safe_json(COLLECTIVE_CIV_DIR / "historical_reconstruction.json", {})
    reconstructions = payload.get("reconstructions", []) if isinstance(payload, dict) else []
    sourced = [item for item in reconstructions if isinstance(item, dict) and bool(item.get("sourced", False))]
    disputed = [item for item in reconstructions if isinstance(item, dict) and bool(item.get("disputed", False))]
    return _overview("HISTORICAL RECONSTRUCTION ENGINE - PHASE 710", "historical-reconstruction overview", [f"Reconstructions tracked: {len(reconstructions)}", f"Sourced reconstructions: {len(sourced)}", f"Disputed reconstructions: {len(disputed)}"], "Guardrail: historical reconstruction should preserve uncertainty, source context, and dispute visibility rather than narrating certainty.")
