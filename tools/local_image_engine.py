from pathlib import Path
from datetime import datetime
import json
import time
import urllib.request
import urllib.error
import shutil
import random
import re


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "local_image_engine.json"

PROMPT_DIR = BASE_DIR / "storage" / "generated_images" / "prompts"
META_DIR = BASE_DIR / "storage" / "generated_images" / "metadata"


def load_image_engine_config() -> dict:
    default = {
        "enabled": True,
        "engine": "comfyui",
        "host": "127.0.0.1",
        "port": 8188,
        "checkpoint": "jarvis_checkpoints/sd_xl_base_1.0.safetensors",
        "output_dir": "/home/janon-emersion-t/Pictures/Jarvis",
        "default_width": 768,
        "default_height": 768,
        "default_steps": 25,
        "default_cfg": 7.0,
        "default_sampler": "euler",
        "default_scheduler": "normal",
        "generation_timeout_seconds": 600
    }

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default

    try:
        loaded = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        default.update(loaded)
        return default
    except Exception:
        return default


def get_output_dir() -> Path:
    config = load_image_engine_config()
    output_dir = config.get("output_dir") or "/home/janon-emersion-t/Pictures/Jarvis"
    path = Path(output_dir).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _base_url() -> str:
    config = load_image_engine_config()
    return f"http://{config['host']}:{config['port']}"


def _get_json(endpoint: str, timeout: int = 10) -> dict:
    url = f"{_base_url()}{endpoint}"
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def is_local_image_engine_running() -> bool:
    try:
        data = _get_json("/system_stats", timeout=3)
        return isinstance(data, dict)
    except Exception:
        return False


def _extract_required_values(object_info: dict, node_name: str, input_name: str) -> list:
    try:
        node = object_info[node_name]
        required = node["input"]["required"]
        value = required[input_name]

        if isinstance(value, list) and value and isinstance(value[0], list):
            return value[0]

        if isinstance(value, tuple) and value and isinstance(value[0], list):
            return value[0]

        return []
    except Exception:
        return []


def get_available_checkpoints() -> list[str]:
    try:
        object_info = _get_json("/object_info/CheckpointLoaderSimple", timeout=10)
        return _extract_required_values(object_info, "CheckpointLoaderSimple", "ckpt_name")
    except Exception:
        return []


def get_available_samplers() -> list[str]:
    try:
        object_info = _get_json("/object_info/KSampler", timeout=10)
        return _extract_required_values(object_info, "KSampler", "sampler_name")
    except Exception:
        return []


def get_available_schedulers() -> list[str]:
    try:
        object_info = _get_json("/object_info/KSampler", timeout=10)
        return _extract_required_values(object_info, "KSampler", "scheduler")
    except Exception:
        return []


def choose_checkpoint(configured_checkpoint: str) -> str:
    checkpoints = get_available_checkpoints()

    if not checkpoints:
        return configured_checkpoint

    if configured_checkpoint in checkpoints:
        return configured_checkpoint

    configured_base = Path(configured_checkpoint).name

    for ckpt in checkpoints:
        if Path(ckpt).name == configured_base:
            return ckpt

    return checkpoints[0]


def choose_sampler(configured_sampler: str) -> str:
    samplers = get_available_samplers()

    if not samplers:
        return configured_sampler

    if configured_sampler in samplers:
        return configured_sampler

    if "euler" in samplers:
        return "euler"

    return samplers[0]


def choose_scheduler(configured_scheduler: str) -> str:
    schedulers = get_available_schedulers()

    if not schedulers:
        return configured_scheduler

    if configured_scheduler in schedulers:
        return configured_scheduler

    if "normal" in schedulers:
        return "normal"

    return schedulers[0]


