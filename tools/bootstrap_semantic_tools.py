from __future__ import annotations

import json
from pathlib import Path


BOOTSTRAP_SEMANTIC_DIR = Path("storage/bootstrap_semantic")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def recursive_autonomous_civilization_bootstrap_engine() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "civilization_bootstrap.json", {})
    bootstraps = payload.get("bootstraps", []) if isinstance(payload, dict) else []
    staged = [item for item in bootstraps if isinstance(item, dict) and bool(item.get("staged", False))]
    unstable = [item for item in bootstraps if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("RECURSIVE AUTONOMOUS CIVILIZATION BOOTSTRAP ENGINE - PHASE 1001", "civilization-bootstrap overview", [f"Bootstraps tracked: {len(bootstraps)}", f"Staged bootstraps: {len(staged)}", f"Unstable bootstraps: {len(unstable)}"], "Guardrail: bootstrap engines should remain sandboxed, reversible, and human-supervised before any autonomous rollout.")


def infinite_agent_coordination_substrate() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "agent_coordination_substrate.json", {})
    agents = payload.get("agents", []) if isinstance(payload, dict) else []
    coordinated = [item for item in agents if isinstance(item, dict) and bool(item.get("coordinated", False))]
    contested = [item for item in agents if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("INFINITE-AGENT COORDINATION SUBSTRATE - PHASE 1002", "agent-coordination overview", [f"Agents tracked: {len(agents)}", f"Coordinated agents: {len(coordinated)}", f"Contested agents: {len(contested)}"], "Guardrail: broad agent coordination should preserve role clarity, bounded autonomy, and clear human interruption paths before scale.")


def universal_semantic_compression_layer() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "semantic_compression.json", {})
    corpora = payload.get("corpora", []) if isinstance(payload, dict) else []
    compressed = [item for item in corpora if isinstance(item, dict) and bool(item.get("compressed", False))]
    lossy = [item for item in corpora if isinstance(item, dict) and bool(item.get("lossy", False))]
    return _overview("UNIVERSAL SEMANTIC COMPRESSION LAYER - PHASE 1003", "semantic-compression overview", [f"Corpora tracked: {len(corpora)}", f"Compressed corpora: {len(compressed)}", f"Lossy corpora: {len(lossy)}"], "Guardrail: semantic compression should preserve provenance, accuracy bounds, and transparent loss characteristics before use.")


def planetary_scale_adaptive_cognition_fabric() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "adaptive_cognition_fabric.json", {})
    regions = payload.get("regions", []) if isinstance(payload, dict) else []
    adaptive = [item for item in regions if isinstance(item, dict) and bool(item.get("adaptive", False))]
    fragmented = [item for item in regions if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("PLANETARY-SCALE ADAPTIVE COGNITION FABRIC - PHASE 1004", "adaptive-cognition-fabric overview", [f"Regions tracked: {len(regions)}", f"Adaptive regions: {len(adaptive)}", f"Fragmented regions: {len(fragmented)}"], "Guardrail: adaptive cognition fabrics should preserve local autonomy, observability, and safe rollback before federation.")


def autonomous_ontology_evolution_framework() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "ontology_evolution.json", {})
    ontologies = payload.get("ontologies", []) if isinstance(payload, dict) else []
    evolved = [item for item in ontologies if isinstance(item, dict) and bool(item.get("evolved", False))]
    conflicted = [item for item in ontologies if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("AUTONOMOUS ONTOLOGY EVOLUTION FRAMEWORK - PHASE 1005", "ontology-evolution overview", [f"Ontologies tracked: {len(ontologies)}", f"Evolved ontologies: {len(evolved)}", f"Conflicted ontologies: {len(conflicted)}"], "Guardrail: ontology evolution should preserve human review, interoperability, and explicit ambiguity before convergence.")


def hyperdimensional_knowledge_indexing_engine() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "hyperdimensional_indexing.json", {})
    indices = payload.get("indices", []) if isinstance(payload, dict) else []
    indexed = [item for item in indices if isinstance(item, dict) and bool(item.get("indexed", False))]
    unstable = [item for item in indices if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("HYPERDIMENSIONAL KNOWLEDGE INDEXING ENGINE - PHASE 1006", "hyperdimensional-indexing overview", [f"Indices tracked: {len(indices)}", f"Indexed dimensions: {len(indexed)}", f"Unstable dimensions: {len(unstable)}"], "Guardrail: high-dimensional indexing should preserve provenance, retrieval transparency, and bounded inference before adoption.")


def recursive_ethics_simulation_runtime() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "ethics_runtime.json", {})
    runtimes = payload.get("runtimes", []) if isinstance(payload, dict) else []
    running = [item for item in runtimes if isinstance(item, dict) and bool(item.get("running", False))]
    runaway = [item for item in runtimes if isinstance(item, dict) and bool(item.get("runaway", False))]
    return _overview("RECURSIVE ETHICS SIMULATION RUNTIME - PHASE 1007", "ethics-runtime overview", [f"Runtimes tracked: {len(runtimes)}", f"Running runtimes: {len(running)}", f"Runaway runtimes: {len(runaway)}"], "Guardrail: ethics runtimes should remain sandboxed, plural, and haltable before any normative influence.")


def universal_memory_harmonization_system() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "memory_harmonization.json", {})
    memories = payload.get("memories", []) if isinstance(payload, dict) else []
    harmonized = [item for item in memories if isinstance(item, dict) and bool(item.get("harmonized", False))]
    drifted = [item for item in memories if isinstance(item, dict) and bool(item.get("drifted", False))]
    return _overview("UNIVERSAL MEMORY HARMONIZATION SYSTEM - PHASE 1008", "memory-harmonization overview", [f"Memories tracked: {len(memories)}", f"Harmonized memories: {len(harmonized)}", f"Drifted memories: {len(drifted)}"], "Guardrail: memory harmonization should preserve provenance, consent, and correction mechanisms before federation.")


def autonomous_collective_reasoning_lattice() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "reasoning_lattice.json", {})
    nodes = payload.get("nodes", []) if isinstance(payload, dict) else []
    reasoned = [item for item in nodes if isinstance(item, dict) and bool(item.get("reasoned", False))]
    conflicted = [item for item in nodes if isinstance(item, dict) and bool(item.get("conflicted", False))]
    return _overview("AUTONOMOUS COLLECTIVE REASONING LATTICE - PHASE 1009", "reasoning-lattice overview", [f"Nodes tracked: {len(nodes)}", f"Reasoned nodes: {len(reasoned)}", f"Conflicted nodes: {len(conflicted)}"], "Guardrail: collective reasoning lattices should preserve disagreement, attribution, and non-coercive synthesis before coordination.")


def self_organizing_planetary_intelligence_grid() -> str:
    payload = _safe_json(BOOTSTRAP_SEMANTIC_DIR / "planetary_intelligence_grid.json", {})
    cells = payload.get("cells", []) if isinstance(payload, dict) else []
    organized = [item for item in cells if isinstance(item, dict) and bool(item.get("organized", False))]
    unstable = [item for item in cells if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("SELF-ORGANIZING PLANETARY INTELLIGENCE GRID - PHASE 1010", "planetary-intelligence-grid overview", [f"Cells tracked: {len(cells)}", f"Organized cells: {len(organized)}", f"Unstable cells: {len(unstable)}"], "Guardrail: self-organizing intelligence grids should preserve observability, layered fail-safes, and human override before scale.")
