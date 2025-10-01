import json

from aio_pika.abc import AbstractIncomingMessage

from backend.api.basic_logs.models import LogModel
from backend.db.db_config import get_async_session
from backend.services.logs_parser import LogsParser
from backend.utils.ws_manager import manager


async def on_message_parser(message: AbstractIncomingMessage):
    user_id = message.headers.get("user_id")
    result = LogsParser().parse_log_lines(message.body.decode().splitlines())

    await manager.send_message(
        user_id,
        {
            'result': result
        }
    )

    async with get_async_session() as session:
        m = LogModel(
            user_id=user_id,
            log_analistics=json.dumps(result)
        )
        await session.add(m)
        await session.commit()

    await message.ack()
