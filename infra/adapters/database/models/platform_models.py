from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PlatformModel(BaseModel):
    id: Optional[str]
    platform_name:  Optional[str]
    is_web:  Optional[bool]
    is_deleted:  bool = False
    created_at: datetime = Field(default_factory=datetime.now)