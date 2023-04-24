from pymongo import MongoClient, IndexModel, ASCENDING
from bson.codec_options import CodecOptions
from pymongo.collection import Collection
from infra.adapters.database.models.user_models import UserModel
from infra.adapters.database.models.access_count_models import AccessCountModel
from infra.adapters.database.models.logs_models import LogsModel
from infra.adapters.database.models.long_url_models import LongUrlModel
from infra.adapters.database.models.platform_models import PlatformModel
from infra.adapters.database.models.shortened_url_models import ShortenedUrlModel

from infra.config.config import settings

client = MongoClient(settings.mongo_uri)
db = client['shortened_url']

def migrate(users: Collection, user: UserModel):
    create_collection_models()
    existing_index = users.index_information().get("password_1")
    if existing_index:
        users.drop_index("password_1")
        
    users.create_indexes([
        IndexModel([("password", ASCENDING)], unique=True, dropDups=True),
        IndexModel([("username", ASCENDING)],unique=True, dropDups=True),
    ])
    users.insert_one(user.dict())

def execute_migration():
    try:
        users = db['users']
        existing_user = users.find_one({'username': 'test@test.com'})
        if existing_user:
         users.delete_one({'username': 'test@test.com'})
    
    except Exception as e:
        print(f"Error database connection: {e}")
        return
    print(users, UserModel)
    user = UserModel(username="test@test.com", password="test")
    migrate(users, user)

def create_collection_models():
   if 'access_count' not in db.list_collection_names():
    access_count_collection = db.create_collection('access_count', codec_options=CodecOptions())
    access_count_collection.insert_one(AccessCountModel().dict())

   if 'logs' not in db.list_collection_names():
    logs_collection = db.create_collection('logs', codec_options=CodecOptions())
    logs_collection.insert_one(LogsModel().dict())

   if 'long_url' not in db.list_collection_names():
    long_url_collection = db.create_collection('long_url', codec_options=CodecOptions())
    long_url_collection.insert_one(LongUrlModel().dict())

   if 'platforms' not in db.list_collection_names():
    platforms_collection = db.create_collection('platforms', codec_options=CodecOptions())
    platforms_collection.insert_one(PlatformModel().dict())
    
   if 'shortened_url' not in db.list_collection_names():
    shortened_url_collection = db.create_collection('shortened_url', codec_options=CodecOptions())
    shortened_url_collection.insert_one(ShortenedUrlModel().dict())
