import asyncio

from backend.rabbitmq.parser.consumer import parser_consume


async def start_consumers():
    await asyncio.gather(parser_consume())
