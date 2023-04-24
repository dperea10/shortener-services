from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class LogsDTO(BaseModel):
    details_id: str
    message: str