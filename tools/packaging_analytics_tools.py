from pathlib import Path
from datetime import datetime
import json
import platform

from tools.project_context_tools import get_current_project_path

STORAGE_DIR = Path("storage")
ANALYTICS_FILE = STORAGE_DIR / "local_analytics_events.json"
SESSIONS_FILE = STORAGE_DIR / "local_sessions.json"
CRASH_FILE = STORAGE_DIR / "crash_log_plan.json"


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected.\nUse: use project <path>"
    return project, None


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _read_json(path: Path, default):
    _ensure_storage()
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception:
        return default


def _write_json(path: Path, data):
    _ensure_storage()
    path.write_text(json.dumps(data, indent=4))


def _has_file(project: Path, name: str) -> bool:
    return (project / name).exists()


def _detect_desktop_stack(project: Path) -> str:
    package_json = project / "package.json"
    pyproject = project / "pyproject.toml"
    requirements = project / "requirements.txt"

    detected = []

    if package_json.exists():
        try:
            data = json.loads(package_json.read_text(errors="replace"))
            deps = {}
            deps.update(data.get("dependencies", {}))
            deps.update(data.get("devDependencies", {}))
            keys = " ".join(deps.keys()).lower()

            if "electron" in keys:
                detected.append("Electron")
            if "tauri" in keys:
                detected.append("Tauri")
            if "react" in keys:
                detected.append("React")
            if "vite" in keys:
                detected.append("Vite")
        except Exception:
            detected.append("Node project")

    if pyproject.exists() or requirements.exists():
        detected.append("Python")

    return ", ".join(detected) if detected else "Unknown"


def windows_installer_generator() -> str:
    project, error = _project()
    if error:
        return error

    stack = _detect_desktop_stack(project)

    return f"""WINDOWS INSTALLER GENERATOR — PHASE 291

Project: {project}
Detected stack: {stack}

Recommended path:
- If Electron is used: electron-builder with NSIS.
- If Python desktop is used: PyInstaller first, then Inno Setup.
- If this is only FastAPI CLI/backend: do not package yet; create a desktop shell first.

Safe build plan:
1. Add app name, version, icon, and publisher metadata.
2. Generate unsigned installer first.
3. Test install/uninstall on a clean Windows machine.
4. Add code signing only after the installer is stable.

Example Electron package.json block:
"build": {{
  "appId": "com.lkprofessionals.jarvis",
  "productName": "JARVIS",
  "win": {{
    "target": "nsis",
    "icon": "desktop/icon.ico"
  }},
  "nsis": {{
    "oneClick": false,
    "allowToChangeInstallationDirectory": true
  }}
}}

Safety:
No installer was generated. This phase is advisory only."""


def linux_appimage_assistant() -> str:
    project, error = _project()
    if error:
        return error

    stack = _detect_desktop_stack(project)

    return f"""LINUX APPIMAGE ASSISTANT — PHASE 292

Project: {project}
Detected stack: {stack}

Recommended path:
- Electron: use electron-builder AppImage target.
- Python GUI: use linuxdeploy + AppRun wrapper.
- CLI/FastAPI backend only: AppImage is premature unless a launcher UI exists.

Electron package.json example:
"linux": {{
  "target": "AppImage",
  "category": "Utility",
  "icon": "desktop/icon.png"
}}

Expected output:
dist/JARVIS-<version>.AppImage

Safety:
No files were created. This is a packaging readiness advisor."""


def mac_packaging_advisor() -> str:
    project, error = _project()
    if error:
        return error

    return f"""MAC PACKAGING ADVISOR — PHASE 293

Project: {project}

Recommended macOS release path:
1. Build .app locally.
2. Package as .dmg.
3. Test on Intel and Apple Silicon if possible.
4. Apple Developer signing is required for professional distribution.
5. Notarization is strongly recommended for trust and Gatekeeper compatibility.

Electron target:
"mac": {{
  "target": "dmg",
  "category": "public.app-category.productivity"
}}

Reality check:
Unsigned macOS apps will scare users. For private use it is okay. For public LKProfessionals release, sign it properly."""


def auto_update_system_planner() -> str:
    project, error = _project()
    if error:
        return error

    return f"""AUTO-UPDATE SYSTEM PLANNER — PHASE 294

Project: {project}

Recommended strategy:
- Private local JARVIS: manual update using git pull is safest.
- Public desktop app: use signed releases.
- Electron app: electron-updater with GitHub Releases.
- Python app: custom update manifest with checksum validation.

Minimum safe update design:
1. Check latest version from trusted source.
2. Download update package.
3. Verify checksum.
4. Never auto-run downloaded scripts.
5. Ask confirmation before installation.
6. Keep rollback copy.

Suggested local command model:
- check for updates
- show update plan
- confirm update
- rollback update

Safety:
Do not implement silent auto-update yet. That is how a helpful assistant becomes a supply-chain liability."""


