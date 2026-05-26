from pathlib import Path
import json
import re

from tools.project_context_tools import get_current_project_path

SKIP_DIRS = {".git", "vendor", "node_modules", "storage", "bootstrap/cache", "venv", "__pycache__"}


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected.\nUse: use project <path-or-shortcut>"
    return Path(project), None


def _skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def _read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() and path.is_file() else ""


def _composer(project: Path) -> dict:
    file = project / "composer.json"
    if not file.exists():
        return {}
    try:
        return json.loads(file.read_text(errors="replace"))
    except Exception:
        return {}


def _env(project: Path) -> str:
    return _read(project / ".env")


def graphql_readiness_checker() -> str:
    project, error = _project()
    if error:
        return error

    composer = _composer(project)
    deps = {}
    deps.update(composer.get("require", {}))
    deps.update(composer.get("require-dev", {}))

    findings = ["GRAPHQL READINESS CHECKER — PHASE 231"]

    has_graphql = any("graphql" in key.lower() or "lighthouse" in key.lower() for key in deps)
    schema_files = list(project.rglob("*.graphql"))

    findings.append(f"GraphQL package detected: {'YES' if has_graphql else 'NO'}")
    findings.append(f"GraphQL schema files found: {len(schema_files)}")

    if schema_files:
        findings.extend(f"- {f.relative_to(project)}" for f in schema_files[:20])

    findings.append("\nRecommendation:")
    if has_graphql:
        findings.append("- Project appears GraphQL-ready. Next inspect schema authorization and resolver safety.")
    else:
        findings.append("- No GraphQL dependency detected. Laravel Lighthouse is the usual Laravel GraphQL option.")

    return "\n".join(findings)


def webhook_simulator() -> str:
    project, error = _project()
    if error:
        return error

    findings = ["WEBHOOK SIMULATOR — PHASE 232", "Read-only inspection. No webhook request was sent."]

    routes_text = ""
    routes_dir = project / "routes"
    if routes_dir.exists():
        for file in routes_dir.glob("*.php"):
            routes_text += "\n" + _read(file)

    webhook_hits = re.findall(r"Route::(?:post|any)\(['\"]([^'\"]*webhook[^'\"]*)['\"]", routes_text, re.I)

    findings.append(f"\nWebhook routes detected: {len(webhook_hits)}")
    findings.extend(f"- {route}" for route in webhook_hits[:30])

    findings.append("\nSafe simulation template:")
    findings.append("curl -X POST <webhook-url> -H 'Content-Type: application/json' -d '{\"event\":\"test\"}'")
    findings.append("\nSafety: JARVIS should not execute webhook calls until a confirm-based action exists.")

    return "\n".join(findings)


def queue_worker_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    env = _env(project)
    config_queue = _read(project / "config" / "queue.php")

    findings = ["QUEUE WORKER ANALYZER — PHASE 233"]
    match = re.search(r"^QUEUE_CONNECTION=(.*)$", env, re.M)

    findings.append(f"QUEUE_CONNECTION: {match.group(1) if match else 'not found'}")
    findings.append(f"config/queue.php exists: {'YES' if config_queue else 'NO'}")

    job_files = list((project / "app" / "Jobs").rglob("*.php")) if (project / "app" / "Jobs").exists() else []
    findings.append(f"Job classes found: {len(job_files)}")
    findings.extend(f"- {f.relative_to(project)}" for f in job_files[:30])

    findings.append("\nRecommendation:")
    findings.append("- For production, use queue:work under Supervisor/systemd. Do not rely on manual terminal workers.")

    return "\n".join(findings)


def horizon_integration_assistant() -> str:
    project, error = _project()
    if error:
        return error

    composer = _composer(project)
    deps = {}
    deps.update(composer.get("require", {}))
    deps.update(composer.get("require-dev", {}))

    findings = ["HORIZON INTEGRATION ASSISTANT — PHASE 234"]

    has_horizon = "laravel/horizon" in deps
    findings.append(f"laravel/horizon installed: {'YES' if has_horizon else 'NO'}")
    findings.append(f"config/horizon.php exists: {'YES' if (project / 'config' / 'horizon.php').exists() else 'NO'}")

    findings.append("\nRecommendation:")
    if has_horizon:
        findings.append("- Horizon is present. Check Redis, supervisor process, and access authorization.")
    else:
        findings.append("- Horizon not installed. Only install it if Redis queues are planned.")

    return "\n".join(findings)


def redis_integration_checker() -> str:
    project, error = _project()
    if error:
        return error

    env = _env(project)
    composer = _composer(project)

    findings = ["REDIS INTEGRATION CHECKER — PHASE 235"]

    deps = {}
    deps.update(composer.get("require", {}))
    deps.update(composer.get("require-dev", {}))

    findings.append(f"predis/predis installed: {'YES' if 'predis/predis' in deps else 'NO'}")
    findings.append(f"phpredis mentioned: {'YES' if 'redis' in str(deps).lower() else 'UNKNOWN'}")

    for key in ["REDIS_HOST", "REDIS_PASSWORD", "REDIS_PORT", "CACHE_STORE", "QUEUE_CONNECTION", "SESSION_DRIVER"]:
        match = re.search(rf"^{key}=(.*)$", env, re.M)
        findings.append(f"{key}: {match.group(1) if match else 'not found'}")

    return "\n".join(findings)


