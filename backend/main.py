import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.v1.routes import traffic, alerts
from services.websocket_manager import manager, traffic_generator

app = FastAPI(title="SIH26145 AI Threat Detection Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic.router, prefix="/api/v1/traffic", tags=["traffic"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])

@app.on_event("startup")
async def startup_event():
    # Start the background task to generate mock unidirectional traffic
    asyncio.create_task(traffic_generator())

@app.websocket("/ws/traffic")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # We don't expect to receive messages in a unidirectional context,
            # but we need to keep the connection open to send messages.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
