from datetime import datetime
from pathlib import Path

from tools.project_context_tools import get_current_project_path


STORAGE_DIR = Path("storage")
RESEARCH_QUEUE_FILE = STORAGE_DIR / "research_queue.md"
LEARNING_LOOP_FILE = STORAGE_DIR / "ai_learning_loop.md"


def _project_line():
    project = get_current_project_path()
    if not project:
        return "Project: No current project selected.\nUse: use project <path>"
    return f"Project: {project}"


def _ensure_storage():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def _append_markdown(path: Path, title: str, body: str):
    _ensure_storage()
    timestamp = datetime.now().isoformat(timespec="seconds")
    entry = f"\n\n## {title}\nDate: {timestamp}\n\n{body.strip()}\n"
    path.write_text(path.read_text() + entry if path.exists() else entry)
    return str(path)


def knowledge_graph_builder(topic="current project"):
    return f"""KNOWLEDGE GRAPH BUILDER — PHASE 324

{_project_line()}

Topic: {topic}

Graph structure:
1. Main entity
2. Related people
3. Related projects
4. Related files
5. Related decisions
6. Related risks
7. Related tasks
8. Related knowledge gaps

Output format:
- Entity: {topic}
- Type: Project / Company / Client / Technical / Academic
- Connected nodes:
  - People
  - Systems
  - Documents
  - Decisions
  - Dependencies
- Missing links:
  - Unknown source
  - Unverified claim
  - Required follow-up

Safety:
Read-only graph builder. No files were modified."""


def company_knowledge_base(topic="company operations"):
    return f"""COMPANY KNOWLEDGE BASE — PHASE 325

{_project_line()}

Topic: {topic}

Knowledge base sections:
1. Company overview
2. Services
3. Products
4. Clients
5. Internal processes
6. Pricing rules
7. Technical standards
8. Marketing rules
9. Brand rules
10. Project history

Recommended storage:
- storage/company_knowledge/
- docs/company/
- docs/sop/
- docs/training/

Safety:
Read-only knowledge base planner. No company data was changed."""


def internal_wiki_generator(topic="project"):
    return f"""INTERNAL WIKI GENERATOR — PHASE 326

{_project_line()}

Wiki topic: {topic}

Wiki page structure:
# {topic.title()}

## Overview
Explain what this is and why it exists.

## Current Status
Mention what is completed, pending, blocked, or deprecated.

## Key Files
List important files and folders.

## Workflow
Explain how the work should be done.

## Decisions
Record important decisions.

## Risks
Mention known issues and limitations.

## Next Actions
List the next practical steps.

Safety:
Wiki draft only. No wiki file was created."""


def sop_documentation_assistant(process="standard process"):
    return f"""SOP DOCUMENTATION ASSISTANT — PHASE 327

{_project_line()}

Process: {process}

SOP format:
1. Purpose
2. Scope
3. Responsible person
4. Required tools
5. Step-by-step procedure
6. Quality checklist
7. Common mistakes
8. Escalation process
9. Completion criteria

SOP principle:
If a junior staff member cannot follow it without asking ten questions, the SOP is not finished.

Safety:
Documentation assistant only. No SOP was saved."""


def staff_training_assistant(topic="company workflow"):
    return f"""STAFF TRAINING ASSISTANT — PHASE 328

{_project_line()}

Training topic: {topic}

Training module:
1. Learning objective
2. Basic explanation
3. Practical example
4. Common mistakes
5. Mini task
6. Review questions
7. Completion checklist

Assessment:
- Can explain the concept
- Can follow the process
- Can complete the task
- Can identify mistakes
- Can ask the right questions

Safety:
Training content only. No staff record was updated."""


def junior_developer_tutor_mode(topic="programming"):
    return f"""JUNIOR DEVELOPER TUTOR MODE — PHASE 329

{_project_line()}

Topic: {topic}

Teaching method:
1. Explain the concept simply.
2. Show where it appears in real projects.
3. Show a small example.
4. Explain the mistake beginners usually make.
5. Give a small practice task.
6. Review the answer with constructive feedback.

Tutor rule:
Do not only give the answer. Teach the thinking pattern.

Safety:
Tutor mode only. No project files were modified."""


def ai_learning_loop_system(lesson=""):
    body = lesson.strip() or "No lesson provided."
    path = _append_markdown(
        LEARNING_LOOP_FILE,
        "AI Learning Loop Entry",
        body,
    )

    return f"""AI LEARNING LOOP SYSTEM — PHASE 330

Learning entry saved to:
{path}

Entry:
{body}

Loop process:
1. Capture lesson.
2. Store lesson.
3. Review repeated mistakes.
4. Convert useful lessons into rules.
5. Apply rules in future work.

Safety:
Only a local markdown learning note was updated."""


