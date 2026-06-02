import re
import shutil
import subprocess
import json
from pathlib import Path

from tools.project_context_tools import set_current_project, get_current_project_path
from tools.content_assistant_tools import website_content_pack

MAX_OUTPUT = 12000
SAFE_BASE_DIRS = [
    Path("/var/www"),
    Path.home() / "Projects",
    Path.home() / "Desktop",
    Path.home() / "Documents",
]


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().split())


def _inside_safe_base(path: Path) -> bool:
    resolved = path.resolve()
    for base in SAFE_BASE_DIRS:
        try:
            resolved.relative_to(base.resolve())
            return True
        except ValueError:
            continue
    return False


def _validate_target_dir(target_dir: str) -> tuple[Path | None, str | None]:
    if not target_dir:
        return None, "Target directory is required."

    path = Path(target_dir).expanduser().resolve()
    if not _inside_safe_base(path):
        allowed = ", ".join(str(item) for item in SAFE_BASE_DIRS)
        return None, f"Blocked target path. Allowed base folders: {allowed}"

    if path.exists() and path.is_file():
        return None, "Target path points to a file, not a directory."

    if path.exists() and any(path.iterdir()):
        return None, "Target directory already exists and is not empty."

    return path, None


def _run(command: list[str], cwd: Path, timeout: int = 1800) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return False, f"Command not found: {command[0]}"
    except Exception as exc:
        return False, f"Command failed: {exc}"

    output = (result.stdout.strip() or result.stderr.strip() or "No output.")[:MAX_OUTPUT]
    return result.returncode == 0, output


def install_laravel_project(target_dir: str, company_name: str | None = None) -> str:
    path, error = _validate_target_dir(target_dir)
    if error:
        return error

    if shutil.which("composer") is None:
        return "Composer is not installed or not available in PATH."

    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)

    ok, output = _run(
        ["composer", "create-project", "laravel/laravel", path.name],
        cwd=parent,
        timeout=3600,
    )

    if not ok:
        return (
            "LARAVEL INSTALL FAILED\n"
            f"Target: {path}\n\n"
            f"{output}"
        )

    set_current_project(str(path))

    lines = [
        "LARAVEL PROJECT CREATED",
        f"Target: {path}",
        "Framework: Laravel",
    ]

    if company_name:
        lines.append(f"Company: {company_name}")

    lines.extend([
        "",
        "Current project context was updated automatically.",
        "",
        output,
    ])
    return "\n".join(lines)


def _project_dir_from_hint(target_dir: str | None = None) -> tuple[Path | None, str | None]:
    if target_dir:
        path = Path(target_dir).expanduser().resolve()
    else:
        current = get_current_project_path()
        if not current:
            return None, "No current project selected. Use a path or set the project context first."
        path = Path(current).resolve()

    if not path.exists() or not path.is_dir():
        return None, "Project directory not found."

    if not _inside_safe_base(path):
        allowed = ", ".join(str(item) for item in SAFE_BASE_DIRS)
        return None, f"Blocked project path. Allowed base folders: {allowed}"

    return path, None


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _detect_package_manager(project_dir: Path, package_name: str, user_input: str) -> str | None:
    text = _normalize(user_input).lower()
    package = (package_name or "").strip().lower()

    has_npm = (project_dir / "package.json").exists()
    has_composer = (project_dir / "composer.json").exists()
    has_pip = (project_dir / "requirements.txt").exists() or (project_dir / "pyproject.toml").exists()
    has_cargo = (project_dir / "Cargo.toml").exists()
    has_go = (project_dir / "go.mod").exists()

    frontend_hints = {
        "tailwindcss", "@tailwindcss/vite", "react", "vue", "svelte", "axios",
        "vite", "next", "nuxt", "eslint", "prettier", "typescript", "alpinejs",
    }
    php_hints = {
        "livewire/livewire", "filament/filament", "spatie/laravel-permission",
        "laravel/sanctum", "laravel/breeze", "laravel/jetstream", "barryvdh/laravel-debugbar",
    }

    if has_npm and not has_composer and not has_pip:
        return "npm"
    if has_composer and not has_npm and not has_pip:
        return "composer"
    if has_pip and not has_npm and not has_composer:
        return "pip"
    if has_cargo:
        return "cargo"
    if has_go:
        return "go"

    if has_npm and has_composer:
        if package.startswith("@") or package in frontend_hints:
            return "npm"
        if package in php_hints or "laravel" in text or "php" in text or "composer" in text:
            return "composer"
        if any(word in text for word in ["frontend", "ui", "css", "javascript", "typescript", "vite"]):
            return "npm"
        if any(word in text for word in ["backend", "php", "artisan", "laravel", "eloquent", "composer"]):
            return "composer"
        if "/" in package and not package.startswith("@"):
            return "composer"
        return "npm"

    return None


def _venv_python(project_dir: Path) -> str:
    for candidate in (project_dir / ".venv" / "bin" / "python", project_dir / "venv" / "bin" / "python"):
        if candidate.exists():
            return str(candidate)
    return "python3"


