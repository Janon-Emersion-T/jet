import os
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
CSS_SOURCE_FILE = DATA_DIR / "css_knowledge_sources.json"
CSS_MANIFEST_FILE = DATA_DIR / "css_knowledge_manifest.json"
LEARNING_LOG_FILE = STORAGE_DIR / "programming_learning_log.jsonl"

DEFAULT_HEADERS = {
    "User-Agent": "JARVIS-CSS-Knowledge-Engine/1.0 (+local private assistant)"
}

CSS_CORE_CONCEPTS = {
    "cascade",
    "specificity",
    "inheritance",
    "box model",
    "normal flow",
    "formatting context",
    "stacking context",
    "containing block",
    "computed value",
    "used value",
    "custom properties",
    "responsive design",
    "progressive enhancement",
}

CSS_LAYOUT_SYSTEMS = {
    "display",
    "position",
    "float",
    "flex",
    "grid",
    "multicol",
    "container queries",
    "media queries",
}

CSS_MODERN_FEATURES = {
    "custom-properties": "CSS variables for design tokens and theme systems.",
    "grid": "Two-dimensional layout system for production page structure.",
    "flexbox": "One-dimensional layout system for alignment and distribution.",
    "container-queries": "Component-level responsive styling based on container size.",
    "cascade-layers": "Layered cascade control using @layer.",
    "nesting": "Native CSS nesting for cleaner grouped selectors.",
    "subgrid": "Grid alignment inherited from a parent grid.",
    "color-mix": "Native color interpolation.",
    "logical-properties": "Writing-mode friendly spacing and sizing.",
    "view-transitions": "Animated page/state transitions where supported.",
}

CSS_RISKY_PATTERNS = [
    (r"!important", "Avoid unnecessary !important. It creates cascade debt."),
    (r"position\s*:\s*absolute", "Absolute positioning can break responsive layouts if overused."),
    (r"width\s*:\s*\d+px", "Fixed pixel widths can hurt responsiveness. Prefer max-width, %, rem, clamp(), or grid/flex."),
    (r"height\s*:\s*\d+px", "Fixed heights can cause overflow. Prefer min-height or content-driven layout."),
    (r"font-size\s*:\s*\d+px", "Pixel font sizes are less flexible. Prefer rem or clamp()."),
    (r"#[0-9a-fA-F]{3,8}", "Hardcoded colors are okay in small CSS, but design systems should use custom properties."),
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

    title = soup.title.get_text(" ", strip=True) if soup.title else "Untitled CSS Source"

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
        "text": body_text,
    }


def _fetch_url(url: str, timeout: int = 30) -> Optional[str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    if response.status_code != 200:
        raise RuntimeError(f"{url} returned HTTP {response.status_code}")

    return response.text


def css_knowledge_status() -> str:
    manifest = _load_json(CSS_MANIFEST_FILE, {"sources": {}})
    sources = manifest.get("sources", {})

    if not sources:
        return (
            "CSS KNOWLEDGE STATUS\n"
            "No CSS knowledge has been learned yet.\n"
            "Run: update css knowledge"
        )

    lines = ["CSS KNOWLEDGE STATUS"]
    lines.append(f"Manifest updated: {manifest.get('updated_at', '-')}")

    for url, item in sources.items():
        lines.append("")
        lines.append(f"Source: {item.get('name', 'Unknown')}")
        lines.append(f"URL: {url}")
        lines.append(f"Type: {item.get('type', '-')}")
        lines.append(f"Last learned: {item.get('last_learned_at', '-')}")
        lines.append(f"Chunks saved: {item.get('chunks_saved', 0)}")
        lines.append(f"Hash: {item.get('hash', '-')[:16]}...")

    return "\n".join(lines)


def update_css_knowledge(force: bool = False) -> str:
    _ensure_data_dir()
    started_at = _now_iso()

    source_data = _load_json(CSS_SOURCE_FILE, None)
    if not source_data:
        return (
            "CSS KNOWLEDGE UPDATE FAILED\n"
            "Missing data/css_knowledge_sources.json"
        )

    manifest = _load_json(CSS_MANIFEST_FILE, {"updated_at": None, "sources": {}})
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
                    "CSS KNOWLEDGE SOURCE\n"
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
                        "css",
                        "web-development",
                        "frontend",
                        "standards",
                        "layout",
                        "responsive-design",
                        source_type,
                    ],
                    source="css-knowledge-engine",
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

        except Exception as e:
            errors.append(f"{name}: {e}")

    manifest["updated_at"] = _now_iso()
    manifest["topic"] = "css"
    manifest["version"] = source_data.get("version", "1.0.0")
    _save_json(CSS_MANIFEST_FILE, manifest)
    _append_learning_log({
        "topic": "css",
        "trigger": "css-route",
        "force": force,
        "started_at": started_at,
        "completed_at": _now_iso(),
        "sources_updated": updated_sources,
        "sources_skipped": skipped_sources,
        "memory_chunks_saved": total_chunks,
        "errors": errors,
        "manifest_path": str(CSS_MANIFEST_FILE),
    })

    lines = [
        "CSS KNOWLEDGE UPDATE COMPLETE",
        f"Sources updated: {updated_sources}",
        f"Sources skipped: {skipped_sources}",
        f"Memory chunks saved: {total_chunks}",
        f"Log: {LEARNING_LOG_FILE}",
        "",
        "JARVIS can now use updated CSS knowledge through vector memory.",
    ]

    if errors:
        lines.append("")
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in errors[:10])

    return "\n".join(lines)


