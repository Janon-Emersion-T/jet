from __future__ import annotations

import json
from pathlib import Path


EXPERIMENTATION_DIR = Path("storage/experimentation_ml")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def autonomous_experimentation_planner() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "experimentation_planner.json", {})
    experiments = payload.get("experiments", []) if isinstance(payload, dict) else []
    prioritized = [item for item in experiments if isinstance(item, dict) and bool(item.get("prioritized", False))]
    approved = [item for item in experiments if isinstance(item, dict) and item.get("status") == "approved"]
    return _overview("AUTONOMOUS EXPERIMENTATION PLANNER - PHASE 601", "experimentation-planning overview", [f"Experiments tracked: {len(experiments)}", f"Prioritized experiments: {len(prioritized)}", f"Approved experiments: {len(approved)}"], "Guardrail: experimentation planning should preserve explicit hypotheses, approval state, and measurable outcomes before launching work.")


def ai_hypothesis_generation() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "hypothesis_generation.json", {})
    hypotheses = payload.get("hypotheses", []) if isinstance(payload, dict) else []
    testable = [item for item in hypotheses if isinstance(item, dict) and bool(item.get("testable", False))]
    reviewed = [item for item in hypotheses if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI HYPOTHESIS GENERATION - PHASE 602", "hypothesis-generation overview", [f"Hypotheses tracked: {len(hypotheses)}", f"Testable hypotheses: {len(testable)}", f"Reviewed hypotheses: {len(reviewed)}"], "Guardrail: generated hypotheses should remain falsifiable, source-aware, and researcher-reviewed before they steer experiments.")


def data_science_orchestration_layer() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "data_science_orchestration.json", {})
    workflows = payload.get("workflows", []) if isinstance(payload, dict) else []
    automated = [item for item in workflows if isinstance(item, dict) and bool(item.get("automated", False))]
    blocked = [item for item in workflows if isinstance(item, dict) and item.get("status") == "blocked"]
    return _overview("DATA SCIENCE ORCHESTRATION LAYER - PHASE 603", "data-science-orchestration overview", [f"Workflows tracked: {len(workflows)}", f"Automated workflows: {len(automated)}", f"Blocked workflows: {len(blocked)}"], "Guardrail: orchestration should preserve reproducibility, ownership, and dependency clarity before automating research workflows.")


def automated_ml_pipeline_manager() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "ml_pipeline_manager.json", {})
    pipelines = payload.get("pipelines", []) if isinstance(payload, dict) else []
    healthy = [item for item in pipelines if isinstance(item, dict) and item.get("status") == "healthy"]
    retraining = [item for item in pipelines if isinstance(item, dict) and bool(item.get("retraining", False))]
    return _overview("AUTOMATED ML PIPELINE MANAGER - PHASE 604", "ml-pipeline overview", [f"Pipelines tracked: {len(pipelines)}", f"Healthy pipelines: {len(healthy)}", f"Retraining pipelines: {len(retraining)}"], "Guardrail: pipeline automation should favor reproducibility, rollback paths, and data lineage before promoting models.")


def ai_dataset_cleaner() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "dataset_cleaner.json", {})
    datasets = payload.get("datasets", []) if isinstance(payload, dict) else []
    cleaned = [item for item in datasets if isinstance(item, dict) and bool(item.get("cleaned", False))]
    flagged = [item for item in datasets if isinstance(item, dict) and bool(item.get("flagged", False))]
    return _overview("AI DATASET CLEANER - PHASE 605", "dataset-cleaning overview", [f"Datasets tracked: {len(datasets)}", f"Cleaned datasets: {len(cleaned)}", f"Flagged datasets: {len(flagged)}"], "Guardrail: dataset cleaning should preserve provenance, avoid silent mutation, and surface risky records before altering training inputs.")


def feature_engineering_assistant() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "feature_engineering.json", {})
    features = payload.get("features", []) if isinstance(payload, dict) else []
    selected = [item for item in features if isinstance(item, dict) and bool(item.get("selected", False))]
    drift_sensitive = [item for item in features if isinstance(item, dict) and bool(item.get("drift_sensitive", False))]
    return _overview("FEATURE ENGINEERING ASSISTANT - PHASE 606", "feature-engineering overview", [f"Features tracked: {len(features)}", f"Selected features: {len(selected)}", f"Drift-sensitive features: {len(drift_sensitive)}"], "Guardrail: feature engineering should favor explainability, leakage prevention, and reproducibility before feeding models.")


def ai_model_lifecycle_manager() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "model_lifecycle.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    deployed = [item for item in models if isinstance(item, dict) and item.get("stage") == "deployed"]
    archived = [item for item in models if isinstance(item, dict) and item.get("stage") == "archived"]
    return _overview("AI MODEL LIFECYCLE MANAGER - PHASE 607", "model-lifecycle overview", [f"Models tracked: {len(models)}", f"Deployed models: {len(deployed)}", f"Archived models: {len(archived)}"], "Guardrail: lifecycle management should make stage transitions explicit, auditable, and reversible before deployment.")


def continuous_model_evaluation() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "continuous_evaluation.json", {})
    evaluations = payload.get("evaluations", []) if isinstance(payload, dict) else []
    passing = [item for item in evaluations if isinstance(item, dict) and item.get("status") == "passing"]
    failing = [item for item in evaluations if isinstance(item, dict) and item.get("status") == "failing"]
    return _overview("CONTINUOUS MODEL EVALUATION - PHASE 608", "continuous-evaluation overview", [f"Evaluations tracked: {len(evaluations)}", f"Passing evaluations: {len(passing)}", f"Failing evaluations: {len(failing)}"], "Guardrail: continuous evaluation should highlight metric drift, benchmark regressions, and uncertainty before automatic rollout.")


def ai_drift_detection_system() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "drift_detection.json", {})
    monitors = payload.get("monitors", []) if isinstance(payload, dict) else []
    drift = [item for item in monitors if isinstance(item, dict) and item.get("drift") == "detected"]
    stable = [item for item in monitors if isinstance(item, dict) and item.get("drift") == "stable"]
    return _overview("AI DRIFT DETECTION SYSTEM - PHASE 609", "drift-detection overview", [f"Monitors tracked: {len(monitors)}", f"Detected drift monitors: {len(drift)}", f"Stable monitors: {len(stable)}"], "Guardrail: drift detection should separate signal from noise and include remediation context before changing production behavior.")


def synthetic_data_generator() -> str:
    payload = _safe_json(EXPERIMENTATION_DIR / "synthetic_data.json", {})
    datasets = payload.get("datasets", []) if isinstance(payload, dict) else []
    privacy = [item for item in datasets if isinstance(item, dict) and bool(item.get("privacy_checked", False))]
    balanced = [item for item in datasets if isinstance(item, dict) and bool(item.get("balanced", False))]
    return _overview("SYNTHETIC DATA GENERATOR - PHASE 610", "synthetic-data overview", [f"Synthetic datasets: {len(datasets)}", f"Privacy-checked datasets: {len(privacy)}", f"Balanced datasets: {len(balanced)}"], "Guardrail: synthetic data should preserve privacy, avoid harmful leakage, and document fidelity limits before use.")
