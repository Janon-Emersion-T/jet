from __future__ import annotations

import json
from pathlib import Path


CIVIC_COLLABORATION_DIR = Path("storage/civic_collaboration")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def rural_connectivity_optimization() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "rural_connectivity.json", {})
    regions = payload.get("regions", []) if isinstance(payload, dict) else []
    connected = [item for item in regions if isinstance(item, dict) and bool(item.get("connected", False))]
    offline = [item for item in regions if isinstance(item, dict) and item.get("status") == "offline"]
    return _overview("RURAL CONNECTIVITY OPTIMIZATION - PHASE 791", "rural-connectivity overview", [f"Regions tracked: {len(regions)}", f"Connected regions: {len(connected)}", f"Offline regions: {len(offline)}"], "Guardrail: connectivity optimization should preserve affordability, access equity, and local consent before rollout.")


def universal_access_knowledge_engine() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "universal_access_knowledge.json", {})
    libraries = payload.get("libraries", []) if isinstance(payload, dict) else []
    open_access = [item for item in libraries if isinstance(item, dict) and bool(item.get("open_access", False))]
    limited = [item for item in libraries if isinstance(item, dict) and bool(item.get("limited", False))]
    return _overview("UNIVERSAL ACCESS KNOWLEDGE ENGINE - PHASE 792", "universal-access-knowledge overview", [f"Libraries tracked: {len(libraries)}", f"Open-access libraries: {len(open_access)}", f"Limited-access libraries: {len(limited)}"], "Guardrail: knowledge access systems should preserve attribution, licensing, and accessibility before broad dissemination.")


def open_source_civilization_framework() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "open_source_civilization.json", {})
    projects = payload.get("projects", []) if isinstance(payload, dict) else []
    maintained = [item for item in projects if isinstance(item, dict) and bool(item.get("maintained", False))]
    collaborative = [item for item in projects if isinstance(item, dict) and bool(item.get("collaborative", False))]
    return _overview("OPEN-SOURCE CIVILIZATION FRAMEWORK - PHASE 793", "open-source-civilization overview", [f"Projects tracked: {len(projects)}", f"Maintained projects: {len(maintained)}", f"Collaborative projects: {len(collaborative)}"], "Guardrail: open-source civilization planning should preserve stewardship, plural governance, and sustainable maintenance before adoption.")


def ai_cooperative_economy_layer() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "cooperative_economy.json", {})
    cooperatives = payload.get("cooperatives", []) if isinstance(payload, dict) else []
    enabled = [item for item in cooperatives if isinstance(item, dict) and bool(item.get("enabled", False))]
    shared = [item for item in cooperatives if isinstance(item, dict) and bool(item.get("shared", False))]
    return _overview("AI COOPERATIVE ECONOMY LAYER - PHASE 794", "cooperative-economy overview", [f"Cooperatives tracked: {len(cooperatives)}", f"Enabled cooperatives: {len(enabled)}", f"Shared-governance cooperatives: {len(shared)}"], "Guardrail: cooperative economy tooling should preserve democratic ownership, fairness, and auditability before allocation decisions.")


def autonomous_research_commons() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "research_commons.json", {})
    commons = payload.get("commons", []) if isinstance(payload, dict) else []
    indexed = [item for item in commons if isinstance(item, dict) and bool(item.get("indexed", False))]
    governed = [item for item in commons if isinstance(item, dict) and bool(item.get("governed", False))]
    return _overview("AUTONOMOUS RESEARCH COMMONS - PHASE 795", "research-commons overview", [f"Commons tracked: {len(commons)}", f"Indexed commons: {len(indexed)}", f"Governed commons: {len(governed)}"], "Guardrail: research commons should preserve open access norms, contributor credit, and governance clarity before automation expands.")


def global_distributed_innovation_network() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "distributed_innovation.json", {})
    hubs = payload.get("hubs", []) if isinstance(payload, dict) else []
    active = [item for item in hubs if isinstance(item, dict) and item.get("status") == "active"]
    linked = [item for item in hubs if isinstance(item, dict) and bool(item.get("linked", False))]
    return _overview("GLOBAL DISTRIBUTED INNOVATION NETWORK - PHASE 796", "distributed-innovation overview", [f"Hubs tracked: {len(hubs)}", f"Active hubs: {len(active)}", f"Linked hubs: {len(linked)}"], "Guardrail: innovation networks should preserve inclusion, local autonomy, and transparent contribution pathways before coordination.")


def ai_assisted_constitutional_drafting() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "constitutional_drafting.json", {})
    drafts = payload.get("drafts", []) if isinstance(payload, dict) else []
    reviewed = [item for item in drafts if isinstance(item, dict) and bool(item.get("reviewed", False))]
    rights_scoped = [item for item in drafts if isinstance(item, dict) and bool(item.get("rights_scoped", False))]
    return _overview("AI-ASSISTED CONSTITUTIONAL DRAFTING - PHASE 797", "constitutional-drafting overview", [f"Drafts tracked: {len(drafts)}", f"Reviewed drafts: {len(reviewed)}", f"Rights-scoped drafts: {len(rights_scoped)}"], "Guardrail: constitutional drafting support should remain advisory, participatory, and subordinate to legitimate democratic process.")


def smart_governance_simulation() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "smart_governance.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    simulated = [item for item in models if isinstance(item, dict) and bool(item.get("simulated", False))]
    contested = [item for item in models if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("SMART GOVERNANCE SIMULATION - PHASE 798", "smart-governance overview", [f"Models tracked: {len(models)}", f"Simulated models: {len(simulated)}", f"Contested models: {len(contested)}"], "Guardrail: governance simulation should preserve plural values, dissent visibility, and human legitimacy before recommendation.")


def autonomous_legal_harmonization() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "legal_harmonization.json", {})
    statutes = payload.get("statutes", []) if isinstance(payload, dict) else []
    aligned = [item for item in statutes if isinstance(item, dict) and bool(item.get("aligned", False))]
    conflicting = [item for item in statutes if isinstance(item, dict) and bool(item.get("conflicting", False))]
    return _overview("AUTONOMOUS LEGAL HARMONIZATION - PHASE 799", "legal-harmonization overview", [f"Statutes tracked: {len(statutes)}", f"Aligned statutes: {len(aligned)}", f"Conflicting statutes: {len(conflicting)}"], "Guardrail: legal harmonization should preserve jurisdictional nuance and human legal review before policy movement.")


def cross_border_collaboration_ai() -> str:
    payload = _safe_json(CIVIC_COLLABORATION_DIR / "cross_border_collaboration.json", {})
    initiatives = payload.get("initiatives", []) if isinstance(payload, dict) else []
    active = [item for item in initiatives if isinstance(item, dict) and item.get("status") == "active"]
    compliant = [item for item in initiatives if isinstance(item, dict) and bool(item.get("compliant", False))]
    return _overview("CROSS-BORDER COLLABORATION AI - PHASE 800", "cross-border-collaboration overview", [f"Initiatives tracked: {len(initiatives)}", f"Active initiatives: {len(active)}", f"Compliant initiatives: {len(compliant)}"], "Guardrail: cross-border collaboration should preserve sovereignty, data protection, and shared accountability before scaling.")
