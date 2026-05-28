from dataclasses import dataclass
from pathlib import Path
import math
import re
from typing import Dict, List, Optional, Tuple

from tools.project_context_tools import get_current_project_path


@dataclass
class ModelCandidate:
    name: str
    quantization: str
    min_ram_gb: float
    gpu_preferred: bool
    use_case: str


@dataclass
class InferenceWorkload:
    prompt_tokens: int
    output_tokens: int
    context_tokens: int
    concurrent_requests: int = 1


@dataclass
class RetrievalDocument:
    path: str
    text: str


MODEL_CANDIDATES = [
    ModelCandidate("llama3.2:3b-instruct-q4", "Q4", 8, False, "fast local assistance"),
    ModelCandidate("mistral:7b-instruct-q4", "Q4", 16, False, "balanced reasoning"),
    ModelCandidate("qwen2.5-coder:7b-q4", "Q4", 16, False, "coding assistance"),
    ModelCandidate("llama3.1:8b-instruct-q5", "Q5", 24, True, "higher quality chat"),
    ModelCandidate("qwen2.5-coder:14b-q4", "Q4", 32, True, "larger coding tasks"),
]


def _tokens(text: str) -> List[str]:
    return re.findall(r"[a-z0-9_]+", text.lower())


def _score_overlap(query: str, document: str) -> float:
    q = set(_tokens(query))
    d = set(_tokens(document))
    if not q or not d:
        return 0.0
    return len(q & d) / math.sqrt(len(q) * len(d))


def quantized_model_selector(ram_gb: float = 16, gpu_available: bool = False, task: str = "general") -> str:
    task_text = task.lower()
    viable = [model for model in MODEL_CANDIDATES if model.min_ram_gb <= ram_gb and (gpu_available or not model.gpu_preferred)]
    if not viable:
        viable = [MODEL_CANDIDATES[0]]
    if "code" in task_text or "coding" in task_text:
        viable = sorted(viable, key=lambda item: ("coder" not in item.name, -item.min_ram_gb))
    else:
        viable = sorted(viable, key=lambda item: -item.min_ram_gb)
    chosen = viable[0]
    lines = [
        "QUANTIZED MODEL SELECTOR - PHASE 381",
        f"Available RAM: {ram_gb:.1f} GB",
        f"GPU available: {gpu_available}",
        f"Task: {task}",
        f"Recommended model: {chosen.name}",
        f"Quantization: {chosen.quantization}",
        f"Use case: {chosen.use_case}",
        "Safety: no model was pulled, loaded, or benchmarked.",
    ]
    return "\n".join(lines)


def model_benchmarking_engine(tokens_per_second: float = 18.0, latency_ms: float = 900.0) -> str:
    status = "FAST" if tokens_per_second >= 25 and latency_ms <= 750 else "USABLE" if tokens_per_second >= 10 else "SLOW"
    lines = [
        "MODEL BENCHMARKING ENGINE - PHASE 382",
        "Mode: read-only benchmark result interpretation.",
        f"Tokens/sec: {tokens_per_second:.1f}",
        f"First-token latency: {latency_ms:.0f} ms",
        f"Status: {status}",
        "Recommendation: benchmark with your real prompts before changing production routing.",
        "Safety: no benchmark command was executed by this report.",
    ]
    return "\n".join(lines)


def ai_inference_profiler(workload: Optional[InferenceWorkload] = None) -> str:
    current = workload or InferenceWorkload(700, 300, 4096, 1)
    total_tokens = (current.prompt_tokens + current.output_tokens) * max(current.concurrent_requests, 1)
    context_pressure = current.context_tokens / 8192
    risk = "HIGH" if total_tokens > 12000 or context_pressure > 1 else "MEDIUM" if total_tokens > 6000 or context_pressure > 0.75 else "LOW"
    lines = [
        "AI INFERENCE PROFILER - PHASE 383",
        f"Prompt tokens: {current.prompt_tokens}",
        f"Output tokens: {current.output_tokens}",
        f"Context window: {current.context_tokens}",
        f"Concurrent requests: {current.concurrent_requests}",
        f"Estimated total active tokens: {total_tokens}",
        f"Pressure: {risk}",
        "Recommendation: reduce concurrency, context, or output length if pressure is high.",
        "Safety: no inference request was sent.",
    ]
    return "\n".join(lines)


def build_document_embeddings(documents: List[RetrievalDocument]) -> Dict[str, Dict[str, int]]:
    vectors: Dict[str, Dict[str, int]] = {}
    for document in documents:
        bag: Dict[str, int] = {}
        for token in _tokens(document.text):
            bag[token] = bag.get(token, 0) + 1
        vectors[document.path] = bag
    return vectors


def document_embedding_engine(documents: Optional[List[RetrievalDocument]] = None) -> str:
    docs = documents or [RetrievalDocument("README.md", "Jarvis local AI assistant documentation")]
    vectors = build_document_embeddings(docs)
    lines = [
        "DOCUMENT EMBEDDING ENGINE - PHASE 385",
        "Mode: local lexical embedding preview.",
        f"Documents embedded: {len(vectors)}",
    ]
    for path, vector in list(vectors.items())[:10]:
        lines.append(f"- {path}: {len(vector)} unique terms")
    lines.append("Safety: no vector database was modified by this preview.")
    return "\n".join(lines)


