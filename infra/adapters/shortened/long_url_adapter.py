from pymongo.errors import PyMongoError
from infra.adapters.database.models.long_url_models import LongUrlModel
from infra.adapters.shortened.base_adapter import BaseAdapter
from bson import ObjectId


class LongURLAdapter(BaseAdapter):
    def register_long_url_adapter(self, long_url_document: LongUrlModel):
        try:
            collection = self.db['long_url']
            long_url_dict = long_url_document.dict()
            result =  collection.insert_one(long_url_dict)
            if result.inserted_id is None:
                return None
            url_long_id = str(result.inserted_id)
            return LongUrlModel(id=url_long_id)
        except PyMongoError as e:
            print(f"An error occurred while creating user: {e}")
            return False

    def get_long_url_by_long_url_adapter(self, long_url: LongUrlModel) -> LongUrlModel:
        collection = self.db['long_url']
        long_url_dict = collection.find_one({"long_url": long_url.long_url, "is_deleted": {"$ne": True}})
        if long_url_dict:
            long_url_dict['id'] = str(long_url_dict.pop('_id'))
            return LongUrlModel(**long_url_dict)
        return None

    def get_long_url_by_id_adapter(self, id: str) -> LongUrlModel:
        collection = self.db['long_url']
        long_url_dict = collection.find_one({"_id": id,"is_deleted": {"$ne": True}})
        if long_url_dict:
            long_url_dict['id'] = str(long_url_dict.pop('_id'))
            return LongUrlModel(**long_url_dict)
        return None

    def get_long_url_by_long_url_id_adapter(self, long_url_id: str) -> LongUrlModel:
        collection = self.db['long_url']
        object_id = ObjectId(long_url_id)
        long_url_dict = collection.find_one({"_id": object_id, "is_deleted": {"$ne": True}})
        if long_url_dict:
            long_url_dict['id'] = str(long_url_dict.pop('_id'))
            long_url_dict['long_url'] = str(long_url_dict.pop('long_url'))
            return LongUrlModel(**long_url_dict)
        return None

    def delete_long_url_by_long_url_id_adapter(self, long_url_id: str) -> LongUrlModel:
        collection = self.db['long_url']
        object_id = ObjectId(long_url_id)
        long_url_dict = collection.update_one({"_id": object_id}, {"$set": {"is_deleted": True}})
        if long_url_dict: return
        return None