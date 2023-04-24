import enum
from infra.adapters.shortened.long_url_adapter import LongURLAdapter
from infra.adapters.shortened.shortened_url_adapter import ShortenedURLAdapter
from infra.handlers.dtos.shortened_url import ShortenedUrlRequestDTO
from infra.handlers.dtos.response import ResponseDTO
import typing
import uuid
import json
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

def create_short_url_use(data_long_url: ShortenedUrlRequestDTO, token: str) -> ResponseDTO:
    user_token = decode_token_base(token)
    if user_token is None:
       response = ResponseDTO(status="Error", message="Unauthorized")       
       return response

    user_model = user_adapter.get_user_by_username(user_token)
    if user_model is None:
       response = ResponseDTO(status="Error", message="UserNotfound")       
       return response

    result_redis = redis_adapter.get_redis(data_long_url)
    if result_redis is None:
      long_url = LongUrlModel(long_url=data_long_url)
      get_by_long_url = long_url_adapter.get_long_url_by_long_url_adapter(long_url)
      if get_by_long_url is not None:
       long_url_id = ShortenedUrlModel(long_url_id=get_by_long_url.id)
       get_short_url = short_url_adapter.get_short_url_by_long_url_id_adapter(long_url_id.long_url_id)
       if get_short_url is None:
        response = ResponseDTO(status="Ok", message="RegisterNotFound")
        return response
       short_url_string = settings.base_url_service + get_short_url.hash_url
       response = ResponseDTO(status="Ok", message="RegisterFound", data={"short_url": short_url_string, "hash_url": get_short_url.hash_url})       
       return response
    else:
     short_url_string = settings.base_url_service + result_redis.hash_url
     response = ResponseDTO(status="Ok", message="RegisterFound", data={"short_url": short_url_string, "hash_url": result_redis.hash_url})  
     return response
    
    hash_url = str(uuid.uuid4())[:5].upper()
    send_to_redis_cache(hash_url, data_long_url)

    long_url_document = LongUrlModel(user_id=user_model.id, long_url=data_long_url)
    long_url_result = long_url_adapter.register_long_url_adapter(long_url_document)
    if long_url_result is None:
      response = ResponseDTO(status="Error", message="UnexpectedError")
      return response
    
    short_url_document = ShortenedUrlModel(user_id = user_model.id, long_url_id=long_url_result.id, hash_url=hash_url)
    short_url_result = short_url_adapter.register_shortened_url_adapter(short_url_document)
    if short_url_result is None:
      response = ResponseDTO(status="Error", message="UnexpectedError")
      return response

    response = ResponseDTO(status="Ok", message="Success", data={"short_url": settings.base_url_service + hash_url, "hash_url": hash_url})
    return response

def send_to_redis_cache(hash_url:str, data_long_url: ShortenedUrlRequestDTO):
    data_long_url_struct = DataShortenedUrlRedis(short_url=settings.base_url_service + hash_url, long_url= data_long_url, hash_url=hash_url, created_at=datetime.now())
    redis_adapter.save_short_url_redis(data_long_url, data_long_url_struct.to_dict())
 