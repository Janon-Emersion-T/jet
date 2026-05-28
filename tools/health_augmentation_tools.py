from __future__ import annotations

import json
from pathlib import Path


HEALTH_AUGMENTATION_DIR = Path("storage/health_augmentation")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(HEALTH_AUGMENTATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def autonomous_refugee_stabilization_engine() -> str:
    return _render("AUTONOMOUS REFUGEE STABILIZATION ENGINE - PHASE 1068", "refugee-stabilization overview", "refugee_stabilization.json", "settlements", "stabilized", "displaced", "Settlements tracked", "Stabilized settlements", "Displaced settlements", "Guardrail: refugee stabilization should preserve dignity, consent, and rights-respecting case management before action.")


def infinite_scale_healthcare_optimization_ai() -> str:
    return _render("INFINITE-SCALE HEALTHCARE OPTIMIZATION AI - PHASE 1069", "healthcare-optimization overview", "healthcare_optimization.json", "systems", "optimized", "overloaded", "Systems tracked", "Optimized systems", "Overloaded systems", "Guardrail: healthcare optimization should preserve patient safety, equity, and clinical oversight before operational use.")


def recursive_epidemiological_prediction_network() -> str:
    return _render("RECURSIVE EPIDEMIOLOGICAL PREDICTION NETWORK - PHASE 1070", "epidemiological-prediction overview", "epidemiological_prediction.json", "signals", "predicted", "outbreaking", "Signals tracked", "Predicted signals", "Outbreaking signals", "Guardrail: epidemiological prediction should preserve uncertainty ranges, public-health ethics, and expert review before action.")


def universal_biomedical_reasoning_substrate() -> str:
    return _render("UNIVERSAL BIOMEDICAL REASONING SUBSTRATE - PHASE 1071", "biomedical-reasoning overview", "biomedical_reasoning.json", "studies", "reasoned", "conflicted", "Studies tracked", "Reasoned studies", "Conflicted studies", "Guardrail: biomedical reasoning should preserve evidence hierarchies, safety review, and clinician accountability before recommendation.")


def adaptive_genomic_simulation_framework() -> str:
    return _render("ADAPTIVE GENOMIC SIMULATION FRAMEWORK - PHASE 1072", "genomic-simulation overview", "genomic_simulation.json", "genomes", "simulated", "uncertain", "Genomes tracked", "Simulated genomes", "Uncertain genomes", "Guardrail: genomic simulation should preserve consent, privacy, and non-discrimination before experimentation.")


def autonomous_longevity_research_engine() -> str:
    return _render("AUTONOMOUS LONGEVITY RESEARCH ENGINE - PHASE 1073", "longevity-research overview", "longevity_research.json", "trials", "active", "speculative", "Trials tracked", "Active trials", "Speculative trials", "Guardrail: longevity research should preserve human-subject ethics, evidence discipline, and equitable access before claims.")


def infinite_scale_cognitive_enhancement_ai() -> str:
    return _render("INFINITE-SCALE COGNITIVE ENHANCEMENT AI - PHASE 1074", "cognitive-enhancement overview", "cognitive_enhancement.json", "protocols", "enhancing", "uneven", "Protocols tracked", "Enhancing protocols", "Uneven protocols", "Guardrail: cognitive enhancement should preserve consent, reversibility, and fairness before deployment.")


def recursive_neuroadaptive_interface_layer() -> str:
    return _render("RECURSIVE NEUROADAPTIVE INTERFACE LAYER - PHASE 1075", "neuroadaptive-interface overview", "neuroadaptive_interface.json", "interfaces", "adaptive", "drifting", "Interfaces tracked", "Adaptive interfaces", "Drifting interfaces", "Guardrail: neuroadaptive interfaces should preserve user control, auditability, and safety cutoffs before live adaptation.")


def universal_prosthetic_cognition_integration() -> str:
    return _render("UNIVERSAL PROSTHETIC COGNITION INTEGRATION - PHASE 1076", "prosthetic-cognition overview", "prosthetic_cognition.json", "integrations", "integrated", "misaligned", "Integrations tracked", "Integrated systems", "Misaligned systems", "Guardrail: prosthetic cognition integration should preserve reliability, user agency, and clinical oversight before rollout.")


def adaptive_human_augmentation_framework() -> str:
    return _render("ADAPTIVE HUMAN AUGMENTATION FRAMEWORK - PHASE 1077", "human-augmentation overview", "human_augmentation.json", "augmentations", "adaptive", "risky", "Augmentations tracked", "Adaptive augmentations", "Risky augmentations", "Guardrail: human augmentation should preserve autonomy, informed consent, and equitable safeguards before deployment.")
