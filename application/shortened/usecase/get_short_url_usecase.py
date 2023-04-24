import enum
from infra.adapters.shortened.long_url_adapter import LongURLAdapter
from infra.adapters.shortened.shortened_url_adapter import ShortenedURLAdapter
from infra.handlers.dtos.shortened_url import ShortenedUrlRequestDTO
from infra.handlers.dtos.response import ResponseDTO
from infra.adapters.shortened.user_adapter import UserAdapter
from infra.adapters.redis.models.redis_model import DataShortenedUrlRedis
from infra.adapters.redis.redis_config import redis_adapter
from infra.adapters.database.models.long_url_models import LongUrlModel
from infra.adapters.database.models.shortened_url_models import ShortenedUrlModel
from infra.config.config import settings
from datetime import datetime
from infra.utils.functions import decode_token_base

long_url_adapter = LongURLAdapter()
short_url_adapter = ShortenedURLAdapter()
user_adapter = UserAdapter()

def get_long_url_by_short_url_use(hash_url: str, token: str) -> ResponseDTO:
    user_token = decode_token_base(token)
    if user_token is None:
       response = ResponseDTO(status="Error", message="Unauthorized")       
       return response

    user_model = user_adapter.get_user_by_username(user_token)
    if user_model is None:
       response = ResponseDTO(status="Error", message="UserNotfound")       
       return response

    result_redis = redis_adapter.get_redis(hash_url)
    if result_redis is None:
      hash_url_model = ShortenedUrlModel(hash_url=hash_url)
      get_short_url = short_url_adapter.get_short_url_by_hash_url_adapter(hash_url_model)
      if get_short_url is not None:
         get_long_url = long_url_adapter.get_long_url_by_long_url_id_adapter(str(get_short_url.long_url_id))
         long_url_data =str(get_long_url.long_url)
         send_to_redis_cache(hash_url, long_url_data)
         response = ResponseDTO(status="Ok", message="Success", data={"long_url": long_url_data})
         return response
    else:
      response = ResponseDTO(status="Ok", message="Success", data={"long_url": result_redis.long_url})
      return response

    response = ResponseDTO(status="Ok", message="NotFound")
    return response

def send_to_redis_cache(hash_url:str, get_long_url: str):
    data_short_url_struct = DataShortenedUrlRedis(short_url=settings.base_url_service + hash_url, long_url= get_long_url, hash_url= hash_url, created_at=datetime.now())
    redis_adapter.save_short_url_redis(hash_url, data_short_url_struct.to_dict())
