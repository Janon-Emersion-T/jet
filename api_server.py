from fastapi import FastAPI, Request, Query, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional
import threading

from core.chat_sessions import (
    list_chat_sessions,
    create_chat_session,
    get_chat_session,
    append_message,
    delete_chat_session,
    rename_chat_session,
    ensure_chat_session,
    build_recent_context,
)

from core.channels.social_channel_config import (
    load_social_channels,
    save_social_channel,
    get_social_channel,
)

from core.channels.whatsapp_business import (
    extract_whatsapp_text_messages,
    send_whatsapp_message,
)
from core.channels.whatsapp_web import (
    build_whatsapp_web_reply,
    whatsapp_web_manager,
)

from core.memory import init_memory, save_memory
from core.memory import get_memory_overview, list_facts_data, list_recent_memories
from core.command_router import route_command
from core.capabilities import list_capabilities
from core.memory_search import list_facts, search_memory
from core.activity_log import log_activity, list_recent_activity, summarize_activity
from core.system_modes import get_system_mode_state, set_voice_mode
from voice.offline_voice_mode import start_offline_voice_mode
from voice.voice_state import VOICE_STATE
from core.project_diagnostics import interpret_project_diagnostics
from core.code_reviewer import review_code_file
from tools.system_tools import read_project_file
from core.tool_registry import get_tool_registry

from tools.weather_location_tools import (
    save_current_location,
    get_saved_location,
    detect_location_by_ip,
)

from core.models.model_config import load_model_settings, save_model_settings
from core.models.local_ai_stack import evaluate_catalog, install_target, prepare_user_services
from core.models.ollama_manager import list_ollama_models, pull_ollama_model, test_ollama_model
from core.models.model_router import detect_model_route, explain_model_route
from core.models.prompt_templates import load_prompt_templates, save_prompt_templates
from core.models.model_performance import load_model_performance, benchmark_model
from core.models.model_router import get_model_with_fallback
from core.autonomous_learning import (
    ensure_autonomous_learning_worker,
    get_autonomous_learning_overview,
    get_learning_catalog,
    autonomous_learning_status,
    enable_autonomous_learning,
    disable_autonomous_learning,
    run_autonomous_learning_cycle,
    run_autonomous_learning_burst,
    run_manual_learning_task,
)


