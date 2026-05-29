from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path


LIFE_OS_DIR = Path("storage/life_os")
HABITS_FILE = LIFE_OS_DIR / "habits.json"
GOALS_FILE = LIFE_OS_DIR / "goals.json"
SLEEP_FILE = LIFE_OS_DIR / "sleep_log.json"
FITNESS_FILE = LIFE_OS_DIR / "fitness.json"
NUTRITION_FILE = LIFE_OS_DIR / "nutrition.json"
WELLNESS_FILE = LIFE_OS_DIR / "wellness_signals.json"


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _list_items(path: Path, key: str):
    payload = _safe_json(path, {key: []})
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return payload[key]
    if isinstance(payload, list):
        return payload
    return []


def personal_life_operating_system() -> str:
    habits = _list_items(HABITS_FILE, "habits")
    goals = _list_items(GOALS_FILE, "goals")
    sleep_entries = _list_items(SLEEP_FILE, "entries")
    return "\n".join(
        [
            "PERSONAL LIFE OPERATING SYSTEM - PHASE 443",
            "Mode: personal operating-system snapshot.",
            f"Habit entries: {len(habits)}",
            f"Goal entries: {len(goals)}",
            f"Sleep log entries: {len(sleep_entries)}",
            "Operating loop: capture signals -> prioritize goals -> schedule habits -> reflect on energy and stress.",
        ]
    )


def habit_tracking_engine() -> str:
    habits = _list_items(HABITS_FILE, "habits")
    active = [item for item in habits if isinstance(item, dict) and item.get("active", True)]
    completed_today = [
        item
        for item in active
        if isinstance(item, dict) and date.today().isoformat() in item.get("completed_dates", [])
    ]
    return "\n".join(
        [
            "HABIT TRACKING ENGINE - PHASE 444",
            "Mode: local habit dashboard.",
            f"Active habits: {len(active)}",
            f"Completed today: {len(completed_today)}",
            "Recommendation: keep habit signals tiny, daily, and visible to the broader planning loop.",
        ]
    )


def goal_execution_planner() -> str:
    goals = _list_items(GOALS_FILE, "goals")
    open_goals = [item for item in goals if isinstance(item, dict) and item.get("status", "open") != "done"]
    priorities = [str(item.get("title", "untitled")) for item in open_goals[:3] if isinstance(item, dict)]
    return "\n".join(
        [
            "GOAL EXECUTION PLANNER - PHASE 445",
            "Mode: local goal-planning dashboard.",
            f"Open goals: {len(open_goals)}",
            f"Top goals: {', '.join(priorities) if priorities else 'none'}",
            "Execution pattern: choose one lead goal, one support goal, and one maintenance goal per day.",
        ]
    )


def daily_optimization_engine() -> str:
    sleep_entries = _list_items(SLEEP_FILE, "entries")
    habits = _list_items(HABITS_FILE, "habits")
    goals = _list_items(GOALS_FILE, "goals")
    return "\n".join(
        [
            "DAILY OPTIMIZATION ENGINE - PHASE 446",
            "Mode: daily planning summary.",
            f"Signals available: sleep={len(sleep_entries)}, habits={len(habits)}, goals={len(goals)}",
            "Suggested order: protect energy first, place deep work second, then fit maintenance and recovery blocks.",
        ]
    )


def sleep_work_pattern_analyzer() -> str:
    entries = _list_items(SLEEP_FILE, "entries")
    durations = [float(item.get("sleep_hours", 0)) for item in entries if isinstance(item, dict)]
    avg_sleep = sum(durations) / len(durations) if durations else 0.0
    return "\n".join(
        [
            "SLEEP/WORK PATTERN ANALYZER - PHASE 447",
            "Mode: sleep pattern review.",
            f"Entries analyzed: {len(entries)}",
            f"Average sleep hours: {avg_sleep:.1f}",
            "Suggestion: relate sleep dips to workload spikes before tuning your schedule aggressively.",
        ]
    )


def fitness_assistant_integration() -> str:
    metrics = _safe_json(FITNESS_FILE, {})
    provider = "apple_health" if os.getenv("APPLE_HEALTH_EXPORT", "").strip() else "google_fit" if os.getenv("GOOGLE_FIT_CREDENTIALS", "").strip() else "manual"
    steps = metrics.get("steps_today", "unknown") if isinstance(metrics, dict) else "unknown"
    return "\n".join(
        [
            "FITNESS ASSISTANT INTEGRATION - PHASE 448",
            "Mode: fitness signal overview.",
            f"Provider: {provider}",
            f"Steps today: {steps}",
            "Suggested metrics: steps, workouts, resting heart rate, recovery, and mobility consistency.",
        ]
    )


def nutrition_planning_assistant() -> str:
    metrics = _safe_json(NUTRITION_FILE, {})
    calories = metrics.get("calories_today", "unknown") if isinstance(metrics, dict) else "unknown"
    protein = metrics.get("protein_g", "unknown") if isinstance(metrics, dict) else "unknown"
    return "\n".join(
        [
            "NUTRITION PLANNING ASSISTANT - PHASE 449",
            "Mode: nutrition planning overview.",
            f"Calories today: {calories}",
            f"Protein grams: {protein}",
            "Planning loop: protein target, hydration, meal timing, and grocery simplicity.",
        ]
    )


def stress_detection_assistant() -> str:
    metrics = _safe_json(WELLNESS_FILE, {})
    score = float(metrics.get("stress_score", 0)) if isinstance(metrics, dict) else 0.0
    state = "HIGH" if score >= 7 else "MEDIUM" if score >= 4 else "LOW"
    return "\n".join(
        [
            "STRESS DETECTION ASSISTANT - PHASE 450",
            "Mode: wellness signal review.",
            f"Stress score: {score:.1f}",
            f"Stress level: {state}",
            "Inputs can include sleep debt, workload, heart-rate trends, interruptions, and manual check-ins.",
        ]
    )
