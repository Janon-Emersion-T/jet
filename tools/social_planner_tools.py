import json
from pathlib import Path
from datetime import datetime, timedelta

CALENDAR_FILE = Path("storage/content_calendar/calendar.json")


def _ensure_calendar():
    CALENDAR_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not CALENDAR_FILE.exists():
        CALENDAR_FILE.write_text(json.dumps([], indent=4), encoding="utf-8")


def _load_calendar():
    _ensure_calendar()
    try:
        return json.loads(CALENDAR_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_calendar(items):
    _ensure_calendar()
    CALENDAR_FILE.write_text(json.dumps(items, indent=4), encoding="utf-8")


def _clean_topic(topic: str) -> str:
    return topic.strip() if topic and topic.strip() else "business technology"


def facebook_post_planner(topic: str) -> str:
    topic = _clean_topic(topic)
    return f"""FACEBOOK POST PLANNER

Topic:
{topic}

Post Angle:
Speak directly to business owners. Keep it practical, trust-building, and easy to understand.

Suggested Post:
Many businesses lose time every day because their systems are still manual, scattered, or outdated.

With the right digital solution, {topic} can improve control, reduce repeated work, and help your business move faster.

LKProfessionals (Pvt) Ltd. helps businesses build practical technology systems that support real growth.

CTA:
Message us to discuss your requirement.

Hashtags:
#LKProfessionals #BusinessGrowth #DigitalSolutions #SriLankaBusiness
"""


def linkedin_post_planner(topic: str) -> str:
    topic = _clean_topic(topic)
    return f"""LINKEDIN POST PLANNER

Topic:
{topic}

Post Angle:
Professional, strategic, founder-to-founder tone.

Suggested Post:
Modern businesses do not grow only by working harder. They grow by building better systems.

{topic} is no longer just a technical upgrade. It is an operational advantage for companies that want better visibility, stronger customer experience, and long-term scalability.

At LKProfessionals (Pvt) Ltd., we focus on building practical, maintainable, business-aligned digital solutions.

CTA:
If your business is planning its next digital step, let us start with a clear conversation.

Hashtags:
#DigitalTransformation #BusinessSystems #LKProfessionals #TechnologyStrategy
"""


def instagram_caption_planner(topic: str) -> str:
    topic = _clean_topic(topic)
    return f"""INSTAGRAM CAPTION PLANNER

Topic:
{topic}

Caption:
Your business deserves systems that work smarter — not harder.

From websites to automation, {topic} can help your brand look professional, serve customers better, and grow with confidence.

Built with care by LKProfessionals (Pvt) Ltd.

CTA:
DM us to start your digital upgrade.

Hashtags:
#LKProfessionals #WebDevelopment #DigitalMarketing #BusinessSriLanka #JaffnaBusiness
"""


def x_post_planner(topic: str) -> str:
    topic = _clean_topic(topic)
    return f"""X POST PLANNER

Topic:
{topic}

Post:
Manual work slows businesses down. Smart systems move them forward.

{topic} can help businesses improve speed, control, and customer experience.

LKProfessionals (Pvt) Ltd. builds practical digital solutions for real business growth.

#LKProfessionals #BusinessTech
"""


def tiktok_script_planner(topic: str) -> str:
    topic = _clean_topic(topic)
    return f"""TIKTOK SCRIPT PLANNER

Topic:
{topic}

Duration:
30–45 seconds

Hook:
"Your business may not be slow because of your staff. It may be slow because of your system."

Scene 1:
Show manual work, papers, spreadsheets, or delayed replies.

Voiceover:
"Many businesses still depend on outdated processes."

Scene 2:
Show website, dashboard, automation, or digital workflow.

Voiceover:
"With {topic}, your business can work faster and look more professional."

Scene 3:
Show LKProfessionals branding or service screen.

Voiceover:
"LKProfessionals (Pvt) Ltd. builds digital systems for businesses that want to grow."

CTA:
"Message us today and upgrade your business."
"""


def content_calendar(topic: str, days: int = 7) -> str:
    topic = _clean_topic(topic)
    items = _load_calendar()

    today = datetime.now()
    created = []

    platforms = ["Facebook", "LinkedIn", "Instagram", "X", "TikTok"]

    for i in range(days):
        date = (today + timedelta(days=i)).date().isoformat()
        platform = platforms[i % len(platforms)]
        item = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S") + str(i),
            "date": date,
            "platform": platform,
            "topic": topic,
            "status": "planned",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        items.append(item)
        created.append(item)

    _save_calendar(items)

    lines = [
        "CONTENT CALENDAR CREATED",
        f"Topic: {topic}",
        "",
        "Planned posts:",
    ]

    for item in created:
        lines.append(f"- {item['date']} | {item['platform']} | {item['topic']} | {item['status']}")

    return "\n".join(lines)


def list_content_calendar() -> str:
    items = _load_calendar()

    if not items:
        return "Content calendar is empty."

    lines = ["CONTENT CALENDAR"]
    for item in items[-30:]:
        lines.append(
            f"- {item['id']} | {item['date']} | {item['platform']} | {item['topic']} | {item['status']}"
        )

    return "\n".join(lines)


def social_planner_help() -> str:
    return """SOCIAL PLANNER COMMANDS — PHASES 171–176

171. facebook post planner for <topic>
172. linkedin post planner for <topic>
173. instagram caption planner for <topic>
174. x post planner for <topic>
175. tiktok script planner for <topic>
176. content calendar for <topic>
     show content calendar
"""
