from __future__ import annotations

import json
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from core.brain import ask_brain
from core.memory import save_memory
from core.vector_memory.vector_store import add_vector_memory
from tools import programming_knowledge_tools as pkt


STORAGE_DIR = Path("storage")
STATE_FILE = STORAGE_DIR / "autonomous_learning_state.json"
LOG_FILE = STORAGE_DIR / "autonomous_learning_log.jsonl"
MANIFEST_DIR = STORAGE_DIR / "autonomous_learning_manifests"
MEDICAL_CATALOG_FILE = Path("data/medical_learning_catalog.json")

DEFAULT_CYCLE_INTERVAL_SECONDS = 180
DISCOVERY_BATCH_SIZE = 2

DOMAIN_PROFILES = {
    "programming": {
        "proficiency_target": "senior-software-engineer",
        "mindset": (
            "Learn with the judgment of a senior software engineer: systems thinking, tradeoffs, "
            "debugging depth, architecture quality, testing discipline, performance awareness, "
            "security posture, maintainability, and production readiness."
        ),
    },
    "medicine": {
        "proficiency_target": "doctor-level-reference",
        "mindset": (
            "Learn with the structure of a doctor-level knowledge base: anatomy, physiology, "
            "diagnostic reasoning, pharmacology, emergency red flags, public health, evidence quality, "
            "and safe clinical escalation. This is educational knowledge, not a replacement for a licensed physician."
        ),
    },
}

DOMAIN_ROADMAPS = {
    "programming": [
        {
            "name": "Foundations",
            "topics": [
                "How Computers Actually Work",
                "Logic and Problem Solving",
                "algorithms and data structures",
                "command line and terminal operations",
                "Git and GitHub workflows",
            ],
        },
        {
            "name": "Core Engineering",
            "topics": [
                "software architecture fundamentals",
                "testing methodologies",
                "clean code principles",
                "database concepts and normalization",
                "operating system fundamentals",
            ],
        },
        {
            "name": "Production Systems",
            "topics": [
                "system design and scalability",
                "web security fundamentals",
                "Docker and containerization",
                "CI/CD pipelines",
                "monitoring and observability",
            ],
        },
        {
            "name": "Advanced Systems",
            "topics": [
                "distributed systems fundamentals",
                "cloud architecture patterns",
                "authentication and authorization systems",
                "AI agent architectures",
                "technical leadership",
            ],
        },
    ],
    "medicine": [
        {
            "name": "Medical Foundations",
            "topics": [
                "Human Anatomy and Physiology",
                "Medical Terminology and Communication",
                "Evidence-Based Medicine Fundamentals",
                "Clinical History and Physical Examination",
            ],
        },
        {
            "name": "Core Clinical Reasoning",
            "topics": [
                "Diagnostics and Laboratory Interpretation",
                "Pharmacology Principles",
                "Infectious Disease and Immunology",
                "Emergency Triage and Red Flags",
            ],
        },
        {
            "name": "System Medicine",
            "topics": [
                "Cardiovascular Medicine Fundamentals",
                "Respiratory Medicine Fundamentals",
                "Endocrinology and Metabolism Fundamentals",
                "Neurology Fundamentals",
            ],
        },
        {
            "name": "Population and Professional Practice",
            "topics": [
                "Preventive Medicine and Public Health",
                "Medical Ethics and Patient Safety",
                "Chronic Disease Management",
                "Clinical Decision Support and Guidelines",
            ],
        },
    ],
}

_WORKER_LOCK = threading.Lock()
_WORKER_THREAD: threading.Thread | None = None


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_dirs() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, data: Any) -> None:
    _ensure_dirs()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _append_jsonl(path: Path, entry: dict) -> None:
    _ensure_dirs()
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _normalize(text: str) -> str:
    return " ".join((text or "").lower().strip().split())


def _slugify(text: str) -> str:
    return pkt._slugify(text)


def _default_state() -> dict:
    return {
        "enabled": True,
        "started_at": _now_iso(),
        "last_cycle_at": None,
        "cycle_interval_seconds": DEFAULT_CYCLE_INTERVAL_SECONDS,
        "active_domains": ["programming", "medicine"],
        "schedule": [],
        "current_task_id": None,
        "completed_topics": {"programming": [], "medicine": []},
        "domain_stage_index": {"programming": 0, "medicine": 0},
        "stats": {
            "tasks_completed": 0,
            "topics_learned": 0,
            "reviews_completed": 0,
            "syntheses_completed": 0,
            "errors": 0,
        },
    }


