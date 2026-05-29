from __future__ import annotations

import json
from pathlib import Path


WORKPLACE_INTEL_DIR = Path("storage/workplace_intelligence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def ai_meeting_participation_agent() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "meeting_agent.json", {})
    meetings = payload.get("meetings", []) if isinstance(payload, dict) else []
    active = [item for item in meetings if isinstance(item, dict) and item.get("status") == "active"]
    followups = [item for item in meetings if isinstance(item, dict) and bool(item.get("followups", False))]
    return _overview("AI MEETING PARTICIPATION AGENT - PHASE 583", "meeting-participation overview", [f"Meetings tracked: {len(meetings)}", f"Active meetings: {len(active)}", f"Meetings with follow-ups: {len(followups)}"], "Guardrail: meeting participation should remain transparent, permissioned, and respectful of context before speaking or acting.")


def autonomous_note_taking_system() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "notes.json", {})
    notes = payload.get("notes", []) if isinstance(payload, dict) else []
    summarized = [item for item in notes if isinstance(item, dict) and bool(item.get("summarized", False))]
    actioned = [item for item in notes if isinstance(item, dict) and bool(item.get("action_items", False))]
    return _overview("AUTONOMOUS NOTE-TAKING SYSTEM - PHASE 584", "note-taking overview", [f"Notes tracked: {len(notes)}", f"Summarized notes: {len(summarized)}", f"Notes with action items: {len(actioned)}"], "Guardrail: note automation should preserve attribution, factual fidelity, and attendee expectations before distributing records.")


def ai_presentation_assistant() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "presentations.json", {})
    decks = payload.get("decks", []) if isinstance(payload, dict) else []
    drafted = [item for item in decks if isinstance(item, dict) and bool(item.get("drafted", False))]
    reviewed = [item for item in decks if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI PRESENTATION ASSISTANT - PHASE 585", "presentation-assistant overview", [f"Decks tracked: {len(decks)}", f"Drafted decks: {len(drafted)}", f"Reviewed decks: {len(reviewed)}"], "Guardrail: presentation support should preserve source accuracy, audience fit, and human approval before publishing slides.")


def live_presentation_co_pilot() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "live_presentations.json", {})
    sessions = payload.get("sessions", []) if isinstance(payload, dict) else []
    live = [item for item in sessions if isinstance(item, dict) and item.get("status") == "live"]
    adapted = [item for item in sessions if isinstance(item, dict) and bool(item.get("adapted", False))]
    return _overview("LIVE PRESENTATION CO-PILOT - PHASE 586", "live-presentation overview", [f"Sessions tracked: {len(sessions)}", f"Live sessions: {len(live)}", f"Adapted sessions: {len(adapted)}"], "Guardrail: live assistance should stay presenter-controlled, low-distraction, and fact-aware before changing what is shown or said.")


def ai_interview_assistant() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "interviews.json", {})
    interviews = payload.get("interviews", []) if isinstance(payload, dict) else []
    structured = [item for item in interviews if isinstance(item, dict) and bool(item.get("structured", False))]
    reviewed = [item for item in interviews if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AI INTERVIEW ASSISTANT - PHASE 587", "interview-assistant overview", [f"Interviews tracked: {len(interviews)}", f"Structured interviews: {len(structured)}", f"Reviewed interview packets: {len(reviewed)}"], "Guardrail: interview support should reduce bias, preserve candidate dignity, and remain recruiter-reviewable before affecting outcomes.")


def candidate_ranking_engine() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "candidate_ranking.json", {})
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else []
    ranked = [item for item in candidates if isinstance(item, dict) and bool(item.get("ranked", False))]
    flagged = [item for item in candidates if isinstance(item, dict) and bool(item.get("needs_review", False))]
    return _overview("CANDIDATE RANKING ENGINE - PHASE 588", "candidate-ranking overview", [f"Candidates tracked: {len(candidates)}", f"Ranked candidates: {len(ranked)}", f"Candidates needing review: {len(flagged)}"], "Guardrail: ranking should remain bias-audited, explainable, and subordinate to human hiring judgment.")


def resume_intelligence_system() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "resume_intelligence.json", {})
    resumes = payload.get("resumes", []) if isinstance(payload, dict) else []
    parsed = [item for item in resumes if isinstance(item, dict) and bool(item.get("parsed", False))]
    matched = [item for item in resumes if isinstance(item, dict) and bool(item.get("matched", False))]
    return _overview("RESUME INTELLIGENCE SYSTEM - PHASE 589", "resume-intelligence overview", [f"Resumes tracked: {len(resumes)}", f"Parsed resumes: {len(parsed)}", f"Matched resumes: {len(matched)}"], "Guardrail: resume intelligence should preserve candidate context, reduce shortcut bias, and invite recruiter review for ambiguous fits.")


def ai_onboarding_mentor() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "onboarding.json", {})
    hires = payload.get("hires", []) if isinstance(payload, dict) else []
    active = [item for item in hires if isinstance(item, dict) and item.get("status") == "active"]
    guided = [item for item in hires if isinstance(item, dict) and bool(item.get("guided", False))]
    return _overview("AI ONBOARDING MENTOR - PHASE 590", "onboarding overview", [f"New hires tracked: {len(hires)}", f"Active onboarding plans: {len(active)}", f"Guided hires: {len(guided)}"], "Guardrail: onboarding automation should support inclusion, clarity, and manager accountability before personalizing workflows.")


