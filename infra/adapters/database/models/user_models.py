from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    id: Optional[str]
    username: Optional[str]
    password: Optional[str]
    is_deleted:  bool = False