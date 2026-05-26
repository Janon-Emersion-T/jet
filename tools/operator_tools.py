from pathlib import Path
from datetime import datetime
import json
import re

from tools.command_guard import block_dangerous_command
from tools.project_context_tools import get_current_project_path


STORAGE_DIR = Path("storage")
REMOTE_APPROVAL_DIR = STORAGE_DIR / "remote_command_approvals"


def _ensure_storage():
    REMOTE_APPROVAL_DIR.mkdir(parents=True, exist_ok=True)


def _now():
    return datetime.now().isoformat(timespec="seconds")


def _approval_file(command_id: str) -> Path:
    return REMOTE_APPROVAL_DIR / f"{command_id}.json"


def _save_remote_approval(command: str):
    _ensure_storage()

    command_id = datetime.now().strftime("%Y%m%d%H%M%S")

    data = {
        "id": command_id,
        "type": "remote_command",
        "command": command,
        "approved": False,
        "executed": False,
        "created_at": _now(),
    }

    _approval_file(command_id).write_text(json.dumps(data, indent=4), encoding="utf-8")
    return data


def operator_help() -> str:
    return """JARVIS OPERATOR COMMANDS — PHASES 211–220

211. vps deployment assistant
212. secure tunnel setup
213. remote command gateway <command>
214. mobile control interface
215. role permission system
216. autonomous operator mode
217. autonomous coding loop
218. self verification before patching
219. multi file patch generation <request>
220. cross file dependency analysis

Safety rule:
These phases are planning/approval-first. No dangerous remote execution is performed automatically.
"""


def vps_deployment_assistant() -> str:
    project = get_current_project_path()

    return f"""VPS DEPLOYMENT ASSISTANT — PHASE 211

Current Project:
{project if project else "No current project selected. Use: use project <path-or-shortcut>"}

Deployment Checklist:
1. Confirm server host, SSH user, and deployment path.
2. Confirm PHP, Node, Composer, and database versions.
3. Confirm Git branch and repository remote.
4. Confirm .env exists only on server, not inside Git.
5. Confirm storage and bootstrap/cache permissions.
6. Confirm build output exists after npm run build.
7. Confirm migrations are reviewed before running.
8. Confirm backup strategy before production deployment.

Recommended Laravel Deployment Flow:
- git pull origin main
- composer install --no-dev --optimize-autoloader
- npm install
- npm run build
- php artisan migrate --force
- php artisan optimize:clear
- php artisan config:cache
- php artisan route:cache
- php artisan view:cache
- php artisan queue:restart
- sudo systemctl reload nginx
- sudo systemctl restart php-fpm service

Safety:
This assistant does not deploy automatically yet.
Next upgrade should create deployment command approvals.
"""


def secure_tunnel_setup() -> str:
    return """SECURE TUNNEL SETUP — PHASE 212

Purpose:
Expose JARVIS safely to your own devices without opening dangerous public access.

Recommended Options:
1. Tailscale
   - Best for private device-to-device access.
   - No public port forwarding needed.
   - Good for mobile control later.

2. Cloudflare Tunnel
   - Good for web dashboard exposure.
   - Requires strict authentication.
   - Never expose raw command routes publicly.

3. SSH Tunnel
   - Traditional and reliable.
   - Best for admin-only access.
   - Example pattern:
     ssh -L 8000:127.0.0.1:8000 user@server

Security Rules:
- Never expose command execution without authentication.
- Never expose JARVIS directly to the public internet.
- Add role/permission checks before mobile control.
- Use read-only mode first.
- Require confirmation for write/deploy/execute actions.

Status:
Planning only. No tunnel was created.
"""


def remote_command_gateway(command: str) -> str:
    command = command.strip()

    if not command:
        return """REMOTE COMMAND GATEWAY — PHASE 213

Invalid format.

Use:
remote command gateway <command>

Example:
remote command gateway systemctl status nginx
"""

    blocked, reason = block_dangerous_command(command)

    if blocked:
        return f"""REMOTE COMMAND GATEWAY — PHASE 213

Command blocked before approval.

Reason:
{reason}

Command:
{command}
"""

    approval = _save_remote_approval(command)

    return f"""REMOTE COMMAND GATEWAY — PHASE 213

Remote command captured for approval.

ID:
{approval["id"]}

Command:
{command}

Status:
Pending approval.

Important:
This phase does NOT execute remote commands yet.
Future command should be:
confirm remote command {approval["id"]}
"""


def mobile_control_interface() -> str:
    return """MOBILE CONTROL INTERFACE — PHASE 214

Goal:
Allow Janon to control JARVIS from phone safely.

Recommended Architecture:
- FastAPI backend remains local.
- Mobile dashboard connects through secure tunnel.
- Read-only dashboard first.
- Command actions require role permission.
- Dangerous actions require confirmation.

Core Screens:
1. System Status
2. Current Project
3. Task Queue
4. Proposal List
5. Command Approvals
6. Linux Admin Tools
7. Operator Mode

Security Requirements:
- Login required.
- Owner role required for execution.
- No anonymous access.
- No direct shell command from mobile.
- Use approval queue only.

Status:
Design phase only. No interface generated yet.
"""


