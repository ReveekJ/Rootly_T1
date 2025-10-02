import json
import uuid

from aio_pika.abc import AbstractIncomingMessage

from backend.api.basic_logs.models import LogModel, LogLineModel
from backend.db.db_config import get_async_session
from backend.services.logs_parser import LogsParser
from backend.utils.ws_manager import manager


async def on_message_parser(message: AbstractIncomingMessage):
    user_id = message.headers.get("user_id")
    name = message.headers.get("name")
    log_id = uuid.UUID(message.headers.get("log_id"))

    result = LogsParser().parse_log_lines(message.body.decode().splitlines())
    async with await get_async_session() as session:
        m = LogModel(
            id=log_id,
            name=name,
            user_id=user_id,
        )
        session.add(m)
        await session.commit()

        for line in result:
            m = LogLineModel(
                id=uuid.uuid4(),
                timestamp=line.get('timestamp'),
                level=line.get('level'),
                section=line.get('section'),
                tf_req_id=line.get('tf_req_id'),
                request_body=json.dumps(line.get('request_body')),
                response_body=json.dumps(line.get('response_body')),
                raw=json.dumps(line.get('raw')),
                log_id=log_id,
            )
            session.add(m)
    # await manager.send_message(
    #     user_id,
    #     {
    #         'result': result
    #     }
    # )

        await session.commit()


    await manager.send_message(
        user_id,
        {
            'result': str(log_id)
        }
    )
    await message.ack()
