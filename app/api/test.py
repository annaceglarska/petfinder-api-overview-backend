import argon2
from flask import Blueprint
from flask_cors import CORS

from app.middleware.auth import token_required


test_api_v1 = Blueprint(
    'test_api_v1', 'test_api_v1', url_prefix='/api/v1/test')

CORS(test_api_v1)


@test_api_v1.route('/protected', methods=['GET'])
@token_required
def protected(user):
    return {"message": "OK"}


@test_api_v1.route('/unprotected', methods=['GET'])
def unprotected():
    return {"message": "OK"}
