from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.database import Database
from abc import ABC, abstractmethod
from infra.config.config import settings


class BaseAdapter(ABC):
    def __init__(self):
        self.client = MongoClient(settings.mongo_uri)
        self.db = self.client[settings.database_name]
    def __del__(self):
        self.client.close()
