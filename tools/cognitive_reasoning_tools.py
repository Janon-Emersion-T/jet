from __future__ import annotations

import json
from pathlib import Path


COGNITIVE_REASONING_DIR = Path("storage/cognitive_reasoning")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def edge_inference_orchestration() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "edge_inference.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    routed = [item for item in nodes if isinstance(item, dict) and bool(item.get("routed", False))]
    degraded = [item for item in nodes if isinstance(item, dict) and item.get("status") == "degraded"]
    return _overview("EDGE INFERENCE ORCHESTRATION - PHASE 671", "edge-inference overview", [f"Nodes tracked: {len(nodes)}", f"Routed nodes: {len(routed)}", f"Degraded nodes: {len(degraded)}"], "Guardrail: edge inference should balance latency, reliability, and model safety before shifting workloads.")


def neuromorphic_computing_research_layer() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "neuromorphic.json", {})
    prototypes = payload.get("prototypes", []) if isinstance(payload, dict) else []
    active = [item for item in prototypes if isinstance(item, dict) and item.get("status") == "active"]
    benchmarked = [item for item in prototypes if isinstance(item, dict) and bool(item.get("benchmarked", False))]
    return _overview("NEUROMORPHIC COMPUTING RESEARCH LAYER - PHASE 672", "neuromorphic-research overview", [f"Prototypes tracked: {len(prototypes)}", f"Active prototypes: {len(active)}", f"Benchmarked prototypes: {len(benchmarked)}"], "Guardrail: neuromorphic research should preserve experimental rigor and hardware constraints before claims of advantage.")


def brain_inspired_memory_architecture() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "brain_memory.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    hierarchical = [item for item in layers if isinstance(item, dict) and bool(item.get("hierarchical", False))]
    persistent = [item for item in layers if isinstance(item, dict) and bool(item.get("persistent", False))]
    return _overview("BRAIN-INSPIRED MEMORY ARCHITECTURE - PHASE 673", "brain-memory overview", [f"Memory layers: {len(layers)}", f"Hierarchical layers: {len(hierarchical)}", f"Persistent layers: {len(persistent)}"], "Guardrail: memory architecture experiments should remain interpretable, resource-aware, and benchmarked before integration.")


def cognitive_reasoning_framework() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "cognitive_reasoning.json", {})
    tasks = payload.get("tasks", []) if isinstance(payload, dict) else []
    solved = [item for item in tasks if isinstance(item, dict) and item.get("status") == "solved"]
    uncertain = [item for item in tasks if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("COGNITIVE REASONING FRAMEWORK - PHASE 674", "cognitive-reasoning overview", [f"Tasks tracked: {len(tasks)}", f"Solved tasks: {len(solved)}", f"Uncertain tasks: {len(uncertain)}"], "Guardrail: cognitive reasoning should preserve uncertainty and reasoning traces rather than overstating certainty.")


def symbolic_neural_hybrid_ai() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "symbolic_neural.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    hybrid = [item for item in models if isinstance(item, dict) and bool(item.get("hybrid", False))]
    explainable = [item for item in models if isinstance(item, dict) and bool(item.get("explainable", False))]
    return _overview("SYMBOLIC + NEURAL HYBRID AI - PHASE 675", "symbolic-neural overview", [f"Models tracked: {len(models)}", f"Hybrid models: {len(hybrid)}", f"Explainable models: {len(explainable)}"], "Guardrail: hybrid architectures should preserve clear interfaces, debuggability, and benchmark evidence before promotion.")


def causal_reasoning_engine() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "causal_reasoning.json", {})
    graphs = payload.get("graphs", []) if isinstance(payload, dict) else []
    validated = [item for item in graphs if isinstance(item, dict) and bool(item.get("validated", False))]
    contested = [item for item in graphs if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("CAUSAL REASONING ENGINE - PHASE 676", "causal-reasoning overview", [f"Graphs tracked: {len(graphs)}", f"Validated graphs: {len(validated)}", f"Contested graphs: {len(contested)}"], "Guardrail: causal reasoning should separate correlation from intervention claims and preserve contested assumptions.")


def ai_abstraction_layer() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "abstraction_layer.json", {})
    abstractions = payload.get("abstractions", []) if isinstance(payload, dict) else []
    reusable = [item for item in abstractions if isinstance(item, dict) and bool(item.get("reusable", False))]
    leaky = [item for item in abstractions if isinstance(item, dict) and bool(item.get("leaky", False))]
    return _overview("AI ABSTRACTION LAYER - PHASE 677", "abstraction-layer overview", [f"Abstractions tracked: {len(abstractions)}", f"Reusable abstractions: {len(reusable)}", f"Leaky abstractions: {len(leaky)}"], "Guardrail: abstractions should reduce complexity without hiding safety-critical behavior or evaluation assumptions.")


def autonomous_theorem_proving() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "theorem_proving.json", {})
    proofs = payload.get("proofs", []) if isinstance(payload, dict) else []
    complete = [item for item in proofs if isinstance(item, dict) and item.get("status") == "complete"]
    checked = [item for item in proofs if isinstance(item, dict) and bool(item.get("checked", False))]
    return _overview("AUTONOMOUS THEOREM PROVING - PHASE 678", "theorem-proving overview", [f"Proof attempts: {len(proofs)}", f"Completed proofs: {len(complete)}", f"Checked proofs: {len(checked)}"], "Guardrail: theorem proving results should remain formally checked and clearly bounded before they are trusted.")


def mathematical_reasoning_engine() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "math_reasoning.json", {})
    problems = payload.get("problems", []) if isinstance(payload, dict) else []
    solved = [item for item in problems if isinstance(item, dict) and item.get("status") == "solved"]
    verified = [item for item in problems if isinstance(item, dict) and bool(item.get("verified", False))]
    return _overview("MATHEMATICAL REASONING ENGINE - PHASE 679", "mathematical-reasoning overview", [f"Problems tracked: {len(problems)}", f"Solved problems: {len(solved)}", f"Verified solutions: {len(verified)}"], "Guardrail: mathematical reasoning should preserve proof visibility and verification rather than relying on opaque confidence.")


def ai_scientific_discovery_assistant() -> str:
    payload = _safe_json(COGNITIVE_REASONING_DIR / "scientific_discovery.json", {})
    discoveries = payload.get("discoveries", []) if isinstance(payload, dict) else []
    promising = [item for item in discoveries if isinstance(item, dict) and bool(item.get("promising", False))]
    replicated = [item for item in discoveries if isinstance(item, dict) and bool(item.get("replicated", False))]
    return _overview("AI SCIENTIFIC DISCOVERY ASSISTANT - PHASE 680", "scientific-discovery overview", [f"Discovery candidates: {len(discoveries)}", f"Promising candidates: {len(promising)}", f"Replicated candidates: {len(replicated)}"], "Guardrail: discovery assistance should preserve replication standards, uncertainty, and researcher oversight before claims.")
