from tools.social_planner_tools import (
    facebook_post_planner,
    linkedin_post_planner,
    instagram_caption_planner,
    x_post_planner,
    tiktok_script_planner,
    content_calendar,
    list_content_calendar,
    social_planner_help,
)


def handle_social_planner_routes(user_input: str, text: str, clean_text: str):
    if text in ["social planner help", "content planner help"]:
        return social_planner_help()

    if text.startswith("facebook post planner for "):
        topic = user_input.replace("facebook post planner for ", "", 1).strip()
        return facebook_post_planner(topic)

    if text.startswith("linkedin post planner for "):
        topic = user_input.replace("linkedin post planner for ", "", 1).strip()
        return linkedin_post_planner(topic)

    if text.startswith("instagram caption planner for "):
        topic = user_input.replace("instagram caption planner for ", "", 1).strip()
        return instagram_caption_planner(topic)

    if text.startswith("x post planner for "):
        topic = user_input.replace("x post planner for ", "", 1).strip()
        return x_post_planner(topic)

    if text.startswith("tiktok script planner for "):
        topic = user_input.replace("tiktok script planner for ", "", 1).strip()
        return tiktok_script_planner(topic)

    if text.startswith("content calendar for "):
        topic = user_input.replace("content calendar for ", "", 1).strip()
        return content_calendar(topic)

    if text in ["show content calendar", "content calendar", "list content calendar"]:
        return list_content_calendar()

    return None
