from __future__ import annotations

import json
from pathlib import Path


COGNITION_REALITY_DIR = Path("storage/cognition_reality")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def global_ethical_reasoning_network() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "ethical_reasoning_network.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    active = [item for item in nodes if isinstance(item, dict) and item.get("status") == "active"]
    disputed = [item for item in nodes if isinstance(item, dict) and bool(item.get("disputed", False))]
    return _overview("GLOBAL ETHICAL REASONING NETWORK - PHASE 931", "ethical-reasoning-network overview", [f"Nodes tracked: {len(nodes)}", f"Active nodes: {len(active)}", f"Disputed nodes: {len(disputed)}"], "Guardrail: ethical reasoning networks should preserve pluralism, transparency, and contested space before consensus.")


def autonomous_planetary_health_monitor() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "planetary_health.json", {})
    indicators = payload.get("indicators", []) if isinstance(payload, dict) else []
    monitored = [item for item in indicators if isinstance(item, dict) and bool(item.get("monitored", False))]
    critical = [item for item in indicators if isinstance(item, dict) and item.get("status") == "critical"]
    return _overview("AUTONOMOUS PLANETARY HEALTH MONITOR - PHASE 932", "planetary-health overview", [f"Indicators tracked: {len(indicators)}", f"Monitored indicators: {len(monitored)}", f"Critical indicators: {len(critical)}"], "Guardrail: planetary health monitoring should preserve scientific integrity and public accountability before action.")


def civilization_scale_simulation_runtime() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "civilization_runtime.json", {})
    runtimes = payload.get("runtimes", []) if isinstance(payload, dict) else []
    running = [item for item in runtimes if isinstance(item, dict) and bool(item.get("running", False))]
    unstable = [item for item in runtimes if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("CIVILIZATION-SCALE SIMULATION RUNTIME - PHASE 933", "civilization-runtime overview", [f"Runtimes tracked: {len(runtimes)}", f"Running runtimes: {len(running)}", f"Unstable runtimes: {len(unstable)}"], "Guardrail: civilization-scale runtimes should remain sandboxed, instrumented, and clearly separated from real governance.")


def universal_semantic_cognition_layer() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "semantic_cognition.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    aligned = [item for item in layers if isinstance(item, dict) and bool(item.get("aligned", False))]
    noisy = [item for item in layers if isinstance(item, dict) and bool(item.get("noisy", False))]
    return _overview("UNIVERSAL SEMANTIC COGNITION LAYER - PHASE 934", "semantic-cognition overview", [f"Layers tracked: {len(layers)}", f"Aligned layers: {len(aligned)}", f"Noisy layers: {len(noisy)}"], "Guardrail: semantic cognition layers should preserve provenance, ambiguity visibility, and bounded inference before deployment.")


def distributed_adaptive_intelligence_substrate() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "adaptive_substrate.json", {})
    substrates = payload.get("substrates", []) if isinstance(payload, dict) else []
    adaptive = [item for item in substrates if isinstance(item, dict) and bool(item.get("adaptive", False))]
    fractured = [item for item in substrates if isinstance(item, dict) and bool(item.get("fractured", False))]
    return _overview("DISTRIBUTED ADAPTIVE INTELLIGENCE SUBSTRATE - PHASE 935", "adaptive-substrate overview", [f"Substrates tracked: {len(substrates)}", f"Adaptive substrates: {len(adaptive)}", f"Fractured substrates: {len(fractured)}"], "Guardrail: adaptive substrates should preserve observability, fault boundaries, and governance clarity before scale.")


def infinite_context_reasoning_framework() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "infinite_context_reasoning.json", {})
    contexts = payload.get("contexts", []) if isinstance(payload, dict) else []
    retained = [item for item in contexts if isinstance(item, dict) and bool(item.get("retained", False))]
    overloaded = [item for item in contexts if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("INFINITE-CONTEXT REASONING FRAMEWORK - PHASE 936", "infinite-context-reasoning overview", [f"Contexts tracked: {len(contexts)}", f"Retained contexts: {len(retained)}", f"Overloaded contexts: {len(overloaded)}"], "Guardrail: large-context reasoning should preserve relevance filtering, privacy, and explicit uncertainty before synthesis.")


def ai_assisted_human_transcendence_sandbox() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "human_transcendence.json", {})
    experiments = payload.get("experiments", []) if isinstance(payload, dict) else []
    sandboxed = [item for item in experiments if isinstance(item, dict) and bool(item.get("sandboxed", False))]
    risky = [item for item in experiments if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("AI-ASSISTED HUMAN TRANSCENDENCE SANDBOX - PHASE 937", "human-transcendence overview", [f"Experiments tracked: {len(experiments)}", f"Sandboxed experiments: {len(sandboxed)}", f"High-risk experiments: {len(risky)}"], "Guardrail: transcendence experiments should remain speculative, consent-driven, and firmly sandboxed before interpretation.")


def universal_interoperability_cognition_mesh() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "cognition_mesh.json", {})
    meshes = payload.get("meshes", []) if isinstance(payload, dict) else []
    interoperable = [item for item in meshes if isinstance(item, dict) and bool(item.get("interoperable", False))]
    drifted = [item for item in meshes if isinstance(item, dict) and bool(item.get("drifted", False))]
    return _overview("UNIVERSAL INTEROPERABILITY COGNITION MESH - PHASE 938", "cognition-mesh overview", [f"Meshes tracked: {len(meshes)}", f"Interoperable meshes: {len(interoperable)}", f"Drifted meshes: {len(drifted)}"], "Guardrail: cognition meshes should preserve open standards, bounded trust, and rollback before federation.")


def planetary_scale_recursive_planning_ai() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "recursive_planning.json", {})
    plans = payload.get("plans", []) if isinstance(payload, dict) else []
    recursive = [item for item in plans if isinstance(item, dict) and bool(item.get("recursive", False))]
    unstable = [item for item in plans if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("PLANETARY-SCALE RECURSIVE PLANNING AI - PHASE 939", "recursive-planning overview", [f"Plans tracked: {len(plans)}", f"Recursive plans: {len(recursive)}", f"Unstable plans: {len(unstable)}"], "Guardrail: recursive planning should preserve human oversight and explicit braking mechanisms before optimization loops close.")


def autonomous_reality_model_refinement_system() -> str:
    payload = _safe_json(COGNITION_REALITY_DIR / "reality_model_refinement.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    refined = [item for item in models if isinstance(item, dict) and bool(item.get("refined", False))]
    mismatched = [item for item in models if isinstance(item, dict) and bool(item.get("mismatched", False))]
    return _overview("AUTONOMOUS REALITY-MODEL REFINEMENT SYSTEM - PHASE 940", "reality-model-refinement overview", [f"Models tracked: {len(models)}", f"Refined models: {len(refined)}", f"Mismatched models: {len(mismatched)}"], "Guardrail: reality-model refinement should preserve empirical grounding and resist self-confirming drift before use.")
