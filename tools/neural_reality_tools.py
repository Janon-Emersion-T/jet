from __future__ import annotations

import json
from pathlib import Path


NEURAL_REALITY_DIR = Path("storage/neural_reality")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def neural_internet_architecture() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "neural_internet.json", {})
    meshes = payload.get("meshes", []) if isinstance(payload, dict) else []
    linked = [item for item in meshes if isinstance(item, dict) and bool(item.get("linked", False))]
    unstable = [item for item in meshes if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("NEURAL INTERNET ARCHITECTURE - PHASE 851", "neural-internet overview", [f"Meshes tracked: {len(meshes)}", f"Linked meshes: {len(linked)}", f"Unstable meshes: {len(unstable)}"], "Guardrail: neural-networked infrastructure should preserve consent, safety boundaries, and human override before connectivity expands.")


def universal_cognitive_api() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "cognitive_api.json", {})
    endpoints = payload.get("endpoints", []) if isinstance(payload, dict) else []
    standardized = [item for item in endpoints if isinstance(item, dict) and bool(item.get("standardized", False))]
    incompatible = [item for item in endpoints if isinstance(item, dict) and bool(item.get("incompatible", False))]
    return _overview("UNIVERSAL COGNITIVE API - PHASE 852", "cognitive-api overview", [f"Endpoints tracked: {len(endpoints)}", f"Standardized endpoints: {len(standardized)}", f"Incompatible endpoints: {len(incompatible)}"], "Guardrail: cognitive APIs should preserve interoperability, access control, and clear version boundaries before federation.")


def autonomous_software_civilization() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "software_civilization.json", {})
    agents = payload.get("agents", []) if isinstance(payload, dict) else []
    coordinated = [item for item in agents if isinstance(item, dict) and bool(item.get("coordinated", False))]
    divergent = [item for item in agents if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("AUTONOMOUS SOFTWARE CIVILIZATION - PHASE 853", "software-civilization overview", [f"Agents tracked: {len(agents)}", f"Coordinated agents: {len(coordinated)}", f"Divergent agents: {len(divergent)}"], "Guardrail: software civilizations should remain sandboxed, observable, and non-authoritative outside simulation contexts.")


def ai_generated_operating_environments() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "operating_environments.json", {})
    environments = payload.get("environments", []) if isinstance(payload, dict) else []
    generated = [item for item in environments if isinstance(item, dict) and bool(item.get("generated", False))]
    unsafe = [item for item in environments if isinstance(item, dict) and bool(item.get("unsafe", False))]
    return _overview("AI-GENERATED OPERATING ENVIRONMENTS - PHASE 854", "operating-environments overview", [f"Environments tracked: {len(environments)}", f"Generated environments: {len(generated)}", f"Unsafe environments: {len(unsafe)}"], "Guardrail: generated operating environments should preserve containment, rollback, and operator review before activation.")


def adaptive_reality_interfaces() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "adaptive_reality.json", {})
    interfaces = payload.get("interfaces", []) if isinstance(payload, dict) else []
    adaptive = [item for item in interfaces if isinstance(item, dict) and bool(item.get("adaptive", False))]
    disorienting = [item for item in interfaces if isinstance(item, dict) and bool(item.get("disorienting", False))]
    return _overview("ADAPTIVE REALITY INTERFACES - PHASE 855", "adaptive-reality overview", [f"Interfaces tracked: {len(interfaces)}", f"Adaptive interfaces: {len(adaptive)}", f"Disorienting interfaces: {len(disorienting)}"], "Guardrail: adaptive interfaces should preserve accessibility, user agency, and cognitive safety before personalization deepens.")


def intelligent_spatial_computing() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "spatial_computing.json", {})
    spaces = payload.get("spaces", []) if isinstance(payload, dict) else []
    mapped = [item for item in spaces if isinstance(item, dict) and bool(item.get("mapped", False))]
    occluded = [item for item in spaces if isinstance(item, dict) and bool(item.get("occluded", False))]
    return _overview("INTELLIGENT SPATIAL COMPUTING - PHASE 856", "spatial-computing overview", [f"Spaces tracked: {len(spaces)}", f"Mapped spaces: {len(mapped)}", f"Occluded spaces: {len(occluded)}"], "Guardrail: spatial computing should preserve privacy, environmental awareness, and clear confidence limits before automation.")


def ai_generated_simulation_layers() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "simulation_layers.json", {})
    layers = payload.get("layers", []) if isinstance(payload, dict) else []
    generated = [item for item in layers if isinstance(item, dict) and bool(item.get("generated", False))]
    inconsistent = [item for item in layers if isinstance(item, dict) and bool(item.get("inconsistent", False))]
    return _overview("AI-GENERATED SIMULATION LAYERS - PHASE 857", "simulation-layers overview", [f"Layers tracked: {len(layers)}", f"Generated layers: {len(generated)}", f"Inconsistent layers: {len(inconsistent)}"], "Guardrail: generated simulation layers should remain auditable and clearly separated from real-world ground truth.")


def persistent_digital_ecosystems() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "digital_ecosystems.json", {})
    ecosystems = payload.get("ecosystems", []) if isinstance(payload, dict) else []
    persistent = [item for item in ecosystems if isinstance(item, dict) and bool(item.get("persistent", False))]
    brittle = [item for item in ecosystems if isinstance(item, dict) and bool(item.get("brittle", False))]
    return _overview("PERSISTENT DIGITAL ECOSYSTEMS - PHASE 858", "digital-ecosystems overview", [f"Ecosystems tracked: {len(ecosystems)}", f"Persistent ecosystems: {len(persistent)}", f"Brittle ecosystems: {len(brittle)}"], "Guardrail: persistent ecosystems should preserve resilience, ownership clarity, and safe shutdown pathways before scale.")


def universal_digital_assistant_framework() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "digital_assistant_framework.json", {})
    assistants = payload.get("assistants", []) if isinstance(payload, dict) else []
    integrated = [item for item in assistants if isinstance(item, dict) and bool(item.get("integrated", False))]
    restricted = [item for item in assistants if isinstance(item, dict) and bool(item.get("restricted", False))]
    return _overview("UNIVERSAL DIGITAL ASSISTANT FRAMEWORK - PHASE 859", "digital-assistant-framework overview", [f"Assistants tracked: {len(assistants)}", f"Integrated assistants: {len(integrated)}", f"Restricted assistants: {len(restricted)}"], "Guardrail: universal assistants should preserve bounded permissions, explainability, and user control before wide delegation.")


def human_cognition_preservation_layer() -> str:
    payload = _safe_json(NEURAL_REALITY_DIR / "cognition_preservation.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    preserved = [item for item in profiles if isinstance(item, dict) and bool(item.get("preserved", False))]
    degraded = [item for item in profiles if isinstance(item, dict) and bool(item.get("degraded", False))]
    return _overview("HUMAN COGNITION PRESERVATION LAYER - PHASE 860", "cognition-preservation overview", [f"Profiles tracked: {len(profiles)}", f"Preserved profiles: {len(preserved)}", f"Degraded profiles: {len(degraded)}"], "Guardrail: cognition preservation should preserve consent, dignity, and clear clinical boundaries before retention or intervention.")
