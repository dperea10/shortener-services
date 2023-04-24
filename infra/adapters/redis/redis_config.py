from infra.adapters.redis.redis import RedisInterface, RedisAdapter

redis_interface = RedisInterface()
redis_adapter = RedisAdapter(redis_interface=redis_interface)