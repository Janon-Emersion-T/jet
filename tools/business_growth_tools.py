from tools.project_context_tools import get_current_project_path


def _project_line():
    project = get_current_project_path()
    if not project:
        return "Project: No current project selected.\nUse: use project <path>"
    return f"Project: {project}"


def ab_testing_planner():
    return f"""A/B TESTING PLANNER — PHASE 311

{_project_line()}

Testing plan:
1. Test one variable at a time.
2. Start with headline, CTA, hero offer, form length, pricing display, or trust proof.
3. Define success metric before testing.
4. Run test until enough traffic is collected.
5. Keep the winning version and document why it won.

Sample test:
- Version A: Standard service headline
- Version B: Outcome-focused headline
- Metric: Form submissions or WhatsApp clicks

Safety:
Read-only planner. No page or campaign was modified."""


def cro_recommendation_engine():
    return f"""CRO RECOMMENDATION ENGINE — PHASE 312

{_project_line()}

CRO recommendations:
1. Place the main CTA above the fold.
2. Reduce form fields.
3. Add proof near decision points.
4. Match landing page message with ad/search intent.
5. Improve mobile spacing and button visibility.
6. Remove weak generic claims.
7. Add urgency only when truthful.

Priority order:
- Fix clarity first.
- Fix trust second.
- Fix friction third.
- Scale traffic last.

Safety:
Read-only recommendation engine."""


def lead_magnet_generator(topic="business"):
    return f"""LEAD MAGNET GENERATOR — PHASE 313

{_project_line()}

Topic: {topic}

Lead magnet ideas:
1. Free checklist
2. Quick audit report
3. Cost calculator
4. Industry guide
5. Template pack
6. Mistake prevention guide
7. Buyer readiness scorecard

Recommended lead magnet:
"{topic.title()} Growth Checklist"

Capture fields:
- Name
- Email
- WhatsApp
- Business type
- Main requirement

Follow-up:
Send useful value first. Sell after trust is created.

Safety:
No file, email, or automation was created."""


def marketing_automation_planner():
    return f"""MARKETING AUTOMATION PLANNER — PHASE 314

{_project_line()}

Automation flow:
1. Visitor submits form.
2. System saves lead.
3. Lead receives confirmation email.
4. Internal team receives notification.
5. Lead enters nurture sequence.
6. Sales follow-up is scheduled.
7. Conversion result is tracked.

Recommended segments:
- New lead
- Hot lead
- Cold lead
- Existing customer
- Lost opportunity

Safety:
Planning only. No automation was activated."""


def email_campaign_assistant(topic="service"):
    return f"""EMAIL CAMPAIGN ASSISTANT — PHASE 315

{_project_line()}

Campaign topic: {topic}

Email sequence:
1. Problem awareness
2. Solution education
3. Proof and credibility
4. Offer introduction
5. Objection handling
6. Final reminder

Suggested subject angles:
- How to improve {topic}
- The hidden cost of ignoring {topic}
- A better way to handle {topic}
- Quick improvement plan for {topic}

Safety:
Drafting guidance only. No email was sent."""


def newsletter_generation_engine(topic="business growth"):
    return f"""NEWSLETTER GENERATION ENGINE — PHASE 316

{_project_line()}

Newsletter topic: {topic}

Structure:
1. Strong subject line
2. Short opening insight
3. Main educational section
4. Practical takeaway
5. Soft CTA
6. Signature

Sample outline:
Subject: Practical ideas for {topic}

Opening:
This week’s focus is simple: improve one business bottleneck before adding more complexity.

Main point:
Explain the issue, show why it matters, and give one action the reader can take today.

CTA:
Ask readers to reply or book a consultation.

Safety:
Newsletter content was planned only."""