def install_project_dependency(package_name: str, target_dir: str | None = None, user_input: str = "") -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    package_name = (package_name or "").strip()
    if not package_name:
        return "Package name is required."

    manager = _detect_package_manager(project_dir, package_name, user_input)
    if not manager:
        return "Could not detect a supported package manager for the current project."

    commands_run: list[str] = []
    outputs: list[str] = []

    if manager == "npm":
        command = ["npm", "install", package_name]
        ok, output = _run(command, cwd=project_dir, timeout=1800)
        commands_run.append(" ".join(command))
        outputs.append(output)
        if not ok:
            return f"DEPENDENCY INSTALL FAILED\nProject: {project_dir}\nManager: npm\n\n{output}"

        package_json = _read_json(project_dir / "package.json")
        if "build" in package_json.get("scripts", {}):
            ok, build_output = _run(["npm", "run", "build"], cwd=project_dir, timeout=1800)
            commands_run.append("npm run build")
            outputs.append(build_output)
            if not ok:
                return (
                    "DEPENDENCY INSTALLED, BUT BUILD FAILED\n"
                    f"Project: {project_dir}\nManager: npm\nPackage: {package_name}\n\n"
                    f"{build_output}"
                )

    elif manager == "composer":
        command = ["composer", "require", package_name]
        ok, output = _run(command, cwd=project_dir, timeout=3600)
        commands_run.append(" ".join(command))
        outputs.append(output)
        if not ok:
            return f"DEPENDENCY INSTALL FAILED\nProject: {project_dir}\nManager: composer\n\n{output}"

    elif manager == "pip":
        python_bin = _venv_python(project_dir)
        command = [python_bin, "-m", "pip", "install", package_name]
        ok, output = _run(command, cwd=project_dir, timeout=3600)
        commands_run.append(" ".join(command))
        outputs.append(output)
        if not ok:
            return f"DEPENDENCY INSTALL FAILED\nProject: {project_dir}\nManager: pip\n\n{output}"

    elif manager == "cargo":
        command = ["cargo", "add", package_name]
        ok, output = _run(command, cwd=project_dir, timeout=1800)
        commands_run.append(" ".join(command))
        outputs.append(output)
        if not ok:
            return f"DEPENDENCY INSTALL FAILED\nProject: {project_dir}\nManager: cargo\n\n{output}"

    elif manager == "go":
        command = ["go", "get", package_name]
        ok, output = _run(command, cwd=project_dir, timeout=1800)
        commands_run.append(" ".join(command))
        outputs.append(output)
        if not ok:
            return f"DEPENDENCY INSTALL FAILED\nProject: {project_dir}\nManager: go\n\n{output}"

    set_current_project(str(project_dir))
    return "\n".join([
        "DEPENDENCY INSTALL COMPLETE",
        f"Project: {project_dir}",
        f"Manager: {manager}",
        f"Package: {package_name}",
        "",
        "Commands executed:",
        *[f"- {command}" for command in commands_run],
        "",
        *outputs,
    ])


def execute_project_automation(user_input: str, target_dir: str | None = None) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    text = _normalize(user_input).lower()
    manager = _detect_package_manager(project_dir, "", user_input)
    commands: list[list[str]] = []
    labels: list[str] = []

    package_json = project_dir / "package.json"
    package_data = _read_json(package_json) if package_json.exists() else {}
    scripts = package_data.get("scripts", {})
    has_artisan = (project_dir / "artisan").exists()
    has_manage_py = (project_dir / "manage.py").exists()

    wants_install = any(phrase in text for phrase in [
        "install dependencies",
        "install deps",
        "setup dependencies",
        "set up dependencies",
        "restore dependencies",
    ])
    wants_build = "build" in text or "compile" in text
    wants_test = "test" in text or "tests" in text
    wants_migrate = "migrate" in text or "migration" in text

    if wants_install:
        if manager == "npm":
            commands.append(["npm", "install"])
            labels.append("npm install")
        elif manager == "composer":
            commands.append(["composer", "install"])
            labels.append("composer install")
        elif manager == "pip":
            if (project_dir / "requirements.txt").exists():
                commands.append([_venv_python(project_dir), "-m", "pip", "install", "-r", "requirements.txt"])
                labels.append("pip install -r requirements.txt")
            elif (project_dir / "pyproject.toml").exists():
                commands.append([_venv_python(project_dir), "-m", "pip", "install", "-e", "."])
                labels.append("pip install -e .")
        elif manager == "cargo":
            commands.append(["cargo", "fetch"])
            labels.append("cargo fetch")
        elif manager == "go":
            commands.append(["go", "mod", "download"])
            labels.append("go mod download")

    if wants_migrate:
        if has_artisan:
            commands.append(["php", "artisan", "migrate", "--force"])
            labels.append("php artisan migrate --force")
        elif has_manage_py:
            commands.append([_venv_python(project_dir), "manage.py", "migrate"])
            labels.append("python manage.py migrate")

    if wants_build:
        if manager == "npm" and "build" in scripts:
            commands.append(["npm", "run", "build"])
            labels.append("npm run build")
        elif manager == "cargo":
            commands.append(["cargo", "build"])
            labels.append("cargo build")
        elif manager == "go":
            commands.append(["go", "build", "./..."])
            labels.append("go build ./...")

    if wants_test:
        if has_artisan:
            commands.append(["php", "artisan", "test"])
            labels.append("php artisan test")
        elif has_manage_py and (project_dir / "pytest.ini").exists():
            commands.append([_venv_python(project_dir), "-m", "pytest"])
            labels.append("python -m pytest")
        elif manager == "pip":
            commands.append([_venv_python(project_dir), "-m", "pytest"])
            labels.append("python -m pytest")
        elif manager == "npm" and "test" in scripts:
            commands.append(["npm", "test"])
            labels.append("npm test")
        elif manager == "cargo":
            commands.append(["cargo", "test"])
            labels.append("cargo test")
        elif manager == "go":
            commands.append(["go", "test", "./..."])
            labels.append("go test ./...")

    if not commands:
        return (
            "PROJECT AUTOMATION NOT SUPPORTED YET\n"
            f"Project: {project_dir}\n"
            "I could not map this request to a safe executable project action."
        )

    outputs: list[str] = []
    for command, label in zip(commands, labels):
        ok, output = _run(command, cwd=project_dir, timeout=3600)
        outputs.append(f"$ {label}\n{output}")
        if not ok:
            return (
                "PROJECT AUTOMATION FAILED\n"
                f"Project: {project_dir}\n"
                f"Manager: {manager or 'unknown'}\n"
                f"Failed command: {label}\n\n"
                f"{output}"
            )

    set_current_project(str(project_dir))
    return "\n".join([
        "PROJECT AUTOMATION COMPLETE",
        f"Project: {project_dir}",
        f"Manager: {manager or 'unknown'}",
        "",
        "Commands executed:",
        *[f"- {label}" for label in labels],
        "",
        *outputs,
    ])


