from __future__ import annotations

import json
from pathlib import Path


SYSTEMS_FRONTIER_DIR = Path("storage/systems_frontier")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def advanced_cryptography_framework() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "advanced_crypto.json", {})
    schemes = payload.get("schemes", []) if isinstance(payload, dict) else []
    approved = [item for item in schemes if isinstance(item, dict) and bool(item.get("approved", False))]
    experimental = [item for item in schemes if isinstance(item, dict) and bool(item.get("experimental", False))]
    return _overview("ADVANCED CRYPTOGRAPHY FRAMEWORK - PHASE 661", "advanced-cryptography overview", [f"Schemes tracked: {len(schemes)}", f"Approved schemes: {len(approved)}", f"Experimental schemes: {len(experimental)}"], "Guardrail: cryptography guidance should prefer reviewed primitives, threat-model fit, and conservative rollout over novelty.")


def post_quantum_security_advisor() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "post_quantum.json", {})
    assets = payload.get("assets", []) if isinstance(payload, dict) else []
    migrated = [item for item in assets if isinstance(item, dict) and bool(item.get("migrated", False))]
    exposed = [item for item in assets if isinstance(item, dict) and item.get("risk") == "high"]
    return _overview("POST-QUANTUM SECURITY ADVISOR - PHASE 662", "post-quantum overview", [f"Assets tracked: {len(assets)}", f"Migrated assets: {len(migrated)}", f"High-risk assets: {len(exposed)}"], "Guardrail: post-quantum planning should remain inventory-driven, migration-aware, and compatibility-tested before cutover.")


def neural_architecture_search_engine() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "nas_engine.json", {})
    searches = payload.get("searches", []) if isinstance(payload, dict) else []
    converged = [item for item in searches if isinstance(item, dict) and bool(item.get("converged", False))]
    costly = [item for item in searches if isinstance(item, dict) and item.get("cost") == "high"]
    return _overview("NEURAL ARCHITECTURE SEARCH ENGINE - PHASE 663", "nas overview", [f"Searches tracked: {len(searches)}", f"Converged searches: {len(converged)}", f"High-cost searches: {len(costly)}"], "Guardrail: architecture search should surface cost, reproducibility, and evaluation quality before adopting a model.")


def autonomous_compiler_optimizer() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "compiler_optimizer.json", {})
    builds = payload.get("builds", []) if isinstance(payload, dict) else []
    optimized = [item for item in builds if isinstance(item, dict) and bool(item.get("optimized", False))]
    regressed = [item for item in builds if isinstance(item, dict) and bool(item.get("regressed", False))]
    return _overview("AUTONOMOUS COMPILER OPTIMIZER - PHASE 664", "compiler-optimization overview", [f"Builds tracked: {len(builds)}", f"Optimized builds: {len(optimized)}", f"Regressed builds: {len(regressed)}"], "Guardrail: compiler optimization should preserve correctness, benchmark visibility, and rollback paths before applying transformations.")


def operating_system_intelligence_layer() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "os_intelligence.json", {})
    subsystems = payload.get("subsystems", []) if isinstance(payload, dict) else []
    healthy = [item for item in subsystems if isinstance(item, dict) and item.get("status") == "healthy"]
    noisy = [item for item in subsystems if isinstance(item, dict) and item.get("status") == "noisy"]
    return _overview("OPERATING SYSTEM INTELLIGENCE LAYER - PHASE 665", "os-intelligence overview", [f"Subsystems tracked: {len(subsystems)}", f"Healthy subsystems: {len(healthy)}", f"Noisy subsystems: {len(noisy)}"], "Guardrail: OS intelligence should remain observable, minimally invasive, and rollback-friendly before changing runtime behavior.")


def ai_kernel_assistant() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "kernel_assistant.json", {})
    advisories = payload.get("advisories", []) if isinstance(payload, dict) else []
    reviewed = [item for item in advisories if isinstance(item, dict) and bool(item.get("reviewed", False))]
    critical = [item for item in advisories if isinstance(item, dict) and item.get("severity") == "critical"]
    return _overview("AI KERNEL ASSISTANT - PHASE 666", "kernel-assistant overview", [f"Advisories tracked: {len(advisories)}", f"Reviewed advisories: {len(reviewed)}", f"Critical advisories: {len(critical)}"], "Guardrail: kernel guidance should remain correctness-first, human-reviewed, and explicit about blast radius before tuning low-level behavior.")


def ai_driven_filesystem_optimizer() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "filesystem_optimizer.json", {})
    volumes = payload.get("volumes", []) if isinstance(payload, dict) else []
    tuned = [item for item in volumes if isinstance(item, dict) and bool(item.get("tuned", False))]
    fragmented = [item for item in volumes if isinstance(item, dict) and item.get("status") == "fragmented"]
    return _overview("AI-DRIVEN FILESYSTEM OPTIMIZER - PHASE 667", "filesystem-optimization overview", [f"Volumes tracked: {len(volumes)}", f"Tuned volumes: {len(tuned)}", f"Fragmented volumes: {len(fragmented)}"], "Guardrail: filesystem optimization should preserve integrity, backup safety, and low-risk rollout before modifying storage behavior.")


def smart_memory_allocation_system() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "memory_allocation.json", {})
    pools = payload.get("pools", []) if isinstance(payload, dict) else []
    balanced = [item for item in pools if isinstance(item, dict) and bool(item.get("balanced", False))]
    pressured = [item for item in pools if isinstance(item, dict) and item.get("status") == "pressured"]
    return _overview("SMART MEMORY ALLOCATION SYSTEM - PHASE 668", "memory-allocation overview", [f"Pools tracked: {len(pools)}", f"Balanced pools: {len(balanced)}", f"Pressured pools: {len(pressured)}"], "Guardrail: memory allocation should preserve stability, avoid starvation, and keep operator visibility before applying adaptive policies.")


def ai_hardware_diagnostics() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "hardware_diagnostics.json", {})
    components = payload.get("components", []) if isinstance(payload, dict) else []
    failing = [item for item in components if isinstance(item, dict) and item.get("health") == "failing"]
    monitored = [item for item in components if isinstance(item, dict) and bool(item.get("monitored", False))]
    return _overview("AI HARDWARE DIAGNOSTICS - PHASE 669", "hardware-diagnostics overview", [f"Components tracked: {len(components)}", f"Failing components: {len(failing)}", f"Monitored components: {len(monitored)}"], "Guardrail: hardware diagnostics should privilege signal quality, serviceability, and non-destructive validation before action.")


def autonomous_chip_optimization() -> str:
    payload = _safe_json(SYSTEMS_FRONTIER_DIR / "chip_optimization.json", {})
    profiles = payload.get("profiles", []) if isinstance(payload, dict) else []
    efficient = [item for item in profiles if isinstance(item, dict) and bool(item.get("efficient", False))]
    constrained = [item for item in profiles if isinstance(item, dict) and bool(item.get("thermal_bound", False))]
    return _overview("AUTONOMOUS CHIP OPTIMIZATION - PHASE 670", "chip-optimization overview", [f"Profiles tracked: {len(profiles)}", f"Efficient profiles: {len(efficient)}", f"Thermally constrained profiles: {len(constrained)}"], "Guardrail: chip optimization should remain thermally safe, benchmark-validated, and reversible before deployment.")
