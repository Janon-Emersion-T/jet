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