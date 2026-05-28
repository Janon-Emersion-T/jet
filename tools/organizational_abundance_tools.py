from __future__ import annotations

import json
from pathlib import Path


ORGANIZATIONAL_ABUNDANCE_DIR = Path("storage/organizational_abundance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(ORGANIZATIONAL_ABUNDANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_startup_incubation_substrate() -> str:
    return _render("UNIVERSAL STARTUP INCUBATION SUBSTRATE - PHASE 1211", "startup-incubation overview", "startup_incubation.json", "cohorts", "incubated", "stalled", "Cohorts tracked", "Incubated cohorts", "Stalled cohorts", "Guardrail: startup incubation should preserve fair access, responsible growth, and non-exploitative support before scaling.")


def adaptive_market_equilibrium_engine() -> str:
    return _render("ADAPTIVE MARKET EQUILIBRIUM ENGINE - PHASE 1212", "market-equilibrium overview", "market_equilibrium.json", "markets", "stabilized", "distorted", "Markets tracked", "Stabilized markets", "Distorted markets", "Guardrail: market equilibrium engines should preserve competition, transparency, and public-interest constraints before intervention.")


def autonomous_value_creation_optimizer() -> str:
    return _render("AUTONOMOUS VALUE-CREATION OPTIMIZER - PHASE 1213", "value-creation overview", "value_creation.json", "value_streams", "optimized", "extractive", "Value streams tracked", "Optimized streams", "Extractive streams", "Guardrail: value creation optimization should preserve human welfare, fairness, and long-horizon sustainability before rollout.")


def infinite_scale_productivity_harmonizer() -> str:
    return _render("INFINITE-SCALE PRODUCTIVITY HARMONIZER - PHASE 1214", "productivity-harmonization overview", "productivity_harmonization.json", "workflows", "harmonized", "overloaded", "Workflows tracked", "Harmonized workflows", "Overloaded workflows", "Guardrail: productivity harmonization should preserve wellbeing, autonomy, and non-coercive pacing before optimization.")


def recursive_enterprise_orchestration_ai() -> str:
    return _render("RECURSIVE ENTERPRISE ORCHESTRATION AI - PHASE 1215", "enterprise-orchestration overview", "enterprise_orchestration.json", "enterprises", "orchestrated", "brittle", "Enterprises tracked", "Orchestrated enterprises", "Brittle enterprises", "Guardrail: enterprise orchestration should preserve auditability, layered approvals, and rollback before execution.")


def universal_corporate_governance_engine() -> str:
    return _render("UNIVERSAL CORPORATE GOVERNANCE ENGINE - PHASE 1216", "corporate-governance overview", "corporate_governance.json", "boards", "governed", "captured", "Boards tracked", "Governed boards", "Captured boards", "Guardrail: corporate governance should preserve fiduciary duties, transparency, and stakeholder accountability before automation.")


def adaptive_stakeholder_balancing_framework() -> str:
    return _render("ADAPTIVE STAKEHOLDER BALANCING FRAMEWORK - PHASE 1217", "stakeholder-balancing overview", "stakeholder_balancing.json", "stakeholder_maps", "balanced", "marginalized", "Stakeholder maps tracked", "Balanced maps", "Marginalized maps", "Guardrail: stakeholder balancing should preserve plural interests, due consideration, and reviewable tradeoffs before recommendation.")


def autonomous_organizational_redesign_ai() -> str:
    return _render("AUTONOMOUS ORGANIZATIONAL REDESIGN AI - PHASE 1218", "organizational-redesign overview", "organizational_redesign.json", "structures", "redesigned", "disrupted", "Structures tracked", "Redesigned structures", "Disrupted structures", "Guardrail: organizational redesign should preserve worker voice, continuity, and transparent rationale before changes.")


def infinite_scale_operational_intelligence_substrate() -> str:
    return _render("INFINITE-SCALE OPERATIONAL INTELLIGENCE SUBSTRATE - PHASE 1219", "operational-intelligence overview", "operational_intelligence.json", "operations", "instrumented", "blind", "Operations tracked", "Instrumented operations", "Blind operations", "Guardrail: operational intelligence should preserve privacy, interpretability, and accountable use before optimization.")


def recursive_management_simulation_engine() -> str:
    return _render("RECURSIVE MANAGEMENT SIMULATION ENGINE - PHASE 1220", "management-simulation overview", "management_simulation.json", "management_loops", "simulated", "chaotic", "Management loops tracked", "Simulated loops", "Chaotic loops", "Guardrail: management simulation should preserve humane leadership, role clarity, and bounded assumptions before prescription.")
