import json
from pathlib import Path
from datetime import datetime

from tools.command_guard import get_workspace

TASK_FILE = Path("storage/task_queue.json")


def _ensure():
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not TASK_FILE.exists():
        TASK_FILE.write_text(json.dumps([], indent=4))


def _load():
    _ensure()
    try:
        return json.loads(TASK_FILE.read_text())
    except Exception:
        return []


def _save(tasks):
    _ensure()
    TASK_FILE.write_text(json.dumps(tasks, indent=4))


def create_local_task_plan(goal: str):
    workspace, error = get_workspace()
    if error:
        return error

    steps = [
        "Inspect current project context",
        "Check git status and changed files",
        "Create project snapshot",
        "Run relevant read-only diagnostics",
        "Prepare proposed changes using safe proposal workflow",
        "Review diff before applying",
        "Apply only after confirmation",
        "Run validation checks",
        "Summarize coding session",
    ]

    lines = [
        "LOCAL TASK PLAN",
        f"Project: {workspace}",
        f"Goal: {goal}",
        "",
        "Recommended steps:",
    ]

    lines.extend(f"{i}. {step}" for i, step in enumerate(steps, start=1))
    return "\n".join(lines)


def add_task(title: str, details: str = ""):
    workspace, error = get_workspace()
    if error:
        return error

    tasks = _load()
    task_id = datetime.now().strftime("%Y%m%d%H%M%S")

    tasks.append({
        "id": task_id,
        "project": str(workspace),
        "title": title,
        "details": details,
        "status": "queued",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    })

    _save(tasks)

    return f"Task queued: {task_id} | {title}"


def list_tasks():
    tasks = _load()

    if not tasks:
        return "Task queue is empty."

    lines = ["TASK QUEUE"]
    for task in reversed(tasks[-30:]):
        lines.append(
            f"- {task['id']} | {task['status']} | {task['title']} | {task.get('project')}"
        )

    return "\n".join(lines)


def update_task_status(task_id: str, status: str):
    tasks = _load()
    found = False

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updated_at"] = datetime.now().isoformat(timespec="seconds")
            found = True
            break

    if not found:
        return "Task not found."

    _save(tasks)
    return f"Task {task_id} updated to: {status}"


def task_status(task_id: str):
    tasks = _load()

    for task in tasks:
        if task["id"] == task_id:
            return (
                "TASK STATUS\n"
                f"ID: {task['id']}\n"
                f"Title: {task['title']}\n"
                f"Status: {task['status']}\n"
                f"Project: {task.get('project')}\n"
                f"Details: {task.get('details', '')}\n"
                f"Created: {task.get('created_at')}\n"
                f"Updated: {task.get('updated_at')}"
            )

    return "Task not found."


def developer_briefing():
    workspace, error = get_workspace()
    if error:
        return error

    tasks = _load()
    project_tasks = [t for t in tasks if t.get("project") == str(workspace)]

    open_tasks = [t for t in project_tasks if t.get("status") in ["queued", "in_progress"]]
    done_tasks = [t for t in project_tasks if t.get("status") == "done"]

    return (
        "DAILY DEVELOPER BRIEFING\n"
        f"Project: {workspace}\n\n"
        f"Open tasks: {len(open_tasks)}\n"
        f"Completed tasks: {len(done_tasks)}\n\n"
        "Recommended start:\n"
        "1. Run: git status\n"
        "2. Run: snapshot project\n"
        "3. Work only through proposal/approval flows\n"
        "4. End with: coding session summary"
    )


def coding_session_summary():
    workspace, error = get_workspace()
    if error:
        return error

    tasks = _load()
    project_tasks = [t for t in tasks if t.get("project") == str(workspace)]

    recent = list(reversed(project_tasks[-10:]))

    lines = [
        "CODING SESSION SUMMARY",
        f"Project: {workspace}",
        "",
        "Recent task activity:",
    ]

    if recent:
        lines.extend(f"- {t['id']} | {t['status']} | {t['title']}" for t in recent)
    else:
        lines.append("- No task activity recorded.")

    lines.extend([
        "",
        "Close-out checklist:",
        "- Review pending proposals",
        "- Check git diff",
        "- Run relevant validation",
        "- Commit clean changes only",
    ])

    return "\n".join(lines)
