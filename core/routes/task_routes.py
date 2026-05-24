from tools.task_planner_tools import (
    create_local_task_plan,
    add_task,
    list_tasks,
    update_task_status,
    task_status,
    developer_briefing,
    coding_session_summary,
)

from tools.tracker_memory_tools import (
    add_tracker_item,
    list_tracker_items,
    update_tracker_status,
)


def handle_task_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("plan task "):
        goal = user_input.replace("plan task ", "", 1).strip()
        return create_local_task_plan(goal)

    if text.startswith("queue task "):
        title = user_input.replace("queue task ", "", 1).strip()
        return add_task(title)

    if text in ["task queue", "list tasks", "show tasks"]:
        return list_tasks()

    if text.startswith("task status "):
        task_id = user_input.replace("task status ", "", 1).strip()
        return task_status(task_id)

    if text.startswith("set task "):
        command = user_input.replace("set task ", "", 1).strip()
        parts = command.split()

        if len(parts) < 2:
            return "Invalid format. Use: set task TASK_ID STATUS"

        return update_task_status(parts[0], parts[1])

    if text in ["daily developer briefing", "developer briefing", "morning briefing"]:
        return developer_briefing()

    if text in ["coding session summary", "session summary"]:
        return coding_session_summary()

    if text.startswith("add bug "):
        title = user_input.replace("add bug ", "", 1).strip()
        return add_tracker_item("bug", title)

    if text in ["bug tracker", "list bugs", "show bugs"]:
        return list_tracker_items("bug")

    if text.startswith("add feature "):
        title = user_input.replace("add feature ", "", 1).strip()
        return add_tracker_item("feature", title)

    if text in ["feature tracker", "list features", "show features"]:
        return list_tracker_items("feature")

    if text.startswith("add roadmap "):
        title = user_input.replace("add roadmap ", "", 1).strip()
        return add_tracker_item("roadmap", title)

    if text in ["project roadmap", "roadmap memory", "show roadmap"]:
        return list_tracker_items("roadmap")

    if text.startswith("set tracker "):
        command = user_input.replace("set tracker ", "", 1).strip()
        parts = command.split()

        if len(parts) < 2:
            return "Invalid format. Use: set tracker ITEM_ID STATUS"

        return update_tracker_status(parts[0], parts[1])

    return None
