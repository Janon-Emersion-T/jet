import re
import json
import time
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from core.vector_memory.vector_store import add_vector_memory


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
JS_SOURCE_FILE = DATA_DIR / "javascript_knowledge_sources.json"
JS_MANIFEST_FILE = DATA_DIR / "javascript_knowledge_manifest.json"
LEARNING_LOG_FILE = STORAGE_DIR / "programming_learning_log.jsonl"

DEFAULT_HEADERS = {
    "User-Agent": "JARVIS-JavaScript-Knowledge-Engine/1.0 (+local private assistant)"
}

JS_CORE_CONCEPTS = {
    "variable", "variables", "let", "const", "var",
    "function", "functions", "arrow function", "scope", "closure",
    "object", "array", "map", "set", "class", "prototype",
    "promise", "promises", "async", "await", "event loop",
    "module", "modules", "import", "export", "dom", "event",
    "fetch", "api", "json", "error handling", "try catch",
    "typescript", "node", "react", "next", "vue"
}

BROWSER_GLOBALS = {
    "window", "document", "navigator", "location", "history",
    "localStorage", "sessionStorage", "fetch", "console"
}

DANGEROUS_PATTERNS = [
    r"\beval\s*\(",
    r"\bnew\s+Function\s*\(",
    r"\bdocument\.write\s*\(",
    r"\binnerHTML\s*=",
    r"\bouterHTML\s*=",
    r"\blocalStorage\.setItem\s*\([^)]*password",
    r"\bsessionStorage\.setItem\s*\([^)]*password",
    r"\bsetTimeout\s*\(\s*['\"]",
    r"\bsetInterval\s*\(\s*['\"]",
]


def _now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(path: Path, default):
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _save_json(path: Path, data) -> None:
    _ensure_data_dir()
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _append_learning_log(entry: dict) -> None:
    _ensure_data_dir()
    with LEARNING_LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"Edit on GitHub|Report a problem with this content", "", text, flags=re.I)
    return text.strip()


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def _chunk_text(text: str, max_chars: int = 1800) -> List[str]:
    paragraphs = re.split(r"(?<=[.!?])\s+", text)
    chunks = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) + 1 > max_chars:
            if current.strip():
                chunks.append(current.strip())
            current = paragraph
        else:
            current = f"{current} {paragraph}".strip()

    if current.strip():
        chunks.append(current.strip())

    return chunks


def _extract_page_text(html: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "canvas", "iframe"]):
        tag.decompose()

    title = soup.title.get_text(" ", strip=True) if soup.title else "Untitled JavaScript Source"

    headings = []
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)
        if text and len(text) < 180:
            headings.append(text)

    body_text = _clean_text(soup.get_text(" "))
    heading_text = " | ".join(headings[:50])

    return {
        "title": title,
        "headings": heading_text,
        "text": body_text
    }


def _fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"{url} returned HTTP {response.status_code}")

    return response.text


def javascript_knowledge_status() -> str:
    manifest = _load_json(JS_MANIFEST_FILE, {"sources": {}})
    sources = manifest.get("sources", {})

    if not sources:
        return (
            "JAVASCRIPT KNOWLEDGE STATUS\n"
            "No JavaScript knowledge has been learned yet.\n"
            "Run: update javascript knowledge"
        )

    lines = ["JAVASCRIPT KNOWLEDGE STATUS"]
    for url, item in sources.items():
        lines.append("")
        lines.append(f"Source: {item.get('name', 'Unknown')}")
        lines.append(f"URL: {url}")
        lines.append(f"Last learned: {item.get('last_learned_at', '-')}")
        lines.append(f"Chunks saved: {item.get('chunks_saved', 0)}")
        lines.append(f"Hash: {item.get('hash', '-')[:16]}...")

    return "\n".join(lines)


