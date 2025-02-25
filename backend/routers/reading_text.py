from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from backend.models import ReadingText
from backend.schemas import ReadingTextCreate, ReadingTextGets
from backend.database import get_session

router = APIRouter(prefix="/readings/texts", tags=["ReadingUnit"])

router.get("/", response_model=List[ReadingTextGets])
async def get_reading_texts(session: Session = Depends(get_session)):
    reading_texts = session.exec(select(ReadingText)).all()
    return [
        ReadingTextGets(
            id=text.id,
            unit=text.reading_unit.name,
            title=text.title
        ) for text in reading_texts
    ]


@router.post("/", response_model=ReadingTextGets)
async def create_reading_text(data: ReadingTextCreate, session: Session = Depends(get_session)):
    new_text = ReadingText(reading_unite_id=data.unit_id, title=data.title, context=data.context)
    try:
        session.add(new_text)
        session.commit()
        session.refresh(new_text)
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"Duplicated data error: {e}")
    except Exception as e:
        print(f"500 [-] Exception: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    return ReadingTextGets(
        id=new_text.id,
        title=new_text.title,
        unit=new_text.reading_unit.name
    )