def role_permission_system() -> str:
    return """ROLE/PERMISSION SYSTEM — PHASE 215

Recommended Roles:
1. owner
   - Full access.
   - Can approve writes and commands.

2. admin
   - Can inspect, plan, and propose.
   - Cannot execute dangerous actions without owner approval.

3. developer
   - Can read projects, propose patches, run safe project checks.

4. viewer
   - Read-only access.

5. mobile
   - Limited dashboard access.

Recommended Permissions:
- read:system
- read:project
- read:memory
- propose:patch
- approve:patch
- rollback:patch
- propose:command
- approve:command
- run:safe_check
- manage:tasks
- manage:settings

Storage Plan:
storage/users.json
storage/roles.json
storage/session_tokens.json

Safety:
Implement permissions before remote/mobile execution.
"""


def autonomous_operator_mode() -> str:
    return """JARVIS AUTONOMOUS OPERATOR MODE — PHASE 216

Correct Meaning:
Autonomous does NOT mean uncontrolled.

Safe Operating Loop:
1. Understand goal.
2. Inspect current project/system.
3. Create plan.
4. Identify required files/commands.
5. Run read-only checks.
6. Generate proposals.
7. Ask for confirmation.
8. Apply only approved patches.
9. Verify result.
10. Summarize outcome.

Allowed Automatically:
- Read files.
- Inspect project.
- Analyze logs.
- Generate plans.
- Generate patch proposals.
- Generate command approvals.

Not Allowed Automatically:
- Delete files.
- Run sudo.
- Deploy production.
- Modify files directly.
- Execute remote commands.
- Install packages.
- Edit secrets.

Status:
Operator mode is blueprint-only until role/approval system is completed.
"""


def autonomous_coding_loop() -> str:
    return """AUTONOMOUS CODING LOOP — PHASE 217

Safe Coding Loop:
1. Read current project context.
2. Detect stack and structure.
3. Locate relevant files.
4. Understand dependencies.
5. Generate implementation plan.
6. Create patch proposal.
7. Run self-verification.
8. Show diff.
9. Wait for confirmation.
10. Apply only after approval.

Required Existing Systems:
- Project context
- SafeWriter
- ProposalManager
- Command approvals
- Project health tools

Next Upgrade:
Connect this loop to multi-file patch generation and self-verification.
"""


def self_verification_before_patching() -> str:
    project = get_current_project_path()

    return f"""SELF-VERIFICATION BEFORE PATCHING — PHASE 218

Current Project:
{project if project else "No current project selected."}

Verification Checklist:
1. Is the current project selected?
2. Are relevant files inspected?
3. Are imports checked?
4. Are route registrations checked?
5. Are helper functions reused?
6. Are safety rules respected?
7. Does the patch avoid command_router bloat?
8. Does the patch preserve backward compatibility?
9. Does the patch include rollback support?
10. Does the patch require confirmation before write?

Recommended Result:
Only create a patch proposal if all checks pass.

Status:
Read-only checklist generated.
"""


def multi_file_patch_generation(request: str) -> str:
    request = request.strip()
    project = get_current_project_path()

    if not request:
        return """MULTI-FILE PATCH GENERATION — PHASE 219

Invalid format.

Use:
multi file patch generation <request>

Example:
multi file patch generation add operator approval routes
"""

    return f"""MULTI-FILE PATCH GENERATION — PHASE 219

Request:
{request}

Current Project:
{project if project else "No current project selected."}

Safe Multi-File Patch Plan:
1. Identify all affected files.
2. Read every affected file before editing.
3. Build dependency map.
4. Generate patch proposal per file.
5. Store every proposal separately.
6. Show combined summary.
7. Require confirmation per proposal or batch confirmation later.
8. Allow rollback per file.

Important:
This phase does not write files directly yet.
It defines the workflow needed for safe multi-file patching.
"""


def cross_file_dependency_analysis() -> str:
    project = get_current_project_path()

    if not project:
        return "CROSS-FILE DEPENDENCY ANALYSIS — PHASE 220\n\nNo current project selected. Use: use project <path-or-shortcut>"

    py_files = list(project.rglob("*.py"))[:200]

    imports = []
    route_files = []
    tool_files = []

    for file in py_files:
        rel = file.relative_to(project)

        if "core/routes" in str(rel):
            route_files.append(str(rel))

        if str(rel).startswith("tools/"):
            tool_files.append(str(rel))

        try:
            content = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(f"{rel}: {stripped}")

    return f"""CROSS-FILE DEPENDENCY ANALYSIS — PHASE 220

Project:
{project}

Route Files:
{chr(10).join("- " + f for f in route_files[:50]) if route_files else "No route files detected."}

Tool Files:
{chr(10).join("- " + f for f in tool_files[:80]) if tool_files else "No tool files detected."}

Detected Imports:
{chr(10).join("- " + i for i in imports[:120]) if imports else "No imports detected."}

Safety Notes:
- Use this before multi-file patching.
- Check route-to-tool imports before adding features.
- Avoid duplicate router imports.
- Prefer adding new route modules instead of bloating command_router.py.
"""
