from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from tools.notification_config import load_notification_settings


STORAGE_DIR = Path("storage")
MEMORY_DB = STORAGE_DIR / "memory.db"
VECTOR_META = STORAGE_DIR / "vector_memory" / "vector_memory.json"
SYNC_QUEUE = STORAGE_DIR / "sync" / "queue.json"
LOCAL_SECRETS = STORAGE_DIR / "local_secrets.json"


def _safe_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _memory_row_count() -> int:
    if not MEMORY_DB.exists():
        return 0
    try:
        conn = sqlite3.connect(str(MEMORY_DB))
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memory")
            row = cursor.fetchone()
            return int(row[0]) if row else 0
        finally:
            conn.close()
    except sqlite3.Error:
        return 0


def _vector_memory_count() -> int:
    data = _safe_json(VECTOR_META, [])
    return len([item for item in data if item.get("active", True)])


def _bool_label(value: bool) -> str:
    return "YES" if value else "NO"


def _provider_status(names: Iterable[str]) -> str:
    return ", ".join(
        f"{name}={'set' if os.getenv(name, '').strip() else 'missing'}" for name in names
    )


@dataclass(frozen=True)
class TrustProviderStatus:
    configured: bool
    backend: str
    details: str


def encrypted_memory_storage() -> str:
    memory_key = os.getenv("JARVIS_MEMORY_KEY", "").strip()
    memory_rows = _memory_row_count()
    vector_rows = _vector_memory_count()
    lines = [
        "ENCRYPTED MEMORY STORAGE - PHASE 421",
        "Mode: read-only encryption readiness review.",
        f"SQLite conversation rows: {memory_rows}",
        f"Vector memory rows: {vector_rows}",
        f"Encryption key configured: {_bool_label(bool(memory_key))}",
    ]
    if memory_key:
        lines.append("Status: key material exists for an encrypted memory wrapper or export pipeline.")
    else:
        lines.append("Status: current local memory stores appear unwrapped at rest.")
        lines.append("Attention: configure JARVIS_MEMORY_KEY before introducing encrypted memory writes.")
    lines.append("Recommended controls: envelope encryption for SQLite exports, encrypted vector snapshots, and key rotation metadata.")
    return "\n".join(lines)


