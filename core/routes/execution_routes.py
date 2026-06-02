from tools.safe_execution_tools import (
    request_npm_run,
    request_composer_run,
    request_shell_command,
    confirm_command,
    list_command_approvals,
)


def handle_execution_routes(user_input: str, text: str, clean_text: str):
    if text.startswith("safe npm run "):
        script = user_input.replace("safe npm run ", "", 1).strip()
        return request_npm_run(script)

    if text.startswith("safe composer run "):
        script = user_input.replace("safe composer run ", "", 1).strip()
        return request_composer_run(script)

    if text.startswith("safe shell "):
        command = user_input.replace("safe shell ", "", 1).strip()
        return request_shell_command(command)

    if text.startswith("confirm command "):
        command_id = user_input.replace("confirm command ", "", 1).strip()
        return confirm_command(command_id)

    if text in ["list command approvals", "command approvals", "pending commands"]:
        return list_command_approvals()

    return None
