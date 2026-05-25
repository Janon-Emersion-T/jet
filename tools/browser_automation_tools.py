import json
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus

from tools.browser_security import safe_url, normalize_domain
from tools.browser_session_tools import (
    PersistentBrowser,
    SCREENSHOT_DIR,
    BROWSER_REPORT_DIR,
    ensure_browser_storage,
)


ALLOWED_SEARCH_ENGINES = {
    "google": "https://www.google.com/search?q=",
    "bing": "https://www.bing.com/search?q=",
    "duckduckgo": "https://duckduckgo.com/?q=",
}

BROWSER_APPROVAL_DIR = Path("storage/browser_approvals")
MAX_TEXT = 12000


def _ensure_approval_dir():
    BROWSER_APPROVAL_DIR.mkdir(parents=True, exist_ok=True)


def _approval_file(action_id: str) -> Path:
    return BROWSER_APPROVAL_DIR / f"{action_id}.json"


def _save_browser_approval(action_type: str, payload: dict) -> dict:
    _ensure_approval_dir()

    action_id = datetime.now().strftime("%Y%m%d%H%M%S")

    data = {
        "id": action_id,
        "type": action_type,
        "payload": payload,
        "approved": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    _approval_file(action_id).write_text(json.dumps(data, indent=4), encoding="utf-8")
    return data


def list_browser_approvals() -> str:
    _ensure_approval_dir()
    files = sorted(BROWSER_APPROVAL_DIR.glob("*.json"), reverse=True)

    if not files:
        return "No browser approvals found."

    lines = ["BROWSER ACTION APPROVALS"]

    for file in files[:20]:
        data = json.loads(file.read_text(encoding="utf-8"))
        status = "approved" if data.get("approved") else "pending"
        lines.append(
            f"- {data['id']} | {status} | {data['type']} | {data.get('payload', {})}"
        )

    return "\n".join(lines)


def browser_open_page(url: str, headless: bool = False) -> str:
    try:
        target_url = safe_url(url)

        with PersistentBrowser(headless=headless) as page:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            title = page.title()
            current_url = page.url

        return (
            "BROWSER OPEN PAGE\n"
            f"Title: {title}\n"
            f"URL: {current_url}\n"
            "Session: persistent"
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
        return browser_open_page(search_url, headless=False)

    except Exception as e:
        return f"Browser search failed: {e}"


def browser_extract_text(url: str, max_chars: int = 6000) -> str:
    try:
        target_url = safe_url(url)

        with PersistentBrowser(headless=True) as page:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            title = page.title()
            body_text = page.locator("body").inner_text(timeout=10000).strip()

        return (
            "BROWSER TEXT EXTRACTION\n"
            f"Title: {title}\n"
            f"URL: {target_url}\n\n"
            f"{body_text[:max_chars]}"
        )

    except Exception as e:
        return f"Browser text extraction failed: {e}"


def browser_page_summary(url: str, max_chars: int = 4000) -> str:
    try:
        target_url = safe_url(url)

        with PersistentBrowser(headless=True) as page:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            title = page.title()
            headings = page.locator("h1, h2, h3").all_inner_texts()
            body_text = page.locator("body").inner_text(timeout=10000).strip()

        clean_headings = [h.strip() for h in headings if h.strip()]
        preview = body_text[:max_chars]

        paragraphs = [
            p.strip()
            for p in body_text.split("\n")
            if len(p.strip()) > 80
        ]

        key_points = paragraphs[:5]

        lines = [
            "BROWSER PAGE SUMMARY",
            f"Title: {title}",
            f"URL: {target_url}",
            "",
            "HEADINGS:",
        ]

        for heading in clean_headings[:20]:
            lines.append(f"- {heading}")

        lines.append("\nKEY POINTS:")
        for point in key_points:
            lines.append(f"- {point[:300]}")

        lines.append("\nTEXT PREVIEW:")
        lines.append(preview)

        return "\n".join(lines)

    except Exception as e:
        return f"Browser page summary failed: {e}"


def browser_extract_links(url: str, limit: int = 50) -> str:
    try:
        target_url = safe_url(url)

        with PersistentBrowser(headless=True) as page:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            links = page.locator("a").evaluate_all(
                f"""
                (els) => els.slice(0, {limit}).map(a => ({{
                    text: a.innerText,
                    href: a.href
                }}))
                """
            )

        lines = ["BROWSER LINK EXTRACTION", f"URL: {target_url}"]

        count = 0

        for link in links:
            text = (link.get("text") or "").strip()
            href = link.get("href") or ""

            if text and href:
                count += 1
                lines.append(f"{count}. {text}: {href}")

        if count == 0:
            lines.append("No readable links found.")

        return "\n".join(lines)

    except Exception as e:
        return f"Browser link extraction failed: {e}"


def browser_screenshot(url: str) -> str:
    try:
        ensure_browser_storage()
        target_url = safe_url(url)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"

        with PersistentBrowser(headless=True) as page:
            page.goto(target_url, wait_until="networkidle", timeout=45000)
            title = page.title()
            page.screenshot(path=str(output_path), full_page=True)

        return (
            "BROWSER SCREENSHOT CAPTURED\n"
            f"Title: {title}\n"
            f"URL: {target_url}\n"
            f"Saved: {output_path}"
        )

    except Exception as e:
        return f"Browser screenshot failed: {e}"


def browser_audit_page(url: str) -> str:
    try:
        ensure_browser_storage()
        target_url = safe_url(url)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOT_DIR / f"audit_{timestamp}.png"

        with PersistentBrowser(headless=True) as page:
            page.goto(target_url, wait_until="networkidle", timeout=45000)

            title = page.title()
            meta_description = (
                page.locator("meta[name='description']").get_attribute("content")
                or ""
            )
            h1_count = page.locator("h1").count()
            image_count = page.locator("img").count()
            link_count = page.locator("a").count()
            button_count = page.locator("button").count()
            page.screenshot(path=str(screenshot_path), full_page=True)

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


def request_browser_click(url: str, selector: str) -> str:
    try:
        target_url = safe_url(url)

        if not selector.strip():
            return "Selector is required."

        approval = _save_browser_approval(
            "click",
            {
                "url": target_url,
                "selector": selector.strip(),
            },
        )

        return (
            "BROWSER CLICK APPROVAL REQUIRED\n"
            f"ID: {approval['id']}\n"
            f"URL: {target_url}\n"
            f"Selector: {selector.strip()}\n\n"
            f"To execute: confirm browser action {approval['id']}"
        )

    except Exception as e:
        return f"Browser click request failed: {e}"


def request_browser_fill(url: str, selector: str, value: str) -> str:
    try:
        target_url = safe_url(url)

        if not selector.strip():
            return "Selector is required."

        approval = _save_browser_approval(
            "fill",
            {
                "url": target_url,
                "selector": selector.strip(),
                "value": value,
            },
        )

        return (
            "BROWSER FORM FILL APPROVAL REQUIRED\n"
            f"ID: {approval['id']}\n"
            f"URL: {target_url}\n"
            f"Selector: {selector.strip()}\n"
            f"Value: {value}\n\n"
            f"To execute: confirm browser action {approval['id']}"
        )

    except Exception as e:
        return f"Browser fill request failed: {e}"


def confirm_browser_action(action_id: str) -> str:
    try:
        file = _approval_file(action_id)

        if not file.exists():
            return "Browser approval request not found."

        data = json.loads(file.read_text(encoding="utf-8"))
        action_type = data.get("type")
        payload = data.get("payload", {})

        target_url = safe_url(payload.get("url", ""))

        with PersistentBrowser(headless=False) as page:
            page.goto(target_url, wait_until="domcontentloaded", timeout=30000)

            if action_type == "click":
                selector = payload["selector"]
                page.locator(selector).first.click(timeout=10000)
                result = f"Clicked selector: {selector}"

            elif action_type == "fill":
                selector = payload["selector"]
                value = payload.get("value", "")
                page.locator(selector).first.fill(value, timeout=10000)
                result = f"Filled selector: {selector}"

            else:
                return f"Unsupported browser action type: {action_type}"

            data["approved"] = True
            data["approved_at"] = datetime.now().isoformat(timespec="seconds")
            data["final_url"] = page.url
            file.write_text(json.dumps(data, indent=4), encoding="utf-8")

        return (
            "BROWSER ACTION EXECUTED\n"
            f"ID: {action_id}\n"
            f"Type: {action_type}\n"
            f"URL: {target_url}\n"
            f"{result}"
        )

    except Exception as e:
        return f"Browser action failed: {e}"


def browser_google_results(query: str, limit: int = 10) -> str:
    try:
        query = query.strip()

        if not query:
            return "Search query is required."

        search_url = "https://www.google.com/search?q=" + quote_plus(query)

        with PersistentBrowser(headless=True) as page:
            page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

            results = page.locator("a").evaluate_all(
                """
                (links) => links.map(a => ({
                    text: a.innerText,
                    href: a.href
                })).filter(item =>
                    item.text &&
                    item.href &&
                    item.href.startsWith("http") &&
                    !item.href.includes("google.com/search") &&
                    !item.href.includes("accounts.google") &&
                    !item.href.includes("support.google")
                ).slice(0, 30)
                """
            )

        lines = [
            "GOOGLE SEARCH PARSER",
            f"Query: {query}",
            "",
            "RESULTS:",
        ]

        count = 0
        seen = set()

        for item in results:
            href = item.get("href", "")
            text = " ".join((item.get("text") or "").split())

            if not href or href in seen:
                continue

            seen.add(href)
            count += 1
            lines.append(f"{count}. {text[:160]}")
            lines.append(f"   {href}")

            if count >= limit:
                break

        if count == 0:
            lines.append("No parseable organic results found. Google may have changed the layout or blocked automated parsing.")

        return "\n".join(lines)

    except Exception as e:
        return f"Google search parser failed: {e}"


def seo_serp_checker(keyword: str, domain: str, limit: int = 30) -> str:
    try:
        keyword = keyword.strip()
        target_domain = normalize_domain(domain)

        if not keyword:
            return "Keyword is required."

        if not target_domain:
            return "Domain is required."

        search_url = "https://www.google.com/search?q=" + quote_plus(keyword)

        with PersistentBrowser(headless=True) as page:
            page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

            results = page.locator("a").evaluate_all(
                """
                (links) => links.map(a => ({
                    text: a.innerText,
                    href: a.href
                })).filter(item =>
                    item.text &&
                    item.href &&
                    item.href.startsWith("http") &&
                    !item.href.includes("google.com/search") &&
                    !item.href.includes("accounts.google") &&
                    !item.href.includes("support.google")
                ).slice(0, 80)
                """
            )

        organic = []
        seen = set()

        for item in results:
            href = item.get("href", "")
            text = " ".join((item.get("text") or "").split())

            if not href or href in seen:
                continue

            seen.add(href)
            organic.append({"title": text, "url": href})

            if len(organic) >= limit:
                break

        position = None
        matched_url = None

        for index, result in enumerate(organic, start=1):
            result_domain = normalize_domain(result["url"])

            if target_domain in result_domain or result_domain in target_domain:
                position = index
                matched_url = result["url"]
                break

        lines = [
            "SEO SERP CHECKER",
            f"Keyword: {keyword}",
            f"Domain: {target_domain}",
            f"Checked results: {len(organic)}",
            "",
        ]

        if position:
            lines.append(f"FOUND: Position {position}")
            lines.append(f"Matched URL: {matched_url}")
        else:
            lines.append(f"NOT FOUND in top {limit} parsed results.")

        lines.append("\nTOP RESULTS:")
        for index, result in enumerate(organic[:10], start=1):
            lines.append(f"{index}. {result['title'][:120]}")
            lines.append(f"   {result['url']}")

        return "\n".join(lines)

    except Exception as e:
        return f"SEO SERP checker failed: {e}"
