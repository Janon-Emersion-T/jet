from __future__ import annotations

import json
from pathlib import Path


DIPLOMATIC_RESILIENCE_DIR = Path("storage/diplomatic_resilience")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def infinite_context_diplomatic_simulation_engine() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "diplomatic_simulation.json", {})
    dialogues = payload.get("dialogues", []) if isinstance(payload, dict) else []
    simulated = [item for item in dialogues if isinstance(item, dict) and bool(item.get("simulated", False))]
    tense = [item for item in dialogues if isinstance(item, dict) and bool(item.get("tense", False))]
    return _overview("INFINITE-CONTEXT DIPLOMATIC SIMULATION ENGINE - PHASE 1011", "diplomatic-simulation overview", [f"Dialogues tracked: {len(dialogues)}", f"Simulated dialogues: {len(simulated)}", f"Tense dialogues: {len(tense)}"], "Guardrail: diplomatic simulation should preserve non-escalation, plural legitimacy, and transparent uncertainty before use.")


def human_machine_consensus_governance_ai() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "consensus_governance.json", {})
    councils = payload.get("councils", []) if isinstance(payload, dict) else []
    consensus = [item for item in councils if isinstance(item, dict) and bool(item.get("consensus", False))]
    fractured = [item for item in councils if isinstance(item, dict) and bool(item.get("fractured", False))]
    return _overview("HUMAN-MACHINE CONSENSUS GOVERNANCE AI - PHASE 1012", "consensus-governance overview", [f"Councils tracked: {len(councils)}", f"Consensus councils: {len(consensus)}", f"Fractured councils: {len(fractured)}"], "Guardrail: consensus governance should preserve dissent, appeals, and accountable human authority before decisions.")


def autonomous_policy_consequence_predictor() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "policy_consequence.json", {})
    policies = payload.get("policies", []) if isinstance(payload, dict) else []
    predicted = [item for item in policies if isinstance(item, dict) and bool(item.get("predicted", False))]
    inequitable = [item for item in policies if isinstance(item, dict) and bool(item.get("inequitable", False))]
    return _overview("AUTONOMOUS POLICY CONSEQUENCE PREDICTOR - PHASE 1013", "policy-consequence overview", [f"Policies tracked: {len(policies)}", f"Predicted policies: {len(predicted)}", f"Inequitable outcomes: {len(inequitable)}"], "Guardrail: policy consequence prediction should preserve fairness review, uncertainty, and public accountability before recommendation.")


def recursive_social_stability_optimizer() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "social_stability_optimizer.json", {})
    optimizers = payload.get("optimizers", []) if isinstance(payload, dict) else []
    stabilized = [item for item in optimizers if isinstance(item, dict) and bool(item.get("stabilized", False))]
    brittle = [item for item in optimizers if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("RECURSIVE SOCIAL STABILITY OPTIMIZER - PHASE 1014", "social-stability-optimizer overview", [f"Optimizers tracked: {len(optimizers)}", f"Stabilized optimizers: {len(stabilized)}", f"Brittle optimizers: {len(brittle)}"], "Guardrail: stability optimization should preserve rights, pluralism, and caution against optimizing for suppression or stasis.")


def universal_trust_propagation_framework() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "trust_propagation.json", {})
    channels = payload.get("channels", []) if isinstance(payload, dict) else []
    trusted = [item for item in channels if isinstance(item, dict) and bool(item.get("trusted", False))]
    weak = [item for item in channels if isinstance(item, dict) and bool(item.get("weak", False))]
    return _overview("UNIVERSAL TRUST PROPAGATION FRAMEWORK - PHASE 1015", "trust-propagation overview", [f"Channels tracked: {len(channels)}", f"Trusted channels: {len(trusted)}", f"Weak channels: {len(weak)}"], "Guardrail: trust propagation should preserve revocation, transparency, and decentralized accountability before adoption.")


def cross_domain_cognitive_fusion_engine() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "cognitive_fusion.json", {})
    domains = payload.get("domains", []) if isinstance(payload, dict) else []
    fused = [item for item in domains if isinstance(item, dict) and bool(item.get("fused", False))]
    noisy = [item for item in domains if isinstance(item, dict) and bool(item.get("noisy", False))]
    return _overview("CROSS-DOMAIN COGNITIVE FUSION ENGINE - PHASE 1016", "cognitive-fusion overview", [f"Domains tracked: {len(domains)}", f"Fused domains: {len(fused)}", f"Noisy domains: {len(noisy)}"], "Guardrail: cognitive fusion should preserve provenance, interpretability, and human review before synthesis.")


def autonomous_meta_learning_substrate() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "meta_learning_substrate.json", {})
    substrates = payload.get("substrates", []) if isinstance(payload, dict) else []
    learning = [item for item in substrates if isinstance(item, dict) and bool(item.get("learning", False))]
    drifting = [item for item in substrates if isinstance(item, dict) and bool(item.get("drifting", False))]
    return _overview("AUTONOMOUS META-LEARNING SUBSTRATE - PHASE 1017", "meta-learning-substrate overview", [f"Substrates tracked: {len(substrates)}", f"Learning substrates: {len(learning)}", f"Drifting substrates: {len(drifting)}"], "Guardrail: meta-learning substrates should preserve bounded adaptation, auditability, and rollback before long-run autonomy.")


def infinite_scale_recursive_planning_network() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "recursive_planning_network.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    recursive = [item for item in nodes if isinstance(item, dict) and bool(item.get("recursive", False))]
    overloaded = [item for item in nodes if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("INFINITE-SCALE RECURSIVE PLANNING NETWORK - PHASE 1018", "recursive-planning-network overview", [f"Nodes tracked: {len(nodes)}", f"Recursive nodes: {len(recursive)}", f"Overloaded nodes: {len(overloaded)}"], "Guardrail: recursive planning networks should preserve layered supervision and bounded execution before scaling.")


def planetary_adaptive_law_simulator() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "adaptive_law_simulator.json", {})
    statutes = payload.get("statutes", []) if isinstance(payload, dict) else []
    simulated = [item for item in statutes if isinstance(item, dict) and bool(item.get("simulated", False))]
    conflicted = [item for item in statutes if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("PLANETARY ADAPTIVE LAW SIMULATOR - PHASE 1019", "adaptive-law-simulator overview", [f"Statutes tracked: {len(statutes)}", f"Simulated statutes: {len(simulated)}", f"Conflicted statutes: {len(conflicted)}"], "Guardrail: adaptive law simulation should preserve jurisdictional nuance, rights review, and democratic legitimacy before advice.")


def distributed_resilience_cognition_layer() -> str:
    payload = _safe_json(DIPLOMATIC_RESILIENCE_DIR / "resilience_cognition_layer.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    resilient = [item for item in layers if isinstance(item, dict) and bool(item.get("resilient", False))]
    fragmented = [item for item in layers if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("DISTRIBUTED RESILIENCE COGNITION LAYER - PHASE 1020", "resilience-cognition overview", [f"Layers tracked: {len(layers)}", f"Resilient layers: {len(resilient)}", f"Fragmented layers: {len(fragmented)}"], "Guardrail: resilience cognition layers should preserve observability, locality, and human accountability before orchestration.")
