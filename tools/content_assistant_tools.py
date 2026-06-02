from datetime import datetime
import re


BRAND_CONTEXT = """
LKProfessionals (Pvt) Ltd. is an IT services company providing web development,
software development, SEO, digital marketing, IT consultation, automation,
business systems, and AI-assisted solutions.
Tone: professional, premium, practical, conversion-focused, Sri Lankan base with global standards.
"""


def _clean_topic(topic: str) -> str:
    return topic.strip() if topic and topic.strip() else "General business technology"


def _company_slug(name: str) -> str:
    cleaned = " ".join((name or "").split()).strip()
    return cleaned if cleaned else "Your Company"


def _slugify_topic(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned or "brand-story"


def website_content_pack(company_name: str, focus: str | None = None) -> dict:
    company_name = _company_slug(company_name)
    focus = (focus or "structured education, expert facilitation, and modern knowledge delivery").strip()

    return {
        "hero_kicker": "Systematic learning for ambitious institutions",
        "hero_title": f"{company_name} helps people learn with more structure, more clarity, and more staying power.",
        "hero_body": (
            f"{company_name} is built for organisations that want education, training, and knowledge systems "
            f"to feel deliberate instead of improvised. We combine {focus} into programs that improve both confidence and outcomes."
        ),
        "hero_cta": "Start a Learning Conversation",
        "hero_secondary_cta": "See How We Work",
        "footer_tagline": "Learning designed for depth, clarity, and real-world impact.",
        "footer_body": (
            f"{company_name} builds structured learning experiences for institutions, professionals, and communities "
            f"that want stronger outcomes without losing the human side of education."
        ),
        "about_intro": (
            f"{company_name} exists for organisations that care about long-term capability, not short-term box-ticking. "
            "We design learning systems that respect how adults actually grow: through sequence, practice, reflection, and reinforcement."
        ),
        "media_intro": (
            f"The media presence of {company_name} should extend the life of teaching. This includes lectures, interviews, "
            "resource libraries, event highlights, and public-facing educational content that stays useful after the event ends."
        ),
        "blogs_intro": (
            f"The blog at {company_name} should feel informed, readable, and trustworthy. It should publish ideas on education strategy, "
            "leadership, professional development, digital learning, and domain-specific practice."
        ),
        "contact_intro": (
            f"{company_name} works best with organisations that want to build meaningful capability, not just deliver a one-off presentation. "
            "Use this page to start conversations about workshops, advisory work, speaking, curriculum design, and partnerships."
        ),
        "brand_promise": "Serious learning systems designed with clarity, structure, and real-world transfer in mind.",
        "tone_words": ["clear", "credible", "structured", "warm", "practical", "premium"],
        "visual_direction": "Editorial clarity, premium institutional confidence, layered layouts, restrained motion, and purposeful typography.",
        "content_pillars": [
            "Learning strategy and program design",
            "Resource persons and expert facilitation",
            "Institutional partnerships and consulting",
            "Media, publishing, and knowledge assets",
            "Professional development and capability building",
        ],
        "cta_messages": [
            "Book a consultation",
            "Plan a workshop series",
            "Invite a resource person",
            "Build a learning system",
        ],
        "unsplash_queries": [
            "education workshop professionals",
            "speaker audience seminar",
            "team learning strategy",
            "modern library study collaboration",
            "professional training session",
        ],
        "page_angles": {
            "home": "Lead with trust, structure, and ambitious outcomes.",
            "about": "Explain the operating philosophy behind the company.",
            "media": "Show that content and events extend the life of teaching.",
            "blog": "Frame publishing as thoughtful, useful, and domain-driven.",
            "contact": "Make outreach feel easy, serious, and partnership-ready.",
        },
    }


def brand_voice_blueprint(company_name: str, focus: str | None = None) -> str:
    company_name = _company_slug(company_name)
    pack = website_content_pack(company_name, focus=focus)

    return f"""BRAND VOICE BLUEPRINT

Company:
{company_name}

Core promise:
{pack["brand_promise"]}

Voice attributes:
- {", ".join(pack["tone_words"])}

Voice rules:
- Sound like an experienced operator, not a hype machine.
- Explain difficult ideas simply without flattening nuance.
- Prefer confidence, clarity, and practical specificity.
- Lead with the reader's problem before the company's offer.
- Make every CTA feel like a professional next step, not a sales shove.

Messaging priorities:
1. Structure beats chaos.
2. Expertise should feel usable, not intimidating.
3. Learning should transfer into real outcomes.
4. Trust is built through clarity, proof, and consistency.

Avoid:
- Empty superlatives.
- Generic corporate filler.
- Trendy phrases that weaken credibility.
- Overly academic wording that slows readability.
"""


def content_system_pack(company_name: str, focus: str | None = None) -> str:
    company_name = _company_slug(company_name)
    pack = website_content_pack(company_name, focus=focus)
    slug = _slugify_topic(company_name)

    unsplash_links = [
        f"https://unsplash.com/s/photos/{query.replace(' ', '-')}"
        for query in pack["unsplash_queries"]
    ]

    return f"""CONTENT SYSTEM PACK

Company:
{company_name}

Brand promise:
{pack["brand_promise"]}

Visual direction:
{pack["visual_direction"]}

Content pillars:
- {pack["content_pillars"][0]}
- {pack["content_pillars"][1]}
- {pack["content_pillars"][2]}
- {pack["content_pillars"][3]}
- {pack["content_pillars"][4]}

Page strategy:
- Home: {pack["page_angles"]["home"]}
- About: {pack["page_angles"]["about"]}
- Media: {pack["page_angles"]["media"]}
- Blog: {pack["page_angles"]["blog"]}
- Contact: {pack["page_angles"]["contact"]}

Recommended CTA system:
- {pack["cta_messages"][0]}
- {pack["cta_messages"][1]}
- {pack["cta_messages"][2]}
- {pack["cta_messages"][3]}

Editorial series ideas:
1. {company_name} Field Notes
2. The {company_name} Playbook
3. Lessons from the Learning Room
4. Expert Resource Person Series
5. Strategy Briefs for Institutions

Image sourcing plan:
- Use candid, high-trust editorial photography over generic office stock.
- Prefer real people teaching, collaborating, presenting, or documenting ideas.
- Use wide establishing images for hero sections and tighter detail shots inside content.
- Keep color grading natural and premium, not oversaturated.

Unsplash sourcing shortcuts:
- {unsplash_links[0]}
- {unsplash_links[1]}
- {unsplash_links[2]}
- {unsplash_links[3]}
- {unsplash_links[4]}

Suggested content slugs:
- /insights/{slug}-field-notes
- /insights/{slug}-playbook
- /media/{slug}-resource-library
"""


def unsplash_image_plan(topic: str) -> str:
    topic = _clean_topic(topic)
    slug = _slugify_topic(topic)
    queries = [
        f"{topic} portrait",
        f"{topic} workshop",
        f"{topic} team collaboration",
        f"{topic} conference",
        f"{topic} editorial",
    ]

    lines = [
        "UNSPLASH IMAGE PLAN",
        "",
        f"Topic: {topic}",
        "",
        "Search queries:",
    ]
    lines.extend(f"- {query}" for query in queries)
    lines.extend([
        "",
        "Unsplash links:",
        *[f"- https://unsplash.com/s/photos/{_slugify_topic(query)}" for query in queries],
        "",
        "Selection rules:",
        "- Prefer human-centered photography over abstract placeholders.",
        "- Choose images with room for headline overlays when selecting hero visuals.",
        "- Avoid obvious staged handshake stock imagery.",
        "- Keep the image set visually consistent in lighting, crop style, and tone.",
        "",
        "Asset naming suggestion:",
        f"- hero-{slug}.jpg",
        f"- feature-{slug}-01.jpg",
        f"- feature-{slug}-02.jpg",
    ])
    return "\n".join(lines)


def blog_idea_generator(topic: str) -> str:
    topic = _clean_topic(topic)

    ideas = [
        f"How {topic} Can Help Businesses Reduce Manual Work",
        f"The Hidden Cost of Ignoring {topic} in Modern Business",
        f"{topic} Strategy for Small and Medium Businesses",
        f"Why Sri Lankan Businesses Should Invest in {topic}",
        f"How LKProfessionals (Pvt) Ltd. Approaches {topic} for Real Business Results",
        f"The Future of {topic}: Practical Trends Business Owners Should Watch",
        f"Common Mistakes Companies Make When Implementing {topic}",
        f"A Founder’s Guide to Choosing the Right {topic} Partner",
        f"How {topic} Improves Customer Experience and Operational Control",
        f"What Business Owners Must Know Before Investing in {topic}",
    ]

    return "BLOG IDEA GENERATOR\n\n" + "\n".join(f"{i+1}. {idea}" for i, idea in enumerate(ideas))


def seo_content_brief_creator(topic: str) -> str:
    topic = _clean_topic(topic)

    return f"""SEO CONTENT BRIEF

Topic:
{topic}

Recommended Title:
{topic}: A Practical Business Guide by LKProfessionals (Pvt) Ltd.

Search Intent:
Informational + commercial investigation.

Target Audience:
Business owners, managers, startups, SMEs, and decision-makers looking for reliable IT solutions.

Primary Keyword:
{topic.lower()}

Secondary Keywords:
- {topic.lower()} services
- {topic.lower()} company
- {topic.lower()} for business
- Sri Lanka IT solutions
- LKProfessionals (Pvt) Ltd.

Suggested Word Count:
1800–2500 words.

Content Structure:
1. Introduction
2. Why this topic matters now
3. Common business problems
4. Practical solution framework
5. Benefits for SMEs and growing businesses
6. Risks of poor implementation
7. How LKProfessionals (Pvt) Ltd. can help
8. Conclusion with CTA

CTA:
Contact LKProfessionals (Pvt) Ltd. for a professional consultation.
"""


def keyword_clustering(seed: str) -> str:
    seed = _clean_topic(seed).lower()

    return f"""KEYWORD CLUSTERING

Core Cluster:
- {seed}
- {seed} services
- {seed} company
- {seed} solutions

Commercial Cluster:
- best {seed} company
- affordable {seed} services
- professional {seed} agency
- hire {seed} experts

Local SEO Cluster:
- {seed} Sri Lanka
- {seed} Jaffna
- IT company in Jaffna
- LKProfessionals {seed}

Problem-Aware Cluster:
- why businesses need {seed}
- {seed} mistakes
- {seed} cost
- {seed} implementation challenges

Content Funnel:
Awareness → Problem education
Consideration → Comparison and benefits
Conversion → Service pages, case studies, proposals
"""


def competitor_page_analyzer(url_or_topic: str) -> str:
    target = _clean_topic(url_or_topic)

    return f"""COMPETITOR PAGE ANALYZER

Target:
{target}

Manual Analysis Checklist:
1. Page title and meta description
2. Main service promise
3. Heading structure
4. CTA placement
5. Trust signals
6. Case studies or testimonials
7. Pricing visibility
8. Technical depth
9. Content originality
10. Conversion friction

What JARVIS Can Do Now:
This is a safe offline-first framework. It does not scrape live pages unless browser/web automation is connected intentionally.

Recommended Output:
- Find competitor positioning gaps
- Improve LKProfessionals page depth
- Add stronger CTA
- Add proof, process, and case study sections
- Build better internal links
"""


def lkp_content_assistant(prompt: str) -> str:
    prompt = _clean_topic(prompt)

    return f"""LKPROFESSIONALS CONTENT ASSISTANT

Brand Context:
{BRAND_CONTEXT.strip()}

Request:
{prompt}

Recommended Direction:
Create content that sounds premium, practical, and business-focused. Avoid cheap hype. Explain the business problem first, then position LKProfessionals (Pvt) Ltd. as the reliable execution partner.

Suggested Message:
LKProfessionals (Pvt) Ltd. helps businesses move from manual, scattered, outdated operations into structured digital systems that improve visibility, control, and growth.
"""


def case_study_builder(project: str) -> str:
    project = _clean_topic(project)

    return f"""CASE STUDY BUILDER

Project:
{project}

Case Study Structure:
1. Client Background
2. Business Problem
3. Challenges Identified
4. LKProfessionals (Pvt) Ltd. Solution
5. Technologies Used
6. Implementation Process
7. Business Outcome
8. Lessons Learned
9. Future Improvements
10. CTA

Draft Angle:
This case study should show business transformation, not just technical delivery.
"""


def proposal_generator(service: str) -> str:
    service = _clean_topic(service)

    return f"""PROPOSAL GENERATOR

Service:
{service}

Proposal Sections:
1. Executive Summary
2. Client Requirement
3. Proposed Solution
4. Scope of Work
5. Deliverables
6. Timeline
7. Investment
8. Payment Terms
9. Client Responsibilities
10. Acceptance

Positioning:
LKProfessionals (Pvt) Ltd. will deliver a professional, scalable, and maintainable solution aligned with the client's business goals.
"""


def quote_generator(service: str) -> str:
    service = _clean_topic(service)

    return f"""QUOTE GENERATOR

Service:
{service}

Quotation Description:
Professional {service} service including planning, implementation, testing, revision, and delivery by LKProfessionals (Pvt) Ltd.

Suggested Quote Format:
- Service Name
- Scope
- Quantity
- Unit Price
- Total
- Payment Terms
- Validity Period
- Notes

Important:
Final price must be confirmed manually before sending to client.
"""


def client_email_draft_mode(request: str) -> str:
    request = _clean_topic(request)

    return f"""CLIENT EMAIL DRAFT MODE

Subject:
Regarding {request}

Email:
Dear Client,

Thank you for contacting LKProfessionals (Pvt) Ltd.

Based on your requirement regarding {request}, we can provide a professional solution tailored to your business needs. Our approach will focus on clear planning, reliable implementation, and long-term maintainability.

Please share any additional details, reference materials, preferred timeline, and expected budget range so we can prepare a more accurate proposal or quotation.

Best regards,
LKProfessionals (Pvt) Ltd.
"""


def social_post_generator(topic: str) -> str:
    topic = _clean_topic(topic)

    return f"""SOCIAL POST GENERATOR

Topic:
{topic}

LinkedIn/Facebook Post:
Your business does not need more confusion. It needs systems that work.

At LKProfessionals (Pvt) Ltd., we help businesses improve operations through professional IT solutions, websites, SEO, digital marketing, and business automation.

If your current process depends too much on manual work, scattered files, or outdated systems, it may be time to upgrade.

LKProfessionals (Pvt) Ltd.
Technology built for business growth.

Hashtags:
#LKProfessionals #BusinessTechnology #WebDevelopment #DigitalMarketing #SEO #SriLankaBusiness
"""


def content_assistant_help() -> str:
    return """CONTENT ASSISTANT COMMANDS — PHASES 161–170

161. blog ideas about <topic>
162. seo brief for <topic>
163. cluster keywords for <seed keyword>
164. analyze competitor page <url or topic>
165. lkp content <request>
166. build case study for <project>
167. generate proposal for <service>
168. generate quote for <service>
169. draft client email for <request>
170. social post for <topic>
171. website content for <company or brand>
172. brand voice for <company or brand>
173. content system for <company or brand>
174. unsplash plan for <topic or brand>
"""
