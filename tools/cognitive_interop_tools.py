from __future__ import annotations

import json
from pathlib import Path


COG_INTEROP_DIR = Path("storage/cognitive_interop")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def probabilistic_reality_modeling() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "probabilistic_reality.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    calibrated = [item for item in models if isinstance(item, dict) and bool(item.get("calibrated", False))]
    unstable = [item for item in models if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("PROBABILISTIC REALITY MODELING - PHASE 821", "probabilistic-reality overview", [f"Models tracked: {len(models)}", f"Calibrated models: {len(calibrated)}", f"Unstable models: {len(unstable)}"], "Guardrail: probabilistic reality models should preserve uncertainty, falsifiability, and careful communication before use.")


def ai_driven_ontology_framework() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "ontology_framework.json", {})
    ontologies = payload.get("ontologies", []) if isinstance(payload, dict) else []
    aligned = [item for item in ontologies if isinstance(item, dict) and bool(item.get("aligned", False))]
    ambiguous = [item for item in ontologies if isinstance(item, dict) and bool(item.get("ambiguous", False))]
    return _overview("AI-DRIVEN ONTOLOGY FRAMEWORK - PHASE 822", "ontology-framework overview", [f"Ontologies tracked: {len(ontologies)}", f"Aligned ontologies: {len(aligned)}", f"Ambiguous ontologies: {len(ambiguous)}"], "Guardrail: ontology generation should preserve human review, interoperability, and ambiguity visibility before standardization.")


def universal_semantic_graph() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "semantic_graph.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    linked = [item for item in nodes if isinstance(item, dict) and bool(item.get("linked", False))]
    orphaned = [item for item in nodes if isinstance(item, dict) and bool(item.get("orphaned", False))]
    return _overview("UNIVERSAL SEMANTIC GRAPH - PHASE 823", "universal-semantic-graph overview", [f"Nodes tracked: {len(nodes)}", f"Linked nodes: {len(linked)}", f"Orphaned nodes: {len(orphaned)}"], "Guardrail: universal semantic graphs should preserve provenance, access control, and correction paths before broad federation.")


def infinite_scale_memory_indexing() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "memory_indexing.json", {})
    shards = payload.get("shards", []) if isinstance(payload, dict) else []
    indexed = [item for item in shards if isinstance(item, dict) and bool(item.get("indexed", False))]
    stale = [item for item in shards if isinstance(item, dict) and item.get("status") == "stale"]
    return _overview("INFINITE-SCALE MEMORY INDEXING - PHASE 824", "memory-indexing overview", [f"Shards tracked: {len(shards)}", f"Indexed shards: {len(indexed)}", f"Stale shards: {len(stale)}"], "Guardrail: large-scale memory indexing should preserve retention boundaries, provenance, and efficient correction before expansion.")


def hyper_personalized_intelligence_layer() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "hyper_personalized_intelligence.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    tailored = [item for item in profiles if isinstance(item, dict) and bool(item.get("tailored", False))]
    bounded = [item for item in profiles if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("HYPER-PERSONALIZED INTELLIGENCE LAYER - PHASE 825", "hyper-personalized-intelligence overview", [f"Profiles tracked: {len(profiles)}", f"Tailored profiles: {len(tailored)}", f"Bounded profiles: {len(bounded)}"], "Guardrail: personalization should preserve consent, privacy, and bounded adaptation before deeper profiling.")


def autonomous_digital_twin_civilization() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "digital_twin_civilization.json", {})
    twins = payload.get("twins", []) if isinstance(payload, dict) else []
    mirrored = [item for item in twins if isinstance(item, dict) and bool(item.get("mirrored", False))]
    volatile = [item for item in twins if isinstance(item, dict) and item.get("status") == "volatile"]
    return _overview("AUTONOMOUS DIGITAL TWIN CIVILIZATION - PHASE 826", "digital-twin-civilization overview", [f"Twins tracked: {len(twins)}", f"Mirrored twins: {len(mirrored)}", f"Volatile twins: {len(volatile)}"], "Guardrail: digital twin civilizations should remain sandboxed, non-prescriptive, and transparent about abstraction limits.")


def ai_driven_evolutionary_modeling() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "evolutionary_modeling.json", {})
    populations = payload.get("populations", []) if isinstance(payload, dict) else []
    modeled = [item for item in populations if isinstance(item, dict) and bool(item.get("modeled", False))]
    divergent = [item for item in populations if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("AI-DRIVEN EVOLUTIONARY MODELING - PHASE 827", "evolutionary-modeling overview", [f"Populations tracked: {len(populations)}", f"Modeled populations: {len(modeled)}", f"Divergent populations: {len(divergent)}"], "Guardrail: evolutionary modeling should preserve ethical boundaries and avoid deterministic interpretations of complex systems.")


def recursive_intelligence_scaling() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "recursive_scaling.json", {})
    loops = payload.get("loops", []) if isinstance(payload, dict) else []
    stabilized = [item for item in loops if isinstance(item, dict) and bool(item.get("stabilized", False))]
    runaway = [item for item in loops if isinstance(item, dict) and bool(item.get("runaway", False))]
    return _overview("RECURSIVE INTELLIGENCE SCALING - PHASE 828", "recursive-scaling overview", [f"Loops tracked: {len(loops)}", f"Stabilized loops: {len(stabilized)}", f"Runaway loops: {len(runaway)}"], "Guardrail: recursive scaling should preserve brakes, auditability, and explicit containment before iteration.")


def planetary_cognitive_operating_system() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "planetary_cognitive_os.json", {})
    regions = payload.get("regions", []) if isinstance(payload, dict) else []
    integrated = [item for item in regions if isinstance(item, dict) and bool(item.get("integrated", False))]
    fragmented = [item for item in regions if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("PLANETARY COGNITIVE OPERATING SYSTEM - PHASE 829", "planetary-cognitive-os overview", [f"Regions tracked: {len(regions)}", f"Integrated regions: {len(integrated)}", f"Fragmented regions: {len(fragmented)}"], "Guardrail: planetary cognition layers should preserve local autonomy, transparency, and federated governance before unification.")


def unified_human_machine_interface() -> str:
    payload = _safe_json(COG_INTEROP_DIR / "human_machine_interface.json", {})
    interfaces = payload.get("interfaces", []) if isinstance(payload, dict) else []
    interoperable = [item for item in interfaces if isinstance(item, dict) and bool(item.get("interoperable", False))]
    inaccessible = [item for item in interfaces if isinstance(item, dict) and bool(item.get("inaccessible", False))]
    return _overview("UNIFIED HUMAN-MACHINE INTERFACE - PHASE 830", "human-machine-interface overview", [f"Interfaces tracked: {len(interfaces)}", f"Interoperable interfaces: {len(interoperable)}", f"Inaccessible interfaces: {len(inaccessible)}"], "Guardrail: unified interfaces should preserve accessibility, user agency, and clear fallbacks before consolidation.")