def local_rag_system(query: str = "deployment", documents: Optional[List[RetrievalDocument]] = None) -> str:
    docs = documents or [
        RetrievalDocument("docs/deploy.md", "Deploy with backups, health checks, and rollback steps."),
        RetrievalDocument("docs/security.md", "Security requires secrets scanning and firewall review."),
    ]
    ranked = sorted(((doc, _score_overlap(query, doc.text)) for doc in docs), key=lambda item: item[1], reverse=True)
    lines = [
        "LOCAL RAG SYSTEM - PHASE 384",
        f"Query: {query}",
        "Mode: local retrieval preview.",
    ]
    for doc, score in ranked[:3]:
        lines.append(f"- {doc.path}: score={score:.3f}")
    lines.append("Safety: no remote search or model generation was performed.")
    return "\n".join(lines)


def semantic_search_dashboard(query: str = "security", documents: Optional[List[RetrievalDocument]] = None) -> str:
    docs = documents or [
        RetrievalDocument("security.md", "Firewall, SSH, and Fail2ban hardening checklist."),
        RetrievalDocument("marketing.md", "SEO and campaign planning notes."),
    ]
    ranked = sorted(((doc.path, _score_overlap(query, doc.text)) for doc in docs), key=lambda item: item[1], reverse=True)
    lines = [
        "SEMANTIC SEARCH DASHBOARD - PHASE 386",
        f"Query: {query}",
        "Top matches:",
    ]
    lines += [f"- {path}: {score:.3f}" for path, score in ranked[:5]]
    lines.append("Safety: dashboard data is generated locally from supplied documents.")
    return "\n".join(lines)


def ai_memory_hierarchy(items: Optional[List[Tuple[str, str]]] = None) -> str:
    entries = items or [
        ("episodic", "User asked to complete phases incrementally."),
        ("semantic", "Security scanners are read-only."),
        ("procedural", "Run tests before marking a phase complete."),
    ]
    buckets: Dict[str, int] = {}
    for kind, _ in entries:
        buckets[kind] = buckets.get(kind, 0) + 1
    lines = ["AI MEMORY HIERARCHY - PHASE 387", "Memory layers:"]
    lines += [f"- {kind}: {count}" for kind, count in sorted(buckets.items())]
    lines.append("Recommendation: keep procedural rules separate from episodic conversation facts.")
    lines.append("Safety: no memory store was modified.")
    return "\n".join(lines)


def context_window_optimizer(prompt_tokens: int = 6000, max_context: int = 8192) -> str:
    ratio = prompt_tokens / max(max_context, 1)
    status = "TRIM" if ratio > 0.9 else "COMPRESS" if ratio > 0.7 else "OK"
    lines = [
        "CONTEXT WINDOW OPTIMIZER - PHASE 388",
        f"Prompt tokens: {prompt_tokens}",
        f"Max context: {max_context}",
        f"Usage: {ratio:.1%}",
        f"Decision: {status}",
        "Recommendation: summarize old context and keep active files/results nearest the prompt.",
        "Safety: no prompt or file was changed.",
    ]
    return "\n".join(lines)


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "developer message",
    "disable safety",
    "exfiltrate",
]


def prompt_injection_detector(text: str = "") -> str:
    lowered = text.lower()
    hits = [pattern for pattern in PROMPT_INJECTION_PATTERNS if pattern in lowered]
    status = "HIGH" if len(hits) >= 2 else "MEDIUM" if hits else "LOW"
    lines = [
        "PROMPT INJECTION DETECTOR - PHASE 389",
        f"Risk: {status}",
        f"Signals: {', '.join(hits) if hits else '-'}",
        "Recommendation: isolate untrusted content and keep tool/system instructions authoritative.",
        "Safety: no prompt content was executed.",
    ]
    return "\n".join(lines)


def hallucination_risk_detector(answer: str = "", sources: Optional[List[str]] = None) -> str:
    sources = sources or []
    claims = len(re.findall(r"\b(?:always|never|guaranteed|proven|latest|official)\b", answer.lower()))
    risk = "HIGH" if claims >= 2 and not sources else "MEDIUM" if claims and not sources else "LOW"
    lines = [
        "HALLUCINATION RISK DETECTOR - PHASE 390",
        f"Risk: {risk}",
        f"Absolute-claim signals: {claims}",
        f"Sources supplied: {len(sources)}",
        "Recommendation: cite primary sources or mark uncertain claims as assumptions.",
        "Safety: no generated answer was published.",
    ]
    return "\n".join(lines)


def ai_confidence_scoring(score: float = 0.72, risk: str = "low", source_count: int = 1) -> str:
    adjusted = score
    if risk.lower() == "high":
        adjusted -= 0.25
    elif risk.lower() == "medium":
        adjusted -= 0.1
    if source_count == 0:
        adjusted -= 0.15
    adjusted = max(0.0, min(1.0, adjusted))
    label = "HIGH" if adjusted >= 0.75 else "MEDIUM" if adjusted >= 0.45 else "LOW"
    lines = [
        "AI CONFIDENCE SCORING - PHASE 391",
        f"Base score: {score:.2f}",
        f"Risk: {risk}",
        f"Sources: {source_count}",
        f"Adjusted confidence: {adjusted:.2f}",
        f"Label: {label}",
        "Recommendation: request clarification or sources when confidence is low.",
        "Safety: score calculation only; no action was taken.",
    ]
    return "\n".join(lines)