def check_laravel_page_status(page_name: str, target_dir: str | None = None) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    if not (project_dir / "artisan").exists():
        return "The current project is not a Laravel application."

    normalized = _normalize(page_name).lower()
    normalized = normalized.replace(" page", "").replace("contact us", "contact-us").replace(" ", "-")
    page_map = {
        "home": ("resources/views/pages/home.blade.php", "/"),
        "about": ("resources/views/pages/about.blade.php", "/about"),
        "media": ("resources/views/pages/media.blade.php", "/media"),
        "blog": ("resources/views/pages/blogs.blade.php", "/blogs"),
        "blogs": ("resources/views/pages/blogs.blade.php", "/blogs"),
        "contact": ("resources/views/pages/contact.blade.php", "/contact-us"),
        "contact-us": ("resources/views/pages/contact.blade.php", "/contact-us"),
        "footer": ("resources/views/layouts/app.blade.php", "shared layout footer"),
    }

    if normalized not in page_map:
        return f"Unknown page or section: {page_name}"

    file_rel, route_hint = page_map[normalized]
    target = project_dir / file_rel
    exists = target.exists()

    lines = [
        "WEBSITE STATUS",
        f"Project: {project_dir}",
        f"Requested page/section: {page_name}",
        f"Exists: {'YES' if exists else 'NO'}",
        f"File: {target}",
        f"Route or section: {route_hint}",
    ]
    if exists:
        preview = target.read_text(encoding="utf-8", errors="replace")[:240].strip()
        lines.extend(["", "Preview:", preview])
    return "\n".join(lines)


def install_tailwind_for_project(target_dir: str | None = None) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    package_json = project_dir / "package.json"
    if not package_json.exists():
        return "package.json not found in the target project."

    data = _read_json(package_json)
    dev_dependencies = data.get("devDependencies", {})
    dependencies = data.get("dependencies", {})
    all_dependencies = {**dependencies, **dev_dependencies}

    already_has_tailwind = "tailwindcss" in all_dependencies
    already_has_vite_plugin = "@tailwindcss/vite" in all_dependencies

    vite_config = project_dir / "vite.config.js"
    app_css = project_dir / "resources" / "css" / "app.css"
    node_modules = project_dir / "node_modules"

    commands_run: list[str] = []

    if not already_has_tailwind or not already_has_vite_plugin:
        ok, output = _run(
            ["npm", "install", "-D", "tailwindcss", "@tailwindcss/vite"],
            cwd=project_dir,
            timeout=1800,
        )
        commands_run.append("npm install -D tailwindcss @tailwindcss/vite")
        if not ok:
            return (
                "TAILWIND INSTALL FAILED\n"
                f"Project: {project_dir}\n\n"
                f"{output}"
            )

    elif not node_modules.exists():
        ok, output = _run(["npm", "install"], cwd=project_dir, timeout=1800)
        commands_run.append("npm install")
        if not ok:
            return (
                "PROJECT DEPENDENCY INSTALL FAILED\n"
                f"Project: {project_dir}\n\n"
                f"{output}"
            )

    notes: list[str] = []

    if vite_config.exists():
        vite_content = vite_config.read_text(encoding="utf-8", errors="replace")
        if "@tailwindcss/vite" in vite_content and "tailwindcss()" in vite_content:
            notes.append("Vite Tailwind plugin already configured.")
        else:
            notes.append("Tailwind package installed, but vite.config.js still needs Tailwind plugin wiring.")
    else:
        notes.append("vite.config.js not found. Tailwind install completed without Vite wiring.")

    if app_css.exists():
        css_content = app_css.read_text(encoding="utf-8", errors="replace")
        if "@import 'tailwindcss';" in css_content or '@import "tailwindcss";' in css_content:
            notes.append("App CSS already imports Tailwind.")
        else:
            app_css.write_text("@import 'tailwindcss';\n\n" + css_content, encoding="utf-8")
            notes.append("Added Tailwind import to resources/css/app.css.")
    else:
        notes.append("resources/css/app.css not found.")

    ok, build_output = _run(["npm", "run", "build"], cwd=project_dir, timeout=1800)
    commands_run.append("npm run build")
    if not ok:
        return (
            "TAILWIND SETUP PARTIALLY COMPLETE\n"
            f"Project: {project_dir}\n"
            + ("\n".join(f"- {note}" for note in notes) if notes else "")
            + "\n\nBuild verification failed:\n"
            + build_output
        )

    set_current_project(str(project_dir))

    lines = [
        "TAILWIND SETUP COMPLETE",
        f"Project: {project_dir}",
        f"Tailwind dependency present: {'YES' if already_has_tailwind else 'ADDED'}",
        f"Tailwind Vite plugin present: {'YES' if already_has_vite_plugin else 'ADDED'}",
        "",
        "Checks:",
    ]
    lines.extend(f"- {note}" for note in notes)
    lines.append("")
    lines.append("Commands executed:")
    lines.extend(f"- {command}" for command in commands_run)
    lines.append("")
    lines.append(build_output)
    return "\n".join(lines)


