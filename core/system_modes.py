import json
from pathlib import Path
from datetime import datetime

STORAGE_DIR = Path("storage")
SYSTEM_MODE_FILE = STORAGE_DIR / "system_mode.json"

DEFAULT_STATE = {
    "system_prompt_version": "v1",
    "personality_profile": "default",
    "active_mode": "default",
    "strict_mode": False,
    "developer_mode": False,
    "voice_mode": False,
    "updated_at": None,
}

VALID_PROMPT_VERSIONS = {
    "v1": "Stable baseline JARVIS prompt.",
    "v2": "More structured, safety-aware, mode-sensitive prompt.",
    "v3": "Advanced workstation assistant prompt with stricter tool honesty.",
}

VALID_MODES = {
    "default": "Balanced private workstation assistant.",
    "business": "Business-focused, strategic, execution-oriented, ROI-aware.",
    "tutor": "Teaches clearly, step by step, with correction and examples.",
    "research": "Careful, source-minded, analytical, skeptical, and evidence-driven.",
    "seo": "SEO-focused: keywords, search intent, topical authority, ranking, and conversion.",
    "social": "Social-media-focused: hooks, platform fit, content calendars, captions, and campaigns.",
}

VALID_PERSONALITIES = {
    "default": "Direct, practical, professional.",
    "formal": "Corporate, structured, precise.",
    "friendly": "Warm, conversational, supportive.",
    "strict": "No-nonsense, corrective, high-discipline.",
    "executive": "CEO-level, strategic, concise, decision-oriented.",
    "teacher": "Patient, explanatory, example-heavy.",
}


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _load_state():
    _ensure_storage()

    if not SYSTEM_MODE_FILE.exists():
        return DEFAULT_STATE.copy()

    try:
        data = json.loads(SYSTEM_MODE_FILE.read_text(encoding="utf-8"))
        state = DEFAULT_STATE.copy()
        state.update(data)
        return state
    except Exception:
        return DEFAULT_STATE.copy()


def _save_state(state):
    _ensure_storage()
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    SYSTEM_MODE_FILE.write_text(json.dumps(state, indent=4), encoding="utf-8")


def get_system_mode_state():
    return _load_state()


def show_system_mode():
    state = _load_state()

    return (
        "JARVIS SYSTEM MODE\n"
        f"- Prompt version: {state['system_prompt_version']}\n"
        f"- Personality: {state['personality_profile']}\n"
        f"- Active mode: {state['active_mode']}\n"
        f"- Strict mode: {state['strict_mode']}\n"
        f"- Developer mode: {state['developer_mode']}\n"
        f"- Updated at: {state.get('updated_at') or 'not set'}"
    )


def list_system_modes():
    lines = ["AVAILABLE JARVIS MODES"]
    for key, value in VALID_MODES.items():
        lines.append(f"- {key}: {value}")

    lines.append("\nAVAILABLE PERSONALITIES")
    for key, value in VALID_PERSONALITIES.items():
        lines.append(f"- {key}: {value}")

    lines.append("\nAVAILABLE PROMPT VERSIONS")
    for key, value in VALID_PROMPT_VERSIONS.items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def reset_system_mode():
    state = DEFAULT_STATE.copy()
    _save_state(state)
    return "JARVIS system mode reset to default."


def set_prompt_version(version):
    version = version.lower().strip()

    if version not in VALID_PROMPT_VERSIONS:
        return (
            "Unknown prompt version.\n"
            "Available versions:\n"
            + "\n".join(f"- {key}: {value}" for key, value in VALID_PROMPT_VERSIONS.items())
        )

    state = _load_state()
    state["system_prompt_version"] = version
    _save_state(state)

    return f"System prompt version set to: {version}"


def set_personality_profile(profile):
    profile = profile.lower().strip()

    if profile not in VALID_PERSONALITIES:
        return (
            "Unknown personality profile.\n"
            "Available profiles:\n"
            + "\n".join(f"- {key}: {value}" for key, value in VALID_PERSONALITIES.items())
        )

    state = _load_state()
    state["personality_profile"] = profile
    _save_state(state)

    return f"Personality profile set to: {profile}"


def set_active_mode(mode):
    mode = mode.lower().strip()

    aliases = {
        "social media": "social",
        "social_media": "social",
        "dev": "developer",
    }

    mode = aliases.get(mode, mode)

    if mode == "developer":
        return set_developer_mode(True)

    if mode not in VALID_MODES:
        return (
            "Unknown mode.\n"
            "Available modes:\n"
            + "\n".join(f"- {key}: {value}" for key, value in VALID_MODES.items())
        )

    state = _load_state()
    state["active_mode"] = mode
    _save_state(state)

    return f"JARVIS mode set to: {mode}"


def set_strict_mode(enabled):
    state = _load_state()
    state["strict_mode"] = bool(enabled)
    _save_state(state)

    return f"Strict mode {'enabled' if enabled else 'disabled'}."


def set_voice_mode(enabled):
    state = _load_state()
    state["voice_mode"] = bool(enabled)
    _save_state(state)

    return f"Voice mode {'enabled' if enabled else 'disabled'}."


def set_developer_mode(enabled):
    state = _load_state()
    state["developer_mode"] = bool(enabled)
    _save_state(state)

    return f"Developer mode {'enabled' if enabled else 'disabled'}."


def build_mode_context():
    state = _load_state()

    mode = state["active_mode"]
    personality = state["personality_profile"]
    prompt_version = state["system_prompt_version"]

    strict_rule = (
        "Strict mode is ON. Be conservative. Do not suggest risky writes, shell commands, browser automation, "
        "deployment, deletion, credential handling, or external actions without confirmation."
        if state["strict_mode"]
        else "Strict mode is OFF. Normal safety rules still apply."
    )

    developer_rule = (
        "Developer mode is ON. Prioritize architecture, debugging, modular code, tests, and implementation details."
        if state["developer_mode"]
        else "Developer mode is OFF. Keep responses practical and balanced."
    )

    return f"""
JARVIS Runtime Configuration:
- System prompt version: {prompt_version}
- Prompt version behavior: {VALID_PROMPT_VERSIONS.get(prompt_version, VALID_PROMPT_VERSIONS["v1"])}
- Personality profile: {personality}
- Personality behavior: {VALID_PERSONALITIES.get(personality, VALID_PERSONALITIES["default"])}
- Active mode: {mode}
- Mode behavior: {VALID_MODES.get(mode, VALID_MODES["default"])}
- Strict mode: {state["strict_mode"]}
- Developer mode: {state["developer_mode"]}

Rules:
- {strict_rule}
- {developer_rule}
- Never claim access to tools unless a real route/tool executed.
- Prefer read-only inspection before write/execution.
- Dangerous actions require confirmation.
""".strip()