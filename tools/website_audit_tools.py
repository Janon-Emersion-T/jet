from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
import time

from tools.browser_security import safe_url
from tools.browser_session_tools import PersistentBrowser


MAX_LINKS_TO_CHECK = 40
TIMEOUT = 10


def _fetch_page_data(url: str) -> dict:
    target_url = safe_url(url)

    with PersistentBrowser(headless=True) as page:
        start = time.time()
        page.goto(target_url, wait_until="networkidle", timeout=45000)
        load_time = round(time.time() - start, 2)

        data = page.evaluate(
            """
            () => {
                const meta = Array.from(document.querySelectorAll('meta')).map(m => ({
                    name: m.getAttribute('name'),
                    property: m.getAttribute('property'),
                    content: m.getAttribute('content')
                }));

                const headings = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => ({
                    tag: h.tagName.toLowerCase(),
                    text: h.innerText.trim()
                }));

                const images = Array.from(document.querySelectorAll('img')).map(img => ({
                    src: img.getAttribute('src') || '',
                    alt: img.getAttribute('alt') || ''
                }));

                const links = Array.from(document.querySelectorAll('a')).map(a => ({
                    text: a.innerText.trim(),
                    href: a.href || ''
                }));

                const bodyText = document.body ? document.body.innerText.trim() : '';

                return {
                    title: document.title || '',
                    canonical: document.querySelector("link[rel='canonical']")?.href || '',
                    meta,
                    headings,
                    images,
                    links,
                    bodyText,
                    url: location.href
                };
            }
            """
        )

    data["load_time"] = load_time
    data["requested_url"] = target_url
    return data


def _meta_content(data: dict, name: str) -> str:
    for item in data.get("meta", []):
        if (item.get("name") or "").lower() == name.lower():
            return item.get("content") or ""
    return ""


def _property_content(data: dict, prop: str) -> str:
    for item in data.get("meta", []):
        if (item.get("property") or "").lower() == prop.lower():
            return item.get("content") or ""
    return ""


def _score_line(label: str, ok: bool, detail: str) -> str:
    mark = "PASS" if ok else "WARN"
    return f"- {mark}: {label} — {detail}"


def meta_tag_analyzer(url: str) -> str:
    try:
        data = _fetch_page_data(url)

        title = data.get("title", "")
        description = _meta_content(data, "description")
        viewport = _meta_content(data, "viewport")
        robots = _meta_content(data, "robots")
        og_title = _property_content(data, "og:title")
        og_description = _property_content(data, "og:description")

        lines = [
            "META TAG ANALYZER",
            f"URL: {data['url']}",
            "",
            _score_line("Title", 30 <= len(title) <= 65, f"{len(title)} chars | {title or 'missing'}"),
            _score_line("Meta description", 120 <= len(description) <= 160, f"{len(description)} chars | {description or 'missing'}"),
            _score_line("Viewport", bool(viewport), viewport or "missing"),
            _score_line("Canonical", bool(data.get("canonical")), data.get("canonical") or "missing"),
            _score_line("Robots meta", bool(robots), robots or "not specified"),
            _score_line("OG title", bool(og_title), og_title or "missing"),
            _score_line("OG description", bool(og_description), og_description or "missing"),
        ]

        return "\n".join(lines)

    except Exception as e:
        return f"Meta tag analyzer failed: {e}"


def heading_analyzer(url: str) -> str:
    try:
        data = _fetch_page_data(url)
        headings = data.get("headings", [])
        h1s = [h for h in headings if h["tag"] == "h1"]

        lines = [
            "HEADING ANALYZER",
            f"URL: {data['url']}",
            "",
            _score_line("Single H1", len(h1s) == 1, f"{len(h1s)} H1 tags found"),
            "",
            "HEADINGS:"
        ]

        for h in headings[:50]:
            lines.append(f"- {h['tag'].upper()}: {h['text'][:120]}")

        return "\n".join(lines)

    except Exception as e:
        return f"Heading analyzer failed: {e}"


def image_alt_checker(url: str) -> str:
    try:
        data = _fetch_page_data(url)
        images = data.get("images", [])

        missing = [img for img in images if not img.get("alt", "").strip()]

        lines = [
            "IMAGE ALT CHECKER",
            f"URL: {data['url']}",
            f"Images found: {len(images)}",
            f"Missing alt: {len(missing)}",
            ""
        ]

        for img in missing[:40]:
            lines.append(f"- Missing alt: {img.get('src') or 'unknown source'}")

        if not missing:
            lines.append("No missing image alt text found.")

        return "\n".join(lines)

    except Exception as e:
        return f"Image alt checker failed: {e}"