def update_javascript_knowledge(force: bool = False) -> str:
    _ensure_data_dir()
    started_at = _now_iso()

    source_data = _load_json(JS_SOURCE_FILE, None)
    if not source_data:
        return (
            "JAVASCRIPT KNOWLEDGE UPDATE FAILED\n"
            "Missing data/javascript_knowledge_sources.json"
        )

    manifest = _load_json(JS_MANIFEST_FILE, {"updated_at": None, "sources": {}})
    manifest_sources = manifest.setdefault("sources", {})

    total_chunks = 0
    updated_sources = 0
    skipped_sources = 0
    errors = []

    for source in source_data.get("sources", []):
        name = source.get("name", "Unnamed source")
        url = source.get("url")
        source_type = source.get("type", "reference")
        priority = int(source.get("priority", 5))

        if not url:
            continue

        try:
            html = _fetch_url(url)
            extracted = _extract_page_text(html)
            text = extracted["text"]
            digest = _content_hash(text)

            old_digest = manifest_sources.get(url, {}).get("hash")

            if old_digest == digest and not force:
                skipped_sources += 1
                continue

            chunks = _chunk_text(text)

            for index, chunk in enumerate(chunks):
                memory_text = (
                    "JAVASCRIPT KNOWLEDGE SOURCE\n"
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
                    tags=[
                        "javascript",
                        "js",
                        "ecmascript",
                        "web-development",
                        "frontend",
                        "browser",
                        "runtime",
                        "standards",
                        source_type
                    ],
                    source="javascript-knowledge-engine",
                    importance=priority
                )

                total_chunks += 1

            manifest_sources[url] = {
                "name": name,
                "type": source_type,
                "priority": priority,
                "hash": digest,
                "last_learned_at": _now_iso(),
                "chunks_saved": len(chunks),
                "title": extracted["title"]
            }

            updated_sources += 1
            time.sleep(1)

        except Exception as e:
            errors.append(f"{name}: {e}")

    manifest["updated_at"] = _now_iso()
    _save_json(JS_MANIFEST_FILE, manifest)
    _append_learning_log({
        "topic": "javascript",
        "trigger": "javascript-route",
        "force": force,
        "started_at": started_at,
        "completed_at": _now_iso(),
        "sources_updated": updated_sources,
        "sources_skipped": skipped_sources,
        "memory_chunks_saved": total_chunks,
        "errors": errors,
        "manifest_path": str(JS_MANIFEST_FILE),
    })

    lines = [
        "JAVASCRIPT KNOWLEDGE UPDATE COMPLETE",
        f"Sources updated: {updated_sources}",
        f"Sources skipped: {skipped_sources}",
        f"Memory chunks saved: {total_chunks}",
        f"Log: {LEARNING_LOG_FILE}",
        "",
        "JARVIS can now use updated JavaScript knowledge through vector memory."
    ]

    if errors:
        lines.append("")
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in errors[:10])

    return "\n".join(lines)


def generate_javascript_blueprint(project_request: str) -> str:
    request = project_request.strip()

    if not request:
        return "Tell me what JavaScript behavior, module, website interaction, or app logic you want."

    return f"""JAVASCRIPT PRACTICAL BLUEPRINT

Request:
{request}

Recommended implementation strategy:

1. Purpose first
- Define what JavaScript must do.
- Do not use JavaScript for structure that belongs to HTML.
- Do not use JavaScript for styling that belongs to CSS.
- Use JavaScript for behavior, state, data flow, validation, interactivity, browser APIs, and application logic.

2. Execution model
- Load scripts with type="module" where possible.
- Keep JavaScript modular.
- Avoid global variables.
- Initialize behavior after DOM readiness when needed.
- Use event delegation for dynamic elements.

3. DOM interaction
- Use querySelector/querySelectorAll carefully.
- Check elements exist before using them.
- Use textContent for text output.
- Avoid unsafe innerHTML unless content is fully trusted and sanitized.
- Keep selectors stable using data-* attributes.

4. State management
- Keep state in plain objects or arrays for vanilla JavaScript.
- Use predictable update functions.
- Keep DOM rendering separate from business logic.

5. Async/data handling
- Use fetch with async/await.
- Handle loading, success, empty, and error states.
- Validate API responses before rendering.
- Use AbortController when requests may be cancelled.

6. Error handling
- Use try/catch for async operations.
- Fail gracefully in the UI.
- Log developer details without exposing sensitive data to users.

7. Security
- Never eval user input.
- Never store passwords or secrets in localStorage.
- Validate and sanitize user-generated content.
- Use CSRF protection in backend-connected forms.
- Treat browser input as hostile.

8. Performance
- Avoid unnecessary DOM reflows.
- Debounce heavy input events.
- Lazy-load non-critical behavior.
- Split code by feature where the project grows.

9. Framework translation
This logic can be converted into:
- Vanilla JavaScript modules
- Laravel Blade + Vite JavaScript
- React components/hooks
- Next.js client components/server actions
- Vue composables/components
- Alpine.js directives
- Node.js backend modules

10. JARVIS execution rule
When building websites, JARVIS should use:
- HTML for structure
- CSS/Tailwind for presentation
- JavaScript for behavior
- Frameworks only when the requested project needs component state, routing, SSR, API integration, or application scale
"""


