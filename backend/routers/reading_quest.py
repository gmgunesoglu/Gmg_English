from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from backend.models import ReadingQuest
from backend.schemas import ReadingQuestPost
from backend.database import get_session

router = APIRouter(prefix="/readings/quests", tags=["ReadingQuest"])

@router.post("/", summary="Create a quest for a text", response_model=str)
async def create_reading_quest(data: ReadingQuestPost, session: Session = Depends(get_session)):
    new_quest = ReadingQuest(
        reading_text_id=data.text_id,
        quest=data.quest,
        option_a=data.option_a,
        option_b=data.option_b,
        option_c=data.option_c,
        option_d=data.option_d,
        correct_option=data.correct_option.value,
        justification=data.justification
    )
    try:
        session.add(new_quest)
        session.commit()
        session.refresh(new_quest)
    except IntegrityError as e:
        print(f"400 [-] IntegrityError: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return "Quest added successfully!"

@router.put("/{reading_quest_id}", summary="Update a quest", response_model=str)
async def update_reading_quest(reading_quest_id: int, data: ReadingQuestPost, session: Session = Depends(get_session)):
    quest = session.get(ReadingQuest, reading_quest_id)
    if quest is None:
        raise HTTPException(status_code=404, detail=f"Quest not found with id: {reading_quest_id}")
    quest.reading_text_id = data.text_id
    quest.quest = data.quest
    quest.option_a = data.option_a
    quest.option_b = data.option_b
    quest.option_c = data.option_c
    quest.option_d = data.option_d
    quest.correct_option = data.correct_option.value
    quest.justification = data.justification
    try:
        session.add(quest)
        session.commit()
        session.refresh(quest)
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return "Quest updated successfully!"

@router.delete("/{reading_quest_id}", summary="Delete a quest", response_model=str)
async def delete_reading_unit(reading_quest_id: int,session: Session = Depends(get_session)):
    quest = session.get(ReadingQuest, reading_quest_id)
    if quest is None:
        raise HTTPException(status_code=404, detail=f"Quest not found with id: {reading_quest_id}")
    try:
        session.delete(quest)
        session.commit()
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return "Text deleted successfully!"