def internal_link_checker(url: str) -> str:
    try:
        data = _fetch_page_data(url)
        base_host = urlparse(data["url"]).netloc.replace("www.", "")
        internal = []
        external = []

        for link in data.get("links", []):
            href = link.get("href", "")
            if not href:
                continue

            host = urlparse(href).netloc.replace("www.", "")
            if host == base_host:
                internal.append(link)
            else:
                external.append(link)

        lines = [
            "INTERNAL LINK CHECKER",
            f"URL: {data['url']}",
            f"Internal links: {len(internal)}",
            f"External links: {len(external)}",
            "",
            "INTERNAL LINK SAMPLE:"
        ]

        for link in internal[:40]:
            text = link.get("text") or "(no anchor text)"
            lines.append(f"- {text[:80]} -> {link.get('href')}")

        return "\n".join(lines)

    except Exception as e:
        return f"Internal link checker failed: {e}"


def _check_url_status(url: str) -> tuple[int | str, str]:
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "JARVIS SEO Auditor"})
        with urlopen(req, timeout=TIMEOUT) as response:
            return response.status, "OK"
    except HTTPError as e:
        return e.code, "HTTP error"
    except URLError as e:
        return "ERR", str(e.reason)
    except Exception as e:
        return "ERR", str(e)


def broken_link_checker(url: str) -> str:
    try:
        data = _fetch_page_data(url)

        checked = []
        for link in data.get("links", [])[:MAX_LINKS_TO_CHECK]:
            href = link.get("href")
            if not href or href.startswith(("mailto:", "tel:", "javascript:")):
                continue

            status, message = _check_url_status(href)
            checked.append((href, status, message))

        broken = [item for item in checked if item[1] == "ERR" or str(item[1]).startswith(("4", "5"))]

        lines = [
            "BROKEN LINK CHECKER",
            f"URL: {data['url']}",
            f"Checked links: {len(checked)}",
            f"Possible broken links: {len(broken)}",
            ""
        ]

        for href, status, message in broken[:40]:
            lines.append(f"- {status}: {href} | {message}")

        if not broken:
            lines.append("No obvious broken links found in checked sample.")

        return "\n".join(lines)

    except Exception as e:
        return f"Broken link checker failed: {e}"


def sitemap_checker(url: str) -> str:
    try:
        target_url = safe_url(url)
        parsed = urlparse(target_url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

        status, message = _check_url_status(sitemap_url)

        return "\n".join([
            "SITEMAP CHECKER",
            f"Sitemap URL: {sitemap_url}",
            f"Status: {status}",
            f"Result: {message}",
        ])

    except Exception as e:
        return f"Sitemap checker failed: {e}"


def robots_checker(url: str) -> str:
    try:
        target_url = safe_url(url)
        parsed = urlparse(target_url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        status, message = _check_url_status(robots_url)

        return "\n".join([
            "ROBOTS.TXT CHECKER",
            f"Robots URL: {robots_url}",
            f"Status: {status}",
            f"Result: {message}",
        ])

    except Exception as e:
        return f"Robots checker failed: {e}"


def page_speed_basic_checker(url: str) -> str:
    try:
        data = _fetch_page_data(url)

        status = "GOOD" if data["load_time"] <= 3 else "NEEDS IMPROVEMENT"

        return "\n".join([
            "PAGE SPEED BASIC CHECKER",
            f"URL: {data['url']}",
            f"Load time: {data['load_time']} seconds",
            f"Basic status: {status}",
            "",
            "Note: This is a basic Playwright timing check, not a full Lighthouse audit."
        ])

    except Exception as e:
        return f"Page speed checker failed: {e}"


def content_quality_analyzer(url: str) -> str:
    try:
        data = _fetch_page_data(url)
        text = data.get("bodyText", "")
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)

        paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 80]
        headings = data.get("headings", [])

        lines = [
            "CONTENT QUALITY ANALYZER",
            f"URL: {data['url']}",
            "",
            _score_line("Word count", word_count >= 300, f"{word_count} words"),
            _score_line("Readable paragraph blocks", len(paragraphs) >= 3, f"{len(paragraphs)} content paragraphs"),
            _score_line("Heading structure", len(headings) >= 3, f"{len(headings)} headings"),
            _score_line("Thin content risk", word_count >= 500, "low risk" if word_count >= 500 else "possible thin content"),
        ]

        return "\n".join(lines)

    except Exception as e:
        return f"Content quality analyzer failed: {e}"


def website_audit(url: str) -> str:
    sections = [
        meta_tag_analyzer(url),
        heading_analyzer(url),
        image_alt_checker(url),
        internal_link_checker(url),
        sitemap_checker(url),
        robots_checker(url),
        page_speed_basic_checker(url),
        content_quality_analyzer(url),
    ]

    return "\n\n" + ("\n\n" + "=" * 80 + "\n\n").join(sections)