def create_javascript_starter_module(title: str = "JARVIS JavaScript Module") -> str:
    safe_title = title.strip() or "JARVIS JavaScript Module"

    return f"""// {safe_title}
// Production-minded vanilla JavaScript module.
// Use with: <script type="module" src="/path/to/app.js"></script>

const appState = {{
  initialized: false,
  items: [],
}};

const selectors = {{
  root: "[data-js-app]",
  message: "[data-js-message]",
  actionButton: "[data-js-action]",
}};

function qs(selector, parent = document) {{
  return parent.querySelector(selector);
}}

function qsa(selector, parent = document) {{
  return Array.from(parent.querySelectorAll(selector));
}}

function setText(element, value) {{
  if (!element) return;
  element.textContent = String(value ?? "");
}}

function setLoading(element, isLoading) {{
  if (!element) return;
  element.toggleAttribute("aria-busy", Boolean(isLoading));
}}

async function fetchJson(url, options = {{}}) {{
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), options.timeout ?? 15000);

  try {{
    const response = await fetch(url, {{
      ...options,
      signal: controller.signal,
      headers: {{
        "Accept": "application/json",
        ...(options.headers || {{}})
      }}
    }});

    if (!response.ok) {{
      throw new Error(`Request failed: ${{response.status}} ${{response.statusText}}`);
    }}

    return await response.json();
  }} finally {{
    window.clearTimeout(timeout);
  }}
}}

function bindEvents(root) {{
  const button = qs(selectors.actionButton, root);

  if (button) {{
    button.addEventListener("click", () => {{
      const message = qs(selectors.message, root);
      setText(message, "JavaScript behavior is working.");
    }});
  }}
}}

function initApp() {{
  const root = qs(selectors.root);

  if (!root) {{
    return;
  }}

  if (appState.initialized) {{
    return;
  }}

  bindEvents(root);
  appState.initialized = true;
}}

if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", initApp);
}} else {{
  initApp();
}}
"""


def audit_javascript_file(path: str) -> str:
    target = (BASE_DIR / path).resolve()

    try:
        target.relative_to(BASE_DIR)
    except ValueError:
        return "JAVASCRIPT AUDIT BLOCKED\nFile path is outside the project directory."

    if not target.exists():
        return f"JAVASCRIPT AUDIT FAILED\nFile not found: {path}"

    if target.suffix.lower() not in {".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"}:
        return (
            "JAVASCRIPT AUDIT WARNING\n"
            f"The file does not look like a JavaScript/TypeScript file: {path}"
        )

    content = target.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    issues = []
    strengths = []

    if "use strict" in content or target.suffix.lower() in {".mjs", ".jsx", ".ts", ".tsx"} or "import " in content:
        strengths.append("Uses module/strict-style execution signals.")
    else:
        issues.append("Consider using ES modules with <script type=\"module\"> or modern bundling.")

    if re.search(r"\bvar\s+", content):
        issues.append("Uses var. Prefer const by default and let when reassignment is required.")

    if re.search(r"\bconsole\.log\s*\(", content):
        issues.append("Contains console.log. Keep only intentional logs or replace with structured error handling.")

    if re.search(r"\bfetch\s*\(", content) and "try" not in content:
        issues.append("Uses fetch but no clear try/catch error handling was detected.")

    if re.search(r"\baddEventListener\s*\(", content):
        strengths.append("Uses addEventListener for behavior binding.")

    if re.search(r"\bquerySelector\s*\(", content):
        strengths.append("Uses modern DOM selection.")

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, content, flags=re.I):
            issues.append(f"Potentially unsafe pattern detected: {pattern}")

    if "innerHTML" in content and "sanitize" not in content.lower():
        issues.append("innerHTML is used without obvious sanitization. Use textContent unless trusted HTML is required.")

    if re.search(r"\blocalStorage\b", content) and re.search(r"token|password|secret", content, flags=re.I):
        issues.append("Possible sensitive data storage in localStorage. Avoid storing secrets in browser storage.")

    if len(lines) > 350:
        issues.append("File is getting large. Consider splitting by feature/module.")

    if not issues:
        issues.append("No major JavaScript issues detected from static inspection.")

    strength_lines = (
        [f"- {item}" for item in strengths]
        if strengths
        else ["- Basic file structure is readable."]
    )

    issue_lines = [f"- {item}" for item in issues]

    return "\n".join([
        "JAVASCRIPT FILE AUDIT",
        f"File: {path}",
        f"Lines: {len(lines)}",
        "",
        "Strengths:",
        *strength_lines,
        "",
        "Recommendations:",
        *issue_lines,
        "",
        "Next step:",
        "For deeper review, ask JARVIS to inspect the feature goal, related HTML, related CSS, and runtime errors together."
    ])


def explain_javascript_concept(concept: str) -> str:
    clean = concept.strip()

    if not clean:
        return "Tell me which JavaScript concept you want explained."

    return f"""JAVASCRIPT CONCEPT EXPLANATION

Concept:
{clean}

Practical explanation method:
1. Define what it does.
2. Explain when to use it.
3. Show a small working example.
4. Explain common mistakes.
5. Explain how it changes in browser JavaScript, Node.js, and frameworks.

JARVIS rule:
For current/future accuracy, use the JavaScript vector knowledge learned from official ECMAScript, MDN, runtime, and framework documentation before giving final implementation guidance.
"""


