from __future__ import annotations

import json
from pathlib import Path


DIGITAL_ECONOMY_DIR = Path("storage/digital_economy")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_key: str, risk_key: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(DIGITAL_ECONOMY_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_key, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_key, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_digital_rights_framework() -> str:
    return _render("UNIVERSAL DIGITAL RIGHTS FRAMEWORK - PHASE 1101", "digital-rights overview", "digital_rights.json", "rights", "protected", "violated", "Rights tracked", "Protected rights", "Violated rights", "Guardrail: digital-rights frameworks should preserve due process, portability, and accountable enforcement before action.")


def adaptive_avatar_identity_engine() -> str:
    return _render("ADAPTIVE AVATAR IDENTITY ENGINE - PHASE 1102", "avatar-identity overview", "avatar_identity.json", "avatars", "verified", "drifting", "Avatars tracked", "Verified avatars", "Drifting avatars", "Guardrail: avatar identity systems should preserve consent, pseudonymity options, and revocation before synchronization.")


def autonomous_virtual_economy_simulator() -> str:
    return _render("AUTONOMOUS VIRTUAL ECONOMY SIMULATOR - PHASE 1103", "virtual-economy overview", "virtual_economy.json", "economies", "simulated", "inflating", "Economies tracked", "Simulated economies", "Inflating economies", "Guardrail: virtual economy simulation should preserve fairness, anti-exploitation safeguards, and human oversight before rollout.")


def infinite_scale_social_interaction_ai() -> str:
    return _render("INFINITE-SCALE SOCIAL INTERACTION AI - PHASE 1104", "social-interaction overview", "social_interaction.json", "communities", "engaged", "polarized", "Communities tracked", "Engaged communities", "Polarized communities", "Guardrail: social interaction systems should preserve safety, non-manipulation, and user control before optimization.")


def recursive_trust_economy_framework() -> str:
    return _render("RECURSIVE TRUST ECONOMY FRAMEWORK - PHASE 1105", "trust-economy overview", "trust_economy.json", "exchanges", "trusted", "fragile", "Exchanges tracked", "Trusted exchanges", "Fragile exchanges", "Guardrail: trust economies should preserve transparency, contestability, and anti-coercive incentives before deployment.")


def universal_reputation_cognition_layer() -> str:
    return _render("UNIVERSAL REPUTATION COGNITION LAYER - PHASE 1106", "reputation-cognition overview", "reputation_cognition.json", "profiles", "credible", "contested", "Profiles tracked", "Credible profiles", "Contested profiles", "Guardrail: reputation cognition should preserve context, appeals, and anti-bias safeguards before ranking.")


def adaptive_cooperative_incentive_engine() -> str:
    return _render("ADAPTIVE COOPERATIVE INCENTIVE ENGINE - PHASE 1107", "cooperative-incentives overview", "cooperative_incentives.json", "programs", "aligned", "misaligned", "Programs tracked", "Aligned programs", "Misaligned programs", "Guardrail: incentive engines should preserve consent, dignity, and non-exploitative coordination before optimization.")


def autonomous_decentralized_collaboration_mesh() -> str:
    return _render("AUTONOMOUS DECENTRALIZED COLLABORATION MESH - PHASE 1108", "decentralized-collaboration overview", "decentralized_collaboration.json", "meshes", "coordinated", "fragmented", "Meshes tracked", "Coordinated meshes", "Fragmented meshes", "Guardrail: decentralized collaboration should preserve transparency, local autonomy, and clear accountability before delegation.")


def infinite_scale_innovation_marketplace_ai() -> str:
    return _render("INFINITE-SCALE INNOVATION MARKETPLACE AI - PHASE 1109", "innovation-marketplace overview", "innovation_marketplace.json", "markets", "active", "captured", "Markets tracked", "Active markets", "Captured markets", "Guardrail: innovation marketplaces should preserve open access, anti-monopoly safeguards, and reviewable ranking before automation.")


def recursive_scientific_discovery_economy() -> str:
    return _render("RECURSIVE SCIENTIFIC DISCOVERY ECONOMY - PHASE 1110", "scientific-discovery-economy overview", "scientific_discovery_economy.json", "pipelines", "funded", "stalled", "Pipelines tracked", "Funded pipelines", "Stalled pipelines", "Guardrail: discovery economies should preserve rigor, replication incentives, and public-interest alignment before optimization.")
