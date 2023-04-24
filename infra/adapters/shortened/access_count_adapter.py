from pymongo.errors import PyMongoError
from fastapi.encoders import jsonable_encoder
from infra.adapters.database.models.access_count_models import AccessCountModel
from infra.handlers.dtos.access_count import AccessCountUrlResponseDTO, ClickDTO
from infra.adapters.shortened.base_adapter import BaseAdapter
from application.shortened.usecase.create_long_url_usecase import long_url_adapter


class AccessCountAdapter(BaseAdapter):
    def register_access_count_adapter(self, access_count: AccessCountModel) ->AccessCountModel:
        try:
            collection = self.db['access_count']
            access_count_dict = access_count.dict()
            result =  collection.insert_one(access_count_dict)
            return result.inserted_id is not None
        except PyMongoError as e:
            print(f"An error occurred while creating user: {e}")
            return False

    def get_access_count_adapter(self, hash_url: AccessCountModel) -> AccessCountModel:
        collection = self.db['access_count']
        access_count_dict = collection.find_one({"hash_url": hash_url.hash_url, "is_deleted": {"$ne": True}})
        if access_count_dict:
            access_count_dict['id'] = str(access_count_dict.pop('_id'))
            return AccessCountModel(**access_count_dict)
        return None

    def get_all_platform_and_browsers_adapter(self) -> AccessCountUrlResponseDTO:
        collection = self.db['shortened_url']
        pipeline = [
            {"$addFields": {"long_url_object_id": {"$toObjectId": "$long_url_id"}}},
            {"$lookup": {"from": "long_url", "localField": "long_url_object_id", "foreignField": "_id", "as": "long_url"}},
            {"$lookup": {"from": "access_count", "localField": "hash_url", "foreignField": "hash_url", "as": "access_counts"}},
            {"$unwind": "$long_url"},
            {"$project": {
                "long_url_id": 1,
                "long_url": "$long_url.long_url",
                "hash_url": 1,
                "user_id": 1,
                "is_deleted": {"$ifNull": ["$long_url.is_deleted", True]},
                "access_counts": {
                    "$map": {
                        "input": "$access_counts",
                        "as": "access_count",
                        "in": {
                            "platform": "$$access_count.platform",
                            "browser": "$$access_count.browser",
                            "shorted_url": "$$access_count.shorted_url"
                        }
                    }
                }
            }}
        ]
        results = collection.aggregate(pipeline)
        shortened_urls = [AccessCountUrlResponseDTO(**result) for result in results]
        return jsonable_encoder(shortened_urls)

    def get_all_records_clicks_used_adapter(self, hash_url:str) -> ClickDTO:
        collection = self.db['shortened_url']
        pipeline = [{'$match': {'$and': [{'hash_url': {'$eq': hash_url}} ]}},
            {'$addFields': {'long_url_object_id': {'$toObjectId': '$long_url_id'}}},
            {'$lookup': {'from': 'long_url', 'localField': 'long_url_object_id','foreignField': '_id','as': 'long_url'}},
            {'$lookup': {'from': 'access_count','localField': 'hash_url','foreignField': 'hash_url','as': 'access_counts'}},
            {'$unwind': '$long_url'},
            {'$project': {'_id': 1,'long_url_id': 1,'long_url': '$long_url.long_url','hash_url': 1,'user_id': 1,
                    'is_deleted': {
                        '$ifNull': [
                            '$long_url.is_deleted',
                            True
                        ]
                    },
                    'access_counts': {
                        '$map': {
                            'input': '$access_counts',
                            'as': 'access_count',
                            'in': {
                                'platform': '$$access_count.platform',
                                'browser': '$$access_count.browser',
                                'shorted_url': '$$access_count.shorted_url'
                            }
                        }
                    }
                }
            },
            {
                '$unwind': '$access_counts'
            },
            {
                '$group': {
                    '_id': {
                        '_id': '$_id',
                        'platform': '$access_counts.platform',
                        'browser': '$access_counts.browser'
                    },
                    'long_url_id': {
                        '$first': '$long_url_id'
                    },
                    'long_url': {
                        '$first': '$long_url'
                    },
                    'hash_url': {
                        '$first': '$hash_url'
                    },
                    'user_id': {
                        '$first': '$user_id'
                    },
                    'is_deleted': {
                        '$first': '$is_deleted'
                    },
                    'platforms': {
                        '$push': {
                            'platform': '$access_counts.platform',
                            'count': 1
                        }
                    },
                    'browsers': {
                        '$push': {
                            'browser': '$access_counts.browser',
                            'count': 1
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'long_url_id': 1,
                    'long_url': 1,
                    'hash_url': 1,
                    'user_id': 1,
                    'is_deleted': 1,
                    'platforms': 1,
                    'browsers': 1,
                    'total_clicks': {
                        '$sum': '$platforms.count'
                    }
                }
            },
        {
            '$group': {
                '_id': {
                    'long_url_id': '$long_url_id',
                    'long_url': '$long_url',
                    'user_id': '$user_id',
                    'is_deleted': '$is_deleted'
                },
                'hash_urls': {
                    '$push': {
                        'hash_url': '$hash_url',
                        'platforms': '$platforms',
                        'browsers': '$browsers',
                        'total_clicks': '$total_clicks'
                    }
                }
            }
        }]
        results = collection.aggregate(pipeline)
        shortened_urls = []
        for item in results:
            long_url_id = item['_id']['long_url_id']
            long_url = item['_id']['long_url']
            user_id = item['_id']['user_id']
            is_deleted = item['_id']['is_deleted']
            hash_urls = []
            for hash_url_item in item['hash_urls']:
                hash_url = hash_url_item['hash_url']
                platforms = []
                for platform_item in hash_url_item['platforms']:
                    platform = platform_item['platform']
                    count = platform_item['count']
                    platforms.append({'platform': platform, 'count': count})
                browsers = []
                for browser_item in hash_url_item['browsers']:
                    browser = browser_item['browser']
                    count = browser_item['count']
                    browsers.append({'browser': browser, 'count': count})
                total_clicks = hash_url_item['total_clicks']
                hash_urls.append({'hash_url': hash_url, 'platforms': platforms, 'browsers': browsers, 'total_clicks': total_clicks})
            shortened_url_dto = ClickDTO(long_url_id, long_url, user_id, is_deleted, hash_urls)

            shortened_urls.append(shortened_url_dto)
            shortened_url_dicts = [shortened_url.to_dict() for shortened_url in shortened_urls]
            return jsonable_encoder(shortened_url_dicts)
