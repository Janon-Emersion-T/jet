from __future__ import annotations

import json
from pathlib import Path


LEGACY_MEANING_DIR = Path("storage/legacy_meaning")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _overview(title: str, mode: str, lines: list[str], guardrail: str) -> str:
    return "\n".join([title, f"Mode: {mode}.", *lines, guardrail])


def legacy_intelligence_archive() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "legacy_archive.json", {})
    archives = payload.get("archives", []) if isinstance(payload, dict) else []
    indexed = [item for item in archives if isinstance(item, dict) and bool(item.get("indexed", False))]
    incomplete = [item for item in archives if isinstance(item, dict) and bool(item.get("incomplete", False))]
    return _overview("LEGACY INTELLIGENCE ARCHIVE - PHASE 861", "legacy-archive overview", [f"Archives tracked: {len(archives)}", f"Indexed archives: {len(indexed)}", f"Incomplete archives: {len(incomplete)}"], "Guardrail: legacy archives should preserve attribution, consent, and contextual integrity before reuse.")


def ai_assisted_immortality_research() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "immortality_research.json", {})
    studies = payload.get("studies", []) if isinstance(payload, dict) else []
    reviewed = [item for item in studies if isinstance(item, dict) and bool(item.get("reviewed", False))]
    speculative = [item for item in studies if isinstance(item, dict) and bool(item.get("speculative", False))]
    return _overview("AI-ASSISTED IMMORTALITY RESEARCH - PHASE 862", "immortality-research overview", [f"Studies tracked: {len(studies)}", f"Reviewed studies: {len(reviewed)}", f"Speculative studies: {len(speculative)}"], "Guardrail: immortality research support should remain speculative, evidence-sensitive, and ethically bounded before claims.")


def consciousness_emulation_sandbox() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "consciousness_emulation.json", {})
    models = payload.get("models", []) if isinstance(payload, dict) else []
    emulated = [item for item in models if isinstance(item, dict) and bool(item.get("emulated", False))]
    unstable = [item for item in models if isinstance(item, dict) and bool(item.get("unstable", False))]
    return _overview("CONSCIOUSNESS EMULATION SANDBOX - PHASE 863", "consciousness-emulation overview", [f"Models tracked: {len(models)}", f"Emulated models: {len(emulated)}", f"Unstable models: {len(unstable)}"], "Guardrail: consciousness emulation should remain sandboxed, non-definitive, and ethically reviewed before interpretation.")


def digital_continuity_framework() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "digital_continuity.json", {})
    continuities = payload.get("continuities", []) if isinstance(payload, dict) else []
    linked = [item for item in continuities if isinstance(item, dict) and bool(item.get("linked", False))]
    ambiguous = [item for item in continuities if isinstance(item, dict) and bool(item.get("ambiguous", False))]
    return _overview("DIGITAL CONTINUITY FRAMEWORK - PHASE 864", "digital-continuity overview", [f"Continuities tracked: {len(continuities)}", f"Linked continuities: {len(linked)}", f"Ambiguous continuities: {len(ambiguous)}"], "Guardrail: digital continuity should preserve consent, identity boundaries, and visible uncertainty before representation.")


def autonomous_philosophical_inquiry() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "philosophical_inquiry.json", {})
    inquiries = payload.get("inquiries", []) if isinstance(payload, dict) else []
    advanced = [item for item in inquiries if isinstance(item, dict) and bool(item.get("advanced", False))]
    unresolved = [item for item in inquiries if isinstance(item, dict) and bool(item.get("unresolved", False))]
    return _overview("AUTONOMOUS PHILOSOPHICAL INQUIRY - PHASE 865", "philosophical-inquiry overview", [f"Inquiries tracked: {len(inquiries)}", f"Advanced inquiries: {len(advanced)}", f"Unresolved inquiries: {len(unresolved)}"], "Guardrail: autonomous inquiry should preserve plural viewpoints and avoid presenting speculative synthesis as settled truth.")


def human_meaning_exploration_ai() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "meaning_exploration.json", {})
    journeys = payload.get("journeys", []) if isinstance(payload, dict) else []
    reflective = [item for item in journeys if isinstance(item, dict) and bool(item.get("reflective", False))]
    vulnerable = [item for item in journeys if isinstance(item, dict) and bool(item.get("vulnerable", False))]
    return _overview("HUMAN MEANING EXPLORATION AI - PHASE 866", "meaning-exploration overview", [f"Journeys tracked: {len(journeys)}", f"Reflective journeys: {len(reflective)}", f"Vulnerable journeys: {len(vulnerable)}"], "Guardrail: meaning exploration should preserve autonomy, emotional safety, and clear non-clinical boundaries before guidance.")


def creative_civilization_accelerator() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "creative_civilization.json", {})
    programs = payload.get("programs", []) if isinstance(payload, dict) else []
    accelerated = [item for item in programs if isinstance(item, dict) and bool(item.get("accelerated", False))]
    stalled = [item for item in programs if isinstance(item, dict) and bool(item.get("stalled", False))]
    return _overview("CREATIVE CIVILIZATION ACCELERATOR - PHASE 867", "creative-civilization overview", [f"Programs tracked: {len(programs)}", f"Accelerated programs: {len(accelerated)}", f"Stalled programs: {len(stalled)}"], "Guardrail: creativity accelerators should preserve attribution, inclusion, and human artistic agency before scaling.")


def infinite_learning_ecosystem() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "infinite_learning.json", {})
    paths = payload.get("paths", []) if isinstance(payload, dict) else []
    adaptive = [item for item in paths if isinstance(item, dict) and bool(item.get("adaptive", False))]
    fragmented = [item for item in paths if isinstance(item, dict) and bool(item.get("fragmented", False))]
    return _overview("INFINITE LEARNING ECOSYSTEM - PHASE 868", "infinite-learning overview", [f"Paths tracked: {len(paths)}", f"Adaptive paths: {len(adaptive)}", f"Fragmented paths: {len(fragmented)}"], "Guardrail: lifelong learning ecosystems should preserve accessibility, coherence, and humane pacing before expansion.")


def autonomous_curiosity_civilization() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "curiosity_civilization.json", {})
    probes = payload.get("probes", []) if isinstance(payload, dict) else []
    active = [item for item in probes if isinstance(item, dict) and item.get("status") == "active"]
    bounded = [item for item in probes if isinstance(item, dict) and bool(item.get("bounded", False))]
    return _overview("AUTONOMOUS CURIOSITY CIVILIZATION - PHASE 869", "curiosity-civilization overview", [f"Probes tracked: {len(probes)}", f"Active probes: {len(active)}", f"Bounded probes: {len(bounded)}"], "Guardrail: curiosity at civilization scale should preserve safety, purpose, and explicit stop conditions before exploration.")


def ai_guided_species_development() -> str:
    payload = _safe_json(LEGACY_MEANING_DIR / "species_development.json", {})
    trajectories = payload.get("trajectories", []) if isinstance(payload, dict) else []
    guided = [item for item in trajectories if isinstance(item, dict) and bool(item.get("guided", False))]
    contested = [item for item in trajectories if isinstance(item, dict) and bool(item.get("contested", False))]
    return _overview("AI-GUIDED SPECIES DEVELOPMENT - PHASE 870", "species-development overview", [f"Trajectories tracked: {len(trajectories)}", f"Guided trajectories: {len(guided)}", f"Contested trajectories: {len(contested)}"], "Guardrail: species-level development ideas should remain speculative, pluralistic, and firmly subordinate to human ethics.")
