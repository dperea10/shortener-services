import jwt
from jwt.exceptions import DecodeError
from infra.config.config import settings

def decode_token_base(token: str)-> str:
    try:
     if token is not None:
      only_token = token.split(' ')[1]
      claims = jwt.decode(only_token, settings.jwt_secret, algorithms=['HS256'])
      return claims['sub']
    except DecodeError as e:
     print(str(e))
