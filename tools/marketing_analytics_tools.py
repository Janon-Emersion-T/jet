from pathlib import Path
import json
import re
from urllib.parse import urlparse

from tools.project_context_tools import get_current_project_path


def _project():
    project = get_current_project_path()
    if not project:
        return None, "No current project selected.\nUse: use project <path>"
    return project, None


def _read_text(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except Exception:
        return ""


def _find_files(project: Path, extensions):
    results = []
    ignored = {"venv", "node_modules", ".git", "storage", "vendor", "__pycache__"}

    for path in project.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in extensions:
            results.append(path)

    return results[:200]


def _scan_project_text(project: Path):
    files = _find_files(project, {".py", ".php", ".js", ".jsx", ".ts", ".tsx", ".html", ".blade.php", ".vue"})
    content = []

    for file in files:
        text = _read_text(file)
        if text:
            content.append((file, text))

    return content


def _count_matches(content, patterns):
    matches = []

    for file, text in content:
        lowered = text.lower()
        for label, pattern in patterns.items():
            if pattern.lower() in lowered:
                matches.append((label, file))

    return matches


def _detect_tracking(project: Path):
    content = _scan_project_text(project)

    patterns = {
        "Google Analytics / gtag": "gtag(",
        "Google Tag Manager": "googletagmanager.com/gtm.js",
        "Google Ads conversion": "google_conversion",
        "Meta Pixel": "fbq(",
        "Microsoft Clarity": "clarity(",
        "Search Console verification": "google-site-verification",
        "Bing verification": "msvalidate.01",
    }

    return _count_matches(content, patterns)


def _format_matches(matches):
    if not matches:
        return "- No tracking or verification snippets detected."

    lines = []
    for label, file in matches[:30]:
        lines.append(f"- {label}: {file}")
    return "\n".join(lines)


def _extract_pages(project: Path):
    files = _find_files(project, {".html", ".php", ".blade.php", ".jsx", ".tsx", ".vue"})
    pages = []

    for file in files:
        text = _read_text(file).lower()
        score = 0

        if "<form" in text:
            score += 2
        if "contact" in text:
            score += 1
        if "quote" in text or "pricing" in text:
            score += 1
        if "button" in text or "btn" in text:
            score += 1
        if "hero" in text:
            score += 1
        if "testimonial" in text:
            score += 1

        if score > 0:
            pages.append((file, score))

    pages.sort(key=lambda item: item[1], reverse=True)
    return pages[:20]


def google_analytics_assistant() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)

    return f"""GOOGLE ANALYTICS ASSISTANT — PHASE 301

Project: {project}

Tracking detection:
{_format_matches(matches)}

What this phase checks:
- GA4 / gtag presence
- Google Tag Manager presence
- Basic analytics readiness
- Whether tracking appears inside project files

Recommended setup:
1. Use Google Tag Manager as the main container.
2. Add GA4 through GTM.
3. Track key events:
   - form_submit
   - phone_click
   - whatsapp_click
   - quote_request
   - purchase
   - lead_generated
4. Keep event names clean and business-focused.

Safety:
Read-only inspection. No analytics code was inserted."""


def search_console_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)
    robots = project / "public" / "robots.txt"
    sitemap = project / "public" / "sitemap.xml"

    return f"""SEARCH CONSOLE ANALYZER — PHASE 302

Project: {project}

Verification detection:
{_format_matches([m for m in matches if "Search Console" in m[0]])}

SEO file check:
- robots.txt: {"FOUND" if robots.exists() else "NOT FOUND"}
- sitemap.xml: {"FOUND" if sitemap.exists() else "NOT FOUND"}

Recommended checks:
1. Confirm domain property is verified.
2. Submit sitemap.xml.
3. Inspect indexed pages.
4. Review coverage issues.
5. Review page experience and Core Web Vitals.
6. Check top queries with high impressions but low CTR.

Safety:
Read-only inspection. No Search Console changes were made."""


def bing_webmaster_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)
    bing_matches = [m for m in matches if "Bing" in m[0]]

    return f"""BING WEBMASTER ANALYZER — PHASE 303

Project: {project}

Bing verification detection:
{_format_matches(bing_matches)}

Recommended checks:
1. Verify the domain in Bing Webmaster Tools.
2. Import from Google Search Console if available.
3. Submit sitemap.xml.
4. Check crawl issues.
5. Review keyword performance.
6. Compare Bing impressions against Google Search Console.

Safety:
Read-only inspection. No Bing configuration was changed."""


def ad_campaign_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    pages = _extract_pages(project)

    lines = []
    if pages:
        for file, score in pages:
            lines.append(f"- {file} | conversion relevance score: {score}")
    else:
        lines.append("- No obvious landing/conversion pages detected.")

    return f"""AD CAMPAIGN ANALYZER — PHASE 304

Project: {project}

Potential landing pages:
{chr(10).join(lines)}

Campaign review framework:
1. Check destination URL accuracy.
2. Confirm search intent matches landing page message.
3. Separate brand, service, competitor, and remarketing campaigns.
4. Avoid mixing Display Network with Search unless intentional.
5. Track conversions before scaling spend.
6. Review wasted spend from irrelevant search terms.

Safety:
Read-only advisor. No ad campaign was modified."""


