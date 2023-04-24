import enum
from infra.adapters.shortened.long_url_adapter import LongURLAdapter
from infra.adapters.shortened.shortened_url_adapter import ShortenedURLAdapter
from infra.adapters.shortened.access_count_adapter import AccessCountAdapter
from infra.adapters.shortened.user_adapter import UserAdapter
from infra.adapters.redis.models.redis_model import DataShortenedUrlRedis
from infra.adapters.redis.redis_config import redis_adapter
from infra.adapters.database.models.long_url_models import LongUrlModel
from infra.adapters.database.models.shortened_url_models import ShortenedUrlModel
from infra.config.config import settings
from datetime import datetime
from infra.utils.functions import decode_token_base
from infra.adapters.database.models.access_count_models import AccessCountModel

long_url_adapter = LongURLAdapter()
short_url_adapter = ShortenedURLAdapter()
access_count_adapter = AccessCountAdapter()
user_adapter = UserAdapter()

def redirect_to_long_url_use(hash_url: str, header: str)-> str:
    save_platform_and_browser(hash_url,header)
    
    redirect = "redirect-" + hash_url
    result_redis = redis_adapter.get_redis(redirect)

    if result_redis is not None: return result_redis.long_url

    hash_url_model = ShortenedUrlModel(hash_url=hash_url)
    get_short_url = short_url_adapter.get_short_url_by_hash_url_adapter(hash_url_model)

    if get_short_url is not None: 
      get_long_url = long_url_adapter.get_long_url_by_long_url_id_adapter(str(get_short_url.long_url_id))
      long_url_data =str(get_long_url.long_url)
      send_to_redis_cache(redirect, long_url_data)
      return long_url_data
   
    return "RedirectNotFound"


def send_to_redis_cache(hash_url:str, get_long_url: str):
    data_short_url_struct = DataShortenedUrlRedis(short_url=settings.base_url_service + hash_url, long_url= get_long_url, hash_url= hash_url, created_at=datetime.now())
    redis_adapter.save_short_url_redis(hash_url, data_short_url_struct.to_dict())

def save_platform_and_browser(hash_url:str, header:str):
   try:
      platform = header.split(') ')[0].split(' (')[1]
   except IndexError:
      platform = 'Other'

   try:
      browser = header.split(') ')[0].split(' (')[0]
   except IndexError:
      browser = 'Other'

   access_count_model = AccessCountModel(hash_url=hash_url, platform=platform, browser=browser, shorted_url=settings.base_url_service+hash_url)
   return access_count_adapter.register_access_count_adapter(access_count_model)
