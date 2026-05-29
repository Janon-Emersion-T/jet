from __future__ import annotations

import json
from pathlib import Path


RESEARCH_EVIDENCE_DIR = Path("storage/research_evidence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RESEARCH_EVIDENCE_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def skill_library_manager() -> str:
    return _render("SKILL LIBRARY MANAGER - PHASE 1721", "skill-library overview", "skill_library_manager.json", "skills", "organized", "missing", "Skills tracked", "Organized skills", "Missing skills", "Guardrail: skill management should preserve source instructions, version awareness, and clear trust boundaries for imported capabilities.")


def tool_learning_framework() -> str:
    return _render("TOOL LEARNING FRAMEWORK - PHASE 1722", "tool-learning overview", "tool_learning_framework.json", "tool_patterns", "learned", "unreliable", "Tool patterns tracked", "Learned patterns", "Unreliable patterns", "Guardrail: tool learning should preserve auditability and avoid silently broadening execution privileges from past behavior.")


def autonomous_documentation_crawler() -> str:
    return _render("AUTONOMOUS DOCUMENTATION CRAWLER - PHASE 1723", "documentation-crawler overview", "documentation_crawler.json", "doc_sources", "indexed", "stale", "Documentation sources tracked", "Indexed sources", "Stale sources", "Guardrail: documentation crawling should preserve source attribution and avoid treating scraped secondary summaries as primary truth.")


def trusted_source_ranking_system() -> str:
    return _render("TRUSTED-SOURCE RANKING SYSTEM - PHASE 1724", "source-ranking overview", "trusted_source_ranking.json", "source_profiles", "trusted", "questionable", "Source profiles tracked", "Trusted sources", "Questionable sources", "Guardrail: source ranking should preserve explicit criteria and avoid hiding contested but relevant sources from human review.")


def local_research_cache() -> str:
    return _render("LOCAL RESEARCH CACHE - PHASE 1725", "local-research-cache overview", "local_research_cache.json", "cache_entries", "fresh", "stale", "Cache entries tracked", "Fresh entries", "Stale entries", "Guardrail: research caching should preserve freshness metadata and never silently serve old evidence as current fact.")


def evidence_first_answer_mode() -> str:
    return _render("EVIDENCE-FIRST ANSWER MODE - PHASE 1726", "evidence-first overview", "evidence_first_answer_mode.json", "answer_paths", "evidenced", "unsupported", "Answer paths tracked", "Evidenced paths", "Unsupported paths", "Guardrail: evidence-first mode should preserve source/claim separation and refuse to imply evidence where none exists.")


def citation_aware_offline_notes() -> str:
    return _render("CITATION-AWARE OFFLINE NOTES - PHASE 1727", "citation-aware-notes overview", "citation_aware_offline_notes.json", "note_entries", "cited", "orphaned", "Note entries tracked", "Cited notes", "Orphaned notes", "Guardrail: offline notes should preserve citation linkage and clearly mark paraphrases versus direct evidence.")


def knowledge_decay_detector() -> str:
    return _render("KNOWLEDGE DECAY DETECTOR - PHASE 1728", "knowledge-decay overview", "knowledge_decay_detector.json", "knowledge_items", "fresh", "decayed", "Knowledge items tracked", "Fresh items", "Decayed items", "Guardrail: decay detection should preserve temporal context and avoid invalidating stable facts based solely on age.")


def stale_information_warning_system() -> str:
    return _render("STALE INFORMATION WARNING SYSTEM - PHASE 1729", "stale-information overview", "stale_information_warning.json", "information_items", "current", "warning", "Information items tracked", "Current items", "Warning items", "Guardrail: stale-information warnings should preserve exact timestamps and avoid certainty when freshness is merely uncertain.")


def self_updating_knowledge_queues() -> str:
    return _render("SELF-UPDATING KNOWLEDGE QUEUES - PHASE 1730", "knowledge-queue overview", "self_updating_knowledge_queues.json", "update_queues", "flowing", "backlogged", "Update queues tracked", "Flowing queues", "Backlogged queues", "Guardrail: self-updating queues should preserve review checkpoints and avoid auto-promoting unverified updates into trusted knowledge.")
