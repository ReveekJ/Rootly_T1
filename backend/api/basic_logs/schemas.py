from typing import List

from pydantic import BaseModel


class HistoryRow(BaseModel):
    id: str
    name: str

class HistoryResponse(BaseModel):
    result: List[HistoryRow]
