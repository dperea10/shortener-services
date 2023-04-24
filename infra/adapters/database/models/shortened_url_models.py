from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ShortenedUrlModel(BaseModel):
    id: Optional[str]
    user_id: Optional[str]
    long_url_id:  Optional[str]
    is_deleted:  bool = False
    hash_url:  Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)

