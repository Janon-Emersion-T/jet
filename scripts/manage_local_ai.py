#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gc
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.models.local_ai_stack import evaluate_catalog, install_target, prepare_user_services


def _print(data: object) -> None:
    print(json.dumps(data, indent=2))


def _run_diffusers(model_id: str, prompt: str, output: str | None) -> int:
    try:
        import torch
        from diffusers import ConsistencyModelPipeline, ShapEPipeline
        from diffusers.utils import export_to_gif, export_to_ply
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"Missing local-ai dependencies: {exc}"}, indent=2))
        return 1

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    output_path = Path(output or ROOT_DIR / "storage" / "local_ai" / "outputs")
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        if model_id == "openai/Shap-E":
            pipe = ShapEPipeline.from_pretrained("openai/shap-e", torch_dtype=dtype, variant="fp16" if device == "cuda" else None, use_safetensors=True)
            pipe = pipe.to(device)
            frames = pipe(prompt, guidance_scale=12.0, num_inference_steps=48, frame_size=256).images
            gif_path = output_path / "shape.gif"
            export_to_gif(frames[0], str(gif_path))
            mesh = pipe(prompt, guidance_scale=12.0, num_inference_steps=48, frame_size=256, output_type="mesh").images
            ply_path = output_path / "shape.ply"
            export_to_ply(mesh[0], str(ply_path))
            _print({"ok": True, "model": model_id, "gif": str(gif_path), "mesh": str(ply_path), "device": device})
            return 0

        if model_id == "openai/diffusers-ct_bedroom256":
            pipe = ConsistencyModelPipeline.from_pretrained("openai/diffusers-ct_bedroom256", torch_dtype=dtype)
            pipe = pipe.to(device)
            image = pipe(prompt or "bedroom interior").images[0]
            image_path = output_path / "ct_bedroom256.png"
            image.save(image_path)
            _print({"ok": True, "model": model_id, "image": str(image_path), "device": device})
            return 0

        _print({"ok": False, "error": f"Unsupported diffusers target: {model_id}"})
        return 1
    finally:
        try:
            del pipe
        except Exception:
            pass
        gc.collect()
        if "torch" in sys.modules and getattr(sys.modules["torch"], "cuda", None) and sys.modules["torch"].cuda.is_available():
            sys.modules["torch"].cuda.empty_cache()


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage local on-demand AI targets for JARVIS.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show hardware-aware local AI catalog status.")
    subparsers.add_parser("prepare", help="Install user-level ChromaDB and resource guard units.")

    install_parser = subparsers.add_parser("install", help="Install or pull one local AI target.")
    install_parser.add_argument("model_id")

    run_parser = subparsers.add_parser("run", help="Run an on-demand Diffusers target locally.")
    run_parser.add_argument("model_id")
    run_parser.add_argument("--prompt", default="A modern bedroom with warm lighting")
    run_parser.add_argument("--output")

    args = parser.parse_args()

    if args.command == "status":
        _print(evaluate_catalog())
        return 0

    if args.command == "prepare":
        _print(prepare_user_services())
        return 0

    if args.command == "install":
        _print(install_target(args.model_id))
        return 0

    if args.command == "run":
        return _run_diffusers(args.model_id, args.prompt, args.output)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
