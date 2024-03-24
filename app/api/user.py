from flask import Blueprint, request, jsonify
from flask_cors import CORS

from app.models.models import User

user_api_v1 = Blueprint(
    'user_api_v1', 'user_api_v1', url_prefix='/api/v1/user')

CORS(user_api_v1)


@user_api_v1.route("/create-user", methods=["POST"])
def create_user():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate password
        password = data.get('password', None)
        repeat_password = data.get('repeat_password', None)
        if not password or not password == repeat_password:
            return {
                "message": "Password is not equal.",
                "data": None,
                "error": "Bad request"
            }
        user, error = User.add_user(data)

        if user:
            return {
                "message": "User created successfully.",
                "data": user,
            }, 201
        else:
            return {
                "message": "Something went wrong!",
                "error": str(error),
                "data": None
            }, 400

    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