def generate_css_blueprint(project_request: str) -> str:
    request = project_request.strip()

    if not request:
        return "Tell me what type of interface, website, component, or framework styling you want."

    return f"""CSS PRACTICAL BLUEPRINT

Request:
{request}

Recommended professional styling architecture:

1. CSS foundation
- Start with a small reset or normalize strategy.
- Use box-sizing: border-box.
- Define design tokens in :root using custom properties.
- Use rem, %, clamp(), min(), max(), and container-friendly units instead of hardcoded pixels everywhere.
- Keep global CSS predictable.

2. Layout strategy
- Use normal document flow first.
- Use Flexbox for one-dimensional alignment.
- Use Grid for two-dimensional page and card layouts.
- Use container queries for reusable responsive components.
- Use media queries for page-level breakpoints.

3. Cascade strategy
- Avoid random selector wars.
- Keep specificity low.
- Prefer classes over deeply nested selectors.
- Use @layer when the project has base, components, utilities, and overrides.
- Avoid !important unless it is a deliberate escape hatch.

4. Responsive strategy
- Mobile-first by default.
- Use fluid typography with clamp().
- Use max-width containers.
- Use flexible grids with repeat(), minmax(), auto-fit, and auto-fill.
- Test narrow, medium, large, and ultra-wide screens.

5. Accessibility and UX
- Preserve visible focus states.
- Respect prefers-reduced-motion.
- Ensure enough color contrast.
- Avoid layout shifts.
- Keep clickable elements comfortable on mobile.

6. Performance
- Keep CSS lean.
- Avoid unused CSS.
- Avoid expensive paint-heavy effects.
- Prefer transform and opacity for animations.
- Use critical CSS carefully when needed.

7. Framework translation
This CSS logic can be translated into:
- Plain CSS
- Laravel Blade CSS files
- React / Next.js CSS modules
- Vue scoped CSS
- Tailwind utility classes
- Bootstrap overrides
- WordPress themes

8. JARVIS execution rule
When generating UI, JARVIS should first build semantic HTML, then design CSS tokens, then layout, then responsive rules, then interaction states, then framework-specific translation.
"""


