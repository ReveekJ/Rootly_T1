import asyncio

from aio_pika.abc import AbstractIncomingMessage

from backend.utils.rabbitmq_utils import get_rabbitmq_connection


async def on_message(message: AbstractIncomingMessage):
    print('consume')
    # TODO: заимплементить парсинг


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
