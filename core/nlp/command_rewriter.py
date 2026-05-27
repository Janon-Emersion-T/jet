from typing import Dict


def rewrite_command(clean_text: str, intent: str, entities: Dict[str, str]) -> str:
    text = clean_text.strip().lower()

    if intent == "project_analysis":
        if "health" in text:
            return "project health"
        if "scan" in text or "inspect" in text or "analyze" in text:
            return "analyze project"

    if intent == "database":
        if "migration" in text:
            return "migration analyzer"
        if "schema" in text:
            return "schema visualization engine"
        if "n+1" in text or "n plus one" in text:
            return "n+1 query detector"
        return "sql query analyzer"

    if intent == "devops":
        if "nginx" in text:
            return "nginx config inspector"
        if "log" in text:
            return "log cleanup assistant"
        if "disk" in text:
            return "disk cleanup assistant"
        if "deploy" in text:
            return "deployment checklist"
        return "git status"

    if intent == "content":
        if "email" in text:
            return "draft client email"
        if "quote" in text or "quotation" in text:
            return "generate quote"
        if "proposal" in text:
            return "generate proposal"
        if "seo" in text:
            return "seo brief"
        if "blog" in text:
            return "blog ideas"
        return clean_text

    if intent == "patch_workflow":
        if "diff" in text:
            return "file diff"
        if "compare" in text:
            return "compare patch"
        if "rollback" in text:
            return "rollback proposal"
        if "apply" in text:
            return "apply proposal"
        return clean_text

    return clean_text
