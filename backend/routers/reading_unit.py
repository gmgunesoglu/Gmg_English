from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from typing import List

from backend.database import get_session
from backend.models import ReadingUnit
from backend.schemas import ReadingUnitGets, ReadingUnitCreate, ReadingTextBase

router = APIRouter(prefix="/readings/units", tags=["ReadingUnit"])

@router.get("/", response_model=List[ReadingUnitGets])
async def get_reading_units(session: Session = Depends(get_session)):
    units = session.exec(select(ReadingUnit)).all()
    return [
        ReadingUnitGets(
            id=unit.id,
            name=unit.name,
            titles=[
                ReadingTextBase(id=text.id, title=text.title) for text in unit.reading_texts
            ]
        )
        for unit in units
    ]

@router.post("/", response_model=str)
async def create_reading_unit(data: ReadingUnitCreate, session: Session = Depends(get_session)):
    new_unit = ReadingUnit(name=data.title)
    try:
        session.add(new_unit)
        session.commit()
        session.refresh(new_unit)
    except IntegrityError as e:
        print(f"400 [-] IntegrityError: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return f"Unit '{new_unit.name}' created successfully!"

@router.put("/{reading_unit_id}", response_model=str)
async def update_reading_unit(reading_unit_id: int, data: ReadingUnitCreate, session: Session = Depends(get_session)):
    unit = session.get(ReadingUnit, reading_unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail=f"Unit not found with id: {reading_unit_id}.")
    unit.name = data.title
    try:
        session.add(unit)
        session.commit()
        session.refresh(unit)
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return f"Unit updated successfully!"

@router.delete("/{reading_unit_id}", response_model=str)
async def delete_reading_unit(reading_unit_id: int,session: Session = Depends(get_session)):
    unit = session.get(ReadingUnit, reading_unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found.")
    try:
        session.delete(unit)
        session.commit()
    except IntegrityError as e:
        print(f"400 [-] Exception: {e}")
        raise HTTPException(status_code=400, detail=f"IntegrityError: {e}")
    return f"Unit deleted successfully!"