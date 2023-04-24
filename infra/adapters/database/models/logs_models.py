from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LogsModel(BaseModel):
    id: Optional[str]
    details_id:  Optional[str]
    message:  Optional[str]
    is_deleted:  bool = False
    created_at: datetime = Field(default_factory=datetime.now)
