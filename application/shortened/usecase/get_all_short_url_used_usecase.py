from infra.adapters.shortened.long_url_adapter import LongURLAdapter
from infra.adapters.shortened.shortened_url_adapter import ShortenedURLAdapter
from infra.handlers.dtos.response import ResponseDTO
from infra.adapters.shortened.user_adapter import UserAdapter
from infra.adapters.redis.models.redis_model import DataShortenedUrlRedis
from infra.adapters.redis.redis_config import redis_adapter
from infra.config.config import settings
from datetime import datetime
from infra.utils.functions import decode_token_base

long_url_adapter = LongURLAdapter()
short_url_adapter = ShortenedURLAdapter()
user_adapter = UserAdapter()

def get_all_short_url_used_use(token: str) -> ResponseDTO:
    user_token = decode_token_base(token)
    if user_token is None:
       response = ResponseDTO(status="Error", message="Unauthorized")       
       return response

    user_model = user_adapter.get_user_by_username(user_token)
    if user_model is None:
       response = ResponseDTO(status="Error", message="UserNotfound")       
       return response

    shorts_urls = short_url_adapter.get_all_short_url_adapter()

    if shorts_urls is not None:
      response = ResponseDTO(status="Ok", message="Success", data={"shorts_urls":shorts_urls})
      return response

    response = ResponseDTO(status="Ok", message="NotFound")
    return response
