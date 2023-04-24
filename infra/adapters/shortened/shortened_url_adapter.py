from pymongo.errors import PyMongoError
from fastapi.encoders import jsonable_encoder
from infra.adapters.database.models.shortened_url_models import ShortenedUrlModel
from infra.handlers.dtos.shortened_url import ShortenedUrlResponseDTO
from infra.adapters.shortened.base_adapter import BaseAdapter


class ShortenedURLAdapter(BaseAdapter):
    def register_shortened_url_adapter(self, short_url_document: ShortenedUrlModel):
        try:
            collection = self.db['shortened_url']
            short_url_dict = short_url_document.dict()
            result =  collection.insert_one(short_url_dict)
            return result.inserted_id is not None
        except PyMongoError as e:
            print(f"An error occurred while creating user: {e}")
            return False

    def get_short_url_by_hash_url_adapter(self, short_url: ShortenedUrlModel) -> ShortenedUrlModel:
        collection = self.db['shortened_url']
        short_url_dict = collection.find_one({"hash_url": short_url.hash_url, "is_deleted": {"$ne": True}})
        if short_url_dict:
            short_url_dict['id'] = str(short_url_dict.pop('_id'))
            return ShortenedUrlModel(**short_url_dict)
        return None

    def get_short_url_by_id_adapter(self, id: str) -> ShortenedUrlModel:
        collection = self.db['shortened_url']
        short_url_dict = collection.find_one({"_id": id, "is_deleted": {"$ne": True}})
        if short_url_dict:
            short_url_dict['id'] = str(short_url_dict.pop('_id'))
            return ShortenedUrlModel(**short_url_dict)
        return None

    def get_short_url_by_long_url_id_adapter(self, long_url_id: str) -> ShortenedUrlModel:
        collection = self.db['shortened_url']
        short_url_dict = collection.find_one({"long_url_id": long_url_id, "is_deleted": {"$ne": True}})
        if short_url_dict:
            short_url_dict['id'] = str(short_url_dict.pop('_id'))
            return ShortenedUrlModel(**short_url_dict)
        return None

    def get_all_short_url_adapter(self) -> ShortenedUrlResponseDTO:
        collection = self.db['shortened_url']
        pipeline = [
        {
            "$addFields": {
                "long_url_object_id": {"$toObjectId": "$long_url_id"}
            }
        },
        {
            "$lookup": {
                "from": "long_url",
                "localField": "long_url_object_id",
                "foreignField": "_id",
                "as": "long_url"
            }
        },
        {"$unwind": "$long_url"},
        {
            "$project": {
                "_id": 1,
                "long_url_id": 1,
                "long_url": "$long_url.long_url",
                "hash_url": 1,
                "user_id": 1,
                "is_deleted": {"$ifNull": ["$long_url.is_deleted", True]}
            }
        }
        ]
        results = collection.aggregate(pipeline)
        shortened_urls = [ShortenedUrlResponseDTO(**result) for result in results]
        return jsonable_encoder(shortened_urls)

    def delete_short_url_by_long_url_id_adapter(self, hash_url: str) -> ShortenedUrlModel:
        collection = self.db['shortened_url']
        short_url_dict = collection.update_one({"hash_url": hash_url}, {"$set": {"is_deleted": True}})
        if short_url_dict: return
        return None