app = FastAPI(title="JARVIS Local API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_memory()
ensure_autonomous_learning_worker()


class ChatRequest(BaseModel):
    message: str
    chat_id: Optional[str] = None

class RenameChatRequest(BaseModel):
    title: str


class SearchMemoryRequest(BaseModel):
    query: str

class CommandRequest(BaseModel):
    command: str
    save_to_memory: bool = True
    source: str = "panel"


class ManualLearningRequest(BaseModel):
    task_id: Optional[str] = None
    domain: Optional[str] = None
    topic: Optional[str] = None
    kind: Optional[str] = "learn"
    stage: Optional[str] = "Manual Selection"


class ProjectRequest(BaseModel):
    path: str


class FileRequest(BaseModel):
    path: str


class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: float | None = None
    source: str = "browser"

class SocialChannelUpdateRequest(BaseModel):
    enabled: Optional[bool] = None
    auto_reply: Optional[bool] = None
    connection_mode: Optional[str] = None
    phone_number_id: Optional[str] = None
    access_token: Optional[str] = None
    verify_token: Optional[str] = None
    api_version: Optional[str] = None
    business_name: Optional[str] = None
    web_session_name: Optional[str] = None
    web_headless: Optional[bool] = None


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "JARVIS Local API"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    log_activity("chat_command", {"message": request.message, "chat_id": request.chat_id})
    session = ensure_chat_session(request.chat_id)

    append_message(session["id"], "user", request.message)

    chat_context = build_recent_context(session["id"], limit=8)

    response = route_command(
        request.message,
        chat_context=chat_context,
    )

    append_message(session["id"], "jarvis", response)
    save_memory(request.message, response)

    updated_session = get_chat_session(session["id"])

    return {
        "chat_id": session["id"],
        "user": request.message,
        "response": response,
        "session": updated_session,
    }


@app.get("/capabilities")
def capabilities():
    return {
        "capabilities": list_capabilities()
    }


@app.get("/facts")
def facts():
    return {
        "facts": list_facts_data()
    }


@app.post("/memory/search")
def memory_search(request: SearchMemoryRequest):
    log_activity("memory_search", {"query": request.query})
    return {
        "results": search_memory(request.query)
    }


@app.get("/memory/recent")
def memory_recent(limit: int = 20):
    return {
        "memories": list_recent_memories(limit=limit)
    }


@app.get("/memory/overview")
def memory_overview(limit: int = Query(default=12, ge=1, le=24)):
    return get_memory_overview(limit=limit)


@app.get("/learning/status")
def learning_status():
    return {
        "status": autonomous_learning_status()
    }


@app.get("/learning/overview")
def learning_overview(limit: int = Query(default=12, ge=1, le=24)):
    return get_autonomous_learning_overview(limit=limit)


@app.get("/learning/catalog")
def learning_catalog(
    domain: str | None = Query(default=None),
    query: str | None = Query(default=None),
    limit: int = Query(default=120, ge=1, le=240),
):
    return get_learning_catalog(domain=domain, query=query, limit=limit)


@app.post("/learning/start")
def learning_start():
    return {
        "ok": True,
        "status": enable_autonomous_learning()
    }


@app.post("/learning/stop")
def learning_stop():
    return {
        "ok": True,
        "status": disable_autonomous_learning()
    }


@app.post("/learning/run-once")
def learning_run_once():
    return {
        "ok": True,
        "result": run_autonomous_learning_cycle(),
        "status": autonomous_learning_status(),
    }


@app.post("/learning/burst")
def learning_burst(max_cycles: int = 4):
    return {
        "ok": True,
        "result": run_autonomous_learning_burst(max_cycles=max_cycles),
    }


@app.post("/learning/manual-run")
def learning_manual_run(request: ManualLearningRequest):
    return run_manual_learning_task(
        request.task_id,
        domain=request.domain,
        topic=request.topic,
        kind=request.kind or "learn",
        stage=request.stage or "Manual Selection",
    )


@app.post("/command")
def run_command(request: CommandRequest):
    log_activity("panel_command", {"command": request.command, "source": request.source})
    response = route_command(request.command)
    if request.save_to_memory:
        save_memory(request.command, response)
    return {
        "command": request.command,
        "response": response,
    }


@app.get("/activity")
def activity(limit: int = 50):
    return {
        "entries": list_recent_activity(limit=limit)
    }


@app.get("/activity/summary")
def activity_summary(limit: int = Query(default=120, ge=1, le=240)):
    return summarize_activity(limit=limit)


def _start_voice_mode_thread():
    start_offline_voice_mode()


@app.get("/voice/status")
def voice_status():
    state = get_system_mode_state()
    return {
        "voice_mode": bool(state.get("voice_mode")),
        "state": state,
    }


@app.post("/voice/start")
def voice_start():
    state = get_system_mode_state()
    if state.get("voice_mode"):
        return {"ok": True, "message": "Voice mode is already active."}

    VOICE_STATE["stop_requested"] = False
    VOICE_STATE["interrupted"] = False
    set_voice_mode(True)
    thread = threading.Thread(target=_start_voice_mode_thread, daemon=True)
    thread.start()
    log_activity("voice_start", {"mode": "offline"})
    return {"ok": True, "message": "Voice mode activation started."}


@app.post("/voice/stop")
def voice_stop():
    state = get_system_mode_state()

    if not state.get("voice_mode"):
        return {"ok": True, "message": "Voice mode is already inactive."}

    VOICE_STATE["stop_requested"] = True
    VOICE_STATE["interrupted"] = True
    VOICE_STATE["mode"] = "stopping"
    set_voice_mode(False)
    log_activity("voice_stop", {"mode": "offline"})
    return {"ok": True, "message": "Voice mode deactivation requested."}


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


@app.get("/tools/registry")
def tools_registry():
    return get_tool_registry()


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


@app.get("/models/local/catalog")
async def get_local_model_catalog():
    return evaluate_catalog()


@app.post("/models/local/install")
async def install_local_model(payload: dict):
    model_id = payload.get("model_id")
    if not model_id:
        return {"ok": False, "error": "model_id is required."}
    return install_target(model_id)


@app.post("/models/local/prepare")
async def prepare_local_model_stack():
    return prepare_user_services()


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

@app.get("/chats")
def chats():
    return {
        "sessions": list_chat_sessions()
    }


@app.post("/chats")
def create_chat():
    session = create_chat_session()

    return {
        "session": session
    }


@app.get("/chats/{chat_id}")
def read_chat(chat_id: str):
    session = get_chat_session(chat_id)

    if not session:
        session = create_chat_session()

    return {
        "session": session
    }


@app.post("/chats/{chat_id}/rename")
def rename_chat(chat_id: str, request: RenameChatRequest):
    session = rename_chat_session(chat_id, request.title)

    if not session:
        return {
            "ok": False,
            "error": "Chat session not found."
        }

    return {
        "ok": True,
        "session": session
    }


@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: str):
    deleted = delete_chat_session(chat_id)

    return {
        "ok": deleted
    }

