from pymongo.errors import PyMongoError
from infra.adapters.shortened.base_adapter import BaseAdapter
from infra.adapters.database.models.user_models import UserModel

class UserAdapter(BaseAdapter):
    def create_user(self, user: UserModel):
        try:
            collection = self.db['users']
            result =  collection.insert_one(user)
            return result.inserted_id is not None
        except PyMongoError as e:
            print(f"An error occurred while creating user: {e}")
            return False

    def get_user_by_username(self, username: str) -> UserModel:
        collection = self.db['users']
        user_dict = collection.find_one({"username": username})
        if user_dict:
            user_dict['id'] = str(user_dict.pop('_id'))
            return UserModel(**user_dict)
        return None
