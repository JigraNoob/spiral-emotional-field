from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/ping')
def ping():
    return jsonify({"status": "pong"})
