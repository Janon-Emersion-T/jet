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
HTML_SOURCE_FILE = DATA_DIR / "html_knowledge_sources.json"
HTML_MANIFEST_FILE = DATA_DIR / "html_knowledge_manifest.json"

DEFAULT_HEADERS = {
    "User-Agent": "JARVIS-HTML-Knowledge-Engine/1.0 (+local private assistant)"
}

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "source", "track", "wbr"
}

SEMANTIC_ELEMENTS = {
    "header", "nav", "main", "section", "article", "aside",
    "footer", "figure", "figcaption", "time", "address", "mark"
}

OBSOLETE_ELEMENTS = {
    "acronym", "applet", "basefont", "big", "center", "dir",
    "font", "frame", "frameset", "marquee", "noframes", "strike", "tt"
}


def _now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


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

    title = soup.title.get_text(" ", strip=True) if soup.title else "Untitled HTML Source"

    headings = []
    for heading in soup.find_all(["h1", "h2", "h3"]):
        text = heading.get_text(" ", strip=True)
        if text and len(text) < 160:
            headings.append(text)

    body_text = _clean_text(soup.get_text(" "))
    heading_text = " | ".join(headings[:40])

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


def html_knowledge_status() -> str:
    manifest = _load_json(HTML_MANIFEST_FILE, {"sources": {}})
    sources = manifest.get("sources", {})

    if not sources:
        return (
            "HTML KNOWLEDGE STATUS\n"
            "No HTML knowledge has been learned yet.\n"
            "Run: update html knowledge"
        )

    lines = ["HTML KNOWLEDGE STATUS"]
    for url, item in sources.items():
        lines.append("")
        lines.append(f"Source: {item.get('name', 'Unknown')}")
        lines.append(f"URL: {url}")
        lines.append(f"Last learned: {item.get('last_learned_at', '-')}")
        lines.append(f"Chunks saved: {item.get('chunks_saved', 0)}")
        lines.append(f"Hash: {item.get('hash', '-')[:16]}...")

    return "\n".join(lines)


def update_html_knowledge(force: bool = False) -> str:
    _ensure_data_dir()

    source_data = _load_json(HTML_SOURCE_FILE, None)
    if not source_data:
        return (
            "HTML KNOWLEDGE UPDATE FAILED\n"
            "Missing data/html_knowledge_sources.json"
        )

    manifest = _load_json(HTML_MANIFEST_FILE, {"updated_at": None, "sources": {}})
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
                    "HTML KNOWLEDGE SOURCE\n"
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
                        "html",
                        "web-development",
                        "frontend",
                        "standards",
                        source_type
                    ],
                    source="html-knowledge-engine",
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
    _save_json(HTML_MANIFEST_FILE, manifest)

    lines = [
        "HTML KNOWLEDGE UPDATE COMPLETE",
        f"Sources updated: {updated_sources}",
        f"Sources skipped: {skipped_sources}",
        f"Memory chunks saved: {total_chunks}",
        "",
        "JARVIS can now use updated HTML knowledge through vector memory."
    ]

    if errors:
        lines.append("")
        lines.append("Errors:")
        lines.extend(f"- {error}" for error in errors[:10])

    return "\n".join(lines)


