from __future__ import annotations

import json
from pathlib import Path


RESEARCH_INTEL_DIR = Path("storage/research_intelligence")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def research_paper_intelligence_engine() -> str:
    payload = _safe_json(RESEARCH_INTEL_DIR / "paper_intelligence.json", {})
    papers = payload.get("papers", []) if isinstance(payload, dict) else []
    indexed = [item for item in papers if isinstance(item, dict) and bool(item.get("indexed", False))]
    priority = [item for item in papers if isinstance(item, dict) and bool(item.get("priority", False))]
    return _overview("RESEARCH PAPER INTELLIGENCE ENGINE - PHASE 598", "paper-intelligence overview", [f"Papers tracked: {len(papers)}", f"Indexed papers: {len(indexed)}", f"Priority papers: {len(priority)}"], "Guardrail: paper intelligence should keep provenance, citation quality, and recency visible before influencing research direction.")


def scientific_literature_summarizer() -> str:
    payload = _safe_json(RESEARCH_INTEL_DIR / "literature_summaries.json", {})
    summaries = payload.get("summaries", []) if isinstance(payload, dict) else []
    reviewed = [item for item in summaries if isinstance(item, dict) and bool(item.get("reviewed", False))]
    uncertain = [item for item in summaries if isinstance(item, dict) and bool(item.get("uncertain", False))]
    return _overview("SCIENTIFIC LITERATURE SUMMARIZER - PHASE 599", "literature-summary overview", [f"Summaries tracked: {len(summaries)}", f"Reviewed summaries: {len(reviewed)}", f"Uncertain summaries: {len(uncertain)}"], "Guardrail: literature summaries should signal uncertainty, preserve nuance, and encourage source checking before they are treated as authoritative.")


def ai_patent_research_assistant() -> str:
    payload = _safe_json(RESEARCH_INTEL_DIR / "patent_research.json", {})
    patents = payload.get("patents", []) if isinstance(payload, dict) else []
    relevant = [item for item in patents if isinstance(item, dict) and bool(item.get("relevant", False))]
    blocked = [item for item in patents if isinstance(item, dict) and bool(item.get("blocking", False))]
    return _overview("AI PATENT RESEARCH ASSISTANT - PHASE 600", "patent-research overview", [f"Patents tracked: {len(patents)}", f"Relevant patents: {len(relevant)}", f"Potential blocking patents: {len(blocked)}"], "Guardrail: patent research should remain advisory, jurisdiction-aware, and counsel-reviewable before shaping filing or launch decisions.")
