import argon2
import jwt
from flask import Blueprint, request, current_app, app, jsonify
from flask_cors import CORS

from app.models.models import User
from app.utils.exceptions import RequestException
from app.utils.validators import validate_email_and_password

auth_api_v1 = Blueprint(
    'auth_api_v1', 'auth_api_v1', url_prefix='/api/v1/auth')

CORS(auth_api_v1)


@auth_api_v1.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return {'message': 'Invalid data', 'data': None}, 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": str(user["_id"])},
                    current_app.config["JWT_SECRET_KEY"],
                    algorithm="HS512"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 401
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500


@auth_api_v1.route('/create-hash', methods=['POST'])
def create_hash():
    try:
        data = request.json
        if not data:
            raise RequestException("Not provided password.")
        password = data.get("password")
        if not password:
            raise RequestException("Not provided password.")
        hashed_password = argon2.PasswordHasher().hash('test')
        data = {
            'hash': hashed_password
        }
        return jsonify(data)
    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
