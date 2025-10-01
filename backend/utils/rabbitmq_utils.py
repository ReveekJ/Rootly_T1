import aio_pika
from aio_pika.abc import AbstractRobustConnection

from backend.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_USER, RABBITMQ_PORT, RABBITMQ_VHOST


async def get_rabbitmq_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        password=RABBITMQ_PASS,
        login=RABBITMQ_USER,
        port=RABBITMQ_PORT,
        virtualhost=RABBITMQ_VHOST
    )
