from fastapi import FastAPI, Request, Query, HTTPException, BackgroundTasks
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import Optional

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
    chat_id: Optional[str] = None

class RenameChatRequest(BaseModel):
    title: str


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

class SocialChannelUpdateRequest(BaseModel):
    enabled: Optional[bool] = None
    auto_reply: Optional[bool] = None
    phone_number_id: Optional[str] = None
    access_token: Optional[str] = None
    verify_token: Optional[str] = None
    api_version: Optional[str] = None
    business_name: Optional[str] = None


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "JARVIS Local API"
    }


@app.post("/chat")
def chat(request: ChatRequest):
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
    updated = save_social_channel(channel, settings)

    return {
        "ok": True,
        "channel": channel,
        "settings": updated,
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