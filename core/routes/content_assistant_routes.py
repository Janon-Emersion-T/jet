from tools.content_assistant_tools import (
    blog_idea_generator,
    seo_content_brief_creator,
    keyword_clustering,
    competitor_page_analyzer,
    lkp_content_assistant,
    case_study_builder,
    proposal_generator,
    quote_generator,
    client_email_draft_mode,
    social_post_generator,
    content_assistant_help,
)


def handle_content_assistant_routes(user_input: str, text: str, clean_text: str):
    if text in ["content assistant help", "marketing assistant help", "lkp content help"]:
        return content_assistant_help()

    if text.startswith("blog ideas about "):
        topic = user_input.replace("blog ideas about ", "", 1).strip()
        return blog_idea_generator(topic)

    if text.startswith("seo brief for "):
        topic = user_input.replace("seo brief for ", "", 1).strip()
        return seo_content_brief_creator(topic)

    if text.startswith("cluster keywords for "):
        seed = user_input.replace("cluster keywords for ", "", 1).strip()
        return keyword_clustering(seed)

    if text.startswith("analyze competitor page "):
        target = user_input.replace("analyze competitor page ", "", 1).strip()
        return competitor_page_analyzer(target)

    if text.startswith("lkp content "):
        request = user_input.replace("lkp content ", "", 1).strip()
        return lkp_content_assistant(request)

    if text.startswith("build case study for "):
        project = user_input.replace("build case study for ", "", 1).strip()
        return case_study_builder(project)

    if text.startswith("generate proposal for "):
        service = user_input.replace("generate proposal for ", "", 1).strip()
        return proposal_generator(service)

    if text.startswith("generate quote for "):
        service = user_input.replace("generate quote for ", "", 1).strip()
        return quote_generator(service)

    if text.startswith("draft client email for "):
        request = user_input.replace("draft client email for ", "", 1).strip()
        return client_email_draft_mode(request)

    if text.startswith("social post for "):
        topic = user_input.replace("social post for ", "", 1).strip()
        return social_post_generator(topic)

    return None
