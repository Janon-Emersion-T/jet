from pathlib import Path
import json
import shutil
import subprocess
import re

from tools.project_context_tools import get_current_project_path

MAX_OUTPUT = 12000


def _project():
    project = get_current_project_path()
    if not project:
        return None, 'No current project selected.\nUse: use project <name or path>'
    return Path(project), None


def _run(command, cwd=None, timeout=25):
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
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


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(errors="replace"))
    except Exception:
        return {}


def _has(project: Path, filename: str) -> bool:
    return (project / filename).exists()


def _detect_stack(project: Path):
    stack = []

    if _has(project, "artisan"):
        stack.append("Laravel")
    if _has(project, "composer.json"):
        stack.append("PHP / Composer")
    if _has(project, "package.json"):
        stack.append("Node / Vite / Frontend")
    if _has(project, "requirements.txt") or _has(project, "main.py"):
        stack.append("Python")
    if _has(project, "Dockerfile") or _has(project, "docker-compose.yml") or _has(project, "compose.yml"):
        stack.append("Docker-aware project")

    return stack or ["Unknown"]


def swagger_openapi_generator():
    project, error = _project()
    if error:
        return error

    api_files = []
    for pattern in ["api_server.py", "main.py"]:
        if (project / pattern).exists():
            api_files.append(project / pattern)

    route_files = list((project / "core").rglob("*routes*.py")) if (project / "core").exists() else []

    lines = [
        "SWAGGER / OPENAPI GENERATOR — PHASE 251",
        f"Project: {project}",
        "",
        "Mode: read-only advisory.",
        "",
    ]

    if not api_files and not route_files:
        lines.append("No obvious FastAPI/API route files found.")
        return "\n".join(lines)

    lines.append("Detected API-related files:")
    for file in api_files + route_files[:30]:
        lines.append(f"- {file.relative_to(project)}")

    lines.append("")
    lines.append("FastAPI already supports OpenAPI automatically if routes are registered.")
    lines.append("Common local URLs:")
    lines.append("- http://127.0.0.1:8000/docs")
    lines.append("- http://127.0.0.1:8000/redoc")
    lines.append("- http://127.0.0.1:8000/openapi.json")
    lines.append("")
    lines.append("Recommendation:")
    lines.append("- Keep this phase read-only.")
    lines.append("- Add export-to-file later using confirm-before-write.")

    return "\n".join(lines)


def readme_auto_generator():
    project, error = _project()
    if error:
        return error

    stack = _detect_stack(project)
    package = _read_json(project / "package.json") if _has(project, "package.json") else {}
    composer = _read_json(project / "composer.json") if _has(project, "composer.json") else {}

    lines = [
        "README AUTO-GENERATOR — PHASE 252",
        f"Project: {project.name}",
        "",
        "# Suggested README Draft",
        "",
        f"## {project.name}",
        "",
        "Local/offline-first developer assistant project.",
        "",
        "## Detected Stack",
    ]

    lines.extend(f"- {item}" for item in stack)

    lines.append("")
    lines.append("## Setup")

    if _has(project, "requirements.txt"):
        lines.append("```bash")
        lines.append("python3 -m venv venv")
        lines.append("source venv/bin/activate")
        lines.append("pip install -r requirements.txt")
        lines.append("```")

    if package:
        lines.append("```bash")
        lines.append("npm install")
        if "scripts" in package:
            scripts = package.get("scripts", {})
            for name in scripts:
                lines.append(f"npm run {name}")
        lines.append("```")

    if composer:
        lines.append("```bash")
        lines.append("composer install")
        lines.append("```")

    lines.append("")
    lines.append("## Run")
    lines.append("```bash")
    lines.append("python3 main.py")
    lines.append("```")

    lines.append("")
    lines.append("Safety note: Generated as preview only. No README file was written.")

    return "\n".join(lines)


def project_onboarding_assistant():
    project, error = _project()
    if error:
        return error

    stack = _detect_stack(project)

    checks = {
        ".git": _has(project, ".git"),
        "requirements.txt": _has(project, "requirements.txt"),
        "README.md": _has(project, "README.md"),
        ".gitignore": _has(project, ".gitignore"),
        "main.py": _has(project, "main.py"),
        "api_server.py": _has(project, "api_server.py"),
    }

    lines = [
        "PROJECT ONBOARDING ASSISTANT — PHASE 253",
        f"Project: {project}",
        "",
        "Detected stack:",
        *[f"- {item}" for item in stack],
        "",
        "Onboarding checklist:",
    ]

    for name, ok in checks.items():
        lines.append(f"- {name}: {'OK' if ok else 'MISSING'}")

    lines.append("")
    lines.append("Recommended first commands:")
    if _has(project, "requirements.txt"):
        lines.append("- python3 -m venv venv")
        lines.append("- source venv/bin/activate")
        lines.append("- pip install -r requirements.txt")
    if _has(project, "main.py"):
        lines.append("- python3 main.py")
    if _has(project, "api_server.py"):
        lines.append("- uvicorn api_server:app --reload")

    return "\n".join(lines)


def developer_environment_checker():
    project, error = _project()
    if error:
        return error

    tools = ["python3", "pip", "git", "node", "npm", "php", "composer", "mysql", "nginx"]

    lines = [
        "DEVELOPER ENVIRONMENT CHECKER — PHASE 254",
        f"Project: {project}",
        "",
    ]

    for tool in tools:
        path = shutil.which(tool)
        if path:
            version = _run([tool, "--version"])
            lines.append(f"- {tool}: OK | {version.splitlines()[0] if version else path}")
        else:
            lines.append(f"- {tool}: MISSING")

    return "\n".join(lines)


