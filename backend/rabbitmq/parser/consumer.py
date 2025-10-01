from aio_pika.abc import AbstractIncomingMessage

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
    await message.ack()
