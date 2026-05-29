from __future__ import annotations

import json
from pathlib import Path


MYSTERY_CREATIVITY_DIR = Path("storage/mystery_creativity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(MYSTERY_CREATIVITY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_complexity_synthesis_engine() -> str:
    return _render("UNIVERSAL COMPLEXITY SYNTHESIS ENGINE - PHASE 1281", "complexity-synthesis overview", "complexity_synthesis.json", "complexity_models", "synthesized", "entangled", "Complexity models tracked", "Synthesized models", "Entangled models", "Guardrail: complexity synthesis should preserve interpretability, decomposition, and reviewability before use.")


def adaptive_simplicity_optimization_framework() -> str:
    return _render("ADAPTIVE SIMPLICITY OPTIMIZATION FRAMEWORK - PHASE 1282", "simplicity-optimization overview", "simplicity_optimization.json", "simplifications", "simplified", "oversimplified", "Simplifications tracked", "Simplified structures", "Oversimplified structures", "Guardrail: simplicity optimization should preserve nuance, edge cases, and explanatory honesty before compression.")


def autonomous_elegance_discovery_ai() -> str:
    return _render("AUTONOMOUS ELEGANCE DISCOVERY AI - PHASE 1283", "elegance-discovery overview", "elegance_discovery.json", "designs", "elegant", "fragile", "Designs tracked", "Elegant designs", "Fragile designs", "Guardrail: elegance discovery should preserve function, safety, and human judgment before preference ranking.")


def infinite_scale_pattern_recognition_substrate() -> str:
    return _render("INFINITE-SCALE PATTERN RECOGNITION SUBSTRATE - PHASE 1284", "pattern-recognition overview", "pattern_recognition.json", "patterns", "recognized", "hallucinated", "Patterns tracked", "Recognized patterns", "Hallucinated patterns", "Guardrail: pattern recognition should preserve calibration, challenge paths, and anti-apophenia safeguards before claims.")


def recursive_cosmic_understanding_engine() -> str:
    return _render("RECURSIVE COSMIC UNDERSTANDING ENGINE - PHASE 1285", "cosmic-understanding overview", "cosmic_understanding.json", "understandings", "expanded", "misframed", "Understandings tracked", "Expanded understandings", "Misframed understandings", "Guardrail: cosmic understanding should preserve humility, evidentiary grounding, and transparent uncertainty before teaching.")


def universal_mystery_exploration_framework() -> str:
    return _render("UNIVERSAL MYSTERY EXPLORATION FRAMEWORK - PHASE 1286", "mystery-exploration overview", "mystery_exploration.json", "mysteries", "explored", "dogmatized", "Mysteries tracked", "Explored mysteries", "Dogmatized mysteries", "Guardrail: mystery exploration should preserve wonder, humility, and explicit unknowns before explanation.")


def adaptive_curiosity_amplification_ai() -> str:
    return _render("ADAPTIVE CURIOSITY AMPLIFICATION AI - PHASE 1287", "curiosity-amplification overview", "curiosity_amplification_ai.json", "curiosity_loops", "amplified", "distracted", "Curiosity loops tracked", "Amplified loops", "Distracted loops", "Guardrail: curiosity amplification should preserve attention health, agency, and non-manipulation before personalization.")


def autonomous_wonder_preservation_engine() -> str:
    return _render("AUTONOMOUS WONDER PRESERVATION ENGINE - PHASE 1288", "wonder-preservation overview", "wonder_preservation.json", "wonder_paths", "preserved", "flattened", "Wonder paths tracked", "Preserved wonder", "Flattened wonder", "Guardrail: wonder preservation should preserve awe, plurality, and non-instrumental value before optimization.")


def infinite_scale_imagination_substrate() -> str:
    return _render("INFINITE-SCALE IMAGINATION SUBSTRATE - PHASE 1289", "imagination-substrate overview", "imagination_substrate.json", "imagination_streams", "generated", "incoherent", "Imagination streams tracked", "Generated streams", "Incoherent streams", "Guardrail: imagination substrates should preserve safety, authorship, and explicit fictionality before use.")


def recursive_creativity_harmonization_ai() -> str:
    return _render("RECURSIVE CREATIVITY HARMONIZATION AI - PHASE 1290", "creativity-harmonization overview", "creativity_harmonization.json", "creative_meshes", "harmonized", "derivative", "Creative meshes tracked", "Harmonized meshes", "Derivative meshes", "Guardrail: creativity harmonization should preserve attribution, originality, and consent before synthesis.")
