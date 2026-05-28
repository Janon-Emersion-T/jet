from __future__ import annotations

import json
from pathlib import Path


ALIGNMENT_FRONTIER_DIR = Path("storage/alignment_governance_frontier")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_negotiation_ai() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "negotiation_ai.json", {})
    negotiations = payload.get("negotiations", []) if isinstance(payload, dict) else []
    resolved = [item for item in negotiations if isinstance(item, dict) and item.get("status") == "resolved"]
    bounded = [item for item in negotiations if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("AUTONOMOUS NEGOTIATION AI - PHASE 691", "negotiation-ai overview", [f"Negotiations tracked: {len(negotiations)}", f"Resolved negotiations: {len(resolved)}", f"Bounded negotiations: {len(bounded)}"], "Guardrail: negotiation automation should stay policy-bounded, transparent, and human-escapable before use.")


def ethical_reasoning_framework() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "ethical_reasoning.json", {})
    scenarios = payload.get("scenarios", []) if isinstance(payload, dict) else []
    justified = [item for item in scenarios if isinstance(item, dict) and bool(item.get("justified", False))]
    contested = [item for item in scenarios if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("ETHICAL REASONING FRAMEWORK - PHASE 692", "ethical-reasoning overview", [f"Scenarios tracked: {len(scenarios)}", f"Justified scenarios: {len(justified)}", f"Contested scenarios: {len(contested)}"], "Guardrail: ethical reasoning should preserve dissent, context, and explicit value tradeoffs before recommendation.")


def moral_dilemma_simulator() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "moral_dilemmas.json", {})
    dilemmas = payload.get("dilemmas", []) if isinstance(payload, dict) else []
    explored = [item for item in dilemmas if isinstance(item, dict) and bool(item.get("explored", False))]
    unresolved = [item for item in dilemmas if isinstance(item, dict) and item.get("status") == "unresolved"]
    return _overview("MORAL DILEMMA SIMULATOR - PHASE 693", "moral-dilemma overview", [f"Dilemmas tracked: {len(dilemmas)}", f"Explored dilemmas: {len(explored)}", f"Unresolved dilemmas: {len(unresolved)}"], "Guardrail: dilemma simulation should remain pedagogical and explicit about normative uncertainty before guiding policy.")


def ai_alignment_monitoring() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "alignment_monitoring.json", {})
    monitors = payload.get("monitors", []) if isinstance(payload, dict) else []
    alerting = [item for item in monitors if isinstance(item, dict) and bool(item.get("alert", False))]
    healthy = [item for item in monitors if isinstance(item, dict) and item.get("status") == "healthy"]
    return _overview("AI ALIGNMENT MONITORING - PHASE 694", "alignment-monitoring overview", [f"Monitors tracked: {len(monitors)}", f"Alerting monitors: {len(alerting)}", f"Healthy monitors: {len(healthy)}"], "Guardrail: alignment monitoring should preserve traceability, calibrated thresholds, and human response paths before escalation.")


def human_values_adaptation_layer() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "values_adaptation.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    adapted = [item for item in profiles if isinstance(item, dict) and bool(item.get("adapted", False))]
    reviewed = [item for item in profiles if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("HUMAN VALUES ADAPTATION LAYER - PHASE 695", "values-adaptation overview", [f"Profiles tracked: {len(profiles)}", f"Adapted profiles: {len(adapted)}", f"Reviewed profiles: {len(reviewed)}"], "Guardrail: value adaptation should remain reversible, reviewable, and conservative before it changes behavior.")


def safe_recursive_self_improvement() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "safe_recursive_improvement.json", {})
    iterations = payload.get("iterations", []) if isinstance(payload, dict) else []
    sandboxed = [item for item in iterations if isinstance(item, dict) and bool(item.get("sandboxed", False))]
    approved = [item for item in iterations if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview("SAFE RECURSIVE SELF-IMPROVEMENT - PHASE 696", "recursive-improvement overview", [f"Iterations tracked: {len(iterations)}", f"Sandboxed iterations: {len(sandboxed)}", f"Approved iterations: {len(approved)}"], "Guardrail: self-improvement should remain sandboxed, monitored, and explicitly approval-gated before adoption.")


def autonomous_architecture_evolution() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "architecture_evolution.json", {})
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else []
    benchmarked = [item for item in candidates if isinstance(item, dict) and bool(item.get("benchmarked", False))]
    risky = [item for item in candidates if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AUTONOMOUS ARCHITECTURE EVOLUTION - PHASE 697", "architecture-evolution overview", [f"Candidates tracked: {len(candidates)}", f"Benchmarked candidates: {len(benchmarked)}", f"High-risk candidates: {len(risky)}"], "Guardrail: architecture evolution should preserve benchmark visibility, safety review, and rollback before promotion.")


def ai_civilization_governance_sandbox() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "civilization_governance.json", {})
    societies = payload.get("societies", []) if isinstance(payload, dict) else []
    simulated = [item for item in societies if isinstance(item, dict) and bool(item.get("simulated", False))]
    monitored = [item for item in societies if isinstance(item, dict) and bool(item.get("monitored", False))]
    return _overview("AI CIVILIZATION GOVERNANCE SANDBOX - PHASE 698", "civilization-governance overview", [f"Societies tracked: {len(societies)}", f"Simulated societies: {len(simulated)}", f"Monitored societies: {len(monitored)}"], "Guardrail: civilization governance sandboxes should remain clearly simulated, ethically framed, and researcher-supervised.")


def synthetic_economy_simulator() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "synthetic_economy.json", {})
    markets = payload.get("markets", []) if isinstance(payload, dict) else []
    active = [item for item in markets if isinstance(item, dict) and item.get("status") == "active"]
    unstable = [item for item in markets if isinstance(item, dict) and item.get("status") == "unstable"]
    return _overview("SYNTHETIC ECONOMY SIMULATOR - PHASE 699", "synthetic-economy overview", [f"Markets tracked: {len(markets)}", f"Active markets: {len(active)}", f"Unstable markets: {len(unstable)}"], "Guardrail: synthetic economy simulations should foreground assumptions, distributional effects, and uncertainty before interpretation.")


def autonomous_digital_nation_model() -> str:
    payload = _safe_json(ALIGNMENT_FRONTIER_DIR / "digital_nation.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    governed = [item for item in models if isinstance(item, dict) and bool(item.get("governed", False))]
    experimental = [item for item in models if isinstance(item, dict) and bool(item.get("experimental", False))]
    return _overview("AUTONOMOUS DIGITAL NATION MODEL - PHASE 700", "digital-nation overview", [f"Nation models: {len(models)}", f"Governed models: {len(governed)}", f"Experimental models: {len(experimental)}"], "Guardrail: digital nation models should remain explicitly simulated, policy-bounded, and subject to human governance before use.")
