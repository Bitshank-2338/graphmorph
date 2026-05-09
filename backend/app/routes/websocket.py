"""
AG-UI streaming endpoint.
Streams reasoning + UI assembly events to the frontend so the workspace
appears to materialize live.

Wire from frontend with: new WebSocket('ws://localhost:8000/ws/stream')
Send: {"query": "..."}
Receive a sequence of: {"event": "reasoning"|"ui_chunk"|"complete", "data": ...}
"""
import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.ai_agent import process_query

router = APIRouter()


@router.websocket("/ws/stream")
async def stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"event": "error", "data": "invalid json"})
                continue

            query = payload.get("query", "").strip()
            if not query:
                await ws.send_json({"event": "error", "data": "empty query"})
                continue

            # Start: stream synthetic reasoning chunks while we work.
            await ws.send_json({"event": "reasoning", "data": "Analyzing graph topology..."})
            await asyncio.sleep(0.25)
            await ws.send_json({"event": "reasoning", "data": "Inferring user intent..."})
            await asyncio.sleep(0.2)

            # Heavy lifting (sync — small enough to run inline for hackathon).
            result = process_query(query)

            # Replay agent reasoning steps with small delays for visual streaming.
            for step in result["reasoning"]:
                await ws.send_json({"event": "reasoning", "data": step})
                await asyncio.sleep(0.15)

            await ws.send_json({"event": "ui_chunk", "data": {"phase": "frame"}})
            await asyncio.sleep(0.1)
            await ws.send_json({"event": "ui_chunk", "data": {"phase": "components"}})
            await asyncio.sleep(0.1)

            await ws.send_json({"event": "complete", "data": result})

    except WebSocketDisconnect:
        return
    except Exception as e:
        try:
            await ws.send_json({"event": "error", "data": str(e)})
        except Exception:
            pass
