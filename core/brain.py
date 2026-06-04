from __future__ import annotations

import subprocess
from typing import Iterable

import requests

from core.models.model_config import load_model_settings
from core.models.model_router import detect_model_route
from core.models.prompt_templates import load_prompt_templates

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"


def _list_installed_models() -> list[str]:
    try:
        response = requests.get(OLLAMA_TAGS_URL, timeout=10)
        response.raise_for_status()
        models = response.json().get("models", [])
        names = [item.get("name", "").strip() for item in models if item.get("name")]
        if names:
            return names
    except Exception:
        pass

    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except Exception:
        return []

    if result.returncode != 0:
        return []

    lines = result.stdout.strip().splitlines()
    return [line.split()[0] for line in lines[1:] if line.split()]


def _resolve_model_name(preferred_model: str, installed_models: Iterable[str]) -> str:
    preferred = (preferred_model or "").strip()
    available = [model.strip() for model in installed_models if model.strip()]

    if not preferred or not available:
        return preferred

    if preferred in available:
        return preferred

    for candidate in available:
        if candidate.startswith(f"{preferred}:"):
            return candidate

    preferred_base = preferred.split(":", 1)[0]

    for candidate in available:
        if candidate.split(":", 1)[0] == preferred_base:
            return candidate

    return preferred


def _unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    for value in values:
        clean = (value or "").strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        ordered.append(clean)

    return ordered


def _build_model_candidates(
    prompt: str,
    route_hint: str | None = None,
    preferred_models: list[str] | None = None,
) -> tuple[str, list[str], dict]:
    settings = load_model_settings()
    route_decision = detect_model_route(prompt)
    route = (route_hint or route_decision.get("route") or "general").strip()
    installed = _list_installed_models()

    if preferred_models:
        raw_candidates = preferred_models
    else:
        route_key = f"{route}_model"
        raw_candidates = [
            settings.get(route_key) or route_decision.get("model"),
            settings.get("fallback_model") or route_decision.get("fallback_model"),
            route_decision.get("model"),
            route_decision.get("fallback_model"),
        ]

    resolved = _unique_preserve_order(
        _resolve_model_name(candidate, installed) for candidate in raw_candidates
    )

    return route, resolved, settings


def ask_brain(
    prompt: str,
    *,
    route_hint: str | None = None,
    system_prompt: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    preferred_models: list[str] | None = None,
) -> str:
    route, model_candidates, settings = _build_model_candidates(
        prompt,
        route_hint=route_hint,
        preferred_models=preferred_models,
    )
    templates = load_prompt_templates()
    system = system_prompt or templates.get(route) or templates.get("general", "")
    options = {
        "temperature": temperature if temperature is not None else settings.get("temperature", 0.3),
        "num_predict": max_tokens if max_tokens is not None else settings.get("max_tokens", 4096),
    }
    keep_alive = settings.get("ollama_keep_alive", "0s")

    if not model_candidates:
        return "Brain error: No Ollama model is configured or available."

    last_error = "Unknown error"

    for model_name in model_candidates:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": options,
            "keep_alive": keep_alive,
        }

        try:
            response = requests.post(OLLAMA_GENERATE_URL, json=payload, timeout=180)
            response.raise_for_status()
            reply = response.json().get("response", "").strip()
            if reply:
                return reply
            last_error = f"Model {model_name} returned an empty response."
        except Exception as exc:
            last_error = f"{model_name}: {exc}"

    return f"Brain error: {last_error}"
