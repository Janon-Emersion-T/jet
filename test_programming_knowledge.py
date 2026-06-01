from core.routes.programming_knowledge_routes import handle_programming_knowledge_routes
from tools.programming_knowledge_tools import (
    infer_programming_knowledge_action,
    list_programming_topics,
    resolve_programming_topic,
)


def test_resolve_programming_topic_aliases():
    assert resolve_programming_topic("python")["topic"] == "python"
    assert resolve_programming_topic("js")["topic"] == "javascript"
    assert resolve_programming_topic("csharp")["topic"] == "c#"
    assert resolve_programming_topic("nodejs")["topic"] == "node"


def test_infer_programming_update_action():
    action = infer_programming_knowledge_action("learn python")
    assert action["action"] == "update"
    assert action["topic"] == "python"


def test_infer_programming_update_all_action():
    action = infer_programming_knowledge_action("learn all programming languages")
    assert action["action"] == "update_all"


def test_new_curriculum_topics_are_available():
    topics = list_programming_topics()
    assert "How Computers Actually Work" in topics
    assert "software architecture fundamentals" in topics
    assert "electronics fundamentals" in topics
    assert "circuit design basics" in topics
    assert "how to remain human while building machines" in topics
    assert "how to orchestrate multiple AI agents together" in topics
    assert "how to maintain human control over increasingly autonomous systems" in topics
    assert "Master React" in topics
    assert "Build Jarvis continuously" in topics
    assert "Build autonomous knowledge ingestion pipelines" in topics
    assert "Build a fully autonomous digital operational empire for LKP" in topics
    assert "TypeScript" in topics
    assert "SQL" in topics
    assert "Protocol Buffers" in topics


def test_infer_long_form_curriculum_topic():
    action = infer_programming_knowledge_action("learn how computers actually work")
    assert action["action"] == "update"
    assert action["topic"] == "How Computers Actually Work"

    action = infer_programming_knowledge_action("learn circuit design basics")
    assert action["action"] == "update"
    assert action["topic"] == "circuit design basics"

    action = infer_programming_knowledge_action("learn how to orchestrate multiple AI agents together")
    assert action["action"] == "update"
    assert action["topic"] == "how to orchestrate multiple AI agents together"

    action = infer_programming_knowledge_action("learn c language")
    assert action["action"] == "update"
    assert action["topic"] == "C"

    action = infer_programming_knowledge_action("learn terraform language")
    assert action["action"] == "update"
    assert action["topic"] == "Terraform Language"

    action = infer_programming_knowledge_action("master react")
    assert action["action"] == "update"
    assert action["topic"] == "Master React"

    action = infer_programming_knowledge_action("build autonomous knowledge ingestion pipelines")
    assert action["action"] == "update"
    assert action["topic"] == "Build autonomous knowledge ingestion pipelines"


def test_programming_route_status(monkeypatch):
    monkeypatch.setattr(
        "core.routes.programming_knowledge_routes.programming_knowledge_status",
        lambda topic_name=None: f"STATUS:{topic_name or 'all'}",
    )

    result = handle_programming_knowledge_routes(
        "python knowledge status",
        "python knowledge status",
        "python knowledge status",
    )
    assert result == "STATUS:python"
