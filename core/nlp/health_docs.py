from pathlib import Path
from typing import List

from core.nlp.production_config import load_nlp_config
from core.nlp.runtime_services import model_cache_status, profile_runtime


PHASE_GROUPS = {
    "NLP-000T..000Z": "File awareness, safety planning, confirmation, explanations, alternatives, permission gating, audit trail",
    "NLP-001A..001F": "Intent memory, habits, shortcuts, recovery, repeated command optimization",
    "NLP-001G..001L": "File, Git, Laravel, server, database, and browser target resolvers",
    "NLP-001M..001R": "Task decomposition, agent/tool selection, dependencies, action classification, approvals",
    "NLP-001S..001X": "Local knowledge context, docs, errors, symbols, route matching, missing capability detection",
    "NLP-001Y..002D": "Voice cleanup, speech correction, dictation, wake word, follow-up and safety confirmation",
    "NLP-002E..002J": "Confidence dashboard, tests, regression scoring, failure analysis and registry suggestions",
    "NLP-002K..002P": "Offline model/cache selection, profiling, warmup, semantic cache and keyword fallback",
    "NLP-002Q..002V": "Business, developer, DevOps, marketing, accounting and research understanding",
    "NLP-002W..002Z": "Unified orchestration, configuration, health and documentation",
}
MODULES = [
    "file_awareness.py", "safety_planner.py", "intent_memory.py", "target_resolvers.py",
    "task_planner.py", "knowledge_context.py", "voice_understanding.py", "quality_services.py",
    "runtime_services.py", "domain_understanding.py", "unified_orchestrator.py",
    "production_config.py", "health_docs.py",
]


def nlp_health_check() -> str:
    missing = [module for module in MODULES if not (Path("core/nlp") / module).exists()]
    config = load_nlp_config()
    runtime = profile_runtime()
    cache = model_cache_status()
    status = "healthy" if not missing and config.get("enabled") else "degraded"
    lines = [
        "NLP-002Y - NLP HEALTH CHECK",
        f"Status: {status}",
        f"Modules installed: {len(MODULES) - len(missing)}/{len(MODULES)}",
        f"Audit enabled: {config['audit_enabled']}",
        f"Memory enabled: {config['memory_enabled']}",
        f"Runtime device: {runtime['device']}",
        f"Embedding model: {runtime['embedding_model']}",
        f"Local model cache locations found: {len(cache['available_locations'])}",
    ]
    if missing:
        lines.append("Missing modules: " + ", ".join(missing))
    return "\n".join(lines)


def generate_nlp_documentation() -> str:
    lines: List[str] = ["NLP-002Z - NLP MODULE DOCUMENTATION", ""]
    for phases, description in PHASE_GROUPS.items():
        lines.append(f"{phases}: {description}")
    lines.extend([
        "",
        "Commands:",
        "- `test unified <command>` analyzes a command through all modules.",
        "- `test safety <command>` explains approval and permission decisions.",
        "- `nlp health` checks production NLP configuration.",
        "- `nlp regression` measures baseline intent cases.",
        "- `nlp docs` prints this module inventory.",
    ])
    return "\n".join(lines)