def linux_package_dependency_checker():
    project, error = _project()
    if error:
        return error

    commands = ["python3", "pip", "git", "curl", "unzip", "nginx", "mysql", "php", "composer", "node", "npm"]

    lines = [
        "LINUX PACKAGE DEPENDENCY CHECKER — PHASE 255",
        f"Project: {project}",
        "",
        "Read-only check. No packages were installed.",
        "",
    ]

    for cmd in commands:
        lines.append(f"- {cmd}: {'FOUND' if shutil.which(cmd) else 'MISSING'}")

    lines.append("")
    lines.append("Ubuntu install hint:")
    lines.append("sudo apt install python3 python3-pip git curl unzip nginx mysql-server php composer nodejs npm")

    return "\n".join(lines)


def docker_awareness_layer():
    project, error = _project()
    if error:
        return error

    docker_files = [
        "Dockerfile",
        "docker-compose.yml",
        "compose.yml",
        ".dockerignore",
    ]

    lines = [
        "DOCKER AWARENESS LAYER — PHASE 256",
        f"Project: {project}",
        "",
        "Important: Docker is optional only. This project should not force Docker.",
        "",
        "Detected Docker files:",
    ]

    found = False
    for file in docker_files:
        exists = _has(project, file)
        if exists:
            found = True
        lines.append(f"- {file}: {'FOUND' if exists else 'NOT FOUND'}")

    lines.append("")
    if found:
        lines.append("Recommendation: Respect existing Docker files, but keep normal local execution available.")
    else:
        lines.append("Recommendation: No Docker needed. Continue with direct local/VPS workflow.")

    return "\n".join(lines)


def shared_hosting_compatibility_checker():
    project, error = _project()
    if error:
        return error

    lines = [
        "SHARED HOSTING COMPATIBILITY CHECKER — PHASE 257",
        f"Project: {project}",
        "",
    ]

    checks = {
        "public directory": _has(project, "public"),
        ".htaccess": _has(project, "public/.htaccess") or _has(project, ".htaccess"),
        "composer.json": _has(project, "composer.json"),
        "package.json": _has(project, "package.json"),
        ".env": _has(project, ".env"),
        "artisan": _has(project, "artisan"),
    }

    for name, ok in checks.items():
        lines.append(f"- {name}: {'OK' if ok else 'MISSING'}")

    lines.append("")
    lines.append("Shared hosting notes:")
    lines.append("- Build assets locally before upload if SSH is unavailable.")
    lines.append("- Upload vendor/ only if composer cannot run on hosting.")
    lines.append("- Point domain document root to public/ where possible.")
    lines.append("- Never expose .env, storage, vendor, or app folders publicly.")

    return "\n".join(lines)


def cpanel_deployment_assistant():
    project, error = _project()
    if error:
        return error

    return f"""CPANEL DEPLOYMENT ASSISTANT — PHASE 258
Project: {project}

Read-only deployment plan.

Recommended cPanel flow:
1. Build assets locally.
2. Upload project files outside public_html if possible.
3. Set document root to /public.
4. Create database and user in MySQL Database Wizard.
5. Import SQL using phpMyAdmin.
6. Configure .env carefully.
7. Run composer install only if terminal access exists.
8. Set storage and bootstrap/cache permissions.
9. Test homepage, login, assets, and forms.

Laravel commands if terminal is available:
php artisan key:generate
php artisan migrate --force
php artisan storage:link
php artisan optimize:clear
php artisan optimize

Safety:
- Do not upload local .git folder.
- Do not expose .env.
- Do not run destructive migration commands without backup.
"""


def hostinger_deployment_assistant():
    project, error = _project()
    if error:
        return error

    return f"""HOSTINGER DEPLOYMENT ASSISTANT — PHASE 259
Project: {project}

Read-only Hostinger deployment plan.

Recommended Hostinger flow:
1. Build frontend assets locally: npm install && npm run build.
2. Upload Laravel project to a folder outside public_html if possible.
3. Point domain/subdomain document root to public/.
4. Create MySQL database in Hostinger panel.
5. Import database using phpMyAdmin.
6. Update .env database, app URL, mail, and cache settings.
7. If SSH exists, run composer install --no-dev --optimize-autoloader.
8. Run php artisan optimize after configuration is correct.
9. Confirm storage permissions and symbolic link.

Without SSH:
- Upload vendor folder after local composer install.
- Upload public/build after local npm build.
- Avoid server-side build dependency.

Safety:
- Keep .env private.
- Never place full Laravel root directly as public web root.
"""


def nginx_virtual_host_generator(domain: str = ""):
    project, error = _project()
    if error:
        return error

    domain = domain.strip() or "example.com"
    php_socket = "/run/php/php8.4-fpm.sock"

    config = f"""server {{
    listen 80;
    listen [::]:80;

    server_name {domain} www.{domain};
    root {project}/public;

    index index.php index.html;

    access_log /var/log/nginx/{domain}.access.log;
    error_log /var/log/nginx/{domain}.error.log;

    location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}

    location ~ \\.php$ {{
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:{php_socket};
    }}

    location ~ /\\.ht {{
        deny all;
    }}
}}
"""

    return f"""NGINX VIRTUAL HOST GENERATOR — PHASE 260
Project: {project}

Preview only. No Nginx file was written.

Suggested config:

{config}

Suggested manual path:
/etc/nginx/sites-available/{domain}

Safe commands after manual review:
sudo nginx -t
sudo systemctl reload nginx
"""
