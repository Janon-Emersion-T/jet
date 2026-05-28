from __future__ import annotations

import json
from pathlib import Path


LEADERSHIP_COORDINATION_DIR = Path("storage/leadership_coordination")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, pos: str, risk: str, key_label: str, pos_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(LEADERSHIP_COORDINATION_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(pos, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{pos_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def universal_leadership_augmentation_ai() -> str:
    return _render("UNIVERSAL LEADERSHIP AUGMENTATION AI - PHASE 1221", "leadership-augmentation overview", "leadership_augmentation.json", "leaders", "augmented", "isolated", "Leaders tracked", "Augmented leaders", "Isolated leaders", "Guardrail: leadership augmentation should preserve accountability, humility, and non-delegable human judgment before use.")


def adaptive_executive_cognition_framework() -> str:
    return _render("ADAPTIVE EXECUTIVE COGNITION FRAMEWORK - PHASE 1222", "executive-cognition overview", "executive_cognition.json", "executives", "supported", "overloaded", "Executives tracked", "Supported executives", "Overloaded executives", "Guardrail: executive cognition tools should preserve rest, ethical judgment, and non-coercive adoption before optimization.")


def autonomous_board_level_reasoning_engine() -> str:
    return _render("AUTONOMOUS BOARD-LEVEL REASONING ENGINE - PHASE 1223", "board-reasoning overview", "board_reasoning.json", "board_cases", "reasoned", "conflicted", "Board cases tracked", "Reasoned cases", "Conflicted cases", "Guardrail: board-level reasoning should preserve fiduciary accountability, dissent, and transparent evidence before recommendation.")


def infinite_scale_strategic_planning_substrate() -> str:
    return _render("INFINITE-SCALE STRATEGIC PLANNING SUBSTRATE - PHASE 1224", "strategic-planning overview", "strategic_planning.json", "strategies", "planned", "fragmented", "Strategies tracked", "Planned strategies", "Fragmented strategies", "Guardrail: strategic planning should preserve mission clarity, risk review, and accountable approvals before coordination.")


def recursive_mission_alignment_ai() -> str:
    return _render("RECURSIVE MISSION ALIGNMENT AI - PHASE 1225", "mission-alignment overview", "mission_alignment.json", "missions", "aligned", "drifting", "Missions tracked", "Aligned missions", "Drifting missions", "Guardrail: mission alignment should preserve authentic purpose, revision rights, and human deliberation before enforcement.")


def universal_purpose_driven_governance_framework() -> str:
    return _render("UNIVERSAL PURPOSE-DRIVEN GOVERNANCE FRAMEWORK - PHASE 1226", "purpose-governance overview", "purpose_governance.json", "governance_loops", "purposeful", "captured", "Governance loops tracked", "Purposeful loops", "Captured loops", "Guardrail: purpose-driven governance should preserve plural stakeholder voice and transparent tradeoffs before scoring.")


def adaptive_institutional_ethics_engine() -> str:
    return _render("ADAPTIVE INSTITUTIONAL ETHICS ENGINE - PHASE 1227", "institutional-ethics overview", "institutional_ethics.json", "ethics_programs", "adaptive", "compromised", "Ethics programs tracked", "Adaptive programs", "Compromised programs", "Guardrail: institutional ethics engines should preserve independence, challenge rights, and public accountability before action.")


def autonomous_global_coordination_ai() -> str:
    return _render("AUTONOMOUS GLOBAL COORDINATION AI - PHASE 1228", "global-coordination overview", "global_coordination.json", "coalitions", "coordinated", "misaligned", "Coalitions tracked", "Coordinated coalitions", "Misaligned coalitions", "Guardrail: global coordination should preserve sovereignty, non-coercion, and transparent consensus-building before orchestration.")


def infinite_scale_humanitarian_optimization_framework() -> str:
    return _render("INFINITE-SCALE HUMANITARIAN OPTIMIZATION FRAMEWORK - PHASE 1229", "humanitarian-optimization overview", "humanitarian_optimization.json", "aid_networks", "optimized", "underserved", "Aid networks tracked", "Optimized aid networks", "Underserved aid networks", "Guardrail: humanitarian optimization should preserve dignity, neutrality, and consent-aware delivery before deployment.")


def recursive_civilization_prosperity_engine() -> str:
    return _render("RECURSIVE CIVILIZATION PROSPERITY ENGINE - PHASE 1230", "civilization-prosperity overview", "civilization_prosperity.json", "prosperity_loops", "prospering", "uneven", "Prosperity loops tracked", "Prospering loops", "Uneven loops", "Guardrail: prosperity engines should preserve justice, sustainability, and local agency before optimization.")
