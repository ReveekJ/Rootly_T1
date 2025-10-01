import uuid

from fastapi import APIRouter
from starlette.websockets import WebSocket

from backend.utils.ws_manager import manager

router = APIRouter(prefix='/ws')

@router.websocket('/connect')
async def websocket_endpoint(websocket: WebSocket):
    user_id = uuid.uuid4()

    await manager.connect(user_id, websocket)