def make_safe_image_filename(prompt: str) -> str:
    text = prompt.lower().strip()

    replacements = {
        "lk professionals": "lkprofessionals",
        "lkprofessionals pvt ltd": "lkprofessionals",
        "lkprofessionals (pvt) ltd": "lkprofessionals",
        "lkprofessionals": "lkprofessionals",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")

    skip_words = {
        "a", "an", "the", "for", "of", "and", "with", "to", "in", "on",
        "create", "generate", "make", "image", "picture", "photo",
        "premium", "professional", "high", "quality", "cinematic", "realistic"
    }

    words = [w for w in text.split("-") if w and w not in skip_words]
    slug = "-".join(words[:8]) or "jarvis-image"
    random_number = random.randint(100000, 999999)

    return f"{slug}-{random_number}.png"


def local_image_engine_status() -> str:
    config = load_image_engine_config()
    running = is_local_image_engine_running()
    checkpoints = get_available_checkpoints() if running else []

    selected_checkpoint = choose_checkpoint(config.get("checkpoint")) if running else config.get("checkpoint")

    lines = [
        "LOCAL IMAGE ENGINE STATUS",
        "",
        f"Enabled: {'YES' if config.get('enabled') else 'NO'}",
        f"Engine: {config.get('engine')}",
        f"Address: {config.get('host')}:{config.get('port')}",
        f"Running: {'YES' if running else 'NO'}",
        f"Configured checkpoint: {config.get('checkpoint')}",
        f"Selected checkpoint: {selected_checkpoint}",
        f"Available checkpoints: {len(checkpoints)}",
        "",
        "Folders:",
        f"- Outputs: {get_output_dir()}",
        f"- Prompts: {PROMPT_DIR}",
        f"- Metadata: {META_DIR}",
        "",
        "Privacy:",
        "- Runs on 127.0.0.1 only.",
        "- No cloud API is used by this tool.",
        "- Model files are loaded from your local computer.",
    ]

    if checkpoints:
        lines.append("")
        lines.append("Detected checkpoint files:")
        for ckpt in checkpoints[:10]:
            lines.append(f"- {ckpt}")

    return "\n".join(lines)


def build_sdxl_workflow(
    prompt: str,
    negative_prompt: str,
    checkpoint: str,
    width: int,
    height: int,
    steps: int,
    cfg: float,
    sampler: str,
    scheduler: str,
    seed: int,
    filename_prefix: str,
) -> dict:
    return {
        "1": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": checkpoint
            }
        },
        "2": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": ["1", 1]
            }
        },
        "3": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["1", 1]
            }
        },
        "4": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        "5": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": scheduler,
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["2", 0],
                "negative": ["3", 0],
                "latent_image": ["4", 0]
            }
        },
        "6": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2]
            }
        },
        "7": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": filename_prefix,
                "images": ["6", 0]
            }
        }
    }


def queue_prompt(workflow: dict) -> str:
    payload = json.dumps({
        "prompt": workflow,
        "client_id": "jarvis-local-image-engine"
    }).encode("utf-8")

    request = urllib.request.Request(
        f"{_base_url()}/prompt",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["prompt_id"]

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"ComfyUI rejected the workflow.\n"
            f"HTTP status: {e.code}\n"
            f"Response body:\n{body}\n\n"
            f"Workflow sent:\n{json.dumps(workflow, indent=2)}"
        )


def get_history(prompt_id: str) -> dict:
    return _get_json(f"/history/{prompt_id}", timeout=10)


def wait_for_completion(prompt_id: str, timeout_seconds: int) -> dict:
    started = time.time()

    while time.time() - started < timeout_seconds:
        history = get_history(prompt_id)

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(2)

    raise TimeoutError("Image generation timed out.")


def extract_output_images(history_item: dict) -> list[dict]:
    images = []
    outputs = history_item.get("outputs", {})

    for node_output in outputs.values():
        for image in node_output.get("images", []):
            images.append(image)

    return images


