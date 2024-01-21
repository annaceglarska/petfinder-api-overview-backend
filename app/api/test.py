from flask import Blueprint, request, jsonify
from flask_cors import CORS

from app.db import get_test

test_api_v1 = Blueprint(
    'test_api_v1', 'test_api_v1', url_prefix='/api/v1/test')

CORS(test_api_v1)


@test_api_v1.route('/', methods=['GET'])
def api_get_test():
    test = get_test()
    response = {
        'data': test
    }
    return jsonify(response)