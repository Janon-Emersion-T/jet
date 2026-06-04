#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "huggingface_dataset_registry.json"


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _output_dir(config: dict) -> Path:
    directory = ROOT_DIR / config.get("output_dir", "storage/huggingface_datasets")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _language_slug(value: str) -> str:
    return (
        _normalize(value)
        .replace("#", "sharp")
        .replace("++", "pp")
        .replace("/", "-")
        .replace(" ", "-")
    )


def _status_payload(config: dict) -> dict:
    out_dir = _output_dir(config)
    programming_dir = out_dir / "programming"
    tamil_dir = out_dir / "tamil"
    programming_files = sorted(programming_dir.glob("*.jsonl"))
    tamil_files = (
        sorted(p.name for p in tamil_dir.iterdir() if p.is_file() and not p.name.startswith("."))
        if tamil_dir.exists()
        else []
    )

    language_counts = {}
    for file in programming_files:
        count = 0
        with file.open("r", encoding="utf-8") as handle:
            for count, _ in enumerate(handle, start=1):
                pass
        language_counts[file.stem] = count

    return {
        "ok": True,
        "output_dir": str(out_dir),
        "programming_languages_downloaded": len(programming_files),
        "programming_language_counts": language_counts,
        "tamil_files": tamil_files,
    }


def _fetch_json(url: str, timeout: int = 60) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _fetch_rows(repo_id: str, config_name: str, split_name: str, offset: int, length: int) -> dict:
    rows_url = (
        "https://datasets-server.huggingface.co/rows"
        f"?dataset={urllib.parse.quote(repo_id, safe='')}"
        f"&config={urllib.parse.quote(config_name, safe='')}"
        f"&split={urllib.parse.quote(split_name, safe='')}"
        f"&offset={offset}&length={length}"
    )
    return _fetch_json(rows_url)


def _append_programming_sample(
    handles: dict[str, object],
    counters: Counter[str],
    out_dir: Path,
    language: str,
    row: dict,
    source_config: str,
    samples_per_language: int,
) -> bool:
    code = row.get("code") or row.get("content") or row.get("text") or ""
    if not language or not code:
        return False

    slug = _language_slug(language)
    if counters[slug] >= samples_per_language:
        return False

    path = out_dir / f"{slug}.jsonl"
    if slug not in handles:
        handles[slug] = path.open("a", encoding="utf-8")

    sample = {
        "language": language,
        "code": code,
        "repo_name": row.get("repo_name"),
        "path": row.get("path"),
        "license": row.get("license"),
        "size": row.get("size"),
        "source_config": source_config,
    }
    handles[slug].write(json.dumps(sample, ensure_ascii=False) + "\n")
    counters[slug] += 1
    return True


def download_programming(config: dict, samples_per_language: int, max_scan_rows: int) -> dict:
    for existing_file in (_output_dir(config) / "programming").glob("*.jsonl"):
        existing_file.unlink()

    out_dir = _output_dir(config) / "programming"
    out_dir.mkdir(parents=True, exist_ok=True)

    programming_cfg = config["programming"]
    repo_id = programming_cfg["repo_id"]
    expected_language_count = int(programming_cfg.get("expected_language_count", 32))
    splits_url = f"https://datasets-server.huggingface.co/splits?dataset={urllib.parse.quote(repo_id, safe='')}"
    split_payload = _fetch_json(splits_url, timeout=30)

    configs = []
    seen_configs = set()
    for item in split_payload.get("splits", []):
        config_name = item.get("config", "")
        split_name = item.get("split", "train")
        if not config_name.endswith("-all"):
            continue
        if config_name in seen_configs:
            continue
        seen_configs.add(config_name)
        configs.append((config_name, split_name))

    counters: Counter[str] = Counter()
    handles: dict[str, object] = {}
    discovered_languages: set[str] = set()
    scanned_rows = 0
    skipped_configs: dict[str, str] = {}
    fallback_batches = 0

    try:
        for config_name, split_name in configs:
            try:
                payload = _fetch_rows(repo_id, config_name, split_name, 0, samples_per_language)
            except urllib.error.HTTPError as exc:
                skipped_configs[config_name] = f"HTTP {exc.code}"
                continue
            except Exception as exc:
                skipped_configs[config_name] = str(exc)
                continue

            for item in payload.get("rows", []):
                row = item.get("row", {})
                scanned_rows += 1
                language = str(row.get("language") or config_name.rsplit("-all", 1)[0]).strip()
                if not language:
                    if scanned_rows >= max_scan_rows:
                        break
                    continue

                discovered_languages.add(language)
                _append_programming_sample(
                    handles,
                    counters,
                    out_dir,
                    language,
                    row,
                    config_name,
                    samples_per_language,
                )

            if scanned_rows >= max_scan_rows:
                break

            if len(discovered_languages) >= expected_language_count and all(
                count >= samples_per_language for count in counters.values()
            ):
                break

        if scanned_rows < max_scan_rows:
            fallback_config = programming_cfg.get("fallback_config", "all-all")
            fallback_split = programming_cfg.get("fallback_split", "train")
            batch_size = int(programming_cfg.get("fallback_batch_size", 100))

            for offset in range(0, max_scan_rows, batch_size):
                try:
                    payload = _fetch_rows(repo_id, fallback_config, fallback_split, offset, batch_size)
                except urllib.error.HTTPError as exc:
                    skipped_configs[fallback_config] = f"HTTP {exc.code}"
                    break
                except Exception as exc:
                    skipped_configs[fallback_config] = str(exc)
                    break

                rows = payload.get("rows", [])
                if not rows:
                    break

                fallback_batches += 1
                for item in rows:
                    row = item.get("row", {})
                    scanned_rows += 1
                    language = str(row.get("language") or "").strip()
                    if not language:
                        if scanned_rows >= max_scan_rows:
                            break
                        continue

                    discovered_languages.add(language)
                    _append_programming_sample(
                        handles,
                        counters,
                        out_dir,
                        language,
                        row,
                        fallback_config,
                        samples_per_language,
                    )

                    if scanned_rows >= max_scan_rows:
                        break

                if scanned_rows >= max_scan_rows:
                    break

                if len(counters) >= expected_language_count and all(
                    count >= samples_per_language for count in counters.values()
                ):
                    break
    finally:
        for handle in handles.values():
            handle.close()

    metadata_path = out_dir / "metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "repo_id": repo_id,
                "samples_per_language": samples_per_language,
                "max_scan_rows": max_scan_rows,
                "scanned_rows": scanned_rows,
                "discovered_languages": sorted(discovered_languages),
                "language_counts": dict(sorted(counters.items())),
                "skipped_configs": skipped_configs,
                "fallback_batches": fallback_batches,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "ok": True,
        "repo_id": repo_id,
        "output_dir": str(out_dir),
        "configs_used": [name for name, _ in configs],
        "scanned_rows": scanned_rows,
        "discovered_languages": sorted(discovered_languages),
        "language_counts": dict(sorted(counters.items())),
        "skipped_configs": skipped_configs,
        "fallback_batches": fallback_batches,
    }


