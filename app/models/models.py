import json
import argon2
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from argon2 import PasswordHasher
from app.db import db
from app.utils.exceptions import MissingAttributeException
from bson import ObjectId


def remove_sensitive_data_from_user_model(user, sensitive_keys):
    for key in sensitive_keys:
        user.pop(key)

    return user


def get_element_by_id(id: str, collection: str):
    try:
        object_id = ObjectId(id)
        return db[collection].find_one({'_id': object_id})

    except Exception as e:
        return e


class User:
    COLLECTION = 'users'
    SENSITIVE_KEYS = ['hash']

    @staticmethod
    def add_user(user_raw_data):
        try:
            password = user_raw_data.get('password', None)
            if not password:
                raise MissingAttributeException('Missing attribute in user data', 'password')
            hashed_password = argon2.PasswordHasher().hash(password)
            user_data = {
                'name': user_raw_data.get('name', None),
                'surname': user_raw_data.get('surname', None),
                'email': user_raw_data.get('email', None),
                'phone': user_raw_data.get('phone', None),
                'hash': hashed_password
            }
            result = db[User.COLLECTION].insert_one(user_data)
            user = db[User.COLLECTION].find_one({'_id': result.inserted_id})
            safe_data = remove_sensitive_data_from_user_model(user, User.SENSITIVE_KEYS)
            return safe_data, None
        except Exception as e:
            return None, e

    @staticmethod
    def edit_user(user_row_data, user_id):
        try:
            user_data = {
                'name': user_row_data.get('name', None),
                'surname': user_row_data.get('surname', None),
                'phone': user_row_data.get('phone', None)
            }
            result = db[User.COLLECTION].update_one({'_id': user_id}, {'$set': user_data})
            return result, None

        except Exception as e:
            return None, e

    @staticmethod
    def get_by_id(id: str):
        user_data = get_element_by_id(id, User.COLLECTION)
        user = remove_sensitive_data_from_user_model(user_data, User.SENSITIVE_KEYS)
        return user

    def login(email: str, password: str):
        user_data = db[User.COLLECTION].find_one({'email': email})
        if not user_data:
            return None

        ph = PasswordHasher()

        try:
            is_password_valid = ph.verify(user_data['hash'], password)
            if is_password_valid:
                user = remove_sensitive_data_from_user_model(user_data, User.SENSITIVE_KEYS)
                return user
            else:
                return None
        except (VerifyMismatchError, VerificationError, InvalidHash) as e:
            return None


