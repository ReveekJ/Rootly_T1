import uuid
from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime

from backend.api.basic_logs.enums import LogLevel, LogSection


class HistoryRow(BaseModel):
    id: uuid.UUID
    name: str

class HistoryResponse(BaseModel):
    result: List[HistoryRow]

class LogLine(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    level: str
    section: Optional[str]
    tf_req_id: Optional[str]
    request_body: Optional[str]
    response_body: Optional[str]
    raw: str
    log_id: uuid.UUID


class Log(BaseModel):
    id: uuid.UUID
    name: str
    user_id: str
    lines: List[LogLine]
