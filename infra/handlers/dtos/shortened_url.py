from pydantic import BaseModel
from typing import List, Optional


class ShortenedUrlDTO(BaseModel):
    user_id: str
    long_url_id: str
    hash_url: str

class ShortenedUrlRequestDTO(BaseModel):
    long_url: str


class ShortenedUrlResponseDTO(BaseModel):
    _id: str
    long_url_id: str
    long_url: str
    hash_url: str
    user_id: Optional[str]
    