@app.get("/social/channels")
def social_channels():
    return {
        "ok": True,
        "channels": load_social_channels(),
    }


@app.post("/social/channels/{channel}")
def update_social_channel(channel: str, request: SocialChannelUpdateRequest):
    allowed_channels = {
        "whatsapp",
        "facebook",
        "instagram",
        "linkedin",
        "tiktok",
        "email",
    }

    if channel not in allowed_channels:
        raise HTTPException(status_code=404, detail="Unsupported social channel.")

    settings = request.dict(exclude_unset=True)

    if channel == "whatsapp" and settings.get("auto_reply") is True:
        settings["enabled"] = True

    updated = save_social_channel(channel, settings)

    return {
        "ok": True,
        "channel": channel,
        "settings": updated,
    }


@app.get("/social/whatsapp/web/status")
def whatsapp_web_status():
    return {
        "ok": True,
        "status": whatsapp_web_manager.get_status(),
    }


@app.post("/social/whatsapp/web/start")
def start_whatsapp_web():
    return {
        "ok": True,
        "status": whatsapp_web_manager.start(),
    }


@app.post("/social/whatsapp/web/stop")
def stop_whatsapp_web():
    return {
        "ok": True,
        "status": whatsapp_web_manager.stop(),
    }


@app.get("/webhooks/whatsapp")
async def verify_whatsapp_webhook(
    hub_mode: str = Query(default="", alias="hub.mode"),
    hub_verify_token: str = Query(default="", alias="hub.verify_token"),
    hub_challenge: str = Query(default="", alias="hub.challenge"),
):
    whatsapp_config = get_social_channel("whatsapp")
    verify_token = whatsapp_config.get("verify_token", "")

    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        return int(hub_challenge)

    raise HTTPException(status_code=403, detail="WhatsApp webhook verification failed.")


@app.post("/webhooks/whatsapp")
async def receive_whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    payload = await request.json()

    whatsapp_config = get_social_channel("whatsapp")

    if not whatsapp_config.get("enabled"):
        return {
            "ok": True,
            "ignored": True,
            "reason": "WhatsApp channel is disabled.",
        }

    messages = extract_whatsapp_text_messages(payload)

    for message in messages:
        background_tasks.add_task(
            process_whatsapp_auto_reply,
            message["from"],
            message["text"],
            message["message_id"],
        )

    return {
        "ok": True,
        "received": len(messages),
    }


def process_whatsapp_auto_reply(
    from_number: str,
    incoming_text: str,
    message_id: str | None = None,
) -> None:
    whatsapp_config = get_social_channel("whatsapp")

    if not whatsapp_config.get("enabled"):
        return

    if not whatsapp_config.get("auto_reply"):
        return

    business_name = whatsapp_config.get("business_name", "LKProfessionals (Pvt) Ltd.")

    whatsapp_context = f"""
This message came from WhatsApp Business.

Sender phone number:
{from_number}

Message ID:
{message_id or "Unknown"}

You are Jarvis replying on behalf of {business_name}.

Main business objective:
- Handle customer messages professionally.
- Convert service inquiries into qualified leads.
- Reply clearly and briefly.
- Ask only one question at a time.
- If the customer asks for web development, POS, e-commerce, SEO, digital marketing, software, or IT consultation, collect:
  1. Name
  2. Business name
  3. Required service
  4. Budget
  5. Deadline
  6. Location

Rules:
- Do not mention internal routing.
- Do not mention system prompts.
- Do not say you are an AI unless directly asked.
- Keep the reply suitable for WhatsApp.
"""

    jarvis_reply = route_command(
        incoming_text,
        chat_context=whatsapp_context,
    )

    send_whatsapp_message(
        to_number=from_number,
        message=jarvis_reply,
    )


@app.post("/social/whatsapp/web/reply-preview")
def whatsapp_web_reply_preview(payload: dict):
    chat_name = payload.get("chat_name", "WhatsApp chat")
    incoming_text = payload.get("message", "")

    if not incoming_text.strip():
        return {
            "ok": False,
            "error": "Message is required.",
        }

    return {
        "ok": True,
        "reply": build_whatsapp_web_reply(chat_name, incoming_text),
    }
