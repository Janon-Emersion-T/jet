from tools.operator_tools import (
    operator_help,
    vps_deployment_assistant,
    secure_tunnel_setup,
    remote_command_gateway,
    mobile_control_interface,
    role_permission_system,
    autonomous_operator_mode,
    autonomous_coding_loop,
    self_verification_before_patching,
    multi_file_patch_generation,
    cross_file_dependency_analysis,
)


def handle_operator_routes(user_input: str, text: str, clean_text: str):
    if text in ["operator help", "jarvis operator help", "phase 211 help"]:
        return operator_help()

    if text in ["vps deployment assistant", "deployment assistant"]:
        return vps_deployment_assistant()

    if text in ["secure tunnel setup", "tunnel setup"]:
        return secure_tunnel_setup()

    if text.startswith("remote command gateway"):
        command = user_input.replace("remote command gateway", "", 1).strip()
        return remote_command_gateway(command)

    if text in ["mobile control interface", "mobile interface"]:
        return mobile_control_interface()

    if text in ["role permission system", "permission system", "roles"]:
        return role_permission_system()

    if text in ["autonomous operator mode", "operator mode"]:
        return autonomous_operator_mode()

    if text in ["autonomous coding loop", "coding loop"]:
        return autonomous_coding_loop()

    if text in ["self verification before patching", "verify before patch"]:
        return self_verification_before_patching()

    if text.startswith("multi file patch generation"):
        request = user_input.replace("multi file patch generation", "", 1).strip()
        return multi_file_patch_generation(request)

    if text in ["cross file dependency analysis", "dependency analysis"]:
        return cross_file_dependency_analysis()

    return None
