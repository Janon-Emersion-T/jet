from __future__ import annotations

import json
from pathlib import Path


POLICY_TRAINING_DIR = Path("storage/policy_training")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(POLICY_TRAINING_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def policy_to_action_mapper() -> str:
    return _render("POLICY-TO-ACTION MAPPER - PHASE 1741", "policy-to-action overview", "policy_to_action_mapper.json", "policy_mappings", "actionable", "ambiguous", "Policy mappings tracked", "Actionable mappings", "Ambiguous mappings", "Guardrail: policy mapping should preserve source wording and clearly mark interpretation versus explicit requirement.")


def sop_compliance_checker() -> str:
    return _render("SOP COMPLIANCE CHECKER - PHASE 1742", "sop-compliance overview", "sop_compliance_checker.json", "sop_checks", "compliant", "gapped", "SOP checks tracked", "Compliant checks", "Gapped checks", "Guardrail: SOP compliance analysis should preserve procedure versioning and avoid implying full compliance from partial evidence.")


def staff_handbook_assistant() -> str:
    return _render("STAFF HANDBOOK ASSISTANT - PHASE 1743", "staff-handbook overview", "staff_handbook_assistant.json", "handbook_sections", "clear", "outdated", "Handbook sections tracked", "Clear sections", "Outdated sections", "Guardrail: handbook assistance should preserve policy nuance and defer jurisdiction-sensitive HR/legal questions for human review.")


def training_module_generator() -> str:
    return _render("TRAINING MODULE GENERATOR - PHASE 1744", "training-module overview", "training_module_generator.json", "training_modules", "ready", "thin", "Training modules tracked", "Ready modules", "Thin modules", "Guardrail: training generation should preserve source accuracy and avoid presenting incomplete drafts as production-ready education.")


def quiz_and_exam_generator() -> str:
    return _render("QUIZ AND EXAM GENERATOR - PHASE 1745", "quiz-generator overview", "quiz_exam_generator.json", "assessment_items", "usable", "ambiguous", "Assessment items tracked", "Usable items", "Ambiguous items", "Guardrail: assessment generation should preserve learning objectives alignment and avoid trick questions disguised as rigor.")


def teach_back_evaluator() -> str:
    return _render("TEACH-BACK EVALUATOR - PHASE 1746", "teach-back overview", "teach_back_evaluator.json", "teach_back_responses", "understood", "unclear", "Teach-back responses tracked", "Understood responses", "Unclear responses", "Guardrail: teach-back evaluation should preserve supportive feedback and avoid overconfident judgment from limited response samples.")


def ai_tutor_personality_modes() -> str:
    return _render("AI TUTOR PERSONALITY MODES - PHASE 1747", "ai-tutor-personality overview", "ai_tutor_personality_modes.json", "tutor_modes", "matched", "mismatched", "Tutor modes tracked", "Matched modes", "Mismatched modes", "Guardrail: tutor personalities should preserve learner dignity and adapt tone without changing the factual content or rigor expected.")


def skill_progression_tracker() -> str:
    return _render("SKILL PROGRESSION TRACKER - PHASE 1748", "skill-progression overview", "skill_progression_tracker.json", "progress_markers", "advancing", "stalled", "Progress markers tracked", "Advancing markers", "Stalled markers", "Guardrail: progression tracking should preserve context and avoid reducing complex learning to one-dimensional scores.")


def learning_retention_engine() -> str:
    return _render("LEARNING RETENTION ENGINE - PHASE 1749", "learning-retention overview", "learning_retention_engine.json", "retention_cycles", "retained", "fading", "Retention cycles tracked", "Retained cycles", "Fading cycles", "Guardrail: retention analysis should preserve spacing-context nuance and avoid claiming mastery from recall alone.")


def company_knowledge_academy() -> str:
    return _render("COMPANY KNOWLEDGE ACADEMY - PHASE 1750", "knowledge-academy overview", "company_knowledge_academy.json", "academy_tracks", "organized", "fragmented", "Academy tracks tracked", "Organized tracks", "Fragmented tracks", "Guardrail: knowledge academy support should preserve source provenance, version control, and role-appropriate access to internal materials.")
