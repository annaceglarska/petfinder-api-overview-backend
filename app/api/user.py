from flask import Blueprint, request, jsonify
from flask_cors import CORS

from app.middleware.auth import token_required
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


@user_api_v1.route("/edit-user", methods=["POST"])
@token_required
def edit_user(user):
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400

        user_id = user.get("_id", None)
        result, error = User.edit_user(data, user_id)

        if result.acknowledged:
            updated_user = User.get_by_id(user_id)
            return {
                "message": "User updated successfully.",
                "data": updated_user,
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
