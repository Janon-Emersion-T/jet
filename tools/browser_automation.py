try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None


def _playwright_missing_response() -> str:
    return (
        "Browser automation is not available in this install profile. "
        "Install the full JARVIS profile to enable Playwright features."
    )

def open_and_read(url: str) -> str:
    if sync_playwright is None:
        return _playwright_missing_response()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto(url, timeout=60000)

            title = page.title()

            browser.close()

            return f"Opened website successfully.\nPage title: {title}"

    except Exception as e:
        return f"Browser automation error: {e}"


def google_search(query: str) -> str:
    if sync_playwright is None:
        return _playwright_missing_response()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            page = browser.new_page()

            page.goto("https://www.google.com")

            page.fill("textarea[name='q']", query)

            page.keyboard.press("Enter")

            page.wait_for_timeout(3000)

            title = page.title()

            browser.close()

            return f"Google search completed.\nResult page: {title}"

    except Exception as e:
        return f"Search error: {e}"
