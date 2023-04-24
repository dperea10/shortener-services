from pydantic import BaseModel, Field
from datetime import datetime

class LongUrlDTO(BaseModel):
    user_id: int
    long_url: str

class ShortUrlRequestDTO(BaseModel):
    short_url: str