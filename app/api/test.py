import argon2
from flask import Blueprint, request, jsonify
from flask_cors import CORS

# from app.db import get_test
from app.models.models import User

test_api_v1 = Blueprint(
    'test_api_v1', 'test_api_v1', url_prefix='/api/v1/test')

CORS(test_api_v1)


@test_api_v1.route('/', methods=['GET'])
def api_get_test():
    test = User().get_by_id("65aec6191c301b0e1c832787")
    response = {
        'password':  argon2.PasswordHasher().hash('test')
    }
    return jsonify(response)