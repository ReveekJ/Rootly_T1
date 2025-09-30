from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    contents = await file.read()

    return contents
