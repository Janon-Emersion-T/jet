from tools.browser_automation_tools import (
    browser_open_page,
    browser_search,
    browser_extract_text,
    browser_screenshot,
)


def handle_browser_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("browser open "):
        url = user_input.replace("browser open ", "", 1).strip()
        return browser_open_page(url)

    if text.startswith("browser search "):
        query = user_input.replace("browser search ", "", 1).strip()
        return browser_search(query)

    if text.startswith("browser bing "):
        query = user_input.replace("browser bing ", "", 1).strip()
        return browser_search(query, engine="bing")

    if text.startswith("browser duck "):
        query = user_input.replace("browser duck ", "", 1).strip()
        return browser_search(query, engine="duckduckgo")

    if text.startswith("browser read "):
        url = user_input.replace("browser read ", "", 1).strip()
        return browser_extract_text(url)

    if text.startswith("browser screenshot "):
        url = user_input.replace("browser screenshot ", "", 1).strip()
        return browser_screenshot(url)

    return None
