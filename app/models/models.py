from argon2.exceptions import VerifyMismatchError
from bson import ObjectId
from mongoengine import Document, EmailField, UUIDField
from mongoengine import StringField


from argon2 import PasswordHasher
from app.db import db


class ObjectBase:

    def _get_element_by_id(self, id: str, collection: str):
        try:
            objectId = ObjectId(id)
            return db[collection].find_one({'_id': objectId})

        except Exception as e:
            return e


class User(Document, ObjectBase):
    COLLECTION = 'users'

    def __init__(self):
        super().__init__()

    email = EmailField(unique=True)
    hash = StringField()

    def get_by_id(self, id: str):
        return super()._get_element_by_id(id, self.COLLECTION)

    def login(self, email: str, password: str):
        user = db[self.COLLECTION].find_one({'email': email})
        if not user:
            return None

        ph = PasswordHasher()

        try:
            is_password_valid = ph.verify(user['hash'], password)
            return user if is_password_valid else None
        except VerifyMismatchError as e:
            return None



