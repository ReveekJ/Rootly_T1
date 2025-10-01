import json

import aio_pika

from backend.utils.rabbitmq_utils import get_rabbitmq_connection


async def process_parsing(user_id: str, data: bytes):
    try:
        connection = await get_rabbitmq_connection()

        async with connection:
            routing_key = "parser_queue"

            channel = await connection.channel()

            await channel.declare_queue(routing_key, durable=True)

            message = aio_pika.Message(
                body=data,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={"user_id": user_id}
            )
            await channel.default_exchange.publish(message, routing_key=routing_key)

        return True
    except Exception as e:
        print(e)

