from fastapi import Request, HTTPException


def get_user_id(request: Request):
    res = request.headers.get("user_id")
    if not res:
        raise HTTPException(status_code=422, detail="user_id not found")
    return res