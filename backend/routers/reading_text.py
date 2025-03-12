from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from backend.models import ReadingText
from backend.schemas import ReadingTextCreate, ReadingTextGets, ReadingTextGet, ReadingQuestBase
from backend.database import get_session

router = APIRouter(prefix="/readings/texts", tags=["ReadingText"])

@router.get("/", summary="Get all titles", response_model=List[ReadingTextGets])
async def get_reading_texts(session: Session = Depends(get_session)):
    reading_texts = session.exec(select(ReadingText)).all()
    return [
        ReadingTextGets(
            id=text.id,
            unit_name=text.reading_unit.name,
            title=text.title
        ) for text in reading_texts
    ]

@router.get("/{reading_text_id}", summary="Get text details", response_model=ReadingTextGet)
async def get_reading_text(reading_text_id:int, session: Session = Depends(get_session)):
    text = session.get(ReadingText, reading_text_id)
    if text is None:
        raise HTTPException(status_code=404, detail=f"Text not found with id: {reading_text_id}.")
    return ReadingTextGet(
        id=text.id,
        unit_name=text.reading_unit.name,
        title=text.title,
        context=text.context,
        quests=[
            ReadingQuestBase(
                id=quest.id,
                quest=quest.quest,
                option_a=quest.option_a,
                option_b=quest.option_b,
                option_c=quest.option_c,
                option_d=quest.option_d,
                correct_option=quest.correct_option,
                justification=quest.justification
            ) for quest in text.reading_quests
        ]
    )

@router.post("/", summary="Create a text", response_model=ReadingTextGets)
async def create_reading_text(data: ReadingTextCreate, session: Session = Depends(get_session)):
    new_text = ReadingText(reading_unit_id=data.unit_id, title=data.title, context=data.context)
    try:
        session.add(new_text)
        session.commit()
        session.refresh(new_text)
    except IntegrityError as e:
        print(f"400 [-] IntegrityError: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return ReadingTextGets(
        id=new_text.id,
        title=new_text.title,
        unit_name=new_text.reading_unit.name
    )

@router.put("/{reading_text_id}", summary="Update a text", response_model=str)
async def update_reading_text(reading_text_id: int, data: ReadingTextCreate, session: Session = Depends(get_session)):
    text = session.get(ReadingText, reading_text_id)
    if text is None:
        raise HTTPException(status_code=404, detail=f"Text not found with id: {reading_text_id}")
    text.title = data.title
    text.reading_unit_id = data.unit_id
    text.context = data.context
    try:
        session.add(text)
        session.commit()
        session.refresh(text)
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return "Text updated successfully!"

@router.delete("/{reading_text_id}",summary="Delete a text",  response_model=str)
async def delete_reading_unit(reading_text_id: int,session: Session = Depends(get_session)):
    text = session.get(ReadingText, reading_text_id)
    if text is None:
        raise HTTPException(status_code=404, detail=f"Unit not found with id: {reading_text_id}")
    try:
        session.delete(text)
        session.commit()
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return "Text deleted successfully!"