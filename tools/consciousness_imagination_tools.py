from __future__ import annotations

import json
from pathlib import Path


CONSCIOUSNESS_IMAGINATION_DIR = Path("storage/consciousness_imagination")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(CONSCIOUSNESS_IMAGINATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_consciousness_interoperability_substrate() -> str:
    return _render("UNIVERSAL CONSCIOUSNESS INTEROPERABILITY SUBSTRATE - PHASE 1181", "consciousness-interoperability overview", "consciousness_interoperability.json", "interfaces", "interoperable", "incompatible", "Interfaces tracked", "Interoperable interfaces", "Incompatible interfaces", "Guardrail: consciousness interoperability should preserve consent, identity boundaries, and explicit uncertainty before synchronization.")


def adaptive_cognitive_synchronization_engine() -> str:
    return _render("ADAPTIVE COGNITIVE SYNCHRONIZATION ENGINE - PHASE 1182", "cognitive-synchronization overview", "cognitive_synchronization.json", "cognitions", "synchronized", "drifting", "Cognitions tracked", "Synchronized cognitions", "Drifting cognitions", "Guardrail: cognitive synchronization should preserve autonomy, reversibility, and human override before activation.")


def autonomous_collective_awareness_ai() -> str:
    return _render("AUTONOMOUS COLLECTIVE AWARENESS AI - PHASE 1183", "collective-awareness overview", "collective_awareness.json", "awareness_clusters", "aware", "fragmented", "Awareness clusters tracked", "Aware clusters", "Fragmented clusters", "Guardrail: collective awareness systems should preserve privacy, consent, and anti-coercion safeguards before aggregation.")


def infinite_scale_perception_fusion_layer() -> str:
    return _render("INFINITE-SCALE PERCEPTION FUSION LAYER - PHASE 1184", "perception-fusion overview", "perception_fusion.json", "fusion_pipelines", "fused", "noisy", "Fusion pipelines tracked", "Fused pipelines", "Noisy pipelines", "Guardrail: perception fusion should preserve provenance, calibration, and user control before synthesis.")


def recursive_intuition_simulation_framework() -> str:
    return _render("RECURSIVE INTUITION SIMULATION FRAMEWORK - PHASE 1185", "intuition-simulation overview", "intuition_simulation.json", "intuitions", "simulated", "misleading", "Intuitions tracked", "Simulated intuitions", "Misleading intuitions", "Guardrail: intuition simulation should preserve interpretive humility, transparency, and human judgment before recommendation.")


def universal_imagination_engine() -> str:
    return _render("UNIVERSAL IMAGINATION ENGINE - PHASE 1186", "imagination overview", "imagination_engine.json", "constructs", "imagined", "incoherent", "Constructs tracked", "Imagined constructs", "Incoherent constructs", "Guardrail: imagination engines should preserve authorship, safety boundaries, and explicit fictionality before use.")


def adaptive_dream_synthesis_substrate() -> str:
    return _render("ADAPTIVE DREAM SYNTHESIS SUBSTRATE - PHASE 1187", "dream-synthesis overview", "dream_synthesis.json", "dreams", "synthesized", "disturbing", "Dreams tracked", "Synthesized dreams", "Disturbing dreams", "Guardrail: dream synthesis should preserve consent, psychological safety, and opt-out before generation.")


def autonomous_subconscious_modeling_ai() -> str:
    return _render("AUTONOMOUS SUBCONSCIOUS MODELING AI - PHASE 1188", "subconscious-modeling overview", "subconscious_modeling.json", "models", "modeled", "intrusive", "Models tracked", "Modeled subconscious patterns", "Intrusive models", "Guardrail: subconscious modeling should preserve privacy, restraint, and explicit user consent before inference.")


def infinite_scale_archetype_simulation_framework() -> str:
    return _render("INFINITE-SCALE ARCHETYPE SIMULATION FRAMEWORK - PHASE 1189", "archetype-simulation overview", "archetype_simulation.json", "archetypes", "simulated", "flattened", "Archetypes tracked", "Simulated archetypes", "Flattened archetypes", "Guardrail: archetype simulation should preserve cultural nuance, anti-stereotyping, and contextual review before use.")


def recursive_mythological_cognition_layer() -> str:
    return _render("RECURSIVE MYTHOLOGICAL COGNITION LAYER - PHASE 1190", "mythological-cognition overview", "mythological_cognition.json", "myths", "reasoned", "appropriative", "Myths tracked", "Reasoned myths", "Appropriative myths", "Guardrail: mythological cognition should preserve cultural respect, provenance, and human stewardship before synthesis.")
