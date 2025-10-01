import json

from aio_pika.abc import AbstractIncomingMessage
from elasticsearch import helpers
from backend.utils.es_utils import get_es_client


async def on_message_es(message: AbstractIncomingMessage):
    actions = []
    es = get_es_client()
    log_lines = message.body.decode().splitlines() # TODO: правильный сплит

    for line in log_lines:
        doc = json.loads(line)
        actions.append({
            "_index": "terraform-logs",
            "_source": doc
        })
        if len(actions) >= 500:
            await helpers.async_bulk(es, actions)
            actions = []
    if actions:
        await helpers.async_bulk(es, actions)