def create_css_starter_stylesheet(project_name: str = "JARVIS Generated Website") -> str:
    safe_name = project_name.strip() or "JARVIS Generated Website"

    return f"""/*
  {safe_name}
  Professional CSS foundation generated by JARVIS.
  Goal: responsive, accessible, maintainable, framework-portable styling.
*/

@layer reset, base, layout, components, utilities;

/* 1. Reset */
@layer reset {{
  *,
  *::before,
  *::after {{
    box-sizing: border-box;
  }}

  html {{
    -webkit-text-size-adjust: 100%;
    text-size-adjust: 100%;
  }}

  body,
  h1,
  h2,
  h3,
  h4,
  p,
  figure,
  blockquote,
  dl,
  dd {{
    margin: 0;
  }}

  ul[role="list"],
  ol[role="list"] {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}

  img,
  picture,
  video,
  canvas,
  svg {{
    display: block;
    max-width: 100%;
  }}

  input,
  button,
  textarea,
  select {{
    font: inherit;
  }}
}}

/* 2. Design tokens */
@layer base {{
  :root {{
    color-scheme: light;

    --font-sans: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

    --color-bg: #ffffff;
    --color-surface: #f8fafc;
    --color-text: #0f172a;
    --color-muted: #475569;
    --color-border: #e2e8f0;
    --color-brand: #2563eb;
    --color-brand-dark: #1d4ed8;

    --radius-sm: 0.5rem;
    --radius-md: 0.875rem;
    --radius-lg: 1.25rem;

    --shadow-sm: 0 1px 2px rgb(15 23 42 / 0.08);
    --shadow-md: 0 16px 35px rgb(15 23 42 / 0.12);

    --container: 72rem;

    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-12: 3rem;
    --space-16: 4rem;
  }}

  body {{
    min-height: 100vh;
    font-family: var(--font-sans);
    font-size: 1rem;
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-bg);
  }}

  a {{
    color: inherit;
    text-decoration-thickness: 0.08em;
    text-underline-offset: 0.18em;
  }}

  a:hover {{
    color: var(--color-brand);
  }}

  :focus-visible {{
    outline: 3px solid color-mix(in srgb, var(--color-brand), white 20%);
    outline-offset: 3px;
  }}

  h1,
  h2,
  h3 {{
    line-height: 1.1;
    text-wrap: balance;
  }}

  h1 {{
    font-size: clamp(2.5rem, 6vw, 5rem);
    letter-spacing: -0.05em;
  }}

  h2 {{
    font-size: clamp(2rem, 4vw, 3.25rem);
    letter-spacing: -0.04em;
  }}

  h3 {{
    font-size: clamp(1.25rem, 2vw, 1.5rem);
  }}

  p {{
    color: var(--color-muted);
  }}
}}

/* 3. Layout */
@layer layout {{
  .container {{
    width: min(100% - 2rem, var(--container));
    margin-inline: auto;
  }}

  .section {{
    padding-block: clamp(4rem, 8vw, 7rem);
  }}

  .stack {{
    display: grid;
    gap: var(--space-6);
  }}

  .cluster {{
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-4);
    align-items: center;
  }}

  .split {{
    display: grid;
    gap: var(--space-8);
    align-items: center;
  }}

  @media (width >= 768px) {{
    .split {{
      grid-template-columns: 1fr 1fr;
    }}
  }}

  .auto-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(16rem, 100%), 1fr));
    gap: var(--space-6);
  }}
}}

/* 4. Components */
@layer components {{
  .site-header {{
    position: sticky;
    top: 0;
    z-index: 10;
    border-bottom: 1px solid var(--color-border);
    background: color-mix(in srgb, var(--color-bg), transparent 8%);
    backdrop-filter: blur(12px);
  }}

  .site-header__inner {{
    min-height: 4.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--space-4);
  }}

  .brand {{
    font-weight: 800;
    letter-spacing: -0.04em;
    text-decoration: none;
  }}

  .nav {{
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-4);
    align-items: center;
  }}

  .button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-height: 2.75rem;
    padding: 0.75rem 1.1rem;
    border: 1px solid transparent;
    border-radius: var(--radius-md);
    background: var(--color-brand);
    color: #ffffff;
    font-weight: 700;
    text-decoration: none;
    box-shadow: var(--shadow-sm);
    transition: transform 160ms ease, background-color 160ms ease, box-shadow 160ms ease;
  }}

  .button:hover {{
    background: var(--color-brand-dark);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }}

  .button--secondary {{
    background: var(--color-surface);
    color: var(--color-text);
    border-color: var(--color-border);
  }}

  .button--secondary:hover {{
    background: #ffffff;
    color: var(--color-brand);
  }}

  .card {{
    display: grid;
    gap: var(--space-3);
    padding: var(--space-6);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    background: var(--color-surface);
    box-shadow: var(--shadow-sm);
  }}

  .hero {{
    padding-block: clamp(5rem, 10vw, 9rem);
  }}

  .hero__content {{
    max-width: 52rem;
  }}

  .eyebrow {{
    color: var(--color-brand);
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.8rem;
  }}
}}

/* 5. Utilities */
@layer utilities {{
  .text-center {{
    text-align: center;
  }}

  .visually-hidden {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    white-space: nowrap;
    border: 0;
  }}

  .flow > * + * {{
    margin-top: var(--flow-space, var(--space-4));
  }}
}}

/* 6. Component-level responsiveness */
@container (width >= 36rem) {{
  .card {{
    padding: var(--space-8);
  }}
}}

/* 7. Motion safety */
@media (prefers-reduced-motion: reduce) {{
  *,
  *::before,
  *::after {{
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }}
}}
"""


