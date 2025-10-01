import asyncio

from backend.rabbitmq.es.consumer import on_message_es
from backend.rabbitmq.parser.consumer import on_message_parser
from backend.utils.registrate_consumer import registrate_consumer


async def start_consumers():
    await asyncio.gather(
        registrate_consumer('parser_queue', on_message_parser),
        registrate_consumer('es_queue', on_message_es)
    )
