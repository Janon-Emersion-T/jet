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
    return None
