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

    if raw_text.startswith("test unified ") or raw_text.startswith("understand command "):
        from core.nlp.unified_orchestrator import format_unified_report
        query = raw_text.replace("test unified", "", 1).replace("understand command", "", 1).strip()
        return format_unified_report(query)

    if raw_text.startswith("test safety "):
        from core.nlp.safety_planner import plan_safe_command
        query = raw_text.replace("test safety", "", 1).strip()
        decision = plan_safe_command(query)
        lines = [
            "NLP-000U..000Y - SAFETY-AWARE COMMAND PLAN",
            f"Command: {query}",
            f"Action: {decision.action_type}",
            f"Safety: {decision.safety_level}",
            f"Confirmation required: {'YES' if decision.requires_confirmation else 'NO'}",
            f"Permission allowed: {'YES' if decision.allowed else 'NO'}",
        ]
        lines += [f"Reason: {reason}" for reason in decision.reasons]
        lines += [f"Alternative: {item}" for item in decision.alternatives]
        return "\n".join(lines)

    if raw_text.startswith("test targets "):
        from core.nlp.target_resolvers import resolve_targets
        query = raw_text.replace("test targets", "", 1).strip()
        targets = resolve_targets(query)
        return (
            "NLP-001G..001L - NATURAL LANGUAGE TARGET RESOLUTION\n"
            f"File: {targets.file or '-'}\nGit: {targets.git or '-'}\n"
            f"Laravel: {targets.laravel or '-'}\nServer: {targets.server or '-'}\n"
            f"Database: {targets.database or '-'}\nBrowser: {targets.browser or '-'}"
        )

    if raw_text.startswith("test task plan "):
        from core.nlp.task_planner import approval_workflow, build_task_plan
        query = raw_text.replace("test task plan", "", 1).strip()
        plan = build_task_plan(query)
        lines = ["NLP-001M..001R - MODULAR TASK PLAN"]
        lines += [
            f"{step.number}. {step.instruction} | {step.agent} | {step.tool} | "
            f"{step.action_type} | approval={step.approval_required}"
            for step in plan.steps
        ]
        lines += approval_workflow(plan)
        return "\n".join(lines)

    if raw_text.startswith("test voice "):
        from core.nlp.voice_understanding import parse_voice_intent
        query = user_input[len("test voice "):].strip()
        result = parse_voice_intent(query)
        return (
            "NLP-001Y..002D - VOICE COMMAND UNDERSTANDING\n"
            f"Clean text: {result.clean_text}\nWake word: {result.wake_word_detected}\n"
            f"Follow-up: {result.follow_up}\nConfirmation: {result.confirmation}\n"
            f"Dictation: {result.dictation or '-'}"
        )

    if raw_text.startswith("test context "):
        from core.nlp.knowledge_context import build_knowledge_context
        query = raw_text.replace("test context", "", 1).strip()
        context = build_knowledge_context(query)
        return (
            "NLP-001S..001X - PROJECT KNOWLEDGE CONTEXT\n"
            f"Handler: {context.route_handler or '-'}\n"
            f"Documentation: {context.documentation or '-'}\n"
            f"Symbols: {context.symbols or '-'}\n"
            f"Errors: {context.related_errors or '-'}\n"
            f"Missing capabilities: {context.missing_capabilities or '-'}"
        )

    if raw_text.startswith("test domain "):
        from core.nlp.domain_understanding import understand_domain
        result = understand_domain(raw_text.replace("test domain", "", 1).strip())
        return (
            "NLP-002Q..002V - DOMAIN UNDERSTANDING\n"
            f"Domain: {result.domain}\nConfidence: {result.confidence}\n"
            f"Keywords: {', '.join(result.matched_keywords) or '-'}"
        )

    if raw_text == "nlp runtime":
        from core.nlp.runtime_services import model_cache_status, profile_runtime
        runtime = profile_runtime()
        cache = model_cache_status()
        return (
            "NLP-002K..002P - OFFLINE NLP RUNTIME\n"
            f"Device: {runtime['device']}\nEmbedding model: {runtime['embedding_model']}\n"
            f"Cache locations found: {cache['available_locations'] or '-'}"
        )

    if raw_text == "nlp regression":
        from core.nlp.unified_orchestrator import orchestrate_command
        from core.nlp.quality_services import analyze_failed_commands, score_intents
        report = score_intents(
            lambda query: orchestrate_command(query, audit=False, remember=False, cache=False).intent
        )
        lines = [
            "NLP-002E..002J - NLP REGRESSION RESULT",
            f"Passed: {report.passed}/{report.total}",
            f"Accuracy: {report.accuracy}",
        ]
        lines += analyze_failed_commands(report)
        return "\n".join(lines)

    if raw_text.startswith("learn shortcut ") and ":::" in user_input:
        from core.nlp.intent_memory import learn_shortcut
        alias, command = user_input[len("learn shortcut "):].split(":::", 1)
        learn_shortcut(alias, command)
        return f"NLP shortcut learned: {alias.strip()} -> {command.strip()}"

    if raw_text in ["nlp habits", "nlp patterns", "nlp optimizations"]:
        from core.nlp.intent_memory import command_habits, intent_patterns, repeated_command_optimizations
        if raw_text == "nlp patterns":
            return f"NLP-001B - INTENT PATTERNS\n{intent_patterns()}"
        if raw_text == "nlp habits":
            return f"NLP-001C - COMMAND HABITS\n{command_habits()}"
        return "NLP-001F - OPTIMIZATIONS\n" + "\n".join(repeated_command_optimizations() or ["No repeated commands yet."])

    if raw_text == "nlp audit":
        from core.nlp.safety_planner import recent_audit_entries
        entries = recent_audit_entries()
        lines = ["NLP-000Z - AUDIT TRAIL"]
        lines += [
            f"- {entry['timestamp']} | {entry['intent']} | {entry['decision']['safety_level']} | {entry['text']}"
            for entry in entries
        ]
        return "\n".join(lines or ["No audit records."])

    if raw_text == "nlp health":
        from core.nlp.health_docs import nlp_health_check
        return nlp_health_check()

    if raw_text in ["nlp docs", "nlp documentation"]:
        from core.nlp.health_docs import generate_nlp_documentation
        return generate_nlp_documentation()

    return None
