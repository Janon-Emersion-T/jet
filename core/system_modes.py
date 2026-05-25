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
    "updated_at": None,
}

VALID_MODES = {
    "default": "Balanced private workstation assistant.",
    "business": "Business-focused, strategic, execution-oriented.",
    "tutor": "Teaches clearly step-by-step with corrections.",
    "research": "Careful, source-minded, analytical.",
    "seo": "SEO-focused content, ranking, keyword and SERP thinking.",
    "social": "Social media content and campaign-oriented.",
}

VALID_PERSONALITIES = {
    "default": "Direct, practical, professional.",
    "formal": "Corporate, structured, precise.",
    "friendly": "Warm, conversational, supportive.",
    "strict": "No-nonsense, corrective, high-discipline.",
}


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _load_state():
    _ensure_storage()

    if not SYSTEM_MODE_FILE.exists():
        return DEFAULT_STATE.copy()

    try:
        data = json.loads(SYSTEM_MODE_FILE.read_text())
        state = DEFAULT_STATE.copy()
        state.update(data)
        return state
    except Exception:
        return DEFAULT_STATE.copy()


def _save_state(state):
    _ensure_storage()
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    SYSTEM_MODE_FILE.write_text(json.dumps(state, indent=4))


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


def set_prompt_version(version):
    version = version.strip()

    if not version:
        return "Prompt version is required."

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


def set_developer_mode(enabled):
    state = _load_state()
    state["developer_mode"] = bool(enabled)
    _save_state(state)

    return f"Developer mode {'enabled' if enabled else 'disabled'}."


def build_mode_context():
    state = _load_state()

    mode = state["active_mode"]
    personality = state["personality_profile"]

    return f"""
JARVIS Runtime Configuration:
- System prompt version: {state['system_prompt_version']}
- Personality profile: {personality}
- Active mode: {mode}
- Strict mode: {state['strict_mode']}
- Developer mode: {state['developer_mode']}

Mode instruction:
{VALID_MODES.get(mode, VALID_MODES['default'])}

Personality instruction:
{VALID_PERSONALITIES.get(personality, VALID_PERSONALITIES['default'])}

Strict mode rule:
{"Be extra cautious. Do not execute or suggest risky actions without confirmation." if state["strict_mode"] else "Normal safety mode."}

Developer mode rule:
{"Prioritize code architecture, debugging, implementation details, and developer-grade explanations." if state["developer_mode"] else "Normal assistant behavior."}
""".strip()