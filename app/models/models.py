from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from bson import ObjectId
from mongoengine import Document, EmailField, UUIDField
from mongoengine import StringField


from argon2 import PasswordHasher
from app.db import db


def remove_sensitive_data_from_user_model(user, sensitive_keys):
    for key in sensitive_keys:
        user.pop(key)

    return user


class ObjectBase:

    def _get_element_by_id(self, id: str, collection: str):
        try:
            object_id = ObjectId(id)
            return db[collection].find_one({'_id': object_id})

        except Exception as e:
            return e


class User(Document, ObjectBase):
    COLLECTION = 'users'
    SENSITIVE_KEYS = ['hash']

    def __init__(self):
        super().__init__()

    email = EmailField(unique=True)
    hash = StringField()

    def get_by_id(self, id: str):
        user_data = super()._get_element_by_id(id, self.COLLECTION)
        user = remove_sensitive_data_from_user_model(user_data, self.SENSITIVE_KEYS)
        return user

    def login(self, email: str, password: str):
        user_data = db[self.COLLECTION].find_one({'email': email})
        if not user_data:
            return None

        ph = PasswordHasher()

        try:
            is_password_valid = ph.verify(user_data['hash'], password)
            if is_password_valid:
                user = remove_sensitive_data_from_user_model(user_data, self.SENSITIVE_KEYS)
                return user
            else:
                return None
        except (VerifyMismatchError, VerificationError, InvalidHash) as e:
            return None






