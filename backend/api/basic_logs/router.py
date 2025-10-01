from fastapi import APIRouter, UploadFile, File

from backend.rabbitmq.parser.producer import process_parsing

router = APIRouter()


@router.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    contents = await file.read()

    await process_parsing(contents)
    return contents # TODO: придумать что возвращать. Скорее всего ничего особо не надо, если будем работать через вебсокеты
