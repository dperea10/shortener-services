from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from infra.adapters.database.models.access_count_models import AccessCountModel


class LongUrlResponseDTO(BaseModel):
    long_url: str
    hash_url: str
    created_at: datetime
    is_deleted: Optional[bool] = False

class AccessCountDTO(BaseModel):
    platform: Optional[str]
    browser: Optional[str]
    shorted_url: Optional[str]

class AccessCountUrlResponseDTO(BaseModel):
    long_url_id: str
    long_url: str
    hash_url: str
    user_id: Optional[str]
    access_counts: Optional[List[AccessCountDTO]] = None

class ClickDTO:
    def __init__(self, long_url_id, long_url, user_id, is_deleted, hash_urls):
        self.long_url_id = long_url_id
        self.long_url = long_url
        self.user_id = user_id
        self.is_deleted = is_deleted
        self.hash_urls = hash_urls
        
    def to_dict(self):
        return {
            'long_url_id': self.long_url_id,
            'long_url': self.long_url,
            'user_id': self.user_id,
            'is_deleted': self.is_deleted,
            'hash_urls': self.hash_urls
        }
