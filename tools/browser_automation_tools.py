from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = Path("storage/browser_screenshots")
ALLOWED_SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q=",
}


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