def _load_state() -> dict:
    state = _read_json(STATE_FILE, _default_state())
    merged = _default_state()
    merged.update(state)
    merged["completed_topics"] = {
        "programming": list(state.get("completed_topics", {}).get("programming", [])),
        "medicine": list(state.get("completed_topics", {}).get("medicine", [])),
    }
    merged["domain_stage_index"] = {
        "programming": int(state.get("domain_stage_index", {}).get("programming", 0)),
        "medicine": int(state.get("domain_stage_index", {}).get("medicine", 0)),
    }
    merged["stats"].update(state.get("stats", {}))
    return merged


def _save_state(state: dict) -> None:
    _write_json(STATE_FILE, state)


def _medical_catalog() -> dict:
    return _read_json(MEDICAL_CATALOG_FILE, {"topics": []})


def _catalog_topics_for_domain(domain: str) -> list[dict]:
    if domain == "programming":
        return list(pkt._load_catalog().get("topics", []))
    if domain == "medicine":
        return list(_medical_catalog().get("topics", []))
    return []


def _resolve_topic_config(domain: str, topic_name: str) -> dict | None:
    normalized = _normalize(topic_name)
    for topic in _catalog_topics_for_domain(domain):
        names = [topic.get("topic", ""), *topic.get("aliases", [])]
        if normalized in {_normalize(name) for name in names if name}:
            resolved = dict(topic)
            resolved["domain"] = domain
            resolved.setdefault("proficiency_target", DOMAIN_PROFILES[domain]["proficiency_target"])
            resolved.setdefault("tags", [])
            return resolved
    return None


def _all_topic_names(domain: str) -> list[str]:
    names = []
    for item in _catalog_topics_for_domain(domain):
        topic = item.get("topic")
        if topic:
            names.append(topic)
    return names


def _known_topic_names(domain: str) -> set[str]:
    return {_normalize(name) for name in _all_topic_names(domain)}


def _schedule_topics(state: dict, domain: str) -> set[str]:
    topics = set()
    for item in state.get("schedule", []):
        if item.get("domain") == domain and item.get("topic"):
            topics.add(_normalize(item["topic"]))
    return topics


def _create_task(domain: str, topic: str, kind: str, stage: str, metadata: dict | None = None) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "domain": domain,
        "topic": topic,
        "kind": kind,
        "stage": stage,
        "status": "pending",
        "created_at": _now_iso(),
        "started_at": None,
        "completed_at": None,
        "metadata": metadata or {},
    }


def _task_signature(domain: str, kind: str, metadata: dict | None = None, topic: str | None = None) -> tuple:
    meta_topics = tuple(_normalize(item) for item in (metadata or {}).get("topics", []))
    return (domain, kind, _normalize(topic or ""), meta_topics)


def _has_task(state: dict, domain: str, kind: str, metadata: dict | None = None, topic: str | None = None) -> bool:
    expected = _task_signature(domain, kind, metadata, topic)
    for task in state.get("schedule", []):
        signature = _task_signature(
            task.get("domain", ""),
            task.get("kind", ""),
            task.get("metadata", {}),
            task.get("topic", ""),
        )
        if signature == expected:
            return True
    return False


def _pending_or_active(state: dict, domain: str) -> list[dict]:
    return [
        task for task in state.get("schedule", [])
        if task.get("domain") == domain and task.get("status") in {"pending", "in_progress"}
    ]


def _recent_completed_topics(state: dict, domain: str, limit: int = 3) -> list[str]:
    return state.get("completed_topics", {}).get(domain, [])[-limit:]


def _append_schedule_block(state: dict, domain: str, stage_name: str, topics: list[str]) -> None:
    for topic in topics:
        state["schedule"].append(_create_task(domain, topic, "learn", stage_name))

    review_topics = _recent_completed_topics(state, domain, limit=3)
    if len(review_topics) >= 2 and not _has_task(
        state,
        domain,
        "review",
        metadata={"topics": review_topics},
        topic=" / ".join(review_topics),
    ):
        state["schedule"].append(
            _create_task(
                domain,
                " / ".join(review_topics),
                "review",
                f"{stage_name} Review",
                {"topics": review_topics},
            )
        )


