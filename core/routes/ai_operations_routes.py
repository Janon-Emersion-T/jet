from tools.ai_model_ops_tools import (
    ai_confidence_scoring,
    ai_inference_profiler,
    ai_memory_hierarchy,
    context_window_optimizer,
    document_embedding_engine,
    hallucination_risk_detector,
    local_rag_system,
    model_benchmarking_engine,
    prompt_injection_detector,
    quantized_model_selector,
    semantic_search_dashboard,
)
from tools.agent_orchestration_tools import (
    coding_agent,
    critic_agent,
    executor_agent,
    marketing_agent,
    multi_agent_orchestration,
    planner_agent,
    research_agent,
    security_agent,
    seo_agent,
)
from tools.agent_governance_tools import (
    action_logging_framework,
    agent_task_marketplace,
    ai_swarm_coordination,
    autonomous_browser_agent,
    autonomous_deployment_agent,
    autonomous_monitoring_agent,
    finance_agent,
    human_approval_gateway,
    role_based_ai_delegation,
    scheduling_agent,
)
from tools.trust_controls_tools import (
    adaptive_permission_escalation,
    ai_ethics_constraints,
    decision_trace_system,
    emergency_shutdown_mode,
    explain_why_engine,
    face_recognition_integration,
    risk_level_scoring_system,
    sandboxed_execution_layer,
    trusted_user_verification,
    voice_biometric_recognition,
)


def _after(user_input: str, prefix: str) -> str:
    return user_input[len(prefix):].strip()


def handle_ai_operations_routes(user_input: str, text: str, clean_text: str):
    if text in ["quantized model selector", "select quantized model", "381 help"]:
        return quantized_model_selector()
    if text in ["model benchmarking engine", "benchmark model plan", "382 help"]:
        return model_benchmarking_engine()
    if text in ["ai inference profiler", "profile inference", "383 help"]:
        return ai_inference_profiler()
    if text in ["local rag system", "local rag preview", "384 help"]:
        return local_rag_system()
    if text in ["document embedding engine", "embed documents", "385 help"]:
        return document_embedding_engine()
    if text in ["semantic search dashboard", "semantic search", "386 help"]:
        return semantic_search_dashboard()
    if text in ["ai memory hierarchy", "memory hierarchy", "387 help"]:
        return ai_memory_hierarchy()
    if text in ["context window optimizer", "optimize context window", "388 help"]:
        return context_window_optimizer()
    if text in ["prompt injection detector", "389 help"]:
        return prompt_injection_detector(user_input)
    if text.startswith("detect prompt injection "):
        return prompt_injection_detector(_after(user_input, "detect prompt injection "))
    if text in ["hallucination risk detector", "390 help"]:
        return hallucination_risk_detector(user_input)
    if text.startswith("detect hallucination risk "):
        return hallucination_risk_detector(_after(user_input, "detect hallucination risk "))
    if text in ["ai confidence scoring", "score ai confidence", "391 help"]:
        return ai_confidence_scoring()
    if text in ["multi-agent orchestration", "multi agent orchestration", "392 help"]:
        return multi_agent_orchestration()
    if text in ["planner agent", "393 help"]:
        return planner_agent()
    if text in ["executor agent", "394 help"]:
        return executor_agent()
    if text in ["critic agent", "395 help"]:
        return critic_agent()
    if text in ["security agent", "396 help"]:
        return security_agent()
    if text in ["seo agent", "397 help"]:
        return seo_agent()
    if text in ["marketing agent", "398 help"]:
        return marketing_agent()
    if text in ["coding agent", "399 help"]:
        return coding_agent()
    if text in ["research agent", "400 help"]:
        return research_agent()
    if text in ["finance agent", "401 help"]:
        return finance_agent()
    if text in ["scheduling agent", "402 help"]:
        return scheduling_agent()
    if text in ["autonomous browser agent", "403 help"]:
        return autonomous_browser_agent()
    if text in ["autonomous deployment agent", "404 help"]:
        return autonomous_deployment_agent()
    if text in ["autonomous monitoring agent", "405 help"]:
        return autonomous_monitoring_agent()
    if text in ["ai swarm coordination", "406 help"]:
        return ai_swarm_coordination()
    if text in ["agent task marketplace", "407 help"]:
        return agent_task_marketplace()
    if text in ["role-based ai delegation", "408 help"]:
        return role_based_ai_delegation()
    if text.startswith("delegate ai task "):
        return role_based_ai_delegation(_after(user_input, "delegate ai task "))
    if text in ["human approval gateway", "409 help"]:
        return human_approval_gateway()
    if text in ["action logging framework", "410 help"]:
        return action_logging_framework()
    if text in ["explain-why engine", "411 help"]:
        return explain_why_engine()
    if text.startswith("explain why "):
        return explain_why_engine(_after(user_input, "explain why "))
    if text in ["decision trace system", "412 help"]:
        return decision_trace_system()
    if text in ["ai ethics constraints", "413 help"]:
        return ai_ethics_constraints()
    if text in ["emergency shutdown mode", "414 help"]:
        return emergency_shutdown_mode()
    if text in ["sandboxed execution layer", "415 help"]:
        return sandboxed_execution_layer()
    if text in ["risk-level scoring system", "416 help"]:
        return risk_level_scoring_system()
    if text.startswith("score risk for "):
        return risk_level_scoring_system(_after(user_input, "score risk for "))
    if text in ["adaptive permission escalation", "417 help"]:
        return adaptive_permission_escalation()
    if text in ["voice biometric recognition", "418 help"]:
        return voice_biometric_recognition()
    if text in ["face recognition integration", "419 help"]:
        return face_recognition_integration()
    if text in ["trusted-user verification", "trusted user verification", "420 help"]:
        return trusted_user_verification()
    return None
