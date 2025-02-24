from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from database import init_db
from routers import reading_unit


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

# routers
app.include_router(reading_unit.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)