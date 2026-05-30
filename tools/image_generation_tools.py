from pathlib import Path
from datetime import datetime


IMAGE_DIR = Path("storage/generated_images/prompts")


def build_image_prompt(simple_prompt: str) -> str:
    simple_prompt = simple_prompt.strip()

    if not simple_prompt:
        return "No image idea provided."

    enhanced_prompt = f"""
Ultra high-quality professional image generation prompt:

Subject:
{simple_prompt}

Style:
Premium, cinematic, realistic, high-end commercial quality.

Details:
Sharp focus, rich lighting, clean composition, elegant depth of field,
professional color grading, visually striking, modern, polished,
advertising-grade output.

Camera / Render:
4K quality, ultra-detailed, realistic textures, balanced lighting,
premium composition, no distortion, no extra text, no watermark.

Negative prompt:
low quality, blurry, distorted, deformed, bad anatomy, messy background,
extra fingers, duplicate objects, watermark, text, logo errors.
""".strip()

    return enhanced_prompt


def save_image_prompt(simple_prompt: str) -> str:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    enhanced_prompt = build_image_prompt(simple_prompt)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = IMAGE_DIR / f"image_prompt_{timestamp}.txt"

    file_path.write_text(enhanced_prompt, encoding="utf-8")

    return (
        "IMAGE PROMPT CREATED\n\n"
        f"Simple prompt:\n{simple_prompt}\n\n"
        f"Enhanced prompt saved to:\n{file_path}\n\n"
        f"Enhanced prompt:\n{enhanced_prompt}"
    )
