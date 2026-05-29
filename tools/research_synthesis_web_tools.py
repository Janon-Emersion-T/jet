from __future__ import annotations

import json
from pathlib import Path


RESEARCH_SYNTHESIS_WEB_DIR = Path("storage/research_synthesis_web")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(RESEARCH_SYNTHESIS_WEB_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def web_research_task_planner() -> str:
    return _render("WEB RESEARCH TASK PLANNER - PHASE 1731", "web-research-planning overview", "web_research_task_planner.json", "research_tasks", "planned", "fuzzy", "Research tasks tracked", "Planned tasks", "Fuzzy tasks", "Guardrail: web research planning should preserve scope clarity, source quality goals, and explicit stopping criteria.")


def browser_reading_comprehension() -> str:
    return _render("BROWSER READING COMPREHENSION - PHASE 1732", "browser-reading overview", "browser_reading_comprehension.json", "reading_passages", "understood", "uncertain", "Reading passages tracked", "Understood passages", "Uncertain passages", "Guardrail: reading comprehension should preserve source context and avoid implying semantic certainty from thin excerpts.")


def source_comparison_engine() -> str:
    return _render("SOURCE COMPARISON ENGINE - PHASE 1733", "source-comparison overview", "source_comparison_engine.json", "source_pairs", "aligned", "conflicting", "Source pairs tracked", "Aligned pairs", "Conflicting pairs", "Guardrail: source comparison should preserve direct quotations/provenance and avoid flattening meaningful disagreements into averages.")


def fact_dispute_resolver() -> str:
    return _render("FACT DISPUTE RESOLVER - PHASE 1734", "fact-dispute overview", "fact_dispute_resolver.json", "disputed_claims", "resolved", "contested", "Disputed claims tracked", "Resolved claims", "Contested claims", "Guardrail: dispute resolution should preserve conflicting evidence and avoid finality where sources remain materially inconsistent.")


def misinformation_risk_flagger() -> str:
    return _render("MISINFORMATION RISK FLAGGER - PHASE 1735", "misinformation-risk overview", "misinformation_risk_flagger.json", "information_signals", "credible", "risky", "Information signals tracked", "Credible signals", "Risky signals", "Guardrail: misinformation flagging should preserve evidentiary reasons and avoid ideological or popularity-based proxies for truth.")


def research_synthesis_dashboard() -> str:
    return _render("RESEARCH SYNTHESIS DASHBOARD - PHASE 1736", "research-synthesis overview", "research_synthesis_dashboard.json", "synthesis_views", "coherent", "fragmented", "Synthesis views tracked", "Coherent views", "Fragmented views", "Guardrail: synthesis dashboards should preserve uncertainty, source diversity, and explicit evidence gaps rather than over-summarizing.")


def academic_paper_ingestion() -> str:
    return _render("ACADEMIC PAPER INGESTION - PHASE 1737", "academic-paper-ingestion overview", "academic_paper_ingestion.json", "paper_entries", "parsed", "partial", "Paper entries tracked", "Parsed papers", "Partial papers", "Guardrail: paper ingestion should preserve citation metadata and distinguish abstract-level impressions from full-method understanding.")


def technical_standard_parser() -> str:
    return _render("TECHNICAL STANDARD PARSER - PHASE 1738", "technical-standard overview", "technical_standard_parser.json", "standard_sections", "parsed", "unclear", "Standard sections tracked", "Parsed sections", "Unclear sections", "Guardrail: standard parsing should preserve normative language and avoid downgrading mandatory requirements into optional guidance.")


def legal_document_comparison() -> str:
    return _render("LEGAL DOCUMENT COMPARISON - PHASE 1739", "legal-doc-comparison overview", "legal_document_comparison.json", "document_pairs", "aligned", "divergent", "Document pairs tracked", "Aligned pairs", "Divergent pairs", "Guardrail: legal comparison should preserve clause-level provenance and avoid unauthorized legal advice from heuristic similarities.")


def contract_clause_risk_scorer() -> str:
    return _render("CONTRACT CLAUSE RISK SCORER - PHASE 1740", "contract-clause-risk overview", "contract_clause_risk_scorer.json", "clause_profiles", "routine", "risky", "Clause profiles tracked", "Routine clauses", "Risky clauses", "Guardrail: clause risk scoring should preserve exact wording evidence and require human/legal review before acting on flagged contract language.")
