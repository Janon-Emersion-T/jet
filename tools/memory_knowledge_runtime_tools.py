from __future__ import annotations

import json
from pathlib import Path


MEMORY_KNOWLEDGE_RUNTIME_DIR = Path("storage/memory_knowledge_runtime")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(MEMORY_KNOWLEDGE_RUNTIME_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def hallucination_suppression_layer() -> str:
    return _render("HALLUCINATION SUPPRESSION LAYER - PHASE 1711", "hallucination-suppression overview", "hallucination_suppression.json", "answer_checks", "grounded", "speculative", "Answer checks tracked", "Grounded checks", "Speculative checks", "Guardrail: hallucination suppression should preserve uncertainty signaling and avoid inventing citations to appear safer.")


def tool_call_validation_engine() -> str:
    return _render("TOOL-CALL VALIDATION ENGINE - PHASE 1712", "tool-call-validation overview", "tool_call_validation_engine.json", "tool_calls", "validated", "unsafe", "Tool calls tracked", "Validated calls", "Unsafe calls", "Guardrail: tool validation should preserve parameter visibility, command safety boundaries, and explicit refusal for overbroad execution.")


def memory_contradiction_resolver() -> str:
    return _render("MEMORY CONTRADICTION RESOLVER - PHASE 1713", "memory-contradiction overview", "memory_contradiction_resolver.json", "memory_pairs", "resolved", "conflicting", "Memory pairs tracked", "Resolved pairs", "Conflicting pairs", "Guardrail: contradiction resolution should preserve original evidence and avoid silently overwriting contested memory.")


def long_term_knowledge_curator() -> str:
    return _render("LONG-TERM KNOWLEDGE CURATOR - PHASE 1714", "long-term-knowledge overview", "long_term_knowledge_curator.json", "knowledge_entries", "curated", "stale", "Knowledge entries tracked", "Curated entries", "Stale entries", "Guardrail: long-term curation should preserve provenance, freshness metadata, and explicit review before promotion into durable memory.")


def personal_ontology_builder() -> str:
    return _render("PERSONAL ONTOLOGY BUILDER - PHASE 1715", "personal-ontology overview", "personal_ontology_builder.json", "ontology_nodes", "linked", "orphaned", "Ontology nodes tracked", "Linked nodes", "Orphaned nodes", "Guardrail: ontology building should preserve user language and avoid imposing brittle taxonomies without clear benefit.")


def work_context_summarizer() -> str:
    return _render("WORK CONTEXT SUMMARIZER - PHASE 1716", "work-context overview", "work_context_summarizer.json", "context_summaries", "useful", "lossy", "Context summaries tracked", "Useful summaries", "Lossy summaries", "Guardrail: context summarization should preserve task-critical nuance and clearly mark when details were omitted.")


def active_project_memory_injection() -> str:
    return _render("ACTIVE PROJECT MEMORY INJECTION - PHASE 1717", "project-memory-injection overview", "active_project_memory_injection.json", "memory_packets", "relevant", "irrelevant", "Memory packets tracked", "Relevant packets", "Irrelevant packets", "Guardrail: project memory injection should preserve scope boundaries and avoid contaminating unrelated tasks with stale context.")


def episodic_memory_timeline() -> str:
    return _render("EPISODIC MEMORY TIMELINE - PHASE 1718", "episodic-memory overview", "episodic_memory_timeline.json", "episodes", "ordered", "ambiguous", "Episodes tracked", "Ordered episodes", "Ambiguous episodes", "Guardrail: episodic timelines should preserve timestamps, provenance, and avoid inventing sequence when records are incomplete.")


def semantic_memory_graph() -> str:
    return _render("SEMANTIC MEMORY GRAPH - PHASE 1719", "semantic-memory overview", "semantic_memory_graph.json", "graph_edges", "grounded", "speculative", "Graph edges tracked", "Grounded edges", "Speculative edges", "Guardrail: semantic graphing should preserve evidence behind links and distinguish inferred relationships from explicit facts.")


def procedural_memory_engine() -> str:
    return _render("PROCEDURAL MEMORY ENGINE - PHASE 1720", "procedural-memory overview", "procedural_memory_engine.json", "procedures", "reusable", "fragile", "Procedures tracked", "Reusable procedures", "Fragile procedures", "Guardrail: procedural memory should preserve versioning, environment assumptions, and explicit opt-out for stale automation habits.")