def audit_css_code(css: str) -> str:
    if not css or len(css.strip()) < 10:
        return "CSS AUDIT FAILED\nNo usable CSS was provided."

    issues = []
    warnings = []
    strengths = []

    normalized = css.lower()

    if "box-sizing" in normalized and "border-box" in normalized:
        strengths.append("Uses border-box sizing foundation.")
    else:
        warnings.append("Consider adding a global box-sizing: border-box reset.")

    if ":root" in normalized and "--" in css:
        strengths.append("Uses custom properties/design tokens.")
    else:
        warnings.append("No clear :root custom property design-token system found.")

    if "@media" in normalized:
        strengths.append("Includes media queries for responsive behavior.")
    else:
        warnings.append("No media queries detected. Ensure the layout is responsive.")

    if "@container" in normalized:
        strengths.append("Uses container queries for component-level responsiveness.")
    else:
        warnings.append("No container queries detected. This is fine for simple pages, but useful for reusable components.")

    if "display: grid" in normalized or "display:grid" in normalized:
        strengths.append("Uses CSS Grid.")
    else:
        warnings.append("No CSS Grid usage detected. Grid is recommended for two-dimensional layouts.")

    if "display: flex" in normalized or "display:flex" in normalized:
        strengths.append("Uses Flexbox.")
    else:
        warnings.append("No Flexbox usage detected. Flexbox is useful for alignment and one-dimensional layouts.")

    if ":focus-visible" in normalized:
        strengths.append("Defines visible keyboard focus states.")
    else:
        issues.append("Missing :focus-visible styling. Keyboard accessibility may suffer.")

    if "prefers-reduced-motion" in normalized:
        strengths.append("Respects reduced motion preference.")
    else:
        warnings.append("No prefers-reduced-motion handling found.")

    if "clamp(" in normalized:
        strengths.append("Uses fluid values with clamp().")
    else:
        warnings.append("No clamp() usage detected. Fluid typography/spacing may improve responsiveness.")

    selector_blocks = re.findall(r"([^{}]+)\{[^{}]*\}", css)
    deep_selectors = [
        selector.strip()
        for selector in selector_blocks
        if selector.strip().count(" ") >= 4 or selector.strip().count(">") >= 3
    ]

    if deep_selectors:
        warnings.append("Some selectors look deeply nested. Keep specificity low and maintainable.")

    for pattern, message in CSS_RISKY_PATTERNS:
        if re.search(pattern, css, flags=re.I):
            warnings.append(message)

    open_braces = css.count("{")
    close_braces = css.count("}")
    if open_braces != close_braces:
        issues.append(f"Brace mismatch detected: {open_braces} opening braces and {close_braces} closing braces.")

    lines = ["CSS AUDIT REPORT", ""]

    lines.append("Strengths:")
    if strengths:
        lines.extend(f"- {item}" for item in strengths)
    else:
        lines.append("- No major strengths detected yet.")

    lines.append("")
    lines.append("Issues:")
    if issues:
        lines.extend(f"- {item}" for item in issues)
    else:
        lines.append("- No critical issues detected.")

    lines.append("")
    lines.append("Warnings:")
    if warnings:
        lines.extend(f"- {item}" for item in warnings)
    else:
        lines.append("- No warnings detected.")

    lines.append("")
    lines.append("Recommendation:")
    if issues:
        lines.append("Fix the critical CSS issues before using this in production.")
    elif warnings:
        lines.append("CSS foundation is usable, but improve the warnings for professional delivery.")
    else:
        lines.append("CSS foundation looks strong for production-level work.")

    return "\n".join(lines)


