from pydantic import BaseModel
from typing import Any

class ResponseDTO(BaseModel):
    status: str
    message: str
    data: Any = None