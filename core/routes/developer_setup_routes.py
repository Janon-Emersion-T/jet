from tools.developer_setup_tools import (
    infer_developer_setup_action,
    install_laravel_project,
    install_tailwind_for_project,
)


def handle_developer_setup_routes(user_input: str, text: str, clean_text: str):
    action = infer_developer_setup_action(user_input)

    if action["action"] == "install_laravel":
        return install_laravel_project(
            action["target_dir"],
            company_name=action.get("company_name"),
        )

    if action["action"] == "install_tailwind":
        return install_tailwind_for_project(action.get("target_dir"))

    if text.startswith("install laravel project "):
        target_dir = user_input.replace("install laravel project ", "", 1).strip()
        return install_laravel_project(target_dir)

    if text.startswith("install tailwind"):
        return install_tailwind_for_project()

    return None