def build_laravel_marketing_site(
    target_dir: str | None = None,
    company_name: str = "Center for Systematic Learning",
    page_names: list[str] | None = None,
) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    if not (project_dir / "artisan").exists():
        return "The current project is not a Laravel application."

    pages = page_names or ["home", "about", "media", "blogs", "contact-us"]
    content_pack = website_content_pack(
        company_name,
        focus="structured education, expert facilitation, research-led media, and institution-ready learning programs",
    )

    routes_content = """<?php

use Illuminate\\Support\\Facades\\Route;

$sitePages = [
    'home' => [
        'title' => 'Center for Systematic Learning',
        'description' => 'A modern learning organisation focused on structured growth, thoughtful teaching, and measurable impact.',
    ],
    'about' => [
        'title' => 'About Us',
        'description' => 'Learn how CSL turns ambitious ideas into repeatable, human-centered learning systems.',
    ],
    'media' => [
        'title' => 'Media',
        'description' => 'Explore lectures, interviews, event highlights, and knowledge resources from CSL.',
    ],
    'blogs' => [
        'title' => 'Blogs',
        'description' => 'Read essays, field notes, and practical guides from the CSL team.',
    ],
    'contact-us' => [
        'title' => 'Contact Us',
        'description' => 'Start a conversation with CSL about training, advisory work, or institutional partnerships.',
    ],
];

Route::get('/', function () use ($sitePages) {
    return view('pages.home', [
        'meta' => $sitePages['home'],
        'pageKey' => 'home',
    ]);
})->name('home');

Route::get('/about', function () use ($sitePages) {
    return view('pages.about', [
        'meta' => $sitePages['about'],
        'pageKey' => 'about',
    ]);
})->name('about');

Route::get('/media', function () use ($sitePages) {
    return view('pages.media', [
        'meta' => $sitePages['media'],
        'pageKey' => 'media',
    ]);
})->name('media');

Route::get('/blogs', function () use ($sitePages) {
    return view('pages.blogs', [
        'meta' => $sitePages['blogs'],
        'pageKey' => 'blogs',
    ]);
})->name('blogs');

Route::get('/contact-us', function () use ($sitePages) {
    return view('pages.contact', [
        'meta' => $sitePages['contact-us'],
        'pageKey' => 'contact-us',
    ]);
})->name('contact');
"""

    layout_content = f"""<!DOCTYPE html>
<html lang="{{{{ str_replace('_', '-', app()->getLocale()) }}}}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{{{ $meta['title'] ?? '{company_name}' }}}}</title>
    <meta name="description" content="{{{{ $meta['description'] ?? '{company_name}' }}}}">
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-[var(--csl-ink)] text-white antialiased">
    <div class="absolute inset-x-0 top-0 -z-10 h-[32rem] bg-[radial-gradient(circle_at_top,rgba(243,173,85,0.28),transparent_42%),linear-gradient(180deg,rgba(8,30,40,1)_0%,rgba(8,30,40,0.96)_52%,rgba(243,244,238,1)_52%,rgba(243,244,238,1)_100%)]"></div>
    <header class="sticky top-0 z-40 border-b border-white/10 bg-[rgba(8,30,40,0.82)] backdrop-blur-xl">
        <div class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-10">
            <a href="{{{{ route('home') }}}}" class="flex items-center gap-3">
                <div class="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/15 bg-white/8 text-sm font-semibold tracking-[0.3em] text-[var(--csl-gold)]">CSL</div>
                <div>
                    <p class="text-xs uppercase tracking-[0.32em] text-white/55">Center for</p>
                    <p class="font-display text-lg text-white">Systematic Learning</p>
                </div>
            </a>
            <nav class="hidden items-center gap-2 lg:flex">
                @php
                    $navItems = [
                        'home' => ['label' => 'Home', 'route' => 'home'],
                        'about' => ['label' => 'About', 'route' => 'about'],
                        'media' => ['label' => 'Media', 'route' => 'media'],
                        'blogs' => ['label' => 'Blogs', 'route' => 'blogs'],
                        'contact-us' => ['label' => 'Contact Us', 'route' => 'contact'],
                    ];
                @endphp
                @foreach ($navItems as $key => $item)
                    <a
                        href="{{{{ route($item['route']) }}}}"
                        class="rounded-full px-4 py-2 text-sm transition {{{{ $pageKey === $key ? 'bg-white text-[var(--csl-ink)] shadow-lg shadow-black/20' : 'text-white/72 hover:bg-white/8 hover:text-white' }}}}"
                    >
                        {{{{ $item['label'] }}}}
                    </a>
                @endforeach
            </nav>
            <a href="{{{{ route('contact') }}}}" class="hidden rounded-full bg-[var(--csl-gold)] px-5 py-3 text-sm font-semibold text-[var(--csl-ink)] transition hover:translate-y-[-1px] hover:bg-[var(--csl-gold-soft)] lg:inline-flex">Start a Conversation</a>
        </div>
    </header>

    <main>
        @yield('content')
    </main>

    <footer class="border-t border-slate-900/10 bg-[var(--csl-paper)] text-slate-800">
        <div class="mx-auto max-w-7xl px-6 py-14 lg:px-10">
            <div class="mb-10 flex flex-col gap-6 rounded-[2rem] bg-[var(--csl-ink)] px-6 py-8 text-white lg:flex-row lg:items-end lg:justify-between lg:px-8">
                <div class="max-w-2xl space-y-4">
                    <p class="text-xs font-semibold uppercase tracking-[0.32em] text-[var(--csl-gold)]">Ready to build a stronger learning system?</p>
                    <h2 class="font-display text-3xl">{content_pack["footer_tagline"]}</h2>
                    <p class="text-base leading-7 text-white/72">{content_pack["footer_body"]}</p>
                </div>
                <div class="flex flex-col gap-3 sm:flex-row">
                    <a href="{{{{ route('contact') }}}}" class="inline-flex items-center justify-center rounded-full bg-[var(--csl-gold)] px-6 py-3 text-sm font-semibold text-[var(--csl-ink)] transition hover:translate-y-[-1px] hover:bg-[var(--csl-gold-soft)]">Book a Consultation</a>
                    <a href="{{{{ route('blogs') }}}}" class="inline-flex items-center justify-center rounded-full border border-white/12 px-6 py-3 text-sm font-semibold text-white transition hover:bg-white/8">Read Insights</a>
                </div>
            </div>
            <div class="grid gap-10 lg:grid-cols-[1.6fr_0.9fr_0.9fr_1fr]">
            <div class="space-y-4">
                <p class="text-xs font-semibold uppercase tracking-[0.32em] text-[var(--csl-teal)]">{company_name}</p>
                <h2 class="font-display text-3xl text-[var(--csl-ink)]">{content_pack["footer_tagline"]}</h2>
                <p class="max-w-xl text-base leading-7 text-slate-600">{content_pack["footer_body"]}</p>
            </div>
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Explore</p>
                <ul class="mt-5 space-y-3 text-sm text-slate-700">
                    <li><a class="transition hover:text-[var(--csl-teal)]" href="{{{{ route('about') }}}}">About Us</a></li>
                    <li><a class="transition hover:text-[var(--csl-teal)]" href="{{{{ route('media') }}}}">Media</a></li>
                    <li><a class="transition hover:text-[var(--csl-teal)]" href="{{{{ route('blogs') }}}}">Blogs</a></li>
                    <li><a class="transition hover:text-[var(--csl-teal)]" href="{{{{ route('contact') }}}}">Contact Us</a></li>
                </ul>
            </div>
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Focus Areas</p>
                <ul class="mt-5 space-y-3 text-sm text-slate-700">
                    <li>Executive education</li>
                    <li>Professional upskilling</li>
                    <li>Research-led media</li>
                    <li>Institutional learning design</li>
                </ul>
            </div>
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Contact</p>
                <ul class="mt-5 space-y-3 text-sm text-slate-700">
                    <li>hello@csl.global</li>
                    <li>+94 11 245 7788</li>
                    <li>Colombo Learning District</li>
                    <li>Mon to Fri, 9:00 AM to 6:00 PM</li>
                </ul>
            </div>
        </div>
    </footer>
</body>
</html>
"""

    home_content = """@extends('layouts.app')

@section('content')
    <section class="mx-auto max-w-7xl px-6 pb-24 pt-16 lg:px-10 lg:pb-32 lg:pt-24">
        <div class="grid gap-12 lg:grid-cols-[1.15fr_0.85fr] lg:items-end">
            <div class="space-y-8">
                <span class="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/8 px-4 py-2 text-xs font-semibold uppercase tracking-[0.28em] text-[var(--csl-gold)]">
                    {content_pack["hero_kicker"]}
                </span>
                <div class="space-y-6">
                    <h1 class="font-display max-w-4xl text-5xl leading-[1.02] text-white sm:text-6xl lg:text-7xl">
                        {content_pack["hero_title"]}
                    </h1>
                    <p class="max-w-2xl text-lg leading-8 text-white/72 sm:text-xl">
                        {content_pack["hero_body"]}
                    </p>
                </div>
                <div class="flex flex-col gap-4 sm:flex-row">
                    <a href="{{ route('contact') }}" class="inline-flex items-center justify-center rounded-full bg-[var(--csl-gold)] px-6 py-3.5 text-sm font-semibold text-[var(--csl-ink)] transition hover:translate-y-[-1px] hover:bg-[var(--csl-gold-soft)]">
                        {content_pack["hero_cta"]}
                    </a>
                    <a href="{{ route('about') }}" class="inline-flex items-center justify-center rounded-full border border-white/15 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-white/8">
                        {content_pack["hero_secondary_cta"]}
                    </a>
                </div>
            </div>
            <div class="rounded-[2rem] border border-white/10 bg-white/6 p-6 shadow-2xl shadow-black/20 backdrop-blur">
                <div class="grid gap-4 sm:grid-cols-2">
                    <div class="rounded-3xl bg-[var(--csl-teal)]/22 p-5">
                        <p class="text-sm uppercase tracking-[0.22em] text-[var(--csl-gold)]">Core focus</p>
                        <p class="mt-3 text-2xl font-semibold text-white">Structured growth pathways</p>
                    </div>
                    <div class="rounded-3xl bg-white/8 p-5">
                        <p class="text-sm uppercase tracking-[0.22em] text-white/55">Signature work</p>
                        <p class="mt-3 text-2xl font-semibold text-white">Leadership, health, and technology learning programs</p>
                    </div>
                    <div class="rounded-3xl bg-white/8 p-5">
                        <p class="text-sm uppercase tracking-[0.22em] text-white/55">Delivery style</p>
                        <p class="mt-3 text-2xl font-semibold text-white">Workshops, cohorts, research media, and advisory support</p>
                    </div>
                    <div class="rounded-3xl bg-[var(--csl-gold)]/18 p-5">
                        <p class="text-sm uppercase tracking-[0.22em] text-[var(--csl-gold)]">Promise</p>
                        <p class="mt-3 text-2xl font-semibold text-white">Clarity without oversimplification</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="bg-[var(--csl-paper)] py-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="grid gap-8 lg:grid-cols-3">
                <div class="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">01. Diagnose</p>
                    <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Map the real learning need.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">We begin with systems thinking, not assumptions. CSL studies context, capability gaps, and the practical outcomes your learners need.</p>
                </div>
                <div class="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">02. Design</p>
                    <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Build the curriculum with discipline.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">Programs are sequenced like strong product systems: foundations first, then guided practice, review, reinforcement, and synthesis.</p>
                </div>
                <div class="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">03. Sustain</p>
                    <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Turn learning into durable capability.</h2>
                    <p class="mt-4 text-base leading-7 text-slate-600">We measure momentum, create reusable media assets, and keep the learning system alive after the first workshop ends.</p>
                </div>
            </div>
        </div>
    </section>
@endsection
"""

    about_content = """@extends('layouts.app')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-[var(--csl-gold)]">About CSL</p>
                <h1 class="mt-5 font-display text-5xl leading-tight text-white">We design learning like a serious system, not a one-off event.</h1>
            </div>
            <div class="space-y-6 text-lg leading-8 text-white/72">
                <p>{content_pack["about_intro"]}</p>
                <p>Our method borrows from education, systems thinking, and high-performance product teams. That means clear sequencing, intentional feedback loops, and strong accountability for the final outcome.</p>
            </div>
        </div>
    </section>

    <section class="bg-[var(--csl-paper)] py-24 text-slate-900">
        <div class="mx-auto max-w-7xl px-6 lg:px-10">
            <div class="grid gap-8 lg:grid-cols-3">
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Mission</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">To help people and institutions learn with more depth, better structure, and stronger transfer into real work.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Approach</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">Every program is designed around foundations, practice, review, synthesis, and measurable evidence of progress.</p>
                </article>
                <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                    <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Standards</p>
                    <p class="mt-4 text-lg leading-8 text-slate-700">We aim for academic integrity, practical clarity, and communication that respects how adults actually learn.</p>
                </article>
            </div>
        </div>
    </section>
@endsection
"""

    media_content = """@extends('layouts.app')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="max-w-3xl">
            <p class="text-sm font-semibold uppercase tracking-[0.28em] text-[var(--csl-gold)]">Media</p>
            <h1 class="mt-5 font-display text-5xl leading-tight text-white">Stories, lectures, interviews, and learning moments worth revisiting.</h1>
            <p class="mt-6 text-lg leading-8 text-white/72">{content_pack["media_intro"]}</p>
        </div>
    </section>

    <section class="bg-[var(--csl-paper)] py-24 text-slate-900">
        <div class="mx-auto grid max-w-7xl gap-8 px-6 lg:grid-cols-3 lg:px-10">
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Featured lecture</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Designing institutions that learn continuously</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">A flagship talk on building teams that improve through evidence, reflection, and better systems.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">In the press</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">CSL conversations with educators and industry leaders</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">Use this space for partnerships, interviews, and public-facing thought leadership.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Resource archive</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Slides, recordings, and downloadable learning tools</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">A clear place to publish assets that extend the life of your teaching and events.</p>
            </article>
        </div>
    </section>
@endsection
"""

    blogs_content = """@extends('layouts.app')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-10 lg:grid-cols-[0.95fr_1.05fr]">
            <div>
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-[var(--csl-gold)]">Blogs</p>
                <h1 class="mt-5 font-display text-5xl leading-tight text-white">A publishing space for serious ideas that still feel readable.</h1>
            </div>
            <p class="text-lg leading-8 text-white/72">{content_pack["blogs_intro"]}</p>
        </div>
    </section>

    <section class="bg-[var(--csl-paper)] py-24 text-slate-900">
        <div class="mx-auto grid max-w-7xl gap-8 px-6 lg:grid-cols-3 lg:px-10">
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Editorial</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Why high-performing organisations treat learning like infrastructure</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">A framework for leaders who want learning systems that scale without becoming shallow.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Practice note</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">Designing review loops that make knowledge stick</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">Practical advice for keeping learning active after workshops, seminars, or training sessions end.</p>
            </article>
            <article class="rounded-[2rem] bg-white p-8 shadow-sm ring-1 ring-slate-200">
                <p class="text-sm font-semibold uppercase tracking-[0.24em] text-[var(--csl-teal)]">Field report</p>
                <h2 class="mt-4 font-display text-3xl text-[var(--csl-ink)]">What institutions gain when media and education work together</h2>
                <p class="mt-4 text-base leading-7 text-slate-600">How resource libraries, video archives, and commentary expand the reach of a learning organisation.</p>
            </article>
        </div>
    </section>
@endsection
"""

    contact_content = """@extends('layouts.app')

@section('content')
    <section class="mx-auto max-w-7xl px-6 py-20 lg:px-10 lg:py-24">
        <div class="grid gap-12 lg:grid-cols-[0.9fr_1.1fr]">
            <div class="space-y-6">
                <p class="text-sm font-semibold uppercase tracking-[0.28em] text-[var(--csl-gold)]">Contact Us</p>
                <h1 class="font-display text-5xl leading-tight text-white">Tell us what you want people to learn, and we’ll help shape the path.</h1>
                <p class="text-lg leading-8 text-white/72">{content_pack["contact_intro"]}</p>
            </div>
            <div class="rounded-[2rem] border border-white/10 bg-white/6 p-8 backdrop-blur">
                <form class="grid gap-4">
                    <div class="grid gap-4 sm:grid-cols-2">
                        <label class="grid gap-2 text-sm text-white/72">
                            Name
                            <input type="text" class="rounded-2xl border border-white/12 bg-white/8 px-4 py-3 text-white outline-none transition focus:border-[var(--csl-gold)]" placeholder="Your name">
                        </label>
                        <label class="grid gap-2 text-sm text-white/72">
                            Email
                            <input type="email" class="rounded-2xl border border-white/12 bg-white/8 px-4 py-3 text-white outline-none transition focus:border-[var(--csl-gold)]" placeholder="you@example.com">
                        </label>
                    </div>
                    <label class="grid gap-2 text-sm text-white/72">
                        Organisation
                        <input type="text" class="rounded-2xl border border-white/12 bg-white/8 px-4 py-3 text-white outline-none transition focus:border-[var(--csl-gold)]" placeholder="Organisation or team">
                    </label>
                    <label class="grid gap-2 text-sm text-white/72">
                        Project brief
                        <textarea rows="5" class="rounded-3xl border border-white/12 bg-white/8 px-4 py-3 text-white outline-none transition focus:border-[var(--csl-gold)]" placeholder="Tell us what you want to build."></textarea>
                    </label>
                    <button type="button" class="inline-flex justify-center rounded-full bg-[var(--csl-gold)] px-6 py-3.5 text-sm font-semibold text-[var(--csl-ink)] transition hover:translate-y-[-1px] hover:bg-[var(--csl-gold-soft)]">
                        Send Inquiry
                    </button>
                </form>
            </div>
        </div>
    </section>
@endsection
"""

    css_content = """@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
@source '../../storage/framework/views/*.php';

@theme {
    --font-sans: 'Instrument Sans', ui-sans-serif, system-ui, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
    --font-display: 'Instrument Sans', ui-sans-serif, system-ui, sans-serif;
    --csl-ink: #081e28;
    --csl-paper: #f3f4ee;
    --csl-teal: #12646b;
    --csl-gold: #f3ad55;
    --csl-gold-soft: #f6c47a;
}

@layer base {
    html {
        scroll-behavior: smooth;
    }

    body {
        font-family: var(--font-sans);
    }
}

@layer utilities {
    .font-display {
        font-family: var(--font-display);
        letter-spacing: -0.04em;
    }
}
"""

    _write_text(project_dir / "routes" / "web.php", routes_content)
    _write_text(project_dir / "resources" / "views" / "layouts" / "app.blade.php", layout_content)
    _write_text(project_dir / "resources" / "views" / "pages" / "home.blade.php", home_content)
    _write_text(project_dir / "resources" / "views" / "pages" / "about.blade.php", about_content)
    _write_text(project_dir / "resources" / "views" / "pages" / "media.blade.php", media_content)
    _write_text(project_dir / "resources" / "views" / "pages" / "blogs.blade.php", blogs_content)
    _write_text(project_dir / "resources" / "views" / "pages" / "contact.blade.php", contact_content)
    _write_text(project_dir / "resources" / "css" / "app.css", css_content)

    commands_run: list[str] = []
    build_output = "Build skipped because no frontend build step was detected."
    if (project_dir / "package.json").exists():
        ok, build_output = _run(["npm", "run", "build"], cwd=project_dir, timeout=1800)
        commands_run.append("npm run build")
        if not ok:
            return f"LARAVEL WEBSITE BUILD PARTIALLY COMPLETE\nProject: {project_dir}\n\n{build_output}"

    set_current_project(str(project_dir))
    return "\n".join([
        "LARAVEL WEBSITE BUILD COMPLETE",
        f"Project: {project_dir}",
        f"Company: {company_name}",
        "Pages created:",
        *[f"- {page}" for page in pages],
        "",
        "Commands executed:",
        *([f"- {command}" for command in commands_run] or ["- No additional commands were required."]),
        "",
        build_output,
    ])


