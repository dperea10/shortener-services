from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_uri: str
    database_name: str
    jwt_secret: str
    host_redis: str
    port_redis: int
    base_url_service: str

    class Config:
        env_prefix = "APP_"
        env_file = ".env"


settings = Settings()