def generate_html_blueprint(project_request: str) -> str:
    request = project_request.strip()

    if not request:
        return "Tell me what type of website or HTML structure you want."

    return f"""HTML PRACTICAL BLUEPRINT

Request:
{request}

Recommended practical structure:

1. Document foundation
- Use <!doctype html>
- Use <html lang="en">
- Include <meta charset="utf-8">
- Include <meta name="viewport" content="width=device-width, initial-scale=1">
- Add useful SEO title and description.

2. Semantic layout
- <header> for brand/navigation.
- <nav> for main navigation links.
- <main> for the unique page content.
- <section> for major content blocks.
- <article> for independent content such as blog cards, services, news, or case studies.
- <aside> only for secondary content.
- <footer> for business/contact/legal links.

3. Accessibility
- Use one clear <h1>.
- Keep heading order logical.
- Add alt text for meaningful images.
- Use button for actions and anchor links for navigation.
- Associate labels with form fields.
- Avoid div-heavy layout when a semantic element exists.

4. Forms
- Use <form>, <label>, <input>, <textarea>, <select>, and <button>.
- Use proper input types: email, tel, url, number, date.
- Add required only when truly required.
- Add autocomplete where useful.

5. SEO-ready HTML
- Add title, description, canonical link, Open Graph tags, and structured headings.
- Use meaningful anchor text.
- Use image width/height where possible.
- Use lazy loading for non-critical images.

6. Framework translation
This HTML structure can be converted into:
- Laravel Blade components
- React / Next.js components
- Vue components
- WordPress templates
- Static HTML
- Tailwind sections
- Bootstrap sections

7. JARVIS execution rule
When generating code, JARVIS should first design the semantic HTML skeleton, then attach CSS/framework classes, then add JavaScript only when behavior is required.
"""


def create_html_starter_page(title: str = "JARVIS Generated Website") -> str:
    safe_title = title.strip() or "JARVIS Generated Website"

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <meta name="description" content="A semantic, accessible, SEO-ready HTML page generated by JARVIS.">
  <link rel="canonical" href="/">
</head>
<body>
  <header>
    <a href="/" aria-label="Go to homepage">{safe_title}</a>

    <nav aria-label="Main navigation">
      <ul>
        <li><a href="#services">Services</a></li>
        <li><a href="#work">Work</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section aria-labelledby="hero-title">
      <h1 id="hero-title">{safe_title}</h1>
      <p>Build a clear, semantic, accessible, and search-friendly website foundation.</p>
      <a href="#contact">Start a project</a>
    </section>

    <section id="services" aria-labelledby="services-title">
      <h2 id="services-title">Services</h2>

      <article>
        <h3>Web Development</h3>
        <p>Modern website development with clean HTML structure.</p>
      </article>

      <article>
        <h3>SEO Foundation</h3>
        <p>Semantic HTML designed to help search engines understand the page.</p>
      </article>
    </section>

    <section id="work" aria-labelledby="work-title">
      <h2 id="work-title">Featured Work</h2>
      <p>Showcase important projects with meaningful content and structure.</p>
    </section>

    <section id="contact" aria-labelledby="contact-title">
      <h2 id="contact-title">Contact</h2>

      <form action="#" method="post">
        <p>
          <label for="name">Name</label>
          <input id="name" name="name" type="text" autocomplete="name" required>
        </p>

        <p>
          <label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
        </p>

        <p>
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="5" required></textarea>
        </p>

        <button type="submit">Send message</button>
      </form>
    </section>
  </main>

  <footer>
    <p>&copy; 2026 {safe_title}. All rights reserved.</p>
  </footer>
