import uuid
from typing import List

from pydantic import BaseModel


class HistoryRow(BaseModel):
    id: uuid.UUID
    name: str

class HistoryResponse(BaseModel):
    result: List[HistoryRow]
