import asyncio
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from starlette.websockets import WebSocket, WebSocketDisconnect
import redis

from backend.src.models import ReadingText
from backend.src.schemas import ReadingTextCreate, ReadingTextGets, ReadingTextGet, ReadingQuestBase
from backend.src.database import get_session

router = APIRouter(prefix="/readings/texts", tags=["ReadingText"])

connected_clients = []
# Redis bağlantısı (Whisper Worker ile haberleşmek için)
redis_conn = redis.Redis(host='localhost', port=6379, db=0)

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
    if len(data.context.strip()) < 100:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type": "string_too_short",
                    "loc": ["body", "context"],
                    "msg": "String should have at least 100 characters without any black characters",
                    "input": data.context,
                    "ctx": {"min_length": 100}
                }
            ]
        )
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
    if len(data.context.strip()) < 100:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "type": "string_too_short",
                    "loc": ["body", "context"],
                    "msg": "String should have at least 100 characters without any black characters",
                    "input": data.context,
                    "ctx": {"min_length": 100}
                }
            ]
        )
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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Bağlantıyı kabul et
    connected_clients.append(websocket)  # Yeni istemciyi bağlılar listesine ekle
    # try:
    #     while True:
    #         # WebSocket üzerinden gelen mesajları al
    #         # data = await websocket.receive_text()
    #         audio_data = await websocket.receive_bytes()
    #         print(f"Ses kaydı alındı, boyut: {len(audio_data)} byte")
    try:
        while True:
            data = await websocket.receive_bytes()  # Gelen ses verisini al
            redis_conn.rpush("audio_queue", data)  # Veriyi Whisper kuyruğuna ekle

            # Whisper'ın yanıt vermesini bekleyelim
            while redis_conn.get("transcript_result") is None:
                await asyncio.sleep(0.1)

            # Sonucu al ve WebSocket üzerinden gönder
            transcript_data = json.loads(redis_conn.get("transcript_result"))
            await websocket.send_text(transcript_data["text"])
            redis_conn.delete("transcript_result")  # Sonucu temizle
    except WebSocketDisconnect:
        connected_clients.remove(websocket)  # Bağlantı koparsa istemciyi listeden çıkar
        print("WebSocket disconnected")

# Mesajı güncelleyen endpoint
@router.get("/message/{message}")
async def update_message(message: str):
    global connected_clients
    # Tüm bağlı istemcilere mesajı gönder
    for websocket in connected_clients:
        await websocket.send_text(f"Updated message: {message}")
        port = websocket.client.port
        print(f"port: {port}")
    return {"message_updated": message}