import json
import uuid

import aio_pika

from backend.utils.rabbitmq_utils import get_rabbitmq_connection


async def process_parsing(user_id: str, filename: str, data: bytes) -> str:
    try:
        connection = await get_rabbitmq_connection()
        log_id = str(uuid.uuid4())
        async with connection:
            routing_key = "parser_queue"

            channel = await connection.channel()

            await channel.declare_queue(routing_key, durable=True)

            message = aio_pika.Message(
                body=data,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                headers={"user_id": user_id, 'name': filename, "log_id": log_id}
            )
            await channel.default_exchange.publish(message, routing_key=routing_key)

        return log_id
    except Exception as e:
        print(e)

