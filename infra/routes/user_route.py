from fastapi import APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from infra.handlers.user_handler import get_token_handler

user = APIRouter()
security = HTTPBasic()

@user.post('/login')
def login(credentials: HTTPBasicCredentials):
    return get_token_handler(credentials)