def adaptive_employee_learning_engine() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "employee_learning.json", {})
    learners = payload.get("learners", []) if isinstance(payload, dict) else []
    adaptive = [item for item in learners if isinstance(item, dict) and bool(item.get("adaptive_path", False))]
    behind = [item for item in learners if isinstance(item, dict) and item.get("status") == "behind"]
    return _overview("ADAPTIVE EMPLOYEE LEARNING ENGINE - PHASE 591", "employee-learning overview", [f"Learners tracked: {len(learners)}", f"Adaptive learning paths: {len(adaptive)}", f"Learners behind pace: {len(behind)}"], "Guardrail: adaptive learning should be supportive, transparent, and aligned with role expectations before it influences performance narratives.")


def skill_gap_analysis_system() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "skill_gap.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    gaps = [item for item in profiles if isinstance(item, dict) and bool(item.get("gap_detected", False))]
    ready = [item for item in profiles if isinstance(item, dict) and bool(item.get("ready", False))]
    return _overview("SKILL-GAP ANALYSIS SYSTEM - PHASE 592", "skill-gap overview", [f"Profiles tracked: {len(profiles)}", f"Profiles with gaps: {len(gaps)}", f"Ready profiles: {len(ready)}"], "Guardrail: skill-gap analysis should separate development guidance from evaluation judgment and remain manager-reviewable.")


def autonomous_curriculum_generation() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "curriculum_generation.json", {})
    curricula = payload.get("curricula", []) if isinstance(payload, dict) else []
    generated = [item for item in curricula if isinstance(item, dict) and bool(item.get("generated", False))]
    reviewed = [item for item in curricula if isinstance(item, dict) and bool(item.get("reviewed", False))]
    return _overview("AUTONOMOUS CURRICULUM GENERATION - PHASE 593", "curriculum-generation overview", [f"Curricula tracked: {len(curricula)}", f"Generated curricula: {len(generated)}", f"Reviewed curricula: {len(reviewed)}"], "Guardrail: curriculum generation should align with role needs, assessment quality, and educator oversight before rollout.")


def ai_certification_trainer() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "certification_trainer.json", {})
    tracks = payload.get("tracks", []) if isinstance(payload, dict) else []
    active = [item for item in tracks if isinstance(item, dict) and item.get("status") == "active"]
    passed = [item for item in tracks if isinstance(item, dict) and bool(item.get("practice_passed", False))]
    return _overview("AI CERTIFICATION TRAINER - PHASE 594", "certification-training overview", [f"Tracks tracked: {len(tracks)}", f"Active tracks: {len(active)}", f"Practice-passed tracks: {len(passed)}"], "Guardrail: certification training should preserve assessment integrity, role relevance, and learner autonomy before certifying readiness.")


def enterprise_lms_intelligence_layer() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "lms_intelligence.json", {})
    courses = payload.get("courses", []) if isinstance(payload, dict) else []
    enriched = [item for item in courses if isinstance(item, dict) and bool(item.get("enriched", False))]
    stale = [item for item in courses if isinstance(item, dict) and item.get("status") == "stale"]
    return _overview("ENTERPRISE LMS INTELLIGENCE LAYER - PHASE 595", "lms-intelligence overview", [f"Courses tracked: {len(courses)}", f"Enriched courses: {len(enriched)}", f"Stale courses: {len(stale)}"], "Guardrail: LMS intelligence should improve discoverability and learning quality without obscuring source ownership or course validity.")


def ai_examination_proctor() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "exam_proctor.json", {})
    exams = payload.get("exams", []) if isinstance(payload, dict) else []
    monitored = [item for item in exams if isinstance(item, dict) and bool(item.get("monitored", False))]
    flagged = [item for item in exams if isinstance(item, dict) and bool(item.get("flagged", False))]
    return _overview("AI EXAMINATION PROCTOR - PHASE 596", "exam-proctor overview", [f"Exams tracked: {len(exams)}", f"Monitored exams: {len(monitored)}", f"Flagged exams: {len(flagged)}"], "Guardrail: proctoring should respect privacy, minimize false accusations, and require human review before penalties.")


def knowledge_retention_analyzer() -> str:
    payload = _safe_json(WORKPLACE_INTEL_DIR / "knowledge_retention.json", {})
    cohorts = payload.get("cohorts", []) if isinstance(payload, dict) else []
    strong = [item for item in cohorts if isinstance(item, dict) and item.get("retention") == "strong"]
    weak = [item for item in cohorts if isinstance(item, dict) and item.get("retention") == "weak"]
    return _overview("KNOWLEDGE RETENTION ANALYZER - PHASE 597", "knowledge-retention overview", [f"Cohorts tracked: {len(cohorts)}", f"Strong-retention cohorts: {len(strong)}", f"Weak-retention cohorts: {len(weak)}"], "Guardrail: retention analysis should support coaching and course improvement rather than shortcutting human development judgment.")
