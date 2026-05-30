from pathlib import Path
from datetime import datetime
import json
import uuid


BASE_DIR = Path(__file__).resolve().parent.parent
JOB_DIR = BASE_DIR / "storage" / "generated_images" / "jobs"
LATEST_JOB_FILE = JOB_DIR / "latest_job.txt"


def _ensure_job_dir():
    JOB_DIR.mkdir(parents=True, exist_ok=True)


def create_image_job(prompt: str) -> dict:
    _ensure_job_dir()

    job_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:8]

    job = {
        "job_id": job_id,
        "status": "queued",
        "prompt": prompt,
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "finished_at": None,
        "result": None,
        "error": None,
    }

    save_image_job(job)
    LATEST_JOB_FILE.write_text(job_id, encoding="utf-8")

    return job


def get_job_path(job_id: str) -> Path:
    _ensure_job_dir()
    return JOB_DIR / f"{job_id}.json"


def save_image_job(job: dict) -> None:
    _ensure_job_dir()
    get_job_path(job["job_id"]).write_text(
        json.dumps(job, indent=2),
        encoding="utf-8",
    )


def load_image_job(job_id: str) -> dict | None:
    path = get_job_path(job_id)

    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_latest_image_job() -> dict | None:
    if not LATEST_JOB_FILE.exists():
        return None

    job_id = LATEST_JOB_FILE.read_text(encoding="utf-8").strip()

    if not job_id:
        return None

    return load_image_job(job_id)


def list_recent_image_jobs(limit: int = 10) -> list[dict]:
    _ensure_job_dir()

    jobs = []

    for path in sorted(JOB_DIR.glob("*.json"), reverse=True)[:limit]:
        try:
            jobs.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue

    return jobs