def _advance_domain_schedule(state: dict, domain: str) -> bool:
    roadmap = DOMAIN_ROADMAPS.get(domain, [])
    completed = {_normalize(item) for item in state["completed_topics"].get(domain, [])}
    scheduled = _schedule_topics(state, domain)
    stage_index = int(state["domain_stage_index"].get(domain, 0))

    while stage_index < len(roadmap):
        stage = roadmap[stage_index]
        available = []
        for topic in stage.get("topics", []):
            normalized = _normalize(topic)
            if normalized in completed or normalized in scheduled:
                continue
            if normalized in _known_topic_names(domain):
                available.append(topic)

        if available:
            _append_schedule_block(state, domain, stage["name"], available[:DISCOVERY_BATCH_SIZE])
            state["domain_stage_index"][domain] = stage_index
            return True

        stage_index += 1
        state["domain_stage_index"][domain] = stage_index

    return _expand_beyond_roadmap(state, domain)


def _expand_beyond_roadmap(state: dict, domain: str) -> bool:
    completed = {_normalize(item) for item in state["completed_topics"].get(domain, [])}
    scheduled = _schedule_topics(state, domain)
    discovered = []

    for topic_name in _all_topic_names(domain):
        normalized = _normalize(topic_name)
        if normalized in completed or normalized in scheduled:
            continue
        discovered.append(topic_name)

    if not discovered:
        recent = _recent_completed_topics(state, domain, limit=4)
        if recent and not _has_task(
            state,
            domain,
            "synthesis",
            metadata={"topics": recent},
            topic=" / ".join(recent),
        ):
            state["schedule"].append(
                _create_task(
                    domain,
                    " / ".join(recent),
                    "synthesis",
                    "Mastery Synthesis",
                    {"topics": recent},
                )
            )
            return True
        return False

    state["schedule"].extend(
        _create_task(domain, topic, "learn", "Autonomous Expansion")
        for topic in discovered[:DISCOVERY_BATCH_SIZE]
    )
    return True


def _ensure_schedule(state: dict) -> bool:
    added = False
    for domain in state.get("active_domains", []):
        if _pending_or_active(state, domain):
            continue
        added = _advance_domain_schedule(state, domain) or added
    return added


def _manifest_path(domain: str, topic: str) -> Path:
    return MANIFEST_DIR / f"{domain}_{_slugify(topic)}.json"


def _generic_learn_topic(topic_config: dict, trigger: str = "autonomous-background") -> dict:
    topic_name = topic_config.get("topic", "unknown")
    domain = topic_config.get("domain", "general")
    proficiency_target = topic_config.get(
        "proficiency_target",
        DOMAIN_PROFILES.get(domain, {}).get("proficiency_target", "advanced-practitioner"),
    )
    manifest_path = _manifest_path(domain, topic_name)
    manifest = _read_json(
        manifest_path,
        {"updated_at": None, "topic": topic_name, "domain": domain, "sources": {}},
    )
    manifest_sources = manifest.setdefault("sources", {})
    total_chunks = 0
    updated_sources = 0
    skipped_sources = 0
    errors: list[str] = []
    started_at = _now_iso()

    for source in topic_config.get("sources", []):
        url = source.get("url")
        name = source.get("name", "Unnamed source")
        source_type = source.get("type", "reference")
        priority = int(source.get("priority", 5))
        if not url:
            continue

        try:
            html = pkt._fetch_url(url)
            extracted = pkt._extract_page_text(html or "", f"{topic_name} Source")
            digest = pkt._content_hash(extracted["text"])
            previous = manifest_sources.get(url, {}).get("hash")
            if previous == digest:
                skipped_sources += 1
                continue

            chunks = pkt._chunk_text(extracted["text"])
            for index, chunk in enumerate(chunks):
                memory_text = (
                    f"{topic_name.upper()} LEARNING SOURCE\n"
                    f"Domain: {domain}\n"
                    f"Learning target: {proficiency_target}\n"
                    f"Source name: {name}\n"
                    f"Source type: {source_type}\n"
                    f"URL: {url}\n"
                    f"Page title: {extracted['title']}\n"
                    f"Headings: {extracted['headings']}\n"
                    f"Chunk: {index + 1}/{len(chunks)}\n\n"
                    f"{chunk}"
                )
                add_vector_memory(
                    memory_text,
                    tags=list(dict.fromkeys([
                        domain,
                        _slugify(topic_name),
                        *topic_config.get("tags", []),
                        source_type,
                        proficiency_target,
                    ])),
                    source=f"{domain}-autonomous-learning",
                    importance=priority,
                )
                total_chunks += 1

            manifest_sources[url] = {
                "name": name,
                "type": source_type,
                "priority": priority,
                "hash": digest,
                "last_learned_at": _now_iso(),
                "chunks_saved": len(chunks),
                "title": extracted["title"],
            }
            updated_sources += 1
            time.sleep(1)
        except Exception as exc:
            errors.append(f"{name}: {exc}")

    manifest["updated_at"] = _now_iso()
    manifest["topic"] = topic_name
    manifest["domain"] = domain
    manifest["proficiency_target"] = proficiency_target
    manifest["sources"] = manifest_sources
    _write_json(manifest_path, manifest)

    result = {
        "domain": domain,
        "topic": topic_name,
        "trigger": trigger,
        "started_at": started_at,
        "completed_at": _now_iso(),
        "sources_updated": updated_sources,
        "sources_skipped": skipped_sources,
        "memory_chunks_saved": total_chunks,
        "errors": errors,
        "manifest_path": str(manifest_path),
    }
    _append_jsonl(LOG_FILE, {"type": "generic_topic_learning", **result})
    return result


