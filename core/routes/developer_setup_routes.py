from tools.developer_setup_tools import (
    build_laravel_marketing_site,
    build_marketing_footer,
    check_laravel_page_status,
    infer_developer_setup_action,
    install_project_dependency,
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

    if action["action"] == "install_dependency":
        return install_project_dependency(
            action.get("package_name", ""),
            target_dir=action.get("target_dir"),
            user_input=user_input,
        )

    if action["action"] == "build_laravel_website":
        return build_laravel_marketing_site(
            target_dir=action.get("target_dir"),
            company_name=action.get("company_name", "Center for Systematic Learning"),
            page_names=action.get("pages"),
        )

    if action["action"] == "build_footer":
        return build_marketing_footer(
            target_dir=action.get("target_dir"),
            company_name=action.get("company_name", "Center for Systematic Learning"),
        )

    if action["action"] == "check_page_status":
        return check_laravel_page_status(
            action.get("page_name", ""),
            target_dir=action.get("target_dir"),
        )

    if text.startswith("install laravel project "):
        target_dir = user_input.replace("install laravel project ", "", 1).strip()
        return install_laravel_project(target_dir)

    if text.startswith("install tailwind"):
        return install_tailwind_for_project()

    if text.startswith("install ") or text.startswith("add "):
        package_name = user_input.split(maxsplit=1)[1].strip() if len(user_input.split()) > 1 else ""
        return install_project_dependency(package_name, user_input=user_input)

    return None
