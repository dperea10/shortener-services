import redis
import json
from infra.config.config import settings
from infra.adapters.redis.models.redis_model import DataShortenedUrlRedis

class MyEncoder:
    def encode(self, data):
        return data.encode('utf-8')

    def decode(self, encoded_data):
        return encoded_data.decode('utf-8')

class RedisInterface:
    def __init__(self):
        self.redis = redis.Redis(host=settings.host_redis, port=settings.port_redis)
    
    def get(self, key):
        return self.redis.get(key)
    
    def set(self, key, value):
        return self.redis.set(key, value)

    def delete(self, key):
        return self.redis.delete(key)

class RedisAdapter:
    def __init__(self, redis_interface):
        self.redis = redis_interface
        self.json = json
    
    def get_redis(self, key):
        data = self.redis.get(f"key:{key}")
        if data is None: return
        data_dict = json.loads(data)
        return  DataShortenedUrlRedis(**data_dict)
    
    def save_short_url_redis(self, hash_url, data):
        encoded_arg = self.json.dumps(data)
        return self.redis.set(f"key:{hash_url}", encoded_arg)

    def delete_redis(self, hash_url):
        return self.redis.delete(f"key:{hash_url}")