def _learn_domain_topic(domain: str, topic: str) -> dict:
    config = _resolve_topic_config(domain, topic)
    if not config:
        raise RuntimeError(f"No learning configuration found for {domain}:{topic}")
    return _generic_learn_topic(config)


def _synthesize_learning_note(domain: str, topics: list[str], mode: str) -> str:
    profile = DOMAIN_PROFILES.get(domain, DOMAIN_PROFILES["programming"])
    prompt = f"""
Create a concise learning synthesis for Janon's autonomous study engine.

Domain: {domain}
Mode: {mode}
Topics:
- """ + "\n- ".join(topics) + f"""

Mastery target:
{profile['proficiency_target']}

Learning mindset:
{profile['mindset']}

Return:
1. What matters most
2. Common mistakes
3. What an expert notices
4. What to study next

Keep it practical and compact.
"""
    return ask_brain(prompt, route_hint="fast", max_tokens=300)


def _run_reflection_task(task: dict) -> dict:
    domain = task["domain"]
    topics = task.get("metadata", {}).get("topics", [])
    note = _synthesize_learning_note(domain, topics, task["kind"])
    title = f"{domain.upper()} {task['kind'].upper()} NOTE"
    memory_text = f"{title}\nTopics: {', '.join(topics)}\n\n{note}"
    add_vector_memory(
        memory_text,
        tags=[domain, task["kind"], "autonomous-learning", DOMAIN_PROFILES[domain]["proficiency_target"]],
        source="autonomous-learning-reflection",
        importance=8,
    )
    save_memory(f"autonomous learning {task['kind']} {domain}", note)
    _append_jsonl(LOG_FILE, {
        "type": f"{task['kind']}_task",
        "domain": domain,
        "topics": topics,
        "completed_at": _now_iso(),
    })
    return {"summary": note, "topics": topics}


def _run_task(task: dict) -> dict:
    if task["kind"] == "learn":
        return _learn_domain_topic(task["domain"], task["topic"])
    if task["kind"] in {"review", "synthesis"}:
        return _run_reflection_task(task)
    raise RuntimeError(f"Unknown learning task kind: {task['kind']}")


