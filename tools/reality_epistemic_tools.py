from __future__ import annotations

import json
from pathlib import Path


REALITY_EPISTEMIC_DIR = Path("storage/reality_epistemic")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(REALITY_EPISTEMIC_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_reality_model_synchronization_ai() -> str:
    return _render("UNIVERSAL REALITY-MODEL SYNCHRONIZATION AI - PHASE 1271", "reality-model-synchronization overview", "reality_model_synchronization.json", "reality_models", "synchronized", "divergent", "Reality models tracked", "Synchronized models", "Divergent models", "Guardrail: reality-model synchronization should preserve disagreement visibility, provenance, and challenge paths before alignment.")


def adaptive_dimensional_cognition_substrate() -> str:
    return _render("ADAPTIVE DIMENSIONAL COGNITION SUBSTRATE - PHASE 1272", "dimensional-cognition overview", "dimensional_cognition.json", "cognition_planes", "adaptive", "disoriented", "Cognition planes tracked", "Adaptive planes", "Disoriented planes", "Guardrail: dimensional cognition should preserve interpretability, user grounding, and safe pacing before exploration.")


def autonomous_multiversal_exploration_engine() -> str:
    return _render("AUTONOMOUS MULTIVERSAL EXPLORATION ENGINE - PHASE 1273", "multiversal-exploration overview", "multiversal_exploration.json", "branches", "explored", "collapsed", "Branches tracked", "Explored branches", "Collapsed branches", "Guardrail: multiversal exploration should preserve uncertainty, explicit fictionality where applicable, and bounded inference before use.")


def infinite_scale_ontological_harmonizer() -> str:
    return _render("INFINITE-SCALE ONTOLOGICAL HARMONIZER - PHASE 1274", "ontological-harmonization overview", "ontological_harmonization.json", "ontologies", "harmonized", "conflicted", "Ontologies tracked", "Harmonized ontologies", "Conflicted ontologies", "Guardrail: ontology harmonization should preserve conceptual diversity, provenance, and challenge rights before convergence.")


def recursive_existence_simulation_framework() -> str:
    return _render("RECURSIVE EXISTENCE SIMULATION FRAMEWORK - PHASE 1275", "existence-simulation overview", "existence_simulation.json", "existence_runs", "simulated", "unstable", "Existence runs tracked", "Simulated runs", "Unstable runs", "Guardrail: existence simulation should preserve humility, ethical review, and non-deterministic framing before conclusions.")


def universal_truth_approximation_ai() -> str:
    return _render("UNIVERSAL TRUTH APPROXIMATION AI - PHASE 1276", "truth-approximation overview", "truth_approximation.json", "truth_estimates", "approximated", "distorted", "Truth estimates tracked", "Approximated truths", "Distorted truths", "Guardrail: truth approximation should preserve uncertainty disclosure, evidence traceability, and human judgment before claims.")


def adaptive_reality_interpretation_engine() -> str:
    return _render("ADAPTIVE REALITY INTERPRETATION ENGINE - PHASE 1277", "reality-interpretation overview", "reality_interpretation.json", "interpretations", "adaptive", "misleading", "Interpretations tracked", "Adaptive interpretations", "Misleading interpretations", "Guardrail: reality interpretation should preserve plurality, humility, and user agency before guidance.")


def autonomous_epistemological_framework() -> str:
    return _render("AUTONOMOUS EPISTEMOLOGICAL FRAMEWORK - PHASE 1278", "epistemological-framework overview", "epistemological_framework.json", "epistemic_models", "grounded", "circular", "Epistemic models tracked", "Grounded models", "Circular models", "Guardrail: epistemological frameworks should preserve explicit assumptions, falsifiability, and contestability before adoption.")


def infinite_scale_knowledge_integrity_substrate() -> str:
    return _render("INFINITE-SCALE KNOWLEDGE INTEGRITY SUBSTRATE - PHASE 1279", "knowledge-integrity overview", "knowledge_integrity.json", "knowledge_graphs", "verified", "corrupted", "Knowledge graphs tracked", "Verified graphs", "Corrupted graphs", "Guardrail: knowledge integrity should preserve provenance, tamper visibility, and repair workflows before dependency.")


def recursive_uncertainty_harmonization_ai() -> str:
    return _render("RECURSIVE UNCERTAINTY HARMONIZATION AI - PHASE 1280", "uncertainty-harmonization overview", "uncertainty_harmonization.json", "uncertainty_models", "harmonized", "overconfident", "Uncertainty models tracked", "Harmonized models", "Overconfident models", "Guardrail: uncertainty harmonization should preserve calibration, abstention, and human interpretation before action.")