def generate_javascript_framework_translation(request: str) -> str:
    clean = request.strip()

    if not clean:
        return "Tell me what JavaScript logic you want translated and to which framework."

    return f"""JAVASCRIPT FRAMEWORK TRANSLATION PLAN

Request:
{clean}

Translation approach:
1. Identify the original JavaScript behavior.
2. Separate pure logic from DOM manipulation.
3. Move state into the framework's state system.
4. Move UI rendering into components/templates.
5. Keep side effects in the correct lifecycle layer.
6. Preserve accessibility and progressive enhancement.
7. Keep API calls isolated in services/composables/hooks.
8. Keep framework-specific code thin and maintainable.

Framework mapping:
- React: component state, hooks, effects, controlled inputs.
- Next.js: server/client component boundary, route handlers, server actions where suitable.
- Vue: refs/reactive state, computed values, watchers, composables.
- Laravel Blade: Vite modules, data-* selectors, progressive enhancement.
- Alpine.js: small declarative interactions only.
- Node.js: backend modules, services, async handlers, validation.

JARVIS rule:
Do not blindly convert syntax. Convert responsibility, lifecycle, state, and data flow correctly.
"""


def infer_javascript_action(user_input: str) -> Dict:
    text = " ".join((user_input or "").lower().strip().split())

    force = any(word in text for word in ["force", "relearn", "refresh all", "from scratch"])

    if any(phrase in text for phrase in [
        "teach yourself javascript",
        "teach yourself js",
        "learn javascript",
        "learn js",
        "update javascript knowledge",
        "update js knowledge",
        "refresh javascript knowledge",
        "refresh js knowledge",
        "latest javascript",
        "latest js",
        "official javascript",
        "official js",
        "ecmascript latest",
    ]):
        return {"action": "update", "force": force}

    if any(phrase in text for phrase in [
        "javascript knowledge status",
        "js knowledge status",
        "check javascript knowledge",
        "check js knowledge",
        "what javascript knowledge",
        "what js knowledge",
        "already know javascript",
        "already know js",
    ]):
        return {"action": "status"}

    if any(phrase in text for phrase in [
        "audit javascript",
        "audit js",
        "check javascript file",
        "check js file",
        "production ready js",
        "production ready javascript",
        "review javascript file",
        "review js file",
    ]):
        path = _extract_probable_file_path(user_input)
        return {"action": "audit", "path": path}

    if any(phrase in text for phrase in [
        "explain javascript",
        "explain js",
        "what is async",
        "what is await",
        "what are promises",
        "what is promise",
        "what is closure",
        "what is event loop",
        "what is dom",
    ]):
        concept = _extract_concept(user_input)
        return {"action": "explain", "concept": concept}

    if any(phrase in text for phrase in [
        "create javascript starter",
        "create js starter",
        "javascript starter",
        "js starter",
        "starter module",
        "vanilla js foundation",
    ]):
        return {"action": "starter", "title": _extract_title(user_input)}

    if any(phrase in text for phrase in [
        "javascript blueprint",
        "js blueprint",
        "javascript foundation",
        "js foundation",
        "build interactive",
        "website behavior",
        "frontend behavior",
    ]):
        return {"action": "blueprint", "request": user_input}

    if any(phrase in text for phrase in [
        "translate javascript",
        "translate js",
        "convert javascript",
        "convert js",
        "to react",
        "to next",
        "to vue",
        "to blade",
        "to alpine",
    ]):
        return {"action": "translate", "request": user_input}

    return {"action": "unknown"}


def _extract_probable_file_path(value: str) -> str:
    patterns = [
        r"([\w./\\-]+\.(?:js|mjs|cjs|jsx|ts|tsx))",
    ]

    for pattern in patterns:
        match = re.search(pattern, value, flags=re.I)
        if match:
            return match.group(1).strip()

    return ""


def _extract_concept(value: str) -> str:
    text = value.strip()

    prefixes = [
        "explain javascript",
        "explain js",
        "what is",
        "what are",
        "tell me about",
    ]

    lowered = text.lower()
    for prefix in prefixes:
        if lowered.startswith(prefix):
            return text[len(prefix):].strip(" ?.")

    for concept in JS_CORE_CONCEPTS:
        if concept in lowered:
            return concept

    return text


def _extract_title(value: str) -> str:
    text = value.strip()

    for phrase in [
        "create javascript starter",
        "create js starter",
        "javascript starter",
        "js starter",
    ]:
        if text.lower().startswith(phrase):
            return text[len(phrase):].strip()

    return "Professional JavaScript Module"