def build_marketing_footer(target_dir: str | None = None, company_name: str = "Center for Systematic Learning") -> str:
    result = build_laravel_marketing_site(
        target_dir=target_dir,
        company_name=company_name,
        page_names=["home", "about", "media", "blogs", "contact-us"],
    )
    return result.replace("LARAVEL WEBSITE BUILD COMPLETE", "LARAVEL FOOTER UPGRADE COMPLETE", 1)


def complete_laravel_content_platform(
    target_dir: str | None = None,
    company_name: str = "Center for Systematic Learning",
) -> str:
    project_dir, error = _project_dir_from_hint(target_dir)
    if error:
        return error

    required_markers = [
        project_dir / "app" / "Http" / "Controllers" / "Admin" / "DashboardController.php",
        project_dir / "app" / "Models" / "BlogPost.php",
        project_dir / "database" / "seeders" / "DatabaseSeeder.php",
        project_dir / "resources" / "views" / "admin" / "dashboard.blade.php",
        project_dir / "resources" / "views" / "pages" / "blogs" / "index.blade.php",
    ]

    missing = [str(marker.relative_to(project_dir)) for marker in required_markers if not marker.exists()]
    if missing:
        return "LARAVEL CONTENT PLATFORM INCOMPLETE\nMissing files:\n- " + "\n- ".join(missing)

    commands_run: list[str] = []

    if (project_dir / "artisan").exists():
        ok, output = _run(["php", "artisan", "migrate", "--force"], cwd=project_dir, timeout=1800)
        commands_run.append("php artisan migrate --force")
        if not ok:
            return f"LARAVEL CONTENT PLATFORM PARTIALLY COMPLETE\nProject: {project_dir}\n\n{output}"

        ok, seed_output = _run(["php", "artisan", "db:seed", "--force"], cwd=project_dir, timeout=1800)
        commands_run.append("php artisan db:seed --force")
        if not ok:
            return f"LARAVEL CONTENT PLATFORM PARTIALLY COMPLETE\nProject: {project_dir}\n\n{seed_output}"

    build_output = "Build skipped because no frontend build step was detected."
    if (project_dir / "package.json").exists():
        ok, build_output = _run(["npm", "run", "build"], cwd=project_dir, timeout=1800)
        commands_run.append("npm run build")
        if not ok:
            return f"LARAVEL CONTENT PLATFORM PARTIALLY COMPLETE\nProject: {project_dir}\n\n{build_output}"

    set_current_project(str(project_dir))
    return "\n".join([
        "LARAVEL CONTENT PLATFORM COMPLETE",
        f"Project: {project_dir}",
        f"Company: {company_name}",
        "",
        "Included features:",
        "- Public marketing site pages",
        "- Admin login flow",
        "- Sidebar-style admin dashboard",
        "- Dynamic blog listing and detail pages",
        "- Five seeded sample blog posts",
        "- Seeded admin account: janonemersion@hotmail.com",
        "",
        "Commands executed:",
        *[f"- {command}" for command in commands_run],
        "",
        build_output,
    ])


