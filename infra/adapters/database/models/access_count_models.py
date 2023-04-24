from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AccessCountModel(BaseModel):
    id: Optional[str]
    platform: Optional[str]
    browser: Optional[str]
    shorted_url: Optional[str]
    hash_url: Optional[str]
    is_deleted:  bool = False
    created_at: datetime = Field(default_factory=datetime.now)
