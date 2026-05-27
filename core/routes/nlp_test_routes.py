def handle_nlp_test_routes(user_input: str, text: str, clean_text: str):
    raw_text = user_input.lower().strip()

    if raw_text.startswith("test multi intent ") or raw_text.startswith("analyze multi intent "):
        from core.nlp.multi_intent_parser import format_multi_intent_report
        query = raw_text.replace("test multi intent", "", 1).replace("analyze multi intent", "", 1).strip()
        return format_multi_intent_report(query)

    if raw_text.startswith("test execution plan ") or raw_text.startswith("plan command "):
        from core.nlp.command_execution_planner import format_execution_plan
        query = raw_text.replace("test execution plan", "", 1).replace("plan command", "", 1).strip()
        return format_execution_plan(query)

    if raw_text.startswith("test route batch ") or raw_text.startswith("prepare batch "):
        from core.nlp.route_batch_processor import format_route_batch
        query = raw_text.replace("test route batch", "", 1).replace("prepare batch", "", 1).strip()
        return format_route_batch(query)

    if raw_text.startswith("test followup v2 "):
        from core.nlp.followup_context_resolver_v2 import format_followup_v2_report
        query = raw_text.replace("test followup v2", "", 1).strip()
        return format_followup_v2_report(query)

    return None
