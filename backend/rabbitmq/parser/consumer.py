import asyncio

from aio_pika.abc import AbstractIncomingMessage

from backend.services.logs_parser import LogsParser
from backend.utils.rabbitmq_utils import get_rabbitmq_connection
from backend.utils.ws_manager import manager


async def on_message(message: AbstractIncomingMessage):
    user_id = message.headers.get("user_id")
    result = LogsParser().parse_log_lines(message.body.decode().splitlines())
    print(user_id)

    await manager.send_message(
        user_id,
        {
            'result': result
        }
    )
    await message.ack()


async def parser_consume():
    try:
        connection = await get_rabbitmq_connection()

        channel = await connection.channel()

        queue_name = "parser_queue"
        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.consume(on_message)

        await asyncio.Future()
    except Exception as e:
        print(e)
