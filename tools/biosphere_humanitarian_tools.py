from __future__ import annotations

import json
from pathlib import Path


BIOSPHERE_HUMANITARIAN_DIR = Path("storage/biosphere_humanitarian")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(BIOSPHERE_HUMANITARIAN_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def autonomous_climate_stabilization_simulator() -> str:
    return _render("AUTONOMOUS CLIMATE STABILIZATION SIMULATOR - PHASE 1058", "climate-stabilization overview", "climate_stabilization.json", "simulations", "stabilized", "volatile", "Simulations tracked", "Stabilized simulations", "Volatile simulations", "Guardrail: climate stabilization simulation should preserve uncertainty, justice, and international accountability before recommendation.")


def infinite_scale_biosphere_monitoring_network() -> str:
    return _render("INFINITE-SCALE BIOSPHERE MONITORING NETWORK - PHASE 1059", "biosphere-monitoring overview", "biosphere_monitoring.json", "sensors", "active", "blind", "Sensors tracked", "Active sensors", "Blind sensors", "Guardrail: biosphere monitoring should preserve ecological context, data integrity, and long-term stewardship before coordination.")


def recursive_biodiversity_restoration_engine() -> str:
    return _render("RECURSIVE BIODIVERSITY RESTORATION ENGINE - PHASE 1060", "biodiversity-restoration overview", "biodiversity_restoration.json", "restorations", "restored", "declining", "Restorations tracked", "Restored ecosystems", "Declining ecosystems", "Guardrail: biodiversity restoration should preserve habitat complexity, local ecology, and non-invasive methods before action.")


def universal_agricultural_intelligence_substrate() -> str:
    return _render("UNIVERSAL AGRICULTURAL INTELLIGENCE SUBSTRATE - PHASE 1061", "agricultural-intelligence overview", "agricultural_intelligence.json", "farms", "optimized", "stressed", "Farms tracked", "Optimized farms", "Stressed farms", "Guardrail: agricultural intelligence should preserve farmer agency, soil health, and regional diversity before deployment.")


def adaptive_ecosystem_resilience_framework() -> str:
    return _render("ADAPTIVE ECOSYSTEM RESILIENCE FRAMEWORK - PHASE 1062", "ecosystem-resilience overview", "ecosystem_resilience.json", "ecosystems", "resilient", "fractured", "Ecosystems tracked", "Resilient ecosystems", "Fractured ecosystems", "Guardrail: ecosystem resilience planning should preserve local stewardship, biodiversity, and slow-variable monitoring before intervention.")


def autonomous_oceanic_stewardship_cognition() -> str:
    return _render("AUTONOMOUS OCEANIC STEWARDSHIP COGNITION - PHASE 1063", "oceanic-stewardship overview", "oceanic_stewardship.json", "zones", "protected", "overfished", "Zones tracked", "Protected zones", "Overfished zones", "Guardrail: oceanic stewardship should preserve marine rights, coastal livelihoods, and ecological thresholds before optimization.")


def infinite_scale_environmental_simulation_runtime() -> str:
    return _render("INFINITE-SCALE ENVIRONMENTAL SIMULATION RUNTIME - PHASE 1064", "environmental-simulation overview", "environmental_simulation.json", "runs", "calibrated", "divergent", "Runs tracked", "Calibrated runs", "Divergent runs", "Guardrail: environmental simulation should preserve model transparency, calibration discipline, and reviewable assumptions before use.")


def recursive_planetary_recovery_ai() -> str:
    return _render("RECURSIVE PLANETARY RECOVERY AI - PHASE 1065", "planetary-recovery overview", "planetary_recovery.json", "recoveries", "recovering", "stalled", "Recoveries tracked", "Recovering plans", "Stalled plans", "Guardrail: planetary recovery should preserve equity, local participation, and long-horizon accountability before prioritization.")


def universal_humanitarian_logistics_framework() -> str:
    return _render("UNIVERSAL HUMANITARIAN LOGISTICS FRAMEWORK - PHASE 1066", "humanitarian-logistics overview", "humanitarian_logistics.json", "missions", "delivered", "blocked", "Missions tracked", "Delivered missions", "Blocked missions", "Guardrail: humanitarian logistics should preserve neutrality, dignity, and consent-aware distribution before dispatch.")


def adaptive_crisis_coordination_intelligence() -> str:
    return _render("ADAPTIVE CRISIS COORDINATION INTELLIGENCE - PHASE 1067", "crisis-coordination overview", "crisis_coordination.json", "responses", "coordinated", "fragmented", "Responses tracked", "Coordinated responses", "Fragmented responses", "Guardrail: crisis coordination should preserve incident clarity, human leadership, and communications redundancy before escalation.")