def _detect_vault_provider() -> TrustProviderStatus:
    if os.getenv("VAULT_ADDR", "").strip():
        return TrustProviderStatus(
            configured=True,
            backend="hashicorp_vault",
            details=_provider_status(["VAULT_ADDR", "VAULT_TOKEN"]),
        )
    if os.getenv("AWS_SECRETS_MANAGER_REGION", "").strip():
        return TrustProviderStatus(
            configured=True,
            backend="aws_secrets_manager",
            details=_provider_status(["AWS_SECRETS_MANAGER_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]),
        )
    if os.getenv("DOPPLER_TOKEN", "").strip():
        return TrustProviderStatus(
            configured=True,
            backend="doppler",
            details=_provider_status(["DOPPLER_TOKEN"]),
        )
    return TrustProviderStatus(configured=False, backend="none", details="No supported vault provider variables detected.")


def secure_vault_integration() -> str:
    status = _detect_vault_provider()
    lines = [
        "SECURE VAULT INTEGRATION - PHASE 422",
        "Mode: read-only provider discovery.",
        f"Backend: {status.backend}",
        f"Configured: {_bool_label(status.configured)}",
        f"Provider details: {status.details}",
    ]
    if status.configured:
        lines.append("Guidance: use the vault for runtime secret retrieval, not source-controlled defaults.")
    else:
        lines.append("Guidance: configure Vault, AWS Secrets Manager, or Doppler before moving sensitive runtime material out of .env.")
    return "\n".join(lines)


def local_secrets_manager() -> str:
    data = _safe_json(LOCAL_SECRETS, {"items": []})
    items = data.get("items", []) if isinstance(data, dict) else []
    names: List[str] = []
    for item in items[:5]:
        key = str(item.get("name", "unnamed")).strip()[:40]
        names.append(key or "unnamed")
    lines = [
        "LOCAL SECRETS MANAGER - PHASE 423",
        "Mode: metadata-only local secret inventory.",
        f"Tracked secret entries: {len(items)}",
    ]
    if names:
        lines.append("Tracked keys: " + ", ".join(names))
    else:
        lines.append("Tracked keys: none")
    lines.append("Safety: values stay redacted; only names and counts are surfaced.")
    return "\n".join(lines)


def zero_trust_agent_architecture() -> str:
    return "\n".join(
        [
            "ZERO-TRUST AGENT ARCHITECTURE - PHASE 424",
            "Principles:",
            "- Every agent starts with read-only assumptions.",
            "- Tool access is granted per task, not per persona.",
            "- High-risk actions require explicit approval and trace logging.",
            "- Secrets are retrieved just in time from a vault boundary.",
            "- Cross-agent delegation preserves the original risk label and owner.",
            "Recommended next step: bind role delegation, trust scoring, and approval routes into a shared policy object.",
        ]
    )


def offline_first_operation_mode() -> str:
    offline_flags = {
        "HF_HUB_OFFLINE": os.getenv("HF_HUB_OFFLINE", "").strip(),
        "TRANSFORMERS_OFFLINE": os.getenv("TRANSFORMERS_OFFLINE", "").strip(),
        "EMAIL_DRY_RUN": os.getenv("EMAIL_DRY_RUN", "").strip(),
    }
    enabled = [name for name, value in offline_flags.items() if value.lower() in {"1", "true", "yes", "on"}]
    lines = [
        "OFFLINE-FIRST OPERATION MODE - PHASE 425",
        "Mode: runtime flag inspection.",
        f"Offline-oriented flags enabled: {', '.join(enabled) if enabled else 'none detected'}",
        "Policy: core command routing, memory, and advisory diagnostics should continue without live network dependencies.",
    ]
    if "HF_HUB_OFFLINE" not in enabled or "TRANSFORMERS_OFFLINE" not in enabled:
        lines.append("Recommendation: set model offline flags during CI and local smoke tests for deterministic behavior.")
    return "\n".join(lines)


def sync_engine_between_devices() -> str:
    queue = _safe_json(SYNC_QUEUE, {"pending": []})
    pending = queue.get("pending", []) if isinstance(queue, dict) else []
    lines = [
        "SYNC ENGINE BETWEEN DEVICES - PHASE 426",
        "Mode: read-only queue readiness review.",
        f"Pending sync items: {len(pending)}",
        f"Queue file present: {_bool_label(SYNC_QUEUE.exists())}",
    ]
    if pending:
        preview = [str(item.get("type", "unknown")) for item in pending[:5] if isinstance(item, dict)]
        lines.append("Pending item types: " + ", ".join(preview))
    else:
        lines.append("Pending item types: none")
    lines.append("Recommended sync contract: append-only event queue, per-device checkpoints, conflict resolution before writes.")
    return "\n".join(lines)


def mobile_companion_app() -> str:
    return "\n".join(
        [
            "MOBILE COMPANION APP - PHASE 427",
            "Planned screens:",
            "- assistant chat",
            "- approvals inbox",
            "- system health",
            "- current project context",
            "- alert center",
            "Safety: read-only by default; write and deploy actions stay behind approval routes.",
        ]
    )


def push_notification_system() -> str:
    settings = load_notification_settings()
    push_provider = "none"
    if os.getenv("PUSHOVER_USER_KEY", "").strip():
        push_provider = "pushover"
    elif os.getenv("FCM_SERVER_KEY", "").strip():
        push_provider = "firebase"
    elif os.getenv("NTFY_TOPIC", "").strip():
        push_provider = "ntfy"
    lines = [
        "PUSH NOTIFICATION SYSTEM - PHASE 428",
        "Mode: attention routing review.",
        f"Email attention recipient: {settings['attention_email']}",
        f"Email attention enabled: {_bool_label(bool(settings['email_attention_events']))}",
        f"Push provider: {push_provider}",
    ]
    if push_provider == "none":
        lines.append("Recommendation: keep email as the baseline and add a push provider for urgent owner-facing events.")
    else:
        lines.append("Guidance: route only attention-level events to push to avoid alert fatigue.")
    return "\n".join(lines)


def wearable_device_integration() -> str:
    provider = "apple_watch" if os.getenv("APPLE_WATCH_WEBHOOK", "").strip() else "generic"
    return "\n".join(
        [
            "WEARABLE DEVICE INTEGRATION - PHASE 429",
            "Mode: design and configuration preview.",
            f"Preferred provider: {provider}",
            "Recommended payloads: approvals, outage alerts, deployment status, and personal reminders.",
            "Safety: wearable actions should confirm on a trusted primary device before executing sensitive commands.",
        ]
    )


def smart_home_integration_layer() -> str:
    provider = "home_assistant" if os.getenv("HOME_ASSISTANT_URL", "").strip() else "none"
    details = _provider_status(["HOME_ASSISTANT_URL", "HOME_ASSISTANT_TOKEN"])
    return "\n".join(
        [
            "SMART HOME INTEGRATION LAYER - PHASE 430",
            "Mode: read-only provider discovery.",
            f"Provider: {provider}",
            f"Configuration: {details}",
            "Recommended scope: presence, lighting scenes, voice announcements, and non-destructive status automations first.",
        ]
    )
