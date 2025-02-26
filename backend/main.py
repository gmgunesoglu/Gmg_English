from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.routers import reading_unit, reading_text, reading_quest


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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)