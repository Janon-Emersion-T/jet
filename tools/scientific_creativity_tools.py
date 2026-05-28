from __future__ import annotations

import json
from pathlib import Path


SCIENTIFIC_CREATIVITY_DIR = Path("storage/scientific_creativity")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def universal_scientific_synthesis_engine() -> str:
    payload = _safe_json(SCIENTIFIC_CREATIVITY_DIR / "scientific_synthesis.json", {})
    syntheses = payload.get("syntheses", []) if isinstance(payload, dict) else []
    integrated = [item for item in syntheses if isinstance(item, dict) and bool(item.get("integrated", False))]
    contested = [item for item in syntheses if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview(
        "UNIVERSAL SCIENTIFIC SYNTHESIS ENGINE - PHASE 1026",
        "scientific-synthesis overview",
        [
            f"Syntheses tracked: {len(syntheses)}",
            f"Integrated syntheses: {len(integrated)}",
            f"Contested syntheses: {len(contested)}",
        ],
        "Guardrail: scientific synthesis should preserve evidence quality, disciplinary nuance, and uncertainty disclosure before recommendation.",
    )


def autonomous_innovation_acceleration_matrix() -> str:
    payload = _safe_json(SCIENTIFIC_CREATIVITY_DIR / "innovation_acceleration.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    accelerated = [item for item in programs if isinstance(item, dict) and bool(item.get("accelerated", False))]
    stalled = [item for item in programs if isinstance(item, dict) and bool(item.get("stalled", False))]
    return _overview(
        "AUTONOMOUS INNOVATION ACCELERATION MATRIX - PHASE 1027",
        "innovation-acceleration overview",
        [
            f"Programs tracked: {len(programs)}",
            f"Accelerated programs: {len(accelerated)}",
            f"Stalled programs: {len(stalled)}",
        ],
        "Guardrail: innovation acceleration should preserve safety review, replication discipline, and public-interest constraints before scaling.",
    )


def infinite_scale_creativity_orchestration_layer() -> str:
    payload = _safe_json(SCIENTIFIC_CREATIVITY_DIR / "creativity_orchestration.json", {})
    ensembles = payload.get("ensembles", []) if isinstance(payload, dict) else []
    orchestrated = [item for item in ensembles if isinstance(item, dict) and bool(item.get("orchestrated", False))]
    chaotic = [item for item in ensembles if isinstance(item, dict) and bool(item.get("chaotic", False))]
    return _overview(
        "INFINITE-SCALE CREATIVITY ORCHESTRATION LAYER - PHASE 1028",
        "creativity-orchestration overview",
        [
            f"Ensembles tracked: {len(ensembles)}",
            f"Orchestrated ensembles: {len(orchestrated)}",
            f"Chaotic ensembles: {len(chaotic)}",
        ],
        "Guardrail: creativity orchestration should preserve authorship clarity, consent, and human curation before publication.",
    )
