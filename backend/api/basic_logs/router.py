import json
import uuid

from fastapi import APIRouter, UploadFile, File, Request
from sqlalchemy import select

from backend.api.basic_logs.models import LogModel
from backend.api.basic_logs.schemas import HistoryResponse, HistoryRow
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
        res = (await session.execute(query)).scalars().all()

    return HistoryResponse(result=[HistoryRow.model_validate(i, from_attributes=True) for i in res])

@router.get('/api/log_analistic/{id}')
async def get_log_analistic(id: str):
    async with await get_async_session() as session:
        query = select(LogModel.log_analistics).where(LogModel.id == id)
        res = (await session.execute(query)).scalars().first()

    return json.dumps(res)
