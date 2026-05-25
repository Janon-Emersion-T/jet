from tools.browser_automation_tools import (
    browser_open_page,
    browser_search,
    browser_extract_text,
    browser_screenshot,
    browser_page_summary,
    browser_audit_page,
    browser_extract_links,
    request_browser_click,
    request_browser_fill,
    confirm_browser_action,
    list_browser_approvals,
    browser_google_results,
    seo_serp_checker,
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

    if text.startswith("browser summarize "):
        url = user_input.replace("browser summarize ", "", 1).strip()
        return browser_page_summary(url)

    if text.startswith("browser links "):
        url = user_input.replace("browser links ", "", 1).strip()
        return browser_extract_links(url)

    if text.startswith("browser screenshot "):
        url = user_input.replace("browser screenshot ", "", 1).strip()
        return browser_screenshot(url)

    if text.startswith("browser audit "):
        url = user_input.replace("browser audit ", "", 1).strip()
        return browser_audit_page(url)

    if text.startswith("browser click "):
        command = user_input.replace("browser click ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: browser click URL ::: CSS_SELECTOR"

        url, selector = command.split(":::", 1)
        return request_browser_click(url.strip(), selector.strip())

    if text.startswith("browser fill "):
        command = user_input.replace("browser fill ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: browser fill URL ::: CSS_SELECTOR ::: VALUE"

        parts = command.split(":::", 2)

        if len(parts) != 3:
            return "Invalid format. Use: browser fill URL ::: CSS_SELECTOR ::: VALUE"

        url, selector, value = parts
        return request_browser_fill(url.strip(), selector.strip(), value.strip())

    if text.startswith("confirm browser action "):
        action_id = user_input.replace("confirm browser action ", "", 1).strip()
        return confirm_browser_action(action_id)

    if text in ["browser approvals", "list browser approvals", "pending browser actions"]:
        return list_browser_approvals()

    if text.startswith("google results "):
        query = user_input.replace("google results ", "", 1).strip()
        return browser_google_results(query)

    if text.startswith("serp check "):
        command = user_input.replace("serp check ", "", 1).strip()

        if ":::" not in command:
            return "Invalid format. Use: serp check KEYWORD ::: DOMAIN"

        keyword, domain = command.split(":::", 1)
        return seo_serp_checker(keyword.strip(), domain.strip())

    return None