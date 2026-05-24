from tools.system_tools import write_project_file

def parse_write_command(user_input: str) -> str:
    """
    Format:
    write file /path/to/file.py ::: content here
    """

    if ":::" not in user_input:
        return "Invalid format. Use: write file /path/to/file.py ::: your content here"

    before, content = user_input.split(":::", 1)

    file_path = before.replace("write file", "", 1).strip()

    if not file_path:
        return "File path missing."

    if not content.strip():
        return "File content missing."

    return write_project_file(file_path, content.strip())