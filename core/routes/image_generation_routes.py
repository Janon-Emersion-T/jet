from tools.image_generation_tools import save_image_prompt


def handle_image_generation_routes(user_input: str, text: str, clean_text: str):
    raw = user_input.lower().strip()

    commands = [
        "create image ",
        "generate image ",
        "make image ",
        "draw image ",
        "image prompt ",
        "create prompt for image ",
    ]

    for command in commands:
        if raw.startswith(command):
            prompt = user_input[len(command):].strip()
            return save_image_prompt(prompt)

    return None
