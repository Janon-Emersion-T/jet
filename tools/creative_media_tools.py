from __future__ import annotations

import json
import os
from pathlib import Path


MEDIA_DIR = Path("storage/creative_media")


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_entries(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def media_generation_assistant() -> str:
    assets = _list_entries(MEDIA_DIR / "assets.json", "assets")
    pending = [item for item in assets if isinstance(item, dict) and item.get("status", "draft") != "done"]
    return "\n".join(
        [
            "MEDIA GENERATION ASSISTANT - PHASE 471",
            "Mode: media backlog overview.",
            f"Tracked assets: {len(assets)}",
            f"Pending assets: {len(pending)}",
            "Focus: brief quality, format fit, approval checkpoints, and version discipline.",
        ]
    )


def ai_video_generation_pipeline() -> str:
    jobs = _list_entries(MEDIA_DIR / "video_jobs.json", "jobs")
    active = [item for item in jobs if isinstance(item, dict) and item.get("status", "queued") in {"queued", "rendering"}]
    engine = os.getenv("VIDEO_GEN_BACKEND", "").strip() or "not configured"
    return "\n".join(
        [
            "AI VIDEO GENERATION PIPELINE - PHASE 472",
            "Mode: video-pipeline readiness review.",
            f"Backend: {engine}",
            f"Tracked jobs: {len(jobs)}",
            f"Active jobs: {len(active)}",
            "Safety: planning and queue visibility only; no render job was started here.",
        ]
    )


def voice_cloning_sandbox() -> str:
    profiles = _list_entries(MEDIA_DIR / "voice_profiles.json", "profiles")
    consented = [item for item in profiles if isinstance(item, dict) and bool(item.get("consent", False))]
    return "\n".join(
        [
            "VOICE CLONING SANDBOX - PHASE 473",
            "Mode: constrained research sandbox.",
            f"Voice profiles: {len(profiles)}",
            f"Profiles with recorded consent: {len(consented)}",
            "Policy: explicit consent, labeling, and non-production experimentation only.",
        ]
    )


def podcast_assistant() -> str:
    episodes = _list_entries(MEDIA_DIR / "podcasts.json", "episodes")
    planned = [item for item in episodes if isinstance(item, dict) and item.get("status", "planned") != "published"]
    return "\n".join(
        [
            "PODCAST ASSISTANT - PHASE 474",
            "Mode: podcast workflow overview.",
            f"Episodes tracked: {len(episodes)}",
            f"Unpublished episodes: {len(planned)}",
            "Workflow: outline, guest prep, recording, edit notes, distribution, and clip extraction.",
        ]
    )


def music_generation_sandbox() -> str:
    tracks = _list_entries(MEDIA_DIR / "music_tracks.json", "tracks")
    stems = sum(int(item.get("stems", 0) or 0) for item in tracks if isinstance(item, dict))
    return "\n".join(
        [
            "MUSIC GENERATION SANDBOX - PHASE 475",
            "Mode: composition sandbox overview.",
            f"Tracked tracks: {len(tracks)}",
            f"Total stems: {stems}",
            "Policy: experimentation only; licensing, attribution, and release decisions stay human-reviewed.",
        ]
    )


def cinematic_storyboard_assistant() -> str:
    boards = _list_entries(MEDIA_DIR / "storyboards.json", "boards")
    scenes = sum(len(item.get("scenes", [])) for item in boards if isinstance(item, dict))
    return "\n".join(
        [
            "CINEMATIC STORYBOARD ASSISTANT - PHASE 476",
            "Mode: storyboard planning overview.",
            f"Storyboard sets: {len(boards)}",
            f"Scene cards: {scenes}",
            "Suggested flow: objective, beat sheet, shot language, visual references, and approval sign-off.",
        ]
    )