def audit_css_file(path: str) -> str:
    target = Path(path).expanduser()

    if not target.exists():
        project_relative = BASE_DIR / path
        if project_relative.exists():
            target = project_relative
        else:
            return f"CSS AUDIT FAILED\nFile not found: {path}"

    if not target.is_file():
        return f"CSS AUDIT FAILED\nPath is not a file: {path}"

    if target.suffix.lower() not in {".css", ".scss", ".sass", ".less", ".vue", ".jsx", ".tsx", ".blade.php", ".html"}:
        return (
            "CSS AUDIT FAILED\n"
            "Unsupported file type for CSS audit. Use .css, .scss, .sass, .less, .vue, .jsx, .tsx, .blade.php, or .html."
        )

    try:
        css = target.read_text(encoding="utf-8", errors="ignore")
        report = audit_css_code(css)
        return f"File: {target}\n\n{report}"
    except Exception as e:
        return f"CSS AUDIT FAILED\n{e}"


def explain_css_concept(concept: str) -> str:
    key = concept.strip().lower().replace("_", "-")

    if not key:
        return "Please provide a CSS concept. Example: explain css cascade"

    concept_map = {
        "cascade": (
            "The cascade decides which CSS rule wins when multiple rules target the same element. "
            "It considers origin, importance, cascade layers, specificity, scope, and source order."
        ),
        "specificity": (
            "Specificity is the selector weight. IDs are heavier than classes, and classes are heavier than elements. "
            "Keep specificity low so the CSS remains maintainable."
        ),
        "box-model": (
            "The box model describes content, padding, border, and margin. "
            "Use box-sizing: border-box to make sizing predictable."
        ),
        "flexbox": (
            "Flexbox is best for one-dimensional layout: rows, columns, alignment, spacing, and distribution."
        ),
        "grid": (
            "CSS Grid is best for two-dimensional layout: rows and columns together."
        ),
        "container-queries": (
            "Container queries allow components to adapt based on their parent/container size, not only the viewport."
        ),
        "media-queries": (
            "Media queries apply CSS based on viewport/device conditions such as width, preference, or media type."
        ),
        "custom-properties": (
            "Custom properties, also called CSS variables, store reusable values such as colors, spacing, fonts, and design tokens."
        ),
        "cascade-layers": (
            "Cascade layers let you control style priority using @layer, commonly separating reset, base, components, utilities, and overrides."
        ),
        "nesting": (
            "CSS nesting allows selectors to be grouped inside parent selectors. Use it carefully to avoid specificity debt."
        ),
    }

    normalized_key = key.replace(" ", "-")
    explanation = concept_map.get(normalized_key)

    if not explanation:
        if normalized_key in CSS_MODERN_FEATURES:
            explanation = CSS_MODERN_FEATURES[normalized_key]
        else:
            explanation = (
                "This CSS concept is not in the local quick map yet. "
                "Run update css knowledge, then search vector memory for the latest official explanation."
            )

    return f"""CSS CONCEPT EXPLANATION

Concept:
{concept}

Practical explanation:
{explanation}

JARVIS rule:
Before using this CSS concept, check:
1. Does it solve a real layout, visual, accessibility, or responsiveness problem?
2. Is it supported enough for the target browsers?
3. Does it reduce complexity or create long-term CSS debt?
4. Can it translate cleanly into Tailwind, Bootstrap, Blade, React, Vue, or plain CSS?
5. Does it preserve accessibility, responsiveness, and maintainability?

For deeper updated knowledge, run:
update css knowledge
"""


def generate_css_framework_translation(request: str) -> str:
    text = request.strip()

    return f"""CSS FRAMEWORK TRANSLATION GUIDE

Request:
{text or "No specific request provided."}

Plain CSS principle:
- Define tokens.
- Build layout.
- Add components.
- Add responsive rules.
- Add states.
- Add motion/accessibility safeguards.

Tailwind translation:
- Tokens become tailwind.config theme values where needed.
- Layout becomes utilities such as grid, flex, gap, max-w, mx-auto, px, py.
- States become hover:, focus-visible:, active:, disabled:.
- Responsive rules become sm:, md:, lg:, xl:, 2xl:.
- Motion safety can use motion-safe: and motion-reduce:.

Bootstrap translation:
- Layout maps to container, row, col, d-flex, gap, align-items, justify-content.
- Components can extend Bootstrap classes with custom CSS variables.
- Avoid fighting Bootstrap specificity. Add a clean project layer.

React / Next.js translation:
- Use CSS modules, global CSS, Tailwind, or styled approach depending on the project.
- Keep design tokens global.
- Keep component styles close to reusable components.

Laravel Blade translation:
- Store global CSS in resources/css/app.css.
- Use Blade components for repeated styled blocks.
- Keep class names predictable and reusable.

Vue translation:
- Use scoped CSS for isolated components.
- Use global CSS for tokens, reset, typography, and layout utilities.
"""


