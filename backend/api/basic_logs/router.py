import json
import uuid

from fastapi import APIRouter, UploadFile, File, Request
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.api.basic_logs.models import LogModel
from backend.api.basic_logs.schemas import HistoryResponse, HistoryRow, Log, LogLine
from backend.db.db_config import get_async_session
from backend.rabbitmq.parser.producer import process_parsing
from backend.utils.fastapi_utils import get_user_id

router = APIRouter()


@router.get("/set-user-id")
async def set_user_id():
    return str(uuid.uuid4())

@router.post('/api/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    user_id = get_user_id(request)

    await process_parsing(user_id, contents)
    return contents

@router.get("/api/get_history", response_model=HistoryResponse)
async def get_history(request: Request):
    async with await get_async_session() as session:
        query = select(LogModel.id, LogModel.name).where(LogModel.user_id == get_user_id(request))
        res = (await session.execute(query)).all()

    return HistoryResponse(result=[HistoryRow.model_validate(i, from_attributes=True) for i in res])

@router.get('/api/log_analistic/{id}', response_model=Log)
async def get_log_analistic(id: uuid.UUID, offset: int = 0, limit: int = 100):
    async with await get_async_session() as session:
        query = select(LogModel).options(selectinload(LogModel.lines)).where(LogModel.id == id)
        res = (await session.execute(query)).scalars().first()

    return Log.model_validate(res, from_attributes=True)

@router.get('/api/get_response_from_req_id/', response_model=LogLine)
async def get_response_from_req_id(req_id: str):
    async with await get_async_session() as session:
        query = select(LogLine).where(LogLine.tf_req_id == req_id)
        res = (await session.execute(query)).scalars().first()

    return LogLine.model_validate(res, from_attributes=True)