def bulk_email_workflow_planner():
    return f"""BULK EMAIL WORKFLOW PLANNER — PHASE 317

{_project_line()}

Bulk email workflow:
1. Clean the contact list.
2. Remove invalid emails.
3. Segment audience.
4. Write compliant email content.
5. Add unsubscribe option.
6. Send in controlled batches.
7. Track opens, clicks, replies, bounces, and unsubscribes.

Important:
Never blast unverified contacts like a cowboy with Wi-Fi. That damages sender reputation fast.

Safety:
Workflow planner only. No bulk email was sent."""


def cold_outreach_assistant(target="client"):
    return f"""COLD OUTREACH ASSISTANT — PHASE 318

{_project_line()}

Target: {target}

Cold outreach structure:
1. Personal opening
2. Relevant business observation
3. Clear problem
4. Short value proposition
5. Low-friction CTA

Message framework:
Hi [Name],

I noticed [specific observation]. Many businesses in your space lose opportunities because [problem].

We help with [solution] so you can [business result].

Would you be open to a quick conversation this week?

Safety:
Assistant only. No message was sent."""


def proposal_personalization_engine(client="client"):
    return f"""PROPOSAL PERSONALIZATION ENGINE — PHASE 319

{_project_line()}

Client: {client}

Personalization checklist:
1. Mention client business type.
2. Mention their current problem.
3. Align service scope with their goal.
4. Use their industry language.
5. Add relevant proof.
6. Keep pricing clear.
7. Add timeline and next step.

Proposal sections:
- Executive summary
- Client requirement
- Recommended solution
- Scope of work
- Timeline
- Investment
- Terms
- Next step

Safety:
No proposal file was generated."""


def client_requirement_extractor(text=""):
    source = text.strip() or "No client text provided."

    return f"""CLIENT REQUIREMENT EXTRACTOR — PHASE 320

Input:
{source}

Extracted requirement framework:
1. Business goal
2. Current problem
3. Required features
4. Users / roles
5. Deadline
6. Budget signal
7. Technical constraints
8. Missing questions

Recommended next action:
Convert the requirement into a scope document before quoting.

Safety:
Read-only extraction. No CRM record was created."""


def meeting_transcription_engine():
    return f"""MEETING TRANSCRIPTION ENGINE — PHASE 321

{_project_line()}

Transcription workflow:
1. Record meeting audio with consent.
2. Convert audio to text using local/offline transcription where possible.
3. Separate speakers if supported.
4. Extract decisions, tasks, risks, and deadlines.
5. Store summary under project notes.

Output format:
- Meeting title
- Date
- Attendees
- Discussion summary
- Decisions
- Action items
- Follow-up questions

Safety:
Planner only. No recording or transcription was executed."""


def audio_summarization_assistant():
    return f"""AUDIO SUMMARIZATION ASSISTANT — PHASE 322

{_project_line()}

Audio summary structure:
1. Main topic
2. Key points
3. Decisions
4. Tasks
5. Deadlines
6. People mentioned
7. Follow-up needed

Recommended local pipeline:
Audio file -> transcription -> summary -> task extraction -> project memory

Safety:
Read-only assistant. No audio file was processed."""


def voice_note_organizer():
    return f"""VOICE NOTE ORGANIZER — PHASE 323

{_project_line()}

Voice note organization:
1. Transcribe note.
2. Detect topic.
3. Detect project/client.
4. Extract tasks.
5. Extract deadlines.
6. Save under correct category.
7. Mark urgent items.

Categories:
- Ideas
- Client requirements
- Tasks
- Personal reminders
- Project decisions
- Follow-up notes

Safety:
Organizer plan only. No voice note was moved or saved."""


def business_growth_help():
    return """BUSINESS GROWTH COMMANDS — PHASES 311–323

311. ab testing planner
312. cro recommendation engine
313. lead magnet generator for <topic>
314. marketing automation planner
315. email campaign assistant for <topic>
316. newsletter generation engine for <topic>
317. bulk email workflow planner
318. cold outreach assistant for <target>
319. proposal personalization engine for <client>
320. client requirement extractor <client text>
321. meeting transcription engine
322. audio summarization assistant
323. voice note organizer"""
