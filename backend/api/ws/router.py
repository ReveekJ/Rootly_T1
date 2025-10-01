import uuid

from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.websockets import WebSocket

from backend.config import APP_URL
from backend.utils.ws_manager import manager

router = APIRouter(prefix='/ws')

@router.websocket('/connect')
async def websocket_endpoint(websocket: WebSocket, response: Response):
    user_id = websocket.cookies.get("user_id")
    if user_id is None:
        user_id = str(uuid.uuid4())

    await manager.connect(user_id, websocket)

    response.set_cookie(
        key="user_id",
        value=user_id,
        httponly=True,
        max_age=60*60*24*365,
        domain=APP_URL
    )

    return response
