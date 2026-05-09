"""
GraphMorph FastAPI entrypoint.
Run: uvicorn app.main:app --reload --port 8000
"""
import os
from pathlib import Path
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes.query import router as query_router
from app.routes.websocket import router as ws_router
from app.services.neo4j_service import neo4j_service

ROOT_ENV = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ROOT_ENV)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm Neo4j connection at boot (no-op if env unset; surfaces error early)
    try:
        neo4j_service.verify()
    except Exception as e:
        print(f"[GraphMorph] Neo4j warmup failed: {e}")
    yield
    neo4j_service.close()


app = FastAPI(
    title="GraphMorph",
    description="Agentic graph-native interface generator.",
    version="0.1.0",
    lifespan=lifespan,
)

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != [""] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, tags=["upload"])
app.include_router(query_router, tags=["query"])
app.include_router(ws_router, tags=["stream"])


@app.get("/")
def root():
    return {
        "service": "GraphMorph",
        "status": "running",
        "endpoints": ["/upload", "/query", "/ws/stream", "/health"],
    }


@app.get("/health")
def health():
    return {"ok": True, "neo4j": neo4j_service.is_alive()}