def google_ads_assistant() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)
    ads_matches = [m for m in matches if "Google Ads" in m[0] or "gtag" in m[0] or "Tag Manager" in m[0]]

    return f"""GOOGLE ADS ASSISTANT — PHASE 305

Project: {project}

Google Ads / tracking readiness:
{_format_matches(ads_matches)}

Recommended Google Ads structure:
- Campaign 1: Brand search
- Campaign 2: High-intent service search
- Campaign 3: Location-based search
- Campaign 4: Remarketing
- Campaign 5: Competitor campaign only if legally and strategically safe

Conversion events to configure:
- Lead form submit
- WhatsApp click
- Phone click
- Purchase / checkout
- Quote request

Safety:
Read-only advisor. No Google Ads API call was made."""


def meta_ads_assistant() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)
    meta_matches = [m for m in matches if "Meta" in m[0]]

    return f"""META ADS ASSISTANT — PHASE 306

Project: {project}

Meta Pixel detection:
{_format_matches(meta_matches)}

Recommended Meta campaign structure:
1. Awareness campaign for cold audience.
2. Engagement campaign for social proof.
3. Lead campaign for quote requests.
4. Retargeting campaign for visitors and engagers.
5. Lookalike campaign after enough conversion data exists.

Recommended events:
- PageView
- ViewContent
- Lead
- Contact
- CompleteRegistration
- Purchase, if e-commerce exists

Safety:
Read-only advisor. No Meta Ads changes were made."""


def ctr_optimization_advisor() -> str:
    project, error = _project()
    if error:
        return error

    return f"""CTR OPTIMIZATION ADVISOR — PHASE 307

Project: {project}

CTR improvement checklist:
1. Align title/headline with user intent.
2. Put the strongest value proposition early.
3. Use numbers where truthful.
4. Add location when local intent matters.
5. Avoid generic wording like "best service" without proof.
6. Use emotional but credible hooks.
7. Match ad headline, meta title, and landing page hero.

Good CTR angle examples:
- Before: Web Development Services
- Better: Laravel Web Development for Growing Businesses
- Stronger: High-Converting Laravel Websites Built for Serious Businesses

Safety:
Read-only advisor. No content was changed."""


def landing_page_conversion_analyzer() -> str:
    project, error = _project()
    if error:
        return error

    pages = _extract_pages(project)

    lines = []
    if pages:
        for file, score in pages:
            lines.append(f"- {file} | conversion relevance score: {score}")
    else:
        lines.append("- No obvious conversion-focused pages detected.")

    return f"""LANDING PAGE CONVERSION ANALYZER — PHASE 308

Project: {project}

Candidate landing pages:
{chr(10).join(lines)}

Conversion checklist:
1. Clear hero headline.
2. One primary CTA above the fold.
3. Fast loading speed.
4. Trust signals near CTA.
5. Simple form with minimum fields.
6. Strong mobile layout.
7. No distracting navigation for paid traffic pages.
8. Message match between ad and landing page.

Safety:
Read-only inspection. No landing page file was modified."""


def heatmap_interpretation_engine() -> str:
    project, error = _project()
    if error:
        return error

    matches = _detect_tracking(project)
    clarity_matches = [m for m in matches if "Clarity" in m[0]]

    return f"""HEATMAP INTERPRETATION ENGINE — PHASE 309

Project: {project}

Heatmap tool detection:
{_format_matches(clarity_matches)}

How to interpret heatmaps:
1. Rage clicks usually mean broken expectation or poor UI clarity.
2. Dead clicks mean users think something is clickable.
3. Scroll drop-off means the page loses value before the CTA.
4. Repeated back-and-forth movement means confusion.
5. Mobile heatmaps matter more than desktop for consumer traffic.
6. Paid traffic recordings must be checked separately from organic traffic.

Recommended tools:
- Microsoft Clarity for free session recordings.
- GA4 events for measurable validation.
- Search Console for organic intent.

Safety:
Read-only advisor. No heatmap script was inserted."""


def funnel_analysis_assistant() -> str:
    project, error = _project()
    if error:
        return error

    return f"""FUNNEL ANALYSIS ASSISTANT — PHASE 310

Project: {project}

Recommended funnel model:
1. Impression
2. Click
3. Landing page view
4. Engagement
5. CTA click
6. Form start
7. Form submit
8. Lead qualification
9. Sale / conversion

Common funnel leaks:
- High impressions, low CTR: weak headline or wrong keyword.
- High CTR, low engagement: bad landing page match.
- High engagement, low CTA: weak offer or poor CTA placement.
- High form start, low submit: form friction.
- Many leads, few sales: targeting or qualification issue.

Minimum tracking events:
- page_view
- cta_click
- form_start
- form_submit
- whatsapp_click
- phone_click
- conversion_success

Safety:
Read-only advisor. No funnel tracking was installed."""


def marketing_analytics_help() -> str:
    return """MARKETING / ANALYTICS COMMANDS — PHASES 301–310

301. google analytics assistant
302. search console analyzer
303. bing webmaster analyzer
304. ad campaign analyzer
305. google ads assistant
306. meta ads assistant
307. ctr optimization advisor
308. landing page conversion analyzer
309. heatmap interpretation engine
310. funnel analysis assistant"""
