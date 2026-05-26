import shutil
import subprocess
from pathlib import Path
from tools.command_guard import block_dangerous_command

MAX_OUTPUT = 12000


def _run(command: list[str], timeout: int = 20, check_guard: bool = True) -> str:
    if check_guard:
        blocked, reason = block_dangerous_command(" ".join(command))
        if blocked:
            return reason

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip() or result.stderr.strip() or "No output."
        return output[:MAX_OUTPUT]
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except Exception as e:
        return f"Command failed: {e}"


def window_manager() -> str:
    session = _run(["bash", "-lc", "echo $XDG_CURRENT_DESKTOP $DESKTOP_SESSION $XDG_SESSION_TYPE"])
    wm = _run(["bash", "-lc", "wmctrl -m 2>/dev/null || echo 'wmctrl not installed'"])
    windows = _run(["bash", "-lc", "wmctrl -l 2>/dev/null | head -30 || echo 'wmctrl not installed'"])

    return f"""WINDOW MANAGER — PHASE 201

Session:
{session}

Window Manager:
{wm}

Open Windows:
{windows}
"""


def linux_system_monitor() -> str:
    uptime = _run(["uptime"])
    memory = _run(["free", "-h"])
    disk = _run(["df", "-h", "/"])
    cpu = _run(["bash", "-lc", "top -bn1 | head -20"])

    return f"""LINUX SYSTEM MONITOR — PHASE 202

Uptime:
{uptime}

Memory:
{memory}

Root Disk:
{disk}

CPU Snapshot:
{cpu}
"""


def disk_cleanup_assistant() -> str:
    home_cache = Path.home() / ".cache"
    apt_cache = "/var/cache/apt"
    journal = _run(["bash", "-lc", "journalctl --disk-usage 2>/dev/null || echo 'journalctl unavailable'"])
    big_dirs = _run(["bash", "-lc", "du -h -d 1 ~ 2>/dev/null | sort -hr | head -15"])

    return f"""DISK CLEANUP ASSISTANT — PHASE 203

This is read-only. No files were deleted.

Journal Usage:
{journal}

Largest Home Directories:
{big_dirs}

Cleanup Suggestions:
- Clear user cache only after review: {home_cache}
- Review apt cache: {apt_cache}
- Review old logs before deleting anything.
- Dangerous cleanup must be built as confirm-based action later.
"""


def log_cleanup_assistant() -> str:
    logs = _run(["bash", "-lc", "find /var/log -type f -printf '%s %p\n' 2>/dev/null | sort -nr | head -20"])
    journal = _run(["bash", "-lc", "journalctl --disk-usage 2>/dev/null || echo 'journalctl unavailable'"])

    return f"""LOG CLEANUP ASSISTANT — PHASE 204

Read-only log inspection.

Largest Log Files:
{logs}

Journal Usage:
{journal}

Safe Recommendation:
Use this phase to inspect only. Add confirm-based cleanup later for journal vacuum or log truncation.
"""


def service_status_checker(service_name: str = "") -> str:
    service_name = service_name.strip()

    if service_name:
        return f"""SERVICE STATUS CHECKER — PHASE 205

Service: {service_name}

{_run(["systemctl", "status", service_name, "--no-pager"], timeout=15)}
"""

    common = ["nginx", "mysql", "mariadb", "php8.4-fpm", "php8.3-fpm", "redis-server"]
    lines = ["SERVICE STATUS CHECKER — PHASE 205", ""]
    for service in common:
        status = _run(["bash", "-lc", f"systemctl is-active {service} 2>/dev/null || true"])
        if status and status != "No output.":
            lines.append(f"- {service}: {status}")
    return "\n".join(lines)


def nginx_config_checker() -> str:
    exists = shutil.which("nginx")
    if not exists:
        return "NGINX CONFIG CHECKER — PHASE 206\n\nnginx command not found."

    test = _run(["nginx", "-t"], timeout=20)
    sites = _run(["bash", "-lc", "ls -la /etc/nginx/sites-enabled 2>/dev/null || echo 'sites-enabled not readable'"])

    return f"""NGINX CONFIG CHECKER — PHASE 206

nginx -t:
{test}

Enabled Sites:
{sites}
"""


def php_fpm_checker() -> str:
    versions = _run(["bash", "-lc", "ls /etc/php 2>/dev/null || echo 'No /etc/php directory'"])
    pools = _run(["bash", "-lc", "find /etc/php -path '*fpm/pool.d/*.conf' -maxdepth 5 2>/dev/null | sort"])
    sockets = _run(["bash", "-lc", "ls -la /run/php 2>/dev/null || echo 'No /run/php directory'"])

    return f"""PHP-FPM CHECKER — PHASE 207

PHP Versions:
{versions}

FPM Pools:
{pools}

Runtime Sockets:
{sockets}
"""


def mysql_checker() -> str:
    status = _run(["bash", "-lc", "systemctl status mysql --no-pager 2>/dev/null || systemctl status mariadb --no-pager 2>/dev/null || echo 'MySQL/MariaDB service not found'"])
    version = _run(["bash", "-lc", "mysql --version 2>/dev/null || mariadb --version 2>/dev/null || echo 'mysql client not found'"])

    return f"""MYSQL CHECKER — PHASE 208

Version:
{version}

Service Status:
{status}
"""


def laravel_deployment_checker() -> str:
    cwd = Path.cwd()
    checks = {
        "artisan": cwd / "artisan",
        ".env": cwd / ".env",
        "composer.json": cwd / "composer.json",
        "public/build/manifest.json": cwd / "public" / "build" / "manifest.json",
        "storage writable": cwd / "storage",
        "bootstrap/cache writable": cwd / "bootstrap" / "cache",
    }

    lines = [f"LARAVEL DEPLOYMENT CHECKER — PHASE 209", f"Path: {cwd}", ""]
    for label, path in checks.items():
        if "writable" in label:
            status = "OK" if path.exists() and path.is_dir() else "MISSING"
        else:
            status = "OK" if path.exists() else "MISSING"
        lines.append(f"- {label}: {status}")

    if (cwd / "artisan").exists():
        lines.append("\nLaravel About:")
        lines.append(_run(["php", "artisan", "about"], timeout=30))

    return "\n".join(lines)


def github_actions_helper() -> str:
    workflows = Path(".github/workflows")
    if not workflows.exists():
        return """GITHUB ACTIONS HELPER — PHASE 210

No .github/workflows directory found.

Recommended next step:
Create a deployment workflow only after confirming:
- server host
- SSH user
- deployment path
- PHP version
- Node version
- build command
"""

    files = list(workflows.glob("*.yml")) + list(workflows.glob("*.yaml"))
    lines = ["GITHUB ACTIONS HELPER — PHASE 210", ""]
    if not files:
        lines.append("Workflow directory exists, but no YAML workflow files found.")
    else:
        lines.append("Detected workflows:")
        lines.extend(f"- {file}" for file in files)

    lines.append("\nSafety Reminder:")
    lines.append("- Never print secrets.")
    lines.append("- Never hardcode SSH keys.")
    lines.append("- Use GitHub repository secrets.")

    return "\n".join(lines)


def linux_admin_help() -> str:
    return """LINUX ADMIN COMMANDS — PHASES 201–210

201. window manager
202. linux system monitor
203. disk cleanup assistant
204. log cleanup assistant
205. service status checker
    service status checker nginx
206. nginx config checker
207. php fpm checker
208. mysql checker
209. laravel deployment checker
210. github actions helper
"""
