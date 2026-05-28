from __future__ import annotations

import json
from pathlib import Path


METAVERSE_GOVERNANCE_DIR = Path("storage/metaverse_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(METAVERSE_GOVERNANCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def autonomous_immersive_experience_substrate() -> str:
    return _render("AUTONOMOUS IMMERSIVE EXPERIENCE SUBSTRATE - PHASE 1098", "immersive-experience overview", "immersive_experience.json", "experiences", "immersive", "unsafe", "Experiences tracked", "Immersive experiences", "Unsafe experiences", "Guardrail: immersive experiences should preserve consent, comfort, and clear exit controls before launch.")


def infinite_scale_augmented_cognition_layer() -> str:
    return _render("INFINITE-SCALE AUGMENTED COGNITION LAYER - PHASE 1099", "augmented-cognition overview", "augmented_cognition.json", "augmentations", "amplified", "overloaded", "Augmentations tracked", "Amplified augmentations", "Overloaded augmentations", "Guardrail: augmented cognition should preserve agency, interpretability, and bounded reliance before deployment.")


def recursive_metaverse_governance_ai() -> str:
    return _render("RECURSIVE METAVERSE GOVERNANCE AI - PHASE 1100", "metaverse-governance overview", "metaverse_governance.json", "realms", "governed", "captured", "Realms tracked", "Governed realms", "Captured realms", "Guardrail: metaverse governance should preserve rights, appeals, and accountable human authority before enforcement.")
