from tools.image_generation_tools import (
    save_image_prompt,
    generate_image,
    image_generation_status,
    image_job_status,
    latest_image_result,
    recent_image_jobs,
)


def _extract_prompt(user_input: str, command: str) -> str:
    return user_input[len(command):].strip()


def _clean_prompt_prefix(prompt: str) -> str:
    lowered = prompt.lower().strip()

    prefixes = [
        "of ",
        "for ",
        "about ",
    ]

    for prefix in prefixes:
        if lowered.startswith(prefix):
            return prompt[len(prefix):].strip()

    return prompt.strip()


def handle_image_generation_routes(user_input: str, text: str, clean_text: str):
    raw = user_input.lower().strip()

    if raw in [
        "image generation status",
        "image generator status",
        "local image engine status",
        "local image generation status",
        "ai image status",
    ]:
        return image_generation_status()

    if raw in [
        "image job status",
        "latest image job",
        "check image job",
    ]:
        return image_job_status()

    if raw.startswith("image job status "):
        job_id = user_input[len("image job status "):].strip()
        return image_job_status(job_id)

    if raw in [
        "latest image",
        "show latest image",
        "latest generated image",
    ]:
        return latest_image_result()

    if raw in [
        "recent image jobs",
        "list image jobs",
        "image jobs",
    ]:
        return recent_image_jobs()

    prompt_only_commands = [
        "image prompt ",
        "create image prompt ",
        "create an image prompt ",
        "generate image prompt ",
        "generate an image prompt ",
        "create prompt for image ",
        "create a prompt for image ",
        "create a prompt for an image ",
    ]

    for command in prompt_only_commands:
        if raw.startswith(command):
            prompt = _extract_prompt(user_input, command)
            prompt = _clean_prompt_prefix(prompt)
            return save_image_prompt(prompt)

    generation_commands = [
        "create image ",
        "create an image ",
        "create a image ",
        "create ai image ",
        "create an ai image ",
        "create a ai image ",

        "generate image ",
        "generate an image ",
        "generate a image ",
        "generate ai image ",
        "generate an ai image ",
        "generate a ai image ",

        "make image ",
        "make an image ",
        "make a image ",
        "make ai image ",
        "make an ai image ",
        "make a ai image ",

        "draw image ",
        "draw an image ",
        "draw a image ",

        "design image ",
        "design an image ",
        "design a image ",

        "produce image ",
        "produce an image ",
        "produce a image ",
    ]

    for command in generation_commands:
        if raw.startswith(command):
            prompt = _extract_prompt(user_input, command)
            prompt = _clean_prompt_prefix(prompt)
            return generate_image(prompt)

    return None