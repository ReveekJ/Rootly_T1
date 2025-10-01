import asyncio
from typing import Callable

from backend.utils.rabbitmq_utils import get_rabbitmq_connection


async def registrate_consumer(queue_name: str, on_message: Callable):
    try:
        connection = await get_rabbitmq_connection()

        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.consume(on_message)

        await asyncio.Future()
    except Exception as e:
        print(e)
