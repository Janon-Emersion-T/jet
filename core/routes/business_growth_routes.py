from tools.business_growth_tools import (
    ab_testing_planner,
    cro_recommendation_engine,
    lead_magnet_generator,
    marketing_automation_planner,
    email_campaign_assistant,
    newsletter_generation_engine,
    bulk_email_workflow_planner,
    cold_outreach_assistant,
    proposal_personalization_engine,
    client_requirement_extractor,
    meeting_transcription_engine,
    audio_summarization_assistant,
    voice_note_organizer,
    business_growth_help,
)


def handle_business_growth_routes(user_input: str, text: str, clean_text: str):
    if text in ["business growth help", "311 323 help", "phases 311 323"]:
        return business_growth_help()

    if text in ["ab testing planner", "a/b testing planner"]:
        return ab_testing_planner()

    if text in ["cro recommendation engine", "cro engine", "conversion rate optimization engine"]:
        return cro_recommendation_engine()

    if text.startswith("lead magnet generator for "):
        topic = user_input.replace("lead magnet generator for ", "", 1).strip()
        return lead_magnet_generator(topic)

    if text in ["lead magnet generator"]:
        return lead_magnet_generator()

    if text in ["marketing automation planner", "automation planner"]:
        return marketing_automation_planner()

    if text.startswith("email campaign assistant for "):
        topic = user_input.replace("email campaign assistant for ", "", 1).strip()
        return email_campaign_assistant(topic)

    if text in ["email campaign assistant"]:
        return email_campaign_assistant()

    if text.startswith("newsletter generation engine for "):
        topic = user_input.replace("newsletter generation engine for ", "", 1).strip()
        return newsletter_generation_engine(topic)

    if text in ["newsletter generation engine", "newsletter engine"]:
        return newsletter_generation_engine()

    if text in ["bulk email workflow planner", "bulk email planner"]:
        return bulk_email_workflow_planner()

    if text.startswith("cold outreach assistant for "):
        target = user_input.replace("cold outreach assistant for ", "", 1).strip()
        return cold_outreach_assistant(target)

    if text in ["cold outreach assistant"]:
        return cold_outreach_assistant()

    if text.startswith("proposal personalization engine for "):
        client = user_input.replace("proposal personalization engine for ", "", 1).strip()
        return proposal_personalization_engine(client)

    if text in ["proposal personalization engine"]:
        return proposal_personalization_engine()

    if text.startswith("client requirement extractor "):
        source = user_input.replace("client requirement extractor ", "", 1).strip()
        return client_requirement_extractor(source)

    if text in ["client requirement extractor"]:
        return client_requirement_extractor()

    if text in ["meeting transcription engine", "meeting transcription"]:
        return meeting_transcription_engine()

    if text in ["audio summarization assistant", "audio summary assistant"]:
        return audio_summarization_assistant()

    if text in ["voice note organizer", "voice organizer"]:
        return voice_note_organizer()

    return None