</body>
</html>"""


def audit_html_code(html: str) -> str:
    if not html or len(html.strip()) < 20:
        return "HTML AUDIT FAILED\nNo usable HTML was provided."

    soup = BeautifulSoup(html, "html.parser")
    issues = []
    warnings = []
    strengths = []

    doctype_ok = html.lstrip().lower().startswith("<!doctype html>")
    if doctype_ok:
        strengths.append("Uses modern <!doctype html>.")
    else:
        issues.append("Missing modern <!doctype html> declaration.")

    html_tag = soup.find("html")
    if html_tag:
        if html_tag.get("lang"):
            strengths.append("The <html> element includes a lang attribute.")
        else:
            issues.append("The <html> element is missing a lang attribute.")
    else:
        issues.append("Missing <html> root element.")

    head = soup.find("head")
    body = soup.find("body")

    if not head:
        issues.append("Missing <head> section.")
    if not body:
        issues.append("Missing <body> section.")

    if soup.find("meta", attrs={"charset": True}):
        strengths.append("Character encoding meta tag exists.")
    else:
        issues.append("Missing <meta charset=\"utf-8\">.")

    viewport = soup.find("meta", attrs={"name": "viewport"})
    if viewport:
        strengths.append("Viewport meta tag exists.")
    else:
        issues.append("Missing responsive viewport meta tag.")

    title = soup.find("title")
    if title and title.get_text(strip=True):
        strengths.append("Page title exists.")
    else:
        issues.append("Missing useful <title>.")

    description = soup.find("meta", attrs={"name": "description"})
    if description and description.get("content"):
        strengths.append("Meta description exists.")
    else:
        warnings.append("Missing meta description.")

    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 1:
        strengths.append("Exactly one <h1> found.")
    elif len(h1_tags) == 0:
        issues.append("Missing <h1>.")
    else:
        warnings.append(f"Multiple <h1> tags found: {len(h1_tags)}.")

    if soup.find("main"):
        strengths.append("Uses <main> landmark.")
    else:
        issues.append("Missing <main> landmark.")

    if soup.find("nav"):
        strengths.append("Uses <nav> for navigation.")
    else:
        warnings.append("No <nav> landmark found.")

    if soup.find("header"):
        strengths.append("Uses <header>.")
    else:
        warnings.append("No <header> found.")

    if soup.find("footer"):
        strengths.append("Uses <footer>.")
    else:
        warnings.append("No <footer> found.")

    for obsolete in sorted(OBSOLETE_ELEMENTS):
        found = soup.find_all(obsolete)
        if found:
            issues.append(f"Obsolete element used: <{obsolete}>.")

    for img in soup.find_all("img"):
        if not img.get("alt"):
            issues.append("An <img> is missing alt text.")

    for label in soup.find_all("label"):
        has_for = bool(label.get("for"))
        wraps_control = bool(label.find(["input", "textarea", "select"]))
        if not has_for and not wraps_control:
            issues.append("A <label> is not connected to a form control.")

    for input_tag in soup.find_all("input"):
        input_type = input_tag.get("type", "text")
        if input_type not in {"hidden", "submit", "button", "reset"}:
            input_id = input_tag.get("id")
            if input_id and soup.find("label", attrs={"for": input_id}):
                continue
            parent_label = input_tag.find_parent("label")
            if not parent_label:
                issues.append(f"Input field is missing a connected label: type={input_type}.")

    lines = ["HTML AUDIT REPORT", ""]

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
        lines.append("Fix the critical issues before using this HTML in production.")
    elif warnings:
        lines.append("HTML foundation is usable, but polish the warnings for professional delivery.")
    else:
        lines.append("HTML foundation looks strong for production-level work.")

    return "\n".join(lines)


def audit_html_file(path: str) -> str:
    target = Path(path).expanduser()

    if not target.exists():
        project_relative = BASE_DIR / path
        if project_relative.exists():
            target = project_relative
        else:
            return f"HTML AUDIT FAILED\nFile not found: {path}"

    if not target.is_file():
        return f"HTML AUDIT FAILED\nPath is not a file: {path}"

    try:
        html = target.read_text(encoding="utf-8", errors="ignore")
        report = audit_html_code(html)
        return f"File: {target}\n\n{report}"
    except Exception as e:
        return f"HTML AUDIT FAILED\n{e}"


def explain_html_element(element: str) -> str:
    tag = element.strip().lower().replace("<", "").replace(">", "").replace("/", "")

    if not tag:
        return "Please provide an HTML element name. Example: explain html element section"

    category = "standard or unknown"
    practical_note = "Use it only when it matches the meaning of the content."

    if tag in VOID_ELEMENTS:
        category = "void element"
        practical_note = "It must not contain child content or a closing tag in normal HTML."
    elif tag in SEMANTIC_ELEMENTS:
        category = "semantic element"
        practical_note = "Use it to describe page meaning, not just layout."
    elif tag in OBSOLETE_ELEMENTS:
        category = "obsolete element"
        practical_note = "Avoid it in modern HTML. Use CSS or a semantic replacement."

    return f"""HTML ELEMENT EXPLANATION