def autonomous_learning_status() -> str:
    state = _load_state()
    if _ensure_schedule(state):
        _save_state(state)
    lines = [
        "AUTONOMOUS LEARNING STATUS",
        f"Enabled: {'YES' if state.get('enabled') else 'NO'}",
        f"Started at: {state.get('started_at') or '-'}",
        f"Last cycle: {state.get('last_cycle_at') or '-'}",
        f"Cycle interval seconds: {state.get('cycle_interval_seconds')}",
        f"Current task id: {state.get('current_task_id') or '-'}",
        "",
        "Domain progress:",
    ]
    for domain in state.get("active_domains", []):
        completed = state.get("completed_topics", {}).get(domain, [])
        pending = len([task for task in state.get("schedule", []) if task.get("domain") == domain and task.get("status") == "pending"])
        lines.append(
            f"- {domain}: completed topics {len(completed)}, pending tasks {pending}, stage index {state.get('domain_stage_index', {}).get(domain, 0)}"
        )

    lines.extend([
        "",
        "Next tasks:",
    ])
    visible_tasks = [
        task for task in state.get("schedule", [])
        if task.get("status") in {"pending", "in_progress", "failed"}
    ][:8]
    for task in visible_tasks:
        lines.append(
            f"- [{task.get('status')}] {task.get('domain')} | {task.get('kind')} | {task.get('topic')} | {task.get('stage')}"
        )
    return "\n".join(lines)


def enable_autonomous_learning() -> str:
    state = _load_state()
    state["enabled"] = True
    _ensure_schedule(state)
    _save_state(state)
    ensure_autonomous_learning_worker()
    return autonomous_learning_status()


def disable_autonomous_learning() -> str:
    state = _load_state()
    state["enabled"] = False
    _save_state(state)
    return autonomous_learning_status()


def run_autonomous_learning_cycle() -> dict | None:
    with _WORKER_LOCK:
        state = _load_state()
        if not state.get("enabled", True):
            return None

        _ensure_schedule(state)
        task = next((item for item in state.get("schedule", []) if item.get("status") == "pending"), None)
        if task is None:
            _save_state(state)
            return None

        task["status"] = "in_progress"
        task["started_at"] = _now_iso()
        state["current_task_id"] = task["id"]
        state["last_cycle_at"] = _now_iso()
        _save_state(state)

    try:
        result = _run_task(task)
        success = True
        error_text = None
    except Exception as exc:
        result = {"errors": [str(exc)]}
        success = False
        error_text = str(exc)

    with _WORKER_LOCK:
        state = _load_state()
        for item in state.get("schedule", []):
            if item.get("id") != task["id"]:
                continue
            item["status"] = "completed" if success else "failed"
            item["completed_at"] = _now_iso()
            item["result"] = result
            break

        if success and task["kind"] == "learn":
            completed = state["completed_topics"].setdefault(task["domain"], [])
            if _normalize(task["topic"]) not in {_normalize(entry) for entry in completed}:
                completed.append(task["topic"])
                state["stats"]["topics_learned"] += 1

            # Schedule a compact synthesis after each successful topic.
            if not _has_task(
                state,
                task["domain"],
                "synthesis",
                metadata={"topics": [task["topic"]]},
                topic=task["topic"],
            ):
                state["schedule"].append(
                    _create_task(
                        task["domain"],
                        task["topic"],
                        "synthesis",
                        f"{task['stage']} Synthesis",
                        {"topics": [task["topic"]]},
                    )
                )

        if success and task["kind"] == "review":
            state["stats"]["reviews_completed"] += 1

        if success and task["kind"] == "synthesis":
            state["stats"]["syntheses_completed"] += 1

        if success:
            state["stats"]["tasks_completed"] += 1
        else:
            state["stats"]["errors"] += 1
            _append_jsonl(LOG_FILE, {
                "type": "learning_task_error",
                "task": task,
                "error": error_text,
                "completed_at": _now_iso(),
            })

        state["current_task_id"] = None
        _ensure_schedule(state)
        _save_state(state)

    return result


def _worker_loop() -> None:
    while True:
        try:
            run_autonomous_learning_cycle()
        except Exception as exc:
            _append_jsonl(LOG_FILE, {
                "type": "worker_loop_error",
                "error": str(exc),
                "time": _now_iso(),
            })

        state = _load_state()
        delay = int(state.get("cycle_interval_seconds", DEFAULT_CYCLE_INTERVAL_SECONDS))
        time.sleep(max(30, delay))


def ensure_autonomous_learning_worker() -> None:
    global _WORKER_THREAD

    with _WORKER_LOCK:
        state = _load_state()
        _ensure_schedule(state)
        _save_state(state)

        if _WORKER_THREAD and _WORKER_THREAD.is_alive():
            return

        _WORKER_THREAD = threading.Thread(
            target=_worker_loop,
            name="jarvis-autonomous-learning",
            daemon=True,
        )
        _WORKER_THREAD.start()
