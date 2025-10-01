import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from backend.api.basic_logs.router import router as basic_logs_router
from backend.api.ws.router import router as ws_router
from backend.rabbitmq.start_consumers import start_consumers

app = FastAPI(

)

app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(basic_logs_router)
app.include_router(ws_router)


@app.on_event("startup")
async def startup():
    asyncio.create_task(start_consumers())

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
