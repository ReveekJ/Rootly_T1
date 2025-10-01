from fastapi import APIRouter, UploadFile, File, Request

from backend.rabbitmq.parser.producer import process_parsing

router = APIRouter()


@router.post('/api/upload')
async def upload(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    user_id = request.cookies.get("user_id")

    await process_parsing(user_id, contents)
    return contents # TODO: придумать что возвращать. Скорее всего ничего особо не надо, если будем работать через вебсокеты
