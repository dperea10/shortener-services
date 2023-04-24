from infra.adapters.database.models.user_models import UserModel
from infra.adapters.shortened.user_adapter import UserAdapter
from datetime import datetime, timedelta
from infra.config.config import settings
import jwt

user_adapter = UserAdapter()

def get_user_token(username: str) -> UserModel:
    user = user_adapter.get_user_by_username(username)
    token_expiration = datetime.utcnow() + timedelta(hours=1)

    token = jwt.encode({
        "sub": user.username,
        "exp": token_expiration.timestamp()
    }, settings.jwt_secret, algorithm="HS256")


    return user, token, token_expiration