def download_tamil(config: dict) -> dict:
    try:
        from huggingface_hub import hf_hub_download
    except Exception as exc:
        return {"ok": False, "error": f"huggingface_hub package is required: {exc}"}

    tamil_cfg = config["tamil"]
    out_dir = _output_dir(config) / "tamil"
    out_dir.mkdir(parents=True, exist_ok=True)

    downloaded: list[str] = []
    for filename in tamil_cfg.get("files", []):
        local_path = hf_hub_download(
            repo_id=tamil_cfg["repo_id"],
            repo_type=tamil_cfg.get("repo_type", "dataset"),
            filename=filename,
            local_dir=str(out_dir),
            local_dir_use_symlinks=False,
        )
        downloaded.append(local_path)

    extracted: list[str] = []
    if tamil_cfg.get("extract_archive"):
        for file in downloaded:
            path = Path(file)
            if path.suffix.lower() != ".zip":
                continue
            extract_dir = out_dir / path.stem
            extract_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(path, "r") as archive:
                archive.extractall(extract_dir)
            extracted.append(str(extract_dir))

    return {
        "ok": True,
        "repo_id": tamil_cfg["repo_id"],
        "output_dir": str(out_dir),
        "downloaded": downloaded,
        "extracted": extracted,
    }


def clear_cache(config: dict) -> dict:
    out_dir = _output_dir(config)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return {"ok": True, "output_dir": str(out_dir)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Download local Hugging Face starter datasets for JARVIS.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status")
    subparsers.add_parser("clear")

    programming_parser = subparsers.add_parser("download-programming")
    programming_parser.add_argument("--samples-per-language", type=int, default=None)
    programming_parser.add_argument("--max-scan-rows", type=int, default=None)

    subparsers.add_parser("download-tamil")
    all_parser = subparsers.add_parser("download-all")
    all_parser.add_argument("--samples-per-language", type=int, default=None)
    all_parser.add_argument("--max-scan-rows", type=int, default=None)

    args = parser.parse_args()
    config = _load_config()

    if args.command == "status":
        print(json.dumps(_status_payload(config), indent=2, ensure_ascii=False))
        return 0

    if args.command == "clear":
        print(json.dumps(clear_cache(config), indent=2, ensure_ascii=False))
        return 0

    if args.command == "download-programming":
        samples = args.samples_per_language or int(config["programming"]["default_samples_per_language"])
        max_rows = args.max_scan_rows or int(config["programming"]["default_max_scan_rows"])
        print(json.dumps(download_programming(config, samples, max_rows), indent=2, ensure_ascii=False))
        return 0

    if args.command == "download-tamil":
        print(json.dumps(download_tamil(config), indent=2, ensure_ascii=False))
        return 0

    if args.command == "download-all":
        samples = args.samples_per_language or int(config["programming"]["default_samples_per_language"])
        max_rows = args.max_scan_rows or int(config["programming"]["default_max_scan_rows"])
        payload = {
            "programming": download_programming(config, samples, max_rows),
            "tamil": download_tamil(config),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
