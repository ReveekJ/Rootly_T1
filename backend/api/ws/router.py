from fastapi import APIRouter
from fastapi.websockets import WebSocket

from backend.utils.ws_manager import manager

router = APIRouter(prefix='/ws')

@router.websocket('/connect')
async def websocket_endpoint(user_id: str, websocket: WebSocket):
    await manager.connect(user_id, websocket)

    while True:
        a = await websocket.receive_text()
        await websocket.send_text(a)
