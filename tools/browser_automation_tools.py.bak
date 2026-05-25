from pathlib import Path
from urllib.parse import quote_plus

from datetime import datetime
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = Path("storage/browser_screenshots")
ALLOWED_SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q=",
}

BROWSER_SESSION_DIR = Path("storage/browser_session")
BROWSER_REPORT_DIR = Path("storage/browser_reports")

BLOCKED_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
}


def _ensure_browser_dirs():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    BROWSER_SESSION_DIR.mkdir(parents=True, exist_ok=True)
    BROWSER_REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _validate_public_url(url: str) -> str:
    target_url = _safe_url(url)
    parsed = urlparse(target_url)

    if parsed.hostname in BLOCKED_HOSTS:
        raise ValueError("Blocked local/internal browser target.")

    return target_url


def browser_page_summary(url: str, max_chars: int = 4000) -> str:
    try:
        target_url = _validate_public_url(url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1200})
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            headings = page.locator("h1, h2, h3").all_inner_texts()
            links = page.locator("a").evaluate_all(
                "(els) => els.slice(0, 25).map(a => ({text: a.innerText, href: a.href}))"
            )
            body_text = page.locator("body").inner_text(timeout=10000).strip()[:max_chars]

            browser.close()

        lines = [
            "BROWSER PAGE SUMMARY",
            f"Title: {title}",
            f"URL: {target_url}",
            "",
            "HEADINGS:",
        ]

        lines.extend(f"- {h.strip()}" for h in headings[:20] if h.strip())

        lines.append("\nTOP LINKS:")
        for link in links:
            text = (link.get("text") or "").strip()
            href = link.get("href") or ""
            if text and href:
                lines.append(f"- {text}: {href}")

        lines.append("\nTEXT PREVIEW:")
        lines.append(body_text)

        return "\n".join(lines)

    except Exception as e:
        return f"Browser page summary failed: {e}"


def browser_audit_page(url: str) -> str:
    try:
        _ensure_browser_dirs()
        target_url = _validate_public_url(url)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"audit_{timestamp}.png"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1200})
            page.goto(target_url, wait_until="networkidle", timeout=45000)

            title = page.title()
            meta_description = page.locator("meta[name='description']").get_attribute("content") or ""
            h1_count = page.locator("h1").count()
            image_count = page.locator("img").count()
            link_count = page.locator("a").count()
            button_count = page.locator("button").count()
            page.screenshot(path=str(screenshot_path), full_page=True)

            browser.close()

        return (
            "BROWSER PAGE AUDIT\n"
            f"Title: {title}\n"
            f"URL: {target_url}\n"
            f"Meta description: {meta_description or 'missing'}\n"
            f"H1 count: {h1_count}\n"
            f"Images: {image_count}\n"
            f"Links: {link_count}\n"
            f"Buttons: {button_count}\n"
            f"Screenshot: {screenshot_path}"
        )

    except Exception as e:
        return f"Browser page audit failed: {e}"


def browser_extract_links(url: str, limit: int = 50) -> str:
    try:
        target_url = _validate_public_url(url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            links = page.locator("a").evaluate_all(
                f"(els) => els.slice(0, {limit}).map(a => ({{text: a.innerText, href: a.href}}))"
            )

            browser.close()

        lines = ["BROWSER LINK EXTRACTION", f"URL: {target_url}"]

        for link in links:
            text = (link.get("text") or "").strip()
            href = link.get("href") or ""
            if text and href:
                lines.append(f"- {text}: {href}")

        return "\n".join(lines)

    except Exception as e:
        return f"Browser link extraction failed: {e}"

def _ensure_storage():
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _safe_url(url: str) -> str:
    url = url.strip()

    if not url:
        raise ValueError("URL is required.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def browser_open_page(url: str) -> str:
    try:
        target_url = _safe_url(url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            current_url = page.url

            browser.close()

        return (
            "BROWSER OPEN PAGE\n"
            f"Title: {title}\n"
            f"URL: {current_url}"
        )

    except Exception as e:
        return f"Browser open failed: {e}"


def browser_search(query: str, engine: str = "google") -> str:
    try:
        query = query.strip()

        if not query:
            return "Search query is required."

        engine = engine.lower().strip()

        if engine not in ALLOWED_SEARCH_ENGINES:
            return (
                "Unsupported search engine.\n"
                "Allowed engines: google, bing, duckduckgo"
            )

        search_url = ALLOWED_SEARCH_ENGINES[engine] + quote_plus(query)
        return browser_open_page(search_url)

    except Exception as e:
        return f"Browser search failed: {e}"


def browser_extract_text(url: str, max_chars: int = 6000) -> str:
    try:
        target_url = _safe_url(url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            body_text = page.locator("body").inner_text(timeout=10000)

            browser.close()

        body_text = body_text.strip()[:max_chars]

        return (
            "BROWSER TEXT EXTRACTION\n"
            f"Title: {title}\n"
            f"URL: {target_url}\n\n"
            f"{body_text}"
        )

    except Exception as e:
        return f"Browser text extraction failed: {e}"


def browser_screenshot(url: str) -> str:
    try:
        _ensure_storage()
        target_url = _safe_url(url)

        file_name = "screenshot.png"
        output_path = SCREENSHOT_DIR / file_name

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1200})
            page.goto(target_url, wait_until="networkidle", timeout=45000)
            page.screenshot(path=str(output_path), full_page=True)
            title = page.title()
            browser.close()

        return (
            "BROWSER SCREENSHOT CAPTURED\n"
            f"Title: {title}\n"
            f"URL: {target_url}\n"
            f"Saved: {output_path}"
        )

    except Exception as e:
        return f"Browser screenshot failed: {e}"
