from __future__ import annotations

import json
from pathlib import Path


LOCAL_MODEL_RUNTIME_DIR = Path("storage/local_model_runtime")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _render(title: str, mode: str, filename: str, key: str, positive_flag: str, risk_flag: str, key_label: str, positive_label: str, risk_label: str, guardrail: str) -> str:
    payload = _safe_json(LOCAL_MODEL_RUNTIME_DIR / filename, {})
    items = payload.get(key, []) if isinstance(payload, dict) else []
    positives = [item for item in items if isinstance(item, dict) and bool(item.get(positive_flag, False))]
    risks = [item for item in items if isinstance(item, dict) and bool(item.get(risk_flag, False))]
    return "\n".join([title, f"Mode: {mode}.", f"{key_label}: {len(items)}", f"{positive_label}: {len(positives)}", f"{risk_label}: {len(risks)}", guardrail])


def local_model_benchmark_lab() -> str:
    return _render("LOCAL MODEL BENCHMARK LAB - PHASE 1701", "local-model-benchmark overview", "local_model_benchmark_lab.json", "benchmark_runs", "usable", "noisy", "Benchmark runs tracked", "Usable runs", "Noisy runs", "Guardrail: benchmark analysis should preserve hardware parity, prompt-set transparency, and avoid overgeneralizing from one workload.")


def model_quantization_advisor() -> str:
    return _render("MODEL QUANTIZATION ADVISOR - PHASE 1702", "model-quantization overview", "model_quantization_advisor.json", "quantization_profiles", "balanced", "degraded", "Quantization profiles tracked", "Balanced profiles", "Degraded profiles", "Guardrail: quantization advice should preserve task-specific quality tradeoffs and note when memory wins cause unacceptable accuracy loss.")


def ollama_model_router() -> str:
    return _render("OLLAMA MODEL ROUTER - PHASE 1703", "ollama-routing overview", "ollama_model_router.json", "routing_paths", "matched", "misrouted", "Routing paths tracked", "Matched paths", "Misrouted paths", "Guardrail: model routing should preserve user intent, cost/latency tradeoff visibility, and deterministic fallbacks when uncertain.")


def hardware_aware_inference_planner() -> str:
    return _render("HARDWARE-AWARE INFERENCE PLANNER - PHASE 1704", "hardware-aware-inference overview", "hardware_aware_inference_planner.json", "inference_plans", "fit", "overloaded", "Inference plans tracked", "Fit plans", "Overloaded plans", "Guardrail: inference planning should preserve thermal, memory, and concurrency constraints instead of optimizing only for peak throughput.")


def cpu_gpu_load_balancer() -> str:
    return _render("CPU/GPU LOAD BALANCER - PHASE 1705", "cpu-gpu-balancing overview", "cpu_gpu_load_balancer.json", "load_paths", "balanced", "saturated", "Load paths tracked", "Balanced paths", "Saturated paths", "Guardrail: load balancing should preserve system responsiveness and avoid starving critical background services for model throughput.")


def context_window_budgeter() -> str:
    return _render("CONTEXT-WINDOW BUDGETER - PHASE 1706", "context-window-budget overview", "context_window_budgeter.json", "context_budgets", "efficient", "overflowing", "Context budgets tracked", "Efficient budgets", "Overflowing budgets", "Guardrail: context budgeting should preserve essential evidence, disclose compression, and avoid silent truncation of critical context.")


def prompt_compression_engine() -> str:
    return _render("PROMPT COMPRESSION ENGINE - PHASE 1707", "prompt-compression overview", "prompt_compression_engine.json", "compression_runs", "faithful", "distorted", "Compression runs tracked", "Faithful runs", "Distorted runs", "Guardrail: prompt compression should preserve instructions hierarchy and clearly mark when details were collapsed or removed.")


def multi_model_debate_mode() -> str:
    return _render("MULTI-MODEL DEBATE MODE - PHASE 1708", "multi-model-debate overview", "multi_model_debate_mode.json", "debate_rounds", "useful", "circular", "Debate rounds tracked", "Useful rounds", "Circular rounds", "Guardrail: model debate should preserve source grounding and avoid presenting consensus among weak evidence as stronger truth.")


def critic_verifier_architecture() -> str:
    return _render("CRITIC-VERIFIER ARCHITECTURE - PHASE 1709", "critic-verifier overview", "critic_verifier_architecture.json", "verification_paths", "checked", "unverified", "Verification paths tracked", "Checked paths", "Unverified paths", "Guardrail: critic-verifier flows should preserve independence between generation and checking rather than superficial self-agreement.")


def answer_confidence_scorer() -> str:
    return _render("ANSWER CONFIDENCE SCORER - PHASE 1710", "answer-confidence overview", "answer_confidence_scorer.json", "answer_scores", "calibrated", "overconfident", "Answer scores tracked", "Calibrated scores", "Overconfident scores", "Guardrail: confidence scoring should preserve calibration transparency and never substitute a score for evidence quality.")
