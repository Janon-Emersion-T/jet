from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from core.memory import init_memory, save_memory
from core.command_router import route_command
from core.capabilities import list_capabilities
from core.memory_search import list_facts, search_memory
from core.project_diagnostics import interpret_project_diagnostics
from core.code_reviewer import review_code_file
from tools.system_tools import read_project_file

from tools.weather_location_tools import (
    save_current_location,
    get_saved_location,
    detect_location_by_ip,
)

from core.models.model_config import load_model_settings, save_model_settings
from core.models.ollama_manager import list_ollama_models, pull_ollama_model, test_ollama_model
from core.models.model_router import detect_model_route, explain_model_route
from core.models.prompt_templates import load_prompt_templates, save_prompt_templates
from core.models.model_performance import load_model_performance, benchmark_model
from core.models.model_router import get_model_with_fallback


app = FastAPI(title="JARVIS Local API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_memory()


class ChatRequest(BaseModel):
    message: str


class SearchMemoryRequest(BaseModel):
    query: str


class ProjectRequest(BaseModel):
    path: str


class FileRequest(BaseModel):
    path: str


class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None
    source: str = "browser"


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "JARVIS Local API"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = route_command(request.message)
    save_memory(request.message, response)

    return {
        "user": request.message,
        "response": response
    }


@app.get("/capabilities")
def capabilities():
    return {
        "capabilities": list_capabilities()
    }


@app.get("/facts")
def facts():
    return {
        "facts": list_facts()
    }


@app.post("/memory/search")
def memory_search(request: SearchMemoryRequest):
    return {
        "results": search_memory(request.query)
    }


@app.post("/project/analyze")
def project_analyze(request: ProjectRequest):
    return {
        "report": interpret_project_diagnostics(request.path)
    }


@app.post("/file/read")
def file_read(request: FileRequest):
    return {
        "content": read_project_file(request.path)
    }


@app.post("/file/review")
def file_review(request: FileRequest):
    return {
        "review": review_code_file(request.path)
    }


@app.post("/location/save")
def location_save(request: LocationRequest):
    return save_current_location(
        latitude=request.latitude,
        longitude=request.longitude,
        accuracy=request.accuracy,
        source=request.source,
    )


@app.get("/location/current")
def location_current():
    location = get_saved_location()

    if not location:
        return {
            "ok": False,
            "message": "No location saved yet."
        }

    return {
        "ok": True,
        "location": location
    }

@app.post("/location/detect-ip")
def location_detect_ip():
    return detect_location_by_ip()


@app.get("/models/settings")
async def get_model_settings():
    return load_model_settings()


@app.post("/models/settings")
async def update_model_settings(payload: dict):
    return save_model_settings(payload)


@app.get("/models/ollama")
async def get_ollama_models():
    return list_ollama_models()


@app.post("/models/ollama/pull")
async def pull_model(payload: dict):
    model = payload.get("model")

    if not model:
        return {"ok": False, "error": "Model name is required."}

    return pull_ollama_model(model)


@app.post("/models/ollama/test")
async def test_model(payload: dict):
    model = payload.get("model")

    if not model:
        return {"ok": False, "error": "Model name is required."}

    return test_ollama_model(model)


@app.post("/models/route")
async def route_model(payload: dict):
    message = payload.get("message", "")
    return detect_model_route(message)


@app.post("/models/route/explain")
async def explain_route(payload: dict):
    message = payload.get("message", "")
    return {"explanation": explain_model_route(message)}


@app.get("/prompts/templates")
async def get_prompt_templates():
    return load_prompt_templates()


@app.post("/prompts/templates")
async def update_prompt_templates(payload: dict):
    return save_prompt_templates(payload)


@app.get("/models/performance")
async def get_model_performance():
    return load_model_performance()


@app.post("/models/performance/test")
async def test_model_performance(payload: dict):
    model = payload.get("model")

    if not model:
        return {"ok": False, "error": "Model name is required."}

    return benchmark_model(model)


@app.post("/models/fallback")
async def model_fallback(payload: dict):
    message = payload.get("message", "")
    return get_model_with_fallback(message)