def telemetry_framework_advisor() -> str:
    project, error = _project()
    if error:
        return error

    return f"""TELEMETRY FRAMEWORK ADVISOR — PHASE 295

Project: {project}

Recommended privacy-first telemetry:
- Local-only by default.
- No personal data collection.
- No keystroke capture.
- No file content capture.
- Event names only.
- Optional export later.

Safe event examples:
- app_started
- command_requested
- route_matched
- tool_completed
- tool_failed
- session_started
- session_ended

Do not collect:
- Full user prompts
- Passwords
- Tokens
- File contents
- Browser content
- Email content

Best architecture:
tools/local_analytics_tools.py later can store anonymized local metrics in storage/local_analytics_events.json."""


def crash_logging_framework() -> str:
    _ensure_storage()
    data = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "platform": platform.platform(),
        "recommended_file": "storage/crash_logs.json",
        "capture": [
            "timestamp",
            "phase",
            "route",
            "tool_name",
            "exception_type",
            "safe_message"
        ],
        "blocked": [
            "secrets",
            "full prompt text",
            "file contents",
            "access tokens"
        ]
    }
    _write_json(CRASH_FILE, data)

    return """CRASH LOGGING FRAMEWORK — PHASE 296

Crash logging plan saved to:
storage/crash_log_plan.json

Recommended implementation:
- Wrap route execution later with try/except.
- Store safe exception summaries.
- Never store secrets or full file contents.
- Add command: crash log reader.

Safety:
Only a local plan file was written. No system monitoring was enabled."""


def local_analytics_engine() -> str:
    _ensure_storage()
    events = _read_json(ANALYTICS_FILE, [])

    summary = {}
    for event in events:
        name = event.get("event", "unknown")
        summary[name] = summary.get(name, 0) + 1

    lines = ["LOCAL ANALYTICS ENGINE — PHASE 297\n"]
    lines.append(f"Analytics file: {ANALYTICS_FILE}")

    if not events:
        lines.append("\nNo local analytics events recorded yet.")
        lines.append("\nRecommended next step:")
        lines.append("Add a safe helper later: record_local_event(event_name, metadata=None)")
    else:
        lines.append("\nEvent summary:")
        for name, count in summary.items():
            lines.append(f"- {name}: {count}")

    lines.append("\nPrivacy mode: local-only.")
    return "\n".join(lines)


def user_behavior_tracker() -> str:
    _ensure_storage()
    sessions = _read_json(SESSIONS_FILE, [])

    session = {
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "source": "manual_command",
        "privacy": "local_only",
        "captures": [
            "session start time",
            "high-level command category later"
        ],
        "blocked": [
            "keystrokes",
            "screen recording",
            "passwords",
            "private file content"
        ]
    }

    sessions.append(session)
    sessions = sessions[-100:]
    _write_json(SESSIONS_FILE, sessions)

    return f"""USER BEHAVIOR TRACKER — PHASE 298

Local session marker recorded.

Total stored sessions: {len(sessions)}
File: storage/local_sessions.json

Important:
This is not surveillance. It only records a safe session marker.
No keystrokes, screen content, prompts, passwords, or private files were captured."""


def session_replay_assistant() -> str:
    return """SESSION REPLAY ASSISTANT — PHASE 299

Recommendation:
Do not build real screen/session replay for private JARVIS yet.

Safe alternative:
- Command timeline replay
- Route timeline replay
- Error timeline replay
- Patch proposal replay
- Tool execution replay

Blocked for now:
- Screen recording
- Browser replay
- Keyboard tracking
- Mouse tracking
- Hidden monitoring

Reason:
Session replay is powerful but dangerous. For JARVIS, local command timeline replay gives 80% of the value with 5% of the risk."""


def microsoft_clarity_assistant() -> str:
    project, error = _project()
    if error:
        return error

    return f"""MICROSOFT CLARITY ASSISTANT — PHASE 300

Project: {project}

Use case:
Microsoft Clarity is useful for websites, landing pages, SaaS dashboards, and client UX audits.

Recommended use:
- Add Clarity only to public/client-facing web apps.
- Do not add it to private JARVIS local UI.
- Do not track admin panels unless there is a clear consent policy.
- Mask sensitive fields.

Laravel Blade placement:
resources/views/layouts/app.blade.php
or the public layout head section.

Safety checklist:
1. Get site owner approval.
2. Add privacy policy mention.
3. Mask forms and sensitive inputs.
4. Do not track local/private tools.
5. Use Clarity recordings for UX improvement, not spying.

Status:
Advisory only. No Clarity script was added."""