def autonomous_research_queue(topic=""):
    research_topic = topic.strip() or "No research topic provided."
    path = _append_markdown(
        RESEARCH_QUEUE_FILE,
        "Research Queue Item",
        research_topic,
    )

    return f"""AUTONOMOUS RESEARCH QUEUE — PHASE 331

Research item saved to:
{path}

Topic:
{research_topic}

Research workflow:
1. Define question.
2. Identify required sources.
3. Validate source quality.
4. Summarize findings.
5. Extract citations.
6. Convert results into action.

Safety:
Queue only. No web research was executed automatically."""


def research_source_validator(source=""):
    item = source.strip() or "No source provided."

    return f"""RESEARCH SOURCE VALIDATOR — PHASE 332

Source:
{item}

Validation checklist:
1. Is the author identifiable?
2. Is the publisher credible?
3. Is the date visible?
4. Is the claim supported by evidence?
5. Is there a conflict of interest?
6. Is the information current?
7. Can another reliable source confirm it?

Risk levels:
- LOW: Official documentation, academic source, government source
- MEDIUM: Reputable blog, company article, expert commentary
- HIGH: Anonymous post, outdated content, unsupported claim

Safety:
Read-only validation. No source was stored."""


def citation_aware_summarizer(text=""):
    source_text = text.strip() or "No text provided."

    return f"""CITATION-AWARE SUMMARIZER — PHASE 333

Input:
{source_text}

Summary method:
1. Separate facts from opinions.
2. Keep claims linked to sources.
3. Mark unsupported statements.
4. Avoid copying long text directly.
5. Preserve names, dates, figures, and source context.

Output template:
- Main idea:
- Key facts:
- Evidence:
- Unverified claims:
- Citation needed:
- Safe summary:

Safety:
Summary framework only. No external citation was generated."""


def academic_writing_assistant(topic="assignment"):
    return f"""ACADEMIC WRITING ASSISTANT — PHASE 334

{_project_line()}

Topic: {topic}

Academic structure:
1. Introduction
2. Background
3. Main discussion
4. Critical analysis
5. Evidence and examples
6. Limitations
7. Conclusion
8. References

Writing rules:
- Use formal academic tone.
- Avoid unsupported claims.
- Explain concepts deeply.
- Connect theory with practical examples.
- Keep paragraphs logical.
- Do not copy source wording.

Safety:
Writing assistant only. No assignment file was created."""


def plagiarism_risk_detector(text=""):
    content = text.strip() or "No text provided."

    return f"""PLAGIARISM-RISK DETECTOR — PHASE 335

Input:
{content}

Risk indicators:
1. Text sounds too close to a source.
2. No citation for specific claims.
3. Same structure as copied material.
4. Too many uncommon phrases.
5. Facts, dates, or statistics without references.
6. AI-style generic phrasing without analysis.

Recommendation:
Rewrite using your own explanation, add citations, include examples, and add critical analysis.

Safety:
Heuristic risk check only. This is not a plagiarism database scan."""


def assignment_formatting_assistant(style="standard academic"):
    return f"""ASSIGNMENT FORMATTING ASSISTANT — PHASE 336

Formatting style: {style}

Checklist:
1. Cover page
2. Table of contents
3. Clear headings
4. Page numbers
5. Consistent font
6. Proper spacing
7. Figure/table captions
8. In-text citations
9. Reference list
10. Appendix if needed

Recommended academic layout:
- Title
- Student details
- Module details
- Lecturer details
- Submission date
- Main content
- References

Safety:
Formatting guidance only. No document was modified."""


def report_generation_engine(topic="project report"):
    return f"""REPORT GENERATION ENGINE — PHASE 337

{_project_line()}

Report topic: {topic}

Report structure:
1. Executive summary
2. Introduction
3. Objectives
4. Methodology
5. Findings
6. Analysis
7. Recommendations
8. Implementation plan
9. Risks
10. Conclusion
11. References
12. Appendix

Professional rule:
A report must not only describe work. It must prove thinking, decisions, evidence, and business value.

Safety:
Report outline only. No file was generated."""


def knowledge_academic_help():
    return """KNOWLEDGE + ACADEMIC COMMANDS — PHASES 324–337

324. knowledge graph builder for <topic>
325. company knowledge base for <topic>
326. internal wiki generator for <topic>
327. sop documentation assistant for <process>
328. staff training assistant for <topic>
329. junior developer tutor mode for <topic>
330. ai learning loop system <lesson>
331. autonomous research queue <topic>
332. research source validator <source>
333. citation aware summarizer <text>
334. academic writing assistant for <topic>
335. plagiarism risk detector <text>
336. assignment formatting assistant
337. report generation engine for <topic>"""
