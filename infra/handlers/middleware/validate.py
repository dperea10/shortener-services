from fastapi import HTTPException, Header
from datetime import datetime

async def verify_token(token: str = Header(None, alias='Authorization')) -> bool:
    if token is None:
         return True
    if token.startswith('Bearer '):
      return True
    return False