Element:
<{tag}>

Category:
{category}

Practical usage:
{practical_note}

JARVIS rule:
Before using <{tag}>, check:
1. Does it describe the meaning of the content?
2. Is it valid in modern HTML?
3. Does it improve accessibility or structure?
4. Can it be translated cleanly into Blade, React, Vue, or another framework?

For deeper updated knowledge, run:
update html knowledge
"""

def infer_html_action(user_input: str) -> dict:
    text = " ".join((user_input or "").lower().strip().split())

    update_words = [
        "teach yourself",
        "learn html",
        "latest html",
        "update html",
        "refresh html",
        "official sources",
        "html standard",
        "html living standard",
        "whatwg",
        "mdn",
        "professional web developer",
        "not just theory",
    ]

    status_words = [
        "do you know html",
        "already know html",
        "check whether you already know html",
        "check if you already know html",
        "html status",
        "html knowledge status",
        "what html do you know",
        "what do you know about html",
        "show html knowledge",
    ]

    audit_words = [
        "audit",
        "check whether",
        "check if",
        "written properly",
        "production ready",
        "validate",
        "review",
        "is correct",
        "is proper",
        "sample html file",
        "sample html",
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
        "website structure",
        "landing page structure",
        "service business website",
    ]

    starter_words = [
        "basic structure",
        "clean html foundation",
        "html foundation",
        "starter",
        "base html",
        "boilerplate",
        "create html",
        "professional website",
        "company landing page",
    ]

    if any(word in text for word in update_words):
        return {"action": "update", "force": False}

    if any(word in text for word in status_words):
        return {"action": "status"}

    if any(word in text for word in audit_words):
        path = extract_html_file_path(user_input)
        return {"action": "audit", "path": path}

    if any(word in text for word in explain_words):
        element = extract_html_element_name(user_input)
        return {"action": "explain", "element": element}

    if any(word in text for word in starter_words):
        title = extract_site_title(user_input)
        return {"action": "starter", "title": title}

    if any(word in text for word in blueprint_words):
        return {"action": "blueprint", "request": user_input.strip()}

    return {"action": "unknown"}


def extract_html_file_path(user_input: str) -> str:
    text = user_input.strip()

    file_match = re.search(r"([\w./\\-]+\.(?:html|htm|blade\.php|php))", text, re.I)
    if file_match:
        return file_match.group(1)

    # Human alias fallback
    lowered = text.lower()
    if "sample html" in lowered or "sample file" in lowered:
        if Path("test_documents/sample.html").exists():
            return "test_documents/sample.html"

    return ""


def extract_html_element_name(user_input: str) -> str:
    text = user_input.lower()

    known_elements = [
        "html", "head", "body", "main", "section", "article", "aside",
        "header", "footer", "nav", "form", "input", "button", "label",
        "meta", "title", "img", "picture", "figure", "figcaption",
        "ul", "ol", "li", "a", "p", "div", "span", "table"
    ]

    tag_match = re.search(r"<\s*([a-z0-9-]+)\s*>", text)
    if tag_match:
        return tag_match.group(1)

    for element in known_elements:
        if f" {element} " in f" {text} ":
            return element

    if "section tag" in text:
        return "section"

    if "article instead of section" in text:
        return "article"

    return ""


def extract_site_title(user_input: str) -> str:
    original = user_input.strip()

    if "lkprofessionals" in original.lower():
        return "LKProfessionals"

    for phrase in [
        "for ",
        "website for ",
        "landing page for ",
        "company landing page for ",
    ]:
        if phrase in original.lower():
            index = original.lower().rfind(phrase)
            title = original[index + len(phrase):].strip()
            if title:
                return title

    return "Professional Website"