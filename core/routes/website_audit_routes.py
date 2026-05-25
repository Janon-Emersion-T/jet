from tools.website_audit_tools import (
    website_audit,
    meta_tag_analyzer,
    heading_analyzer,
    image_alt_checker,
    internal_link_checker,
    broken_link_checker,
    sitemap_checker,
    robots_checker,
    page_speed_basic_checker,
    content_quality_analyzer,
)


def handle_website_audit_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("website audit "):
        url = user_input.replace("website audit ", "", 1).strip()
        return website_audit(url)

    if text.startswith("meta tag analyzer "):
        url = user_input.replace("meta tag analyzer ", "", 1).strip()
        return meta_tag_analyzer(url)

    if text.startswith("heading analyzer "):
        url = user_input.replace("heading analyzer ", "", 1).strip()
        return heading_analyzer(url)

    if text.startswith("image alt checker "):
        url = user_input.replace("image alt checker ", "", 1).strip()
        return image_alt_checker(url)

    if text.startswith("internal link checker "):
        url = user_input.replace("internal link checker ", "", 1).strip()
        return internal_link_checker(url)

    if text.startswith("broken link checker "):
        url = user_input.replace("broken link checker ", "", 1).strip()
        return broken_link_checker(url)

    if text.startswith("sitemap checker "):
        url = user_input.replace("sitemap checker ", "", 1).strip()
        return sitemap_checker(url)

    if text.startswith("robots checker "):
        url = user_input.replace("robots checker ", "", 1).strip()
        return robots_checker(url)

    if text.startswith("page speed basic checker "):
        url = user_input.replace("page speed basic checker ", "", 1).strip()
        return page_speed_basic_checker(url)

    if text.startswith("content quality analyzer "):
        url = user_input.replace("content quality analyzer ", "", 1).strip()
        return content_quality_analyzer(url)

    return None