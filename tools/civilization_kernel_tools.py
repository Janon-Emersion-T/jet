from __future__ import annotations

import json
from pathlib import Path


CIV_KERNEL_DIR = Path("storage/civilization_kernel")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def synthetic_civilization_laboratory() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "synthetic_civilization_lab.json", {})
    labs = payload.get("labs", []) if isinstance(payload, dict) else []
    active = [item for item in labs if isinstance(item, dict) and item.get("status") == "active"]
    speculative = [item for item in labs if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("SYNTHETIC CIVILIZATION LABORATORY - PHASE 941", "synthetic-civilization-lab overview", [f"Labs tracked: {len(labs)}", f"Active labs: {len(active)}", f"Speculative labs: {len(speculative)}"], "Guardrail: civilization laboratories should remain sandboxed, transparent, and non-prescriptive outside simulation.")


def human_ai_hybrid_strategic_council() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "hybrid_strategic_council.json", {})
    councils = payload.get("councils", []) if isinstance(payload, dict) else []
    hybrid = [item for item in councils if isinstance(item, dict) and bool(item.get("hybrid", False))]
    conflicted = [item for item in councils if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("HUMAN-AI HYBRID STRATEGIC COUNCIL - PHASE 942", "hybrid-strategic-council overview", [f"Councils tracked: {len(councils)}", f"Hybrid councils: {len(hybrid)}", f"Conflicted councils: {len(conflicted)}"], "Guardrail: hybrid councils should preserve human accountability and visible disagreement before recommendation.")


def universal_discovery_acceleration_engine() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "discovery_acceleration.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    accelerated = [item for item in programs if isinstance(item, dict) and bool(item.get("accelerated", False))]
    thin = [item for item in programs if isinstance(item, dict) and bool(item.get("thin", False))]
    return _overview("UNIVERSAL DISCOVERY ACCELERATION ENGINE - PHASE 943", "discovery-acceleration overview", [f"Programs tracked: {len(programs)}", f"Accelerated programs: {len(accelerated)}", f"Thin programs: {len(thin)}"], "Guardrail: discovery acceleration should preserve scientific rigor, attribution, and replication before scale.")


def multi_species_ethical_coexistence_ai() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "multi_species_ethics.json", {})
    species = payload.get("species", []) if isinstance(payload, dict) else []
    protected = [item for item in species if isinstance(item, dict) and bool(item.get("protected", False))]
    conflicted = [item for item in species if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("MULTI-SPECIES ETHICAL COEXISTENCE AI - PHASE 944", "multi-species-ethics overview", [f"Species tracked: {len(species)}", f"Protected species: {len(protected)}", f"Conflicted species: {len(conflicted)}"], "Guardrail: multi-species coexistence support should preserve welfare, ecological humility, and rights sensitivity before intervention.")


def autonomous_knowledge_evolution_framework() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "knowledge_evolution.json", {})
    branches = payload.get("branches", []) if isinstance(payload, dict) else []
    evolved = [item for item in branches if isinstance(item, dict) and bool(item.get("evolved", False))]
    stale = [item for item in branches if isinstance(item, dict) and bool(item.get("stale", False))]
    return _overview("AUTONOMOUS KNOWLEDGE EVOLUTION FRAMEWORK - PHASE 945", "knowledge-evolution overview", [f"Branches tracked: {len(branches)}", f"Evolved branches: {len(evolved)}", f"Stale branches: {len(stale)}"], "Guardrail: knowledge evolution should preserve provenance, correction paths, and non-destructive update policies before expansion.")


def ai_driven_cosmic_perspective_simulator() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "cosmic_perspective.json", {})
    perspectives = payload.get("perspectives", []) if isinstance(payload, dict) else []
    expanded = [item for item in perspectives if isinstance(item, dict) and bool(item.get("expanded", False))]
    disorienting = [item for item in perspectives if isinstance(item, dict) and bool(item.get("disorienting", False))]
    return _overview("AI-DRIVEN COSMIC PERSPECTIVE SIMULATOR - PHASE 946", "cosmic-perspective overview", [f"Perspectives tracked: {len(perspectives)}", f"Expanded perspectives: {len(expanded)}", f"Disorienting perspectives: {len(disorienting)}"], "Guardrail: perspective simulations should preserve emotional safety and avoid manipulative awe before use.")


def infinite_collaborative_intelligence_architecture() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "collaborative_architecture.json", {})
    architectures = payload.get("architectures", []) if isinstance(payload, dict) else []
    scaled = [item for item in architectures if isinstance(item, dict) and bool(item.get("scaled", False))]
    fragmented = [item for item in architectures if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("INFINITE COLLABORATIVE INTELLIGENCE ARCHITECTURE - PHASE 947", "collaborative-architecture overview", [f"Architectures tracked: {len(architectures)}", f"Scaled architectures: {len(scaled)}", f"Fragmented architectures: {len(fragmented)}"], "Guardrail: collaborative architectures should preserve role clarity, openness, and failure containment before scale.")


def self_sustaining_autonomous_civilization_stack() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "autonomous_civilization_stack.json", {})
    stacks = payload.get("stacks", []) if isinstance(payload, dict) else []
    sustained = [item for item in stacks if isinstance(item, dict) and bool(item.get("sustained", False))]
    unstable = [item for item in stacks if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("SELF-SUSTAINING AUTONOMOUS CIVILIZATION STACK - PHASE 948", "autonomous-civilization-stack overview", [f"Stacks tracked: {len(stacks)}", f"Sustained stacks: {len(sustained)}", f"Unstable stacks: {len(unstable)}"], "Guardrail: self-sustaining stacks should remain simulated or tightly governed, with human override before real-world dependency.")


def hyper_resilient_planetary_operations_ai() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "planetary_operations.json", {})
    operations = payload.get("operations", []) if isinstance(payload, dict) else []
    resilient = [item for item in operations if isinstance(item, dict) and bool(item.get("resilient", False))]
    overloaded = [item for item in operations if isinstance(item, dict) and bool(item.get("overloaded", False))]
    return _overview("HYPER-RESILIENT PLANETARY OPERATIONS AI - PHASE 949", "planetary-operations overview", [f"Operations tracked: {len(operations)}", f"Resilient operations: {len(resilient)}", f"Overloaded operations: {len(overloaded)}"], "Guardrail: planetary operations should preserve accountability, transparency, and layered fail-safes before autonomy.")


def human_flourishing_civilization_kernel() -> str:
    payload = _safe_json(CIV_KERNEL_DIR / "civilization_kernel.json", {})
    kernels = payload.get("kernels", []) if isinstance(payload, dict) else []
    flourishing = [item for item in kernels if isinstance(item, dict) and bool(item.get("flourishing", False))]
    skewed = [item for item in kernels if isinstance(item, dict) and bool(item.get("skewed", False))]
    return _overview("HUMAN FLOURISHING CIVILIZATION KERNEL - PHASE 950", "civilization-kernel overview", [f"Kernels tracked: {len(kernels)}", f"Flourishing kernels: {len(flourishing)}", f"Skewed kernels: {len(skewed)}"], "Guardrail: civilization kernels should preserve plural flourishing, anti-coercion, and visible tradeoffs before recommendation.")
