from __future__ import annotations

import json
from pathlib import Path


AI_SUSTAIN_DIR = Path("storage/ai_sustainability_governance")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def sustainable_ai_compute_management() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "sustainable_compute.json", {})
    fleets = payload.get("fleets", []) if isinstance(payload, dict) else []
    optimized = [item for item in fleets if isinstance(item, dict) and bool(item.get("optimized", False))]
    wasteful = [item for item in fleets if isinstance(item, dict) and bool(item.get("wasteful", False))]
    return _overview("SUSTAINABLE AI COMPUTE MANAGEMENT - PHASE 841", "sustainable-compute overview", [f"Fleets tracked: {len(fleets)}", f"Optimized fleets: {len(optimized)}", f"Wasteful fleets: {len(wasteful)}"], "Guardrail: sustainable compute management should preserve service reliability and transparent environmental tradeoffs before optimization.")


def energy_aware_inference_scheduling() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "energy_aware_scheduling.json", {})
    jobs = payload.get("jobs", []) if isinstance(payload, dict) else []
    shifted = [item for item in jobs if isinstance(item, dict) and bool(item.get("shifted", False))]
    urgent = [item for item in jobs if isinstance(item, dict) and item.get("priority") == "urgent"]
    return _overview("ENERGY-AWARE INFERENCE SCHEDULING - PHASE 842", "energy-aware-scheduling overview", [f"Jobs tracked: {len(jobs)}", f"Shifted jobs: {len(shifted)}", f"Urgent jobs: {len(urgent)}"], "Guardrail: energy-aware scheduling should preserve latency commitments, fairness, and explicit overrides before deferral.")


def carbon_neutral_ai_framework() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "carbon_neutral_ai.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    offset = [item for item in programs if isinstance(item, dict) and bool(item.get("offset", False))]
    uncovered = [item for item in programs if isinstance(item, dict) and bool(item.get("uncovered", False))]
    return _overview("CARBON-NEUTRAL AI FRAMEWORK - PHASE 843", "carbon-neutral-ai overview", [f"Programs tracked: {len(programs)}", f"Offset programs: {len(offset)}", f"Uncovered programs: {len(uncovered)}"], "Guardrail: carbon claims should remain measurable, auditable, and honest about residual emissions before external reporting.")


def ai_ethics_telemetry() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "ethics_telemetry.json", {})
    signals = payload.get("signals", []) if isinstance(payload, dict) else []
    monitored = [item for item in signals if isinstance(item, dict) and bool(item.get("monitored", False))]
    anomalous = [item for item in signals if isinstance(item, dict) and bool(item.get("anomalous", False))]
    return _overview("AI ETHICS TELEMETRY - PHASE 844", "ethics-telemetry overview", [f"Signals tracked: {len(signals)}", f"Monitored signals: {len(monitored)}", f"Anomalous signals: {len(anomalous)}"], "Guardrail: ethics telemetry should preserve privacy, contextual interpretation, and actionable human review before enforcement.")


def autonomous_transparency_reporting() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "transparency_reporting.json", {})
    reports = payload.get("reports", []) if isinstance(payload, dict) else []
    published = [item for item in reports if isinstance(item, dict) and bool(item.get("published", False))]
    delayed = [item for item in reports if isinstance(item, dict) and bool(item.get("delayed", False))]
    return _overview("AUTONOMOUS TRANSPARENCY REPORTING - PHASE 845", "transparency-reporting overview", [f"Reports tracked: {len(reports)}", f"Published reports: {len(published)}", f"Delayed reports: {len(delayed)}"], "Guardrail: transparency reporting should preserve factual completeness, scope clarity, and human accountability before release.")


def explainable_planetary_ai() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "explainable_planetary_ai.json", {})
    decisions = payload.get("decisions", []) if isinstance(payload, dict) else []
    explained = [item for item in decisions if isinstance(item, dict) and bool(item.get("explained", False))]
    opaque = [item for item in decisions if isinstance(item, dict) and bool(item.get("opaque", False))]
    return _overview("EXPLAINABLE PLANETARY AI - PHASE 846", "explainable-planetary-ai overview", [f"Decisions tracked: {len(decisions)}", f"Explained decisions: {len(explained)}", f"Opaque decisions: {len(opaque)}"], "Guardrail: planetary-scale AI should preserve legibility, contestability, and local context before influence.")


def ai_democracy_participation_engine() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "democracy_participation.json", {})
    forums = payload.get("forums", []) if isinstance(payload, dict) else []
    active = [item for item in forums if isinstance(item, dict) and item.get("status") == "active"]
    inclusive = [item for item in forums if isinstance(item, dict) and bool(item.get("inclusive", False))]
    return _overview("AI DEMOCRACY PARTICIPATION ENGINE - PHASE 847", "democracy-participation overview", [f"Forums tracked: {len(forums)}", f"Active forums: {len(active)}", f"Inclusive forums: {len(inclusive)}"], "Guardrail: participation tooling should preserve fairness, anti-manipulation safeguards, and user agency before civic deployment.")


def collective_reasoning_networks() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "collective_reasoning.json", {})
    networks = payload.get("networks", []) if isinstance(payload, dict) else []
    synchronized = [item for item in networks if isinstance(item, dict) and bool(item.get("synchronized", False))]
    divergent = [item for item in networks if isinstance(item, dict) and bool(item.get("divergent", False))]
    return _overview("COLLECTIVE REASONING NETWORKS - PHASE 848", "collective-reasoning overview", [f"Networks tracked: {len(networks)}", f"Synchronized networks: {len(synchronized)}", f"Divergent networks: {len(divergent)}"], "Guardrail: collective reasoning should preserve dissent, source attribution, and non-coercive synthesis before consensus.")


def swarm_cognition_framework() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "swarm_cognition.json", {})
    swarms = payload.get("swarms", []) if isinstance(payload, dict) else []
    coordinated = [item for item in swarms if isinstance(item, dict) and bool(item.get("coordinated", False))]
    unstable = [item for item in swarms if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("SWARM COGNITION FRAMEWORK - PHASE 849", "swarm-cognition overview", [f"Swarms tracked: {len(swarms)}", f"Coordinated swarms: {len(coordinated)}", f"Unstable swarms: {len(unstable)}"], "Guardrail: swarm cognition should preserve controllability, observability, and human interruption before autonomy scales.")


def shared_human_ai_memory_fabric() -> str:
    payload = _safe_json(AI_SUSTAIN_DIR / "shared_memory_fabric.json", {})
    memories = payload.get("memories", []) if isinstance(payload, dict) else []
    shared = [item for item in memories if isinstance(item, dict) and bool(item.get("shared", False))]
    restricted = [item for item in memories if isinstance(item, dict) and bool(item.get("restricted", False))]
    return _overview("SHARED HUMAN-AI MEMORY FABRIC - PHASE 850", "shared-memory-fabric overview", [f"Memories tracked: {len(memories)}", f"Shared memories: {len(shared)}", f"Restricted memories: {len(restricted)}"], "Guardrail: shared memory fabrics should preserve consent, provenance, and fine-grained access boundaries before federation.")
