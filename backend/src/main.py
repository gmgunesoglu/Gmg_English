from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import List
from backend.src.database import init_db
from backend.src.routers import reading_unit, reading_text, reading_quest


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular'ın çalıştığı adres
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Tüm başlıklara izin ver
)

# routers
app.include_router(reading_unit.router)
app.include_router(reading_text.router)
app.include_router(reading_quest.router)


# Bağlantıdaki tüm istemcileri tutacağız
connected_clients: List[WebSocket] = []

# Mesajı güncelleyen endpoint
@app.get("/update_message/{message}")
async def update_message(message: str):
    global connected_clients
    # Tüm bağlı istemcilere mesajı gönder
    for websocket in connected_clients:
        await websocket.send_text(f"Updated message: {message}")
    return {"message_updated": message}

# WebSocket bağlantısı
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Bağlantıyı kabul et
    connected_clients.append(websocket)  # Yeni istemciyi bağlılar listesine ekle
    try:
        while True:
            # WebSocket üzerinden gelen mesajları al
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)  # Bağlantı koparsa istemciyi listeden çıkar
        print("WebSocket disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)