def resolve_comfy_output_path(image_info: dict) -> Path:
    filename = image_info.get("filename")

    if not filename:
        raise FileNotFoundError("ComfyUI did not return an output filename.")

    subfolder = image_info.get("subfolder") or ""

    candidate_paths = [
        get_output_dir() / subfolder / filename,
        BASE_DIR / "engines" / "ComfyUI" / "output" / subfolder / filename,
        BASE_DIR / "storage" / "generated_images" / "outputs" / subfolder / filename,
    ]

    for path in candidate_paths:
        if path.exists():
            return path

    search_roots = [
        get_output_dir(),
        BASE_DIR / "engines" / "ComfyUI" / "output",
        BASE_DIR / "storage" / "generated_images" / "outputs",
    ]

    for root in search_roots:
        if root.exists():
            matches = list(root.rglob(filename))
            if matches:
                return matches[0]

    # ComfyUI sometimes reports filename formats slightly differently.
    stem = Path(filename).stem
    for root in search_roots:
        if root.exists():
            matches = list(root.rglob(f"{stem}*.png"))
            if matches:
                return matches[0]

    raise FileNotFoundError(
        "ComfyUI reported an output image, but JARVIS could not locate it.\n"
        f"Reported filename: {filename}\n"
        f"Reported subfolder: {subfolder}\n"
        "Checked paths:\n"
        + "\n".join(str(x) for x in candidate_paths)
    )


def generate_local_image(
    prompt: str,
    negative_prompt: str,
    width: int | None = None,
    height: int | None = None,
    steps: int | None = None,
    cfg: float | None = None,
    filename_prompt: str | None = None,
) -> dict:
    config = load_image_engine_config()

    if not config.get("enabled", True):
        return {
            "ok": False,
            "error": "Local image engine is disabled in config/local_image_engine.json"
        }

    if not is_local_image_engine_running():
        return {
            "ok": False,
            "error": "Local image engine is not running. Restart JARVIS with python3 main.py."
        }

    output_dir = get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    META_DIR.mkdir(parents=True, exist_ok=True)

    checkpoint = choose_checkpoint(config.get("checkpoint"))
    sampler = choose_sampler(config.get("default_sampler", "euler"))
    scheduler = choose_scheduler(config.get("default_scheduler", "normal"))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seed = random.randint(1, 999999999999999)
    filename_prefix = f"jarvis_temp_{timestamp}"

    width = int(width or config.get("default_width", 768))
    height = int(height or config.get("default_height", 768))
    steps = int(steps or config.get("default_steps", 25))
    cfg = float(cfg or config.get("default_cfg", 7.0))

    workflow = build_sdxl_workflow(
        prompt=prompt,
        negative_prompt=negative_prompt,
        checkpoint=checkpoint,
        width=width,
        height=height,
        steps=steps,
        cfg=cfg,
        sampler=sampler,
        scheduler=scheduler,
        seed=seed,
        filename_prefix=filename_prefix,
    )

    prompt_path = PROMPT_DIR / f"{filename_prefix}_prompt.txt"
    metadata_path = META_DIR / f"{filename_prefix}.json"

    prompt_path.write_text(prompt, encoding="utf-8")

    try:
        prompt_id = queue_prompt(workflow)

        history_item = wait_for_completion(
            prompt_id,
            timeout_seconds=int(config.get("generation_timeout_seconds", 600)),
        )

        images = extract_output_images(history_item)

        if not images:
            return {
                "ok": False,
                "error": f"Generation finished but ComfyUI returned no image. History: {json.dumps(history_item, indent=2)}"
            }

        source_path = resolve_comfy_output_path(images[0])

        if not source_path.exists():
            return {
                "ok": False,
                "error": f"Generated image was reported but not found at: {source_path}"
            }

        safe_filename = make_safe_image_filename(filename_prompt or prompt)
        final_path = output_dir / safe_filename

        if source_path != final_path:
            shutil.copy2(source_path, final_path)

        metadata = {
            "ok": True,
            "engine": "comfyui",
            "prompt_id": prompt_id,
            "checkpoint": checkpoint,
            "sampler": sampler,
            "scheduler": scheduler,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "steps": steps,
            "cfg": cfg,
            "seed": seed,
            "source_path": str(source_path),
            "image_path": str(final_path),
            "prompt_path": str(prompt_path),
            "created_at": datetime.now().isoformat(),
        }

        metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        return {
            "ok": True,
            "image_path": str(final_path),
            "prompt_path": str(prompt_path),
            "metadata_path": str(metadata_path),
            "seed": seed,
            "width": width,
            "height": height,
            "steps": steps,
            "checkpoint": checkpoint,
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }
