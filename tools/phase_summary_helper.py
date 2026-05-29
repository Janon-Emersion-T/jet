from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable


def safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value


def command_variants(title: str) -> list[str]:
    lowered = title.lower().strip()
    normalized = re.sub(r"[^a-z0-9]+", " ", lowered).strip()
    hyphenated = normalized.replace(" ", "-")
    variants = [lowered]
    for candidate in (normalized, hyphenated):
        if candidate and candidate not in variants:
            variants.append(candidate)
    return variants


def build_phase_handler(namespace: dict, module_dir_name: str, config: dict) -> Callable[[], str]:
    def handler() -> str:
        module_dir = namespace[module_dir_name]
        payload = safe_json(module_dir / config["filename"], {})
        records = payload.get(config.get("collection_key", "records"), []) if isinstance(payload, dict) else []
        healthy = [item for item in records if isinstance(item, dict) and bool(item.get(config.get("healthy_flag", "healthy"), False))]
        attention = [item for item in records if isinstance(item, dict) and bool(item.get(config.get("attention_flag", "attention"), False))]
        return "\n".join([
            f"{config['title'].upper()} - PHASE {config['phase']}",
            f"Mode: {config.get('mode', slugify(config['title']).replace('_', '-'))} overview.",
            f"Records tracked: {len(records)}",
            f"Healthy signals: {len(healthy)}",
            f"Attention signals: {len(attention)}",
            config.get(
                "guardrail",
                "Guardrail: advisory summaries should preserve source context, separate observed signals from assumptions, and require human approval for consequential actions.",
            ),
        ])

    handler.__name__ = config["name"]
    handler.__doc__ = f"Phase {config['phase']}: {config['title']}"
    return handler


def build_phase_module(namespace: dict, module_dir_name: str, phase_configs: list[dict]) -> list[tuple[list[str], Callable[[], str]]]:
    routes = []
    for config in phase_configs:
        handler = build_phase_handler(namespace, module_dir_name, config)
        namespace[config["name"]] = handler
        aliases = command_variants(config["title"])
        aliases.append(f"{config['phase']} help")
        routes.append((aliases, handler))
    return routes
