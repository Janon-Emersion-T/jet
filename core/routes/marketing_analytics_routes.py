from tools.marketing_analytics_tools import (
    google_analytics_assistant,
    search_console_analyzer,
    bing_webmaster_analyzer,
    ad_campaign_analyzer,
    google_ads_assistant,
    meta_ads_assistant,
    ctr_optimization_advisor,
    landing_page_conversion_analyzer,
    heatmap_interpretation_engine,
    funnel_analysis_assistant,
    marketing_analytics_help,
)


def handle_marketing_analytics_routes(user_input: str, text: str, clean_text: str):
    if text in ["google analytics assistant", "ga assistant", "ga4 assistant"]:
        return google_analytics_assistant()

    if text in ["search console analyzer", "google search console analyzer", "gsc analyzer"]:
        return search_console_analyzer()

    if text in ["bing webmaster analyzer", "bing webmaster tools analyzer", "bing analyzer"]:
        return bing_webmaster_analyzer()

    if text in ["ad campaign analyzer", "campaign analyzer", "ads campaign analyzer"]:
        return ad_campaign_analyzer()

    if text in ["google ads assistant", "google ads analyzer", "adwords assistant"]:
        return google_ads_assistant()

    if text in ["meta ads assistant", "facebook ads assistant", "instagram ads assistant"]:
        return meta_ads_assistant()

    if text in ["ctr optimization advisor", "ctr advisor", "ctr optimization"]:
        return ctr_optimization_advisor()

    if text in ["landing page conversion analyzer", "conversion analyzer", "landing page analyzer"]:
        return landing_page_conversion_analyzer()

    if text in ["heatmap interpretation engine", "heatmap analyzer", "heatmap interpretation"]:
        return heatmap_interpretation_engine()

    if text in ["funnel analysis assistant", "funnel analyzer", "funnel assistant"]:
        return funnel_analysis_assistant()

    if text in ["marketing analytics help", "301 310 help", "phases 301 310"]:
        return marketing_analytics_help()

    return None