def cache_strategy_advisor() -> str:
    project, error = _project()
    if error:
        return error

    env = _env(project)
    findings = ["CACHE STRATEGY ADVISOR — PHASE 236"]

    for key in ["CACHE_STORE", "CACHE_DRIVER", "QUEUE_CONNECTION", "SESSION_DRIVER"]:
        match = re.search(rf"^{key}=(.*)$", env, re.M)
        findings.append(f"{key}: {match.group(1) if match else 'not found'}")

    findings.append("\nAdvice:")
    findings.append("- Local/small app: file cache is acceptable.")
    findings.append("- SaaS/multi-tenant app: Redis is better for cache, queues, sessions, and rate limiting.")
    findings.append("- Never cache tenant-sensitive data without tenant-specific cache keys.")

    return "\n".join(findings)


def session_handling_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    env = _env(project)
    config = _read(project / "config" / "session.php")

    findings = ["SESSION HANDLING ANALYZER — PHASE 237"]

    for key in ["SESSION_DRIVER", "SESSION_LIFETIME", "SESSION_ENCRYPT", "SESSION_DOMAIN", "APP_URL"]:
        match = re.search(rf"^{key}=(.*)$", env, re.M)
        findings.append(f"{key}: {match.group(1) if match else 'not found'}")

    findings.append(f"config/session.php exists: {'YES' if config else 'NO'}")

    findings.append("\nRisk note:")
    findings.append("- For multi-tenant apps, session domain and tenant switching must be handled carefully.")

    return "\n".join(findings)


def authentication_flow_inspector() -> str:
    project, error = _project()
    if error:
        return error

    findings = ["AUTHENTICATION FLOW INSPECTOR — PHASE 238"]

    markers = {
        "Laravel Breeze": ["laravel/breeze", "resources/views/auth"],
        "Laravel Jetstream": ["laravel/jetstream"],
        "Fortify": ["laravel/fortify"],
        "Sanctum": ["laravel/sanctum"],
    }

    composer_text = json.dumps(_composer(project)).lower()

    for name, checks in markers.items():
        detected = any(check.lower() in composer_text or (project / check).exists() for check in checks)
        findings.append(f"{name}: {'YES' if detected else 'NO'}")

    auth_views = list((project / "resources" / "views" / "auth").rglob("*.php")) if (project / "resources" / "views" / "auth").exists() else []
    findings.append(f"Auth views found: {len(auth_views)}")

    return "\n".join(findings)


def rbac_permission_auditor() -> str:
    project, error = _project()
    if error:
        return error

    composer = _composer(project)
    composer_text = json.dumps(composer).lower()

    findings = ["RBAC PERMISSION AUDITOR — PHASE 239"]

    findings.append(f"Spatie permission package: {'YES' if 'spatie/laravel-permission' in composer_text else 'NO'}")

    role_refs = []
    permission_refs = []

    for file in project.rglob("*.php"):
        if _skip(file):
            continue
        text = _read(file)
        if "hasRole" in text or "assignRole" in text or "can(" in text or "permission" in text.lower():
            role_refs.append(file.relative_to(project))

    findings.append(f"RBAC-related files detected: {len(role_refs)}")
    findings.extend(f"- {f}" for f in role_refs[:40])

    findings.append("\nAudit advice:")
    findings.append("- Check super-admin bypass carefully.")
    findings.append("- Check role assignment screens for privilege escalation.")
    findings.append("- Tenant-scoped roles must never leak across companies.")

    return "\n".join(findings)


def multi_tenant_isolation_checker() -> str:
    project, error = _project()
    if error:
        return error

    findings = ["MULTI-TENANT ISOLATION CHECKER — PHASE 240"]

    tenant_terms = ["company_id", "tenant_id", "team_id", "organization_id", "account_id"]
    model_files = list((project / "app" / "Models").rglob("*.php")) if (project / "app" / "Models").exists() else []

    scoped = []
    unscoped = []

    for file in model_files:
        text = _read(file)
        if any(term in text for term in tenant_terms):
            scoped.append(file.relative_to(project))
        else:
            unscoped.append(file.relative_to(project))

    findings.append(f"Models with tenant-like fields: {len(scoped)}")
    findings.extend(f"- {f}" for f in scoped[:40])

    findings.append(f"\nModels without obvious tenant field: {len(unscoped)}")
    findings.extend(f"- {f}" for f in unscoped[:40])

    findings.append("\nCritical warning:")
    findings.append("- This is a static signal only. Real isolation requires checking queries, policies, middleware, and global scopes.")

    return "\n".join(findings)
