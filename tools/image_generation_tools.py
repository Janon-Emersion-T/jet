from pathlib import Path
from datetime import datetime
import threading
import traceback

from tools.local_image_engine import (
    generate_local_image,
    local_image_engine_status,
)

from tools.image_job_store import (
    create_image_job,
    load_image_job,
    load_latest_image_job,
    list_recent_image_jobs,
    save_image_job,
)


IMAGE_DIR = Path("storage/generated_images/prompts")


def clean_generation_prompt(prompt: str) -> str:
    import re

    prompt = prompt.strip()

    # Remove resolution tokens from the visual prompt.
    prompt = re.sub(r"\b\d{3,4}x\d{3,4}\b", "", prompt, flags=re.IGNORECASE)

    # Remove vague command residue if present.
    prompt = prompt.replace("generate image", "")
    prompt = prompt.replace("create image", "")
    prompt = prompt.replace("make image", "")
    prompt = prompt.replace("draw image", "")

    prompt = re.sub(r"\s+", " ", prompt).strip()

    return prompt


def build_image_prompt(simple_prompt: str) -> str:
    simple_prompt = clean_generation_prompt(simple_prompt)

    if not simple_prompt:
        return "No image idea provided."

    enhanced_prompt = f"""
{simple_prompt}

Premium photorealistic image, high-end studio photography, professional product photography,
luxury editorial composition, natural realistic lighting, soft shadows, elegant depth of field,
sharp subject focus, realistic materials, refined details, balanced exposure, clean background,
commercial-grade quality, realistic proportions, modern premium visual style.

Strict visual rules:
no text, no letters, no words, no captions, no watermark, no logo text, no fake typography,
no poster layout, no magazine cover, no banner, no collage, no split panels, no duplicated subject,
no distorted objects, no messy background.

Camera direction:
professional DSLR photography, 85mm lens look, realistic bokeh, high dynamic range,
crisp details, natural color grading, luxury brand campaign quality.
""".strip()

    return enhanced_prompt


def build_negative_prompt() -> str:
    return (
        "text, letters, words, typography, watermark, signature, logo text, fake text, "
        "poster, banner, collage, split screen, duplicate cake, multiple panels, "
        "low quality, blurry, pixelated, distorted, deformed, bad anatomy, bad hands, "
        "extra fingers, missing fingers, duplicate objects, ugly, amateur, messy background, "
        "poor composition, overexposed, underexposed, plastic, unrealistic proportions, "
        "mutated, noise, artifacts, jpeg artifacts, cropped subject"
    )


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


def parse_image_size_from_text(text: str) -> tuple[int, int]:
    lowered = text.lower()

    if "512x512" in lowered:
        return 512, 512

    if "768x768" in lowered:
        return 768, 768

    if "1024x1024" in lowered:
        return 1024, 1024

    if "portrait" in lowered:
        return 832, 1216

    if "landscape" in lowered:
        return 1216, 832

    if "wide" in lowered:
        return 1344, 768

    return 1024, 1024


def _run_image_job(job_id: str) -> None:
    job = load_image_job(job_id)

    if not job:
        return

    debug_log_path = Path("storage/generated_images/metadata") / f"{job_id}_debug.log"
    debug_log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(message: str):
        with debug_log_path.open("a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")

    try:
        log("Job loaded.")
        job["status"] = "running"
        job["started_at"] = datetime.now().isoformat()
        job["debug_log"] = str(debug_log_path)
        save_image_job(job)

        simple_prompt = job["prompt"]
        log(f"Simple prompt: {simple_prompt}")

        width, height = parse_image_size_from_text(simple_prompt)
        log(f"Image size: {width}x{height}")

        enhanced_prompt = build_image_prompt(simple_prompt)
        negative_prompt = build_negative_prompt()

        log("Calling local image engine.")

        result = generate_local_image(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            filename_prompt=simple_prompt,
        )

        log(f"Local image engine result: {result}")

        if not result.get("ok"):
            job["status"] = "failed"
            job["error"] = result.get("error", "Unknown image generation error.")
            job["finished_at"] = datetime.now().isoformat()
            save_image_job(job)
            log(f"Job failed: {job['error']}")
            return

        job["status"] = "completed"
        job["result"] = result
        job["finished_at"] = datetime.now().isoformat()
        save_image_job(job)
        log("Job completed successfully.")

    except Exception as e:
        error_text = f"{e}\n\n{traceback.format_exc()}"
        job["status"] = "failed"
        job["error"] = error_text
        job["finished_at"] = datetime.now().isoformat()
        save_image_job(job)
        log(f"Exception: {error_text}")

def generate_image(simple_prompt: str) -> str:
    simple_prompt = simple_prompt.strip()

    if not simple_prompt:
        return "No image idea provided."

    job = create_image_job(simple_prompt)

    thread = threading.Thread(
        target=_run_image_job,
        args=(job["job_id"],),
        daemon=True,
    )
    thread.start()

    return (
        "IMAGE GENERATION JOB STARTED\n\n"
        f"Job ID:\n{job['job_id']}\n\n"
        "JARVIS is generating the image in the background.\n\n"
        "Use this command after a while:\n"
        "image job status\n\n"
        "Or:\n"
        f"image job status {job['job_id']}"
    )


def image_job_status(job_id: str | None = None) -> str:
    if job_id:
        job = load_image_job(job_id)
    else:
        job = load_latest_image_job()

    if not job:
        return "No image generation job found."

    lines = [
        "IMAGE JOB STATUS",
        "",
        f"Job ID: {job.get('job_id')}",
        f"Status: {job.get('status')}",
        f"Created: {job.get('created_at')}",
        f"Started: {job.get('started_at') or '-'}",
        f"Finished: {job.get('finished_at') or '-'}",
        "",
        "Prompt:",
        job.get("prompt", "-"),
    ]

    if job.get("status") == "completed" and job.get("result"):
        result = job["result"]
        lines.extend([
            "",
            "Result:",
            f"Image: {result.get('image_path')}",
            f"Prompt file: {result.get('prompt_path')}",
            f"Metadata: {result.get('metadata_path')}",
            f"Checkpoint: {result.get('checkpoint')}",
            f"Size: {result.get('width')}x{result.get('height')}",
            f"Steps: {result.get('steps')}",
            f"Seed: {result.get('seed')}",
        ])

    if job.get("status") == "failed":
        lines.extend([
            "",
            "Error:",
            job.get("error") or "Unknown error",
        ])

    return "\n".join(lines)


def latest_image_result() -> str:
    job = load_latest_image_job()

    if not job:
        return "No image generation job found."

    if job.get("status") != "completed":
        return (
            "Latest image is not completed yet.\n\n"
            f"Current status: {job.get('status')}\n\n"
            "Use:\nimage job status"
        )

    result = job.get("result") or {}

    return (
        "LATEST GENERATED IMAGE\n\n"
        f"Image:\n{result.get('image_path')}\n\n"
        f"Prompt:\n{result.get('prompt_path')}\n\n"
        f"Metadata:\n{result.get('metadata_path')}"
    )


def recent_image_jobs() -> str:
    jobs = list_recent_image_jobs(limit=10)

    if not jobs:
        return "No recent image jobs found."

    lines = ["RECENT IMAGE JOBS", ""]

    for job in jobs:
        lines.append(
            f"- {job.get('job_id')} | {job.get('status')} | {job.get('created_at')} | {job.get('prompt')[:80]}"
        )

    return "\n".join(lines)


def image_generation_status() -> str:
    return local_image_engine_status()