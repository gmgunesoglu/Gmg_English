from sqlalchemy import Index, func
from sqlmodel import SQLModel, create_engine, Session
from backend.models import ReadingText, ReadingQuest, ReadingUnit

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/gmg_english"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session