def infer_developer_setup_action(user_input: str, chat_context: str | None = None) -> dict:
    text = _normalize(user_input).lower()
    context = _normalize(chat_context or "").lower()
    combined = f"{text}\n{context}"
    current_project = get_current_project_path()

    laravel_match = re.search(
        r"(?:install|create|setup|set up|make).{0,40}\blaravel\b",
        combined,
        flags=re.I | re.S,
    )
    tailwind_match = re.search(
        r"(?:install|setup|set up|configure|add).{0,40}\btailwind\b",
        combined,
        flags=re.I | re.S,
    )
    website_build_match = re.search(
        r"(?:build|create|make|design).{0,40}\b(?:website|site|web app|pages?)\b",
        combined,
        flags=re.I | re.S,
    )
    footer_build_match = re.search(
        r"(?:build|create|make|implement|add|upgrade).{0,24}\bfooter\b",
        combined,
        flags=re.I | re.S,
    )
    full_platform_match = re.search(
        r"\b(auth pages?|admin login|dashboard|dynamic blog|sample blogs?|seed(?:er|ed)? admin)\b",
        combined,
        flags=re.I | re.S,
    )
    status_match = re.search(
        r"(?:did you create|did you build|is there|check)\s+(?:the\s+)?(home|about|media|blog|blogs|contact(?:\s+us)?|footer)",
        combined,
        flags=re.I | re.S,
    )
    page_bundle_match = re.search(
        r"\bhome\b.*\babout\b.*\bmedia\b.*\bblogs?\b.*\bcontact(?:\s+us)?\b",
        combined,
        flags=re.I | re.S,
    )
    dependency_match = re.search(
        r"(?:install|add|require)\s+([@a-z0-9_.-]+/[a-z0-9_.-]+|@[a-z0-9_.-]+/[a-z0-9_.-]+|[a-z0-9_.-]+)",
        text,
        flags=re.I,
    )
    automation_match = re.search(
        r"\b(install dependencies|install deps|setup dependencies|set up dependencies|restore dependencies|run tests?|build(?: the)? project|compile(?: the)? project|migrate(?: the)? database|run migrations?)\b",
        combined,
        flags=re.I | re.S,
    )
    explicit_path_match = re.search(
        r"(/var/www/[a-zA-Z0-9._-]+|~/[a-zA-Z0-9_./-]+)",
        combined,
    )
    base_www_match = re.search(r"/var/www/?", combined)
    folder_name_match = re.search(
        r"folder named\s+([a-zA-Z0-9._-]+)|named\s+([a-zA-Z0-9._-]+)\s+and install laravel",
        combined,
        flags=re.I,
    )

    company_match = re.search(
        r'company name\s+"([^"]+)"|company name\s+\'([^\']+)\'',
        combined,
        flags=re.I,
    )
    company_name = None
    if company_match:
        company_name = next((group for group in company_match.groups() if group), None)

    target_dir = explicit_path_match.group(1) if explicit_path_match else None

    if not target_dir and base_www_match and folder_name_match:
        folder_name = next((group for group in folder_name_match.groups() if group), None)
        if folder_name:
            target_dir = f"/var/www/{folder_name}"

    if (full_platform_match or (laravel_match and (website_build_match or page_bundle_match))) and (current_project or target_dir):
        return {
            "action": "complete_laravel_platform",
            "target_dir": target_dir or (str(current_project) if current_project else None),
            "company_name": company_name or "Center for Systematic Learning",
        }

    if laravel_match and target_dir:
        return {
            "action": "install_laravel",
            "target_dir": target_dir,
            "company_name": company_name,
        }

    if tailwind_match:
        if target_dir:
            return {
                "action": "install_tailwind",
                "target_dir": target_dir,
            }
        if "same project" in combined or "current project" in combined or current_project:
            return {
                "action": "install_tailwind",
                "target_dir": str(current_project) if current_project else None,
            }

    if footer_build_match and (current_project or target_dir):
        return {
            "action": "build_footer",
            "target_dir": target_dir or (str(current_project) if current_project else None),
            "company_name": company_name or "Center for Systematic Learning",
        }

    if status_match and (current_project or target_dir):
        return {
            "action": "check_page_status",
            "target_dir": target_dir or (str(current_project) if current_project else None),
            "page_name": status_match.group(1),
        }

    if (website_build_match or page_bundle_match) and (current_project or target_dir):
        return {
            "action": "build_laravel_website",
            "target_dir": target_dir or (str(current_project) if current_project else None),
            "company_name": company_name or "Center for Systematic Learning",
            "pages": ["home", "about", "media", "blogs", "contact-us"],
        }

    if automation_match and (current_project or target_dir):
        return {
            "action": "project_automation",
            "target_dir": target_dir or (str(current_project) if current_project else None),
        }

    if dependency_match:
        package_name = dependency_match.group(1).strip()
        if package_name not in {"laravel", "tailwind"} and (current_project or target_dir):
            return {
                "action": "install_dependency",
                "target_dir": target_dir or (str(current_project) if current_project else None),
                "package_name": package_name,
            }

    return {"action": "unknown"}
