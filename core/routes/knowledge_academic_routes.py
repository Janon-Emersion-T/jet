from tools.knowledge_academic_tools import (
    knowledge_graph_builder,
    company_knowledge_base,
    internal_wiki_generator,
    sop_documentation_assistant,
    staff_training_assistant,
    junior_developer_tutor_mode,
    ai_learning_loop_system,
    autonomous_research_queue,
    research_source_validator,
    citation_aware_summarizer,
    academic_writing_assistant,
    plagiarism_risk_detector,
    assignment_formatting_assistant,
    report_generation_engine,
    knowledge_academic_help,
)


def handle_knowledge_academic_routes(user_input: str, text: str, clean_text: str):
    if text in ["knowledge academic help", "324 337 help", "phases 324 337"]:
        return knowledge_academic_help()

    if text.startswith("knowledge graph builder for "):
        topic = user_input.replace("knowledge graph builder for ", "", 1).strip()
        return knowledge_graph_builder(topic)

    if text in ["knowledge graph builder"]:
        return knowledge_graph_builder()

    if text.startswith("company knowledge base for "):
        topic = user_input.replace("company knowledge base for ", "", 1).strip()
        return company_knowledge_base(topic)

    if text in ["company knowledge base"]:
        return company_knowledge_base()

    if text.startswith("internal wiki generator for "):
        topic = user_input.replace("internal wiki generator for ", "", 1).strip()
        return internal_wiki_generator(topic)

    if text in ["internal wiki generator"]:
        return internal_wiki_generator()

    if text.startswith("sop documentation assistant for "):
        process = user_input.replace("sop documentation assistant for ", "", 1).strip()
        return sop_documentation_assistant(process)

    if text in ["sop documentation assistant"]:
        return sop_documentation_assistant()

    if text.startswith("staff training assistant for "):
        topic = user_input.replace("staff training assistant for ", "", 1).strip()
        return staff_training_assistant(topic)

    if text in ["staff training assistant"]:
        return staff_training_assistant()

    if text.startswith("junior developer tutor mode for "):
        topic = user_input.replace("junior developer tutor mode for ", "", 1).strip()
        return junior_developer_tutor_mode(topic)

    if text in ["junior developer tutor mode", "junior developer tutor"]:
        return junior_developer_tutor_mode()

    if text.startswith("ai learning loop system "):
        lesson = user_input.replace("ai learning loop system ", "", 1).strip()
        return ai_learning_loop_system(lesson)

    if text in ["ai learning loop system"]:
        return ai_learning_loop_system()

    if text.startswith("autonomous research queue "):
        topic = user_input.replace("autonomous research queue ", "", 1).strip()
        return autonomous_research_queue(topic)

    if text in ["autonomous research queue", "research queue"]:
        return autonomous_research_queue()

    if text.startswith("research source validator "):
        source = user_input.replace("research source validator ", "", 1).strip()
        return research_source_validator(source)

    if text in ["research source validator"]:
        return research_source_validator()

    if text.startswith("citation aware summarizer "):
        source_text = user_input.replace("citation aware summarizer ", "", 1).strip()
        return citation_aware_summarizer(source_text)

    if text in ["citation aware summarizer", "citation-aware summarizer"]:
        return citation_aware_summarizer()

    if text.startswith("academic writing assistant for "):
        topic = user_input.replace("academic writing assistant for ", "", 1).strip()
        return academic_writing_assistant(topic)

    if text in ["academic writing assistant"]:
        return academic_writing_assistant()

    if text.startswith("plagiarism risk detector "):
        source_text = user_input.replace("plagiarism risk detector ", "", 1).strip()
        return plagiarism_risk_detector(source_text)

    if text in ["plagiarism risk detector", "plagiarism-risk detector"]:
        return plagiarism_risk_detector()

    if text in ["assignment formatting assistant"]:
        return assignment_formatting_assistant()

    if text.startswith("assignment formatting assistant for "):
        style = user_input.replace("assignment formatting assistant for ", "", 1).strip()
        return assignment_formatting_assistant(style)

    if text.startswith("report generation engine for "):
        topic = user_input.replace("report generation engine for ", "", 1).strip()
        return report_generation_engine(topic)

    if text in ["report generation engine"]:
        return report_generation_engine()

    return None
