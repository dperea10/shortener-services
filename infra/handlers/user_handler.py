from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from application.shortened.usecase.user_usecase import get_user_token


def get_token_handler(credentials: HTTPBasicCredentials):
    user, token, token_expiration = get_user_token(credentials.username)
    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": token_expiration
    }
