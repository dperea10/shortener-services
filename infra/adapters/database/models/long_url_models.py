from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LongUrlModel(BaseModel):
    id: Optional[str]
    user_id:  Optional[str]
    long_url:  Optional[str]
    is_deleted:  bool = False
    created_at: datetime = Field(default_factory=datetime.now)