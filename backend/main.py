from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from backend.database import init_db
from backend.routers import reading_unit, reading_text, reading_quest


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# routers
app.include_router(reading_unit.router)
app.include_router(reading_text.router)
app.include_router(reading_quest.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)