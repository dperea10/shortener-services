import enum
from infra.adapters.shortened.long_url_adapter import LongURLAdapter
from infra.adapters.shortened.shortened_url_adapter import ShortenedURLAdapter
from infra.handlers.dtos.shortened_url import ShortenedUrlRequestDTO
from infra.handlers.dtos.response import ResponseDTO
from infra.adapters.shortened.user_adapter import UserAdapter
from infra.adapters.redis.redis_config import redis_adapter
from infra.adapters.database.models.shortened_url_models import ShortenedUrlModel
from infra.config.config import settings
from datetime import datetime
from infra.utils.functions import decode_token_base

long_url_adapter = LongURLAdapter()
short_url_adapter = ShortenedURLAdapter()
user_adapter = UserAdapter()

def delete_short_url_use(hash_url: str, token: str) -> ResponseDTO:
    user_token = decode_token_base(token)
    if user_token is None:
       response = ResponseDTO(status="Error", message="Unauthorized")       
       return response

    user_model = user_adapter.get_user_by_username(user_token)
    if user_model is None:
       response = ResponseDTO(status="Error", message="UserNotfound")       
       return response

    redis_adapter.delete_redis(hash_url)
    hash_url_model = ShortenedUrlModel(hash_url=hash_url)
    get_short_url = short_url_adapter.get_short_url_by_hash_url_adapter(hash_url_model)
    if get_short_url is None:
      response = ResponseDTO(status="Error", message="RegisterNotFound")
      return response

    get_long_url = long_url_adapter.get_long_url_by_long_url_id_adapter(str(get_short_url.long_url_id))
    if get_short_url is None: return ResponseDTO(status="Error", message="RegisterNotFound")
 
    is_deleted = short_url_adapter.delete_short_url_by_long_url_id_adapter(hash_url)
    if is_deleted is not None: return ResponseDTO(status="Error", message="RegisterNotFound")

    long_url_id = str(get_long_url.id)   
    is_deleted_long = long_url_adapter.delete_long_url_by_long_url_id_adapter(long_url_id)
    if is_deleted_long is not None: return ResponseDTO(status="Error", message="RegisterNotFound")

    response = ResponseDTO(status="Ok", message="Deleted")
    return response
