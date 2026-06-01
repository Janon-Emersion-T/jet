from dataclasses import dataclass
from typing import Dict, List, Optional

from core.nlp.domain_understanding import DomainDecision, understand_domain
from core.nlp.file_awareness import FileAwarenessResult, understand_file_command
from core.nlp.intent_memory import expand_personal_shortcut, remember_intent
from core.nlp.knowledge_context import KnowledgeContext, build_knowledge_context
from core.nlp_engine import NLPResult, analyze_command
from core.nlp.production_config import load_nlp_config
from core.nlp.quality_services import confidence_dashboard
from core.nlp.runtime_services import (
    RuntimeProfile,
    keyword_fallback,
    profile_runtime,
    semantic_cache_get,
    semantic_cache_put,
)
from core.nlp.safety_planner import SafetyDecision, gate_route, log_nlp_audit
from core.nlp.target_resolvers import ResolvedTargets, resolve_targets
from core.nlp.task_planner import TaskPlan, build_task_plan


@dataclass
class UnifiedNLPResult:
    original_text: str
    normalized_text: str
    clean_text: str
    tokens: List[str]
    intent: str
    confidence: float
    canonical_command: Optional[str]
    entities: Dict[str, str]
    matched_phrase: Optional[str]
    safety_level: str
    engine: str
    route_hint: Optional[str]
    file_awareness: FileAwarenessResult
    safety: SafetyDecision
    targets: ResolvedTargets
    plan: TaskPlan
    knowledge: KnowledgeContext
    domain: DomainDecision
    dashboard: Dict[str, object]
    runtime: RuntimeProfile


def orchestrate_command(user_input: str, audit: bool = True, remember: bool = True,
                        cache: bool = True) -> UnifiedNLPResult:
    config = load_nlp_config()
    expanded = expand_personal_shortcut(user_input) if config["memory_enabled"] else user_input
    cached = semantic_cache_get(expanded) if cache and config["semantic_cache_enabled"] else None
    base: NLPResult = analyze_command(expanded)
    fallback_intent = keyword_fallback(base.clean_text)
    intent = base.intent if base.confidence >= config["confidence_threshold"] else fallback_intent or base.intent
    files = understand_file_command(expanded, base.entities)
    targets = resolve_targets(expanded, base.entities)
    if files.targets and files.action != "none":
        intent = "project_analysis"
    safety = gate_route(expanded, base.route_hint, config["default_role"])
    plan = build_task_plan(expanded, base.route_hint, config["default_role"])
    knowledge = build_knowledge_context(expanded) if config["knowledge_enabled"] else KnowledgeContext()
    domain = understand_domain(expanded)
    entities = dict(base.entities)
    if targets.file:
        entities["resolved_file"] = targets.file
    dashboard = confidence_dashboard(base.confidence, safety.safety_level, domain.domain)
    runtime_data = profile_runtime()
    runtime = RuntimeProfile(
        runtime_data["embedding_model"],
        runtime_data["device"],
        cache_hit=bool(cached),
        keyword_fallback=bool(fallback_intent and intent == fallback_intent),
    )
    result = UnifiedNLPResult(
        original_text=user_input,
        normalized_text=base.normalized_text,
        clean_text=base.clean_text,
        tokens=base.tokens,
        intent=intent,
        confidence=base.confidence,
        canonical_command=base.canonical_command,
        entities=entities,
        matched_phrase=base.matched_phrase,
        safety_level=safety.safety_level,
        engine="nlp-002w-unified-orchestrator",
        route_hint=base.route_hint,
        file_awareness=files,
        safety=safety,
        targets=targets,
        plan=plan,
        knowledge=knowledge,
        domain=domain,
        dashboard=dashboard,
        runtime=runtime,
    )
    if remember and config["memory_enabled"]:
        remember_intent(user_input, result.intent, result.route_hint)
    if audit and config["audit_enabled"]:
        log_nlp_audit(user_input, result.intent, result.route_hint, safety, {
            "confidence": result.confidence, "domain": domain.domain,
        })
    if cache and config["semantic_cache_enabled"]:
        semantic_cache_put(expanded, {
            "intent": result.intent,
            "route_hint": result.route_hint,
            "confidence": result.confidence,
            "domain": result.domain.domain,
        })
    return result


def format_unified_report(user_input: str) -> str:
    result = orchestrate_command(user_input)
    target_values = {
        key: value for key, value in {
            "file": result.targets.file, "git": result.targets.git,
            "laravel": result.targets.laravel, "server": result.targets.server,
            "database": result.targets.database, "browser": result.targets.browser,
        }.items() if value
    }
    lines = [
        "PHASE NLP-002W - FINAL UNIFIED NLP ORCHESTRATOR",
        "",
        f"Original: {result.original_text}",
        f"Clean command: {result.clean_text}",
        f"Intent: {result.intent} ({result.confidence})",
        f"Route: {result.route_hint or 'none'}",
        f"Domain: {result.domain.domain}",
        f"Safety: {result.safety.safety_level}",
        f"Confirmation required: {'YES' if result.safety.requires_confirmation else 'NO'}",
        f"Permission allowed: {'YES' if result.safety.allowed else 'NO'}",
        f"Steps: {len(result.plan.steps)}",
        f"Targets: {target_values or 'none'}",
        f"Suggested handler: {result.knowledge.route_handler or 'none'}",
        f"Semantic cache hit: {'YES' if result.runtime.cache_hit else 'NO'}",
    ]
    for reason in result.safety.reasons:
        lines.append(f"Safety reason: {reason}")
    for alternative in result.safety.alternatives:
        lines.append(f"Safe alternative: {alternative}")
    return "\n".join(lines)
