from typing import List, Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.__active_connections: List[Dict] = []

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.__active_connections.append({"user_id": user_id, "socket": websocket})

    async def disconnect(self, user_id: str, ws: WebSocket):
        self.__active_connections.remove({"user_id": user_id, "socket": ws})

    async def send_message(self, user_id: str, message: dict):
        try:
            matches = [x for x in self.__active_connections if x["user_id"] == user_id]
            for ws in matches:
                await ws['socket'].send_json(message)
        except Exception as e:
            print(e)


manager = ConnectionManager()