def infer_css_action(user_input: str) -> dict:
    text = " ".join((user_input or "").lower().strip().split())

    update_words = [
        "teach yourself css",
        "learn css",
        "latest css",
        "update css",
        "refresh css",
        "official css",
        "css standard",
        "css snapshot",
        "w3c css",
        "mdn css",
        "professional css",
        "not just theory",
    ]

    status_words = [
        "do you know css",
        "already know css",
        "check css knowledge",
        "css status",
        "css knowledge status",
        "what css do you know",
        "show css knowledge",
    ]

    audit_words = [
        "audit css",
        "check css",
        "css file",
        "style file",
        "stylesheet",
        "production ready css",
        "validate css",
        "review css",
        "is this css correct",
        "is my css proper",
    ]

    explain_words = [
        "what is",
        "correct use",
        "when should i use",
        "explain",
        "difference between",
        "instead of",
    ]

    blueprint_words = [
        "plan",
        "structure",
        "blueprint",
        "website style",
        "landing page style",
        "responsive style",
        "css architecture",
        "design system",
    ]

    starter_words = [
        "starter css",
        "base css",
        "css foundation",
        "create css",
        "professional stylesheet",
        "stylesheet foundation",
        "modern css",
    ]

    translate_words = [
        "tailwind",
        "bootstrap",
        "react",
        "next",
        "vue",
        "blade",
        "framework",
        "convert css",
        "translate css",
    ]

    if any(word in text for word in update_words):
        return {"action": "update", "force": False}

    if "force update css" in text or "relearn css" in text or "refresh all css" in text:
        return {"action": "update", "force": True}

    if any(word in text for word in status_words):
        return {"action": "status"}

    if any(word in text for word in audit_words):
        path = extract_css_file_path(user_input)
        return {"action": "audit", "path": path}

    if any(word in text for word in starter_words):
        title = extract_project_name(user_input)
        return {"action": "starter", "title": title}

    if any(word in text for word in translate_words):
        return {"action": "translate", "request": user_input.strip()}

    if any(word in text for word in explain_words):
        concept = extract_css_concept_name(user_input)
        return {"action": "explain", "concept": concept}

    if any(word in text for word in blueprint_words):
        return {"action": "blueprint", "request": user_input.strip()}

    return {"action": "unknown"}


def extract_css_file_path(user_input: str) -> str:
    text = user_input.strip()

    file_match = re.search(
        r"([\w./\\-]+\.(?:css|scss|sass|less|vue|jsx|tsx|blade\.php|html))",
        text,
        re.I,
    )
    if file_match:
        return file_match.group(1)

    lowered = text.lower()
    if "sample css" in lowered or "sample stylesheet" in lowered:
        if Path("test_documents/sample.css").exists():
            return "test_documents/sample.css"

    return ""


def extract_css_concept_name(user_input: str) -> str:
    text = user_input.lower()

    known_concepts = [
        "cascade",
        "specificity",
        "box model",
        "box-model",
        "flexbox",
        "flex",
        "grid",
        "container queries",
        "container-queries",
        "media queries",
        "media-queries",
        "custom properties",
        "custom-properties",
        "css variables",
        "cascade layers",
        "cascade-layers",
        "nesting",
        "subgrid",
        "color-mix",
        "logical properties",
        "logical-properties",
        "view transitions",
        "view-transitions",
    ]

    for concept in known_concepts:
        if concept in text:
            normalized = concept.replace("css variables", "custom-properties")
            return normalized

    property_match = re.search(r"(?:explain|what is|use of)\s+([a-z-]+)", text)
    if property_match:
        return property_match.group(1)

    return ""


def extract_project_name(user_input: str) -> str:
    original = user_input.strip()

    if "lkprofessionals" in original.lower():
        return "LKProfessionals"

    for phrase in [
        "for ",
        "website for ",
        "stylesheet for ",
        "css for ",
        "landing page for ",
    ]:
        if phrase in original.lower():
            index = original.lower().rfind(phrase)
            title = original[index + len(phrase):].strip()
            if title:
                return title

    return "Professional Website"
