from flask import Blueprint, request, jsonify, g
from .database import get_db
from .services import UserService
from .auth import token_required, generate_token
from .errors import bad_request_error, unauthorized_error, forbidden_error, not_found_error, conflict_error

bp = Blueprint('routes', __name__)

@bp.before_request
def before_request():
    g.user_service = UserService(get_db())

@bp.route('/')
def home():
    return jsonify({"status": "ok", "message": "User Management System"}), 200

@bp.route('/users', methods=['GET'])
@token_required
def get_all_users():
    users = g.user_service.get_all_users()
    return jsonify(users), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    user = g.user_service.get_user_by_id(user_id)
    if user is None:
        return not_found_error(f"User with id {user_id} not found")
    return jsonify(user), 200

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return bad_request_error("Invalid JSON")

    user, message = g.user_service.create_user(data)
    if user is None:
        if message == "Email already exists":
            return conflict_error(message)
        return bad_request_error(message)

    return jsonify(user), 201

@bp.route('/user/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.get_json()
    if not data:
        return bad_request_error("Invalid JSON")

    user, message = g.user_service.update_user(user_id, data, g.current_user)

    if user is None:
        if message == "Permission denied":
            return forbidden_error(message)
        if message == "User not found":
            return not_found_error(message)
        if message == "Email already exists":
            return conflict_error(message)
        return bad_request_error(message)

    return jsonify(user), 200

@bp.route('/user/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    success, message = g.user_service.delete_user(user_id, g.current_user)
    if not success:
        if message == "Permission denied":
            return forbidden_error(message)
        return not_found_error(message)

    return jsonify({"message": f"User {user_id} deleted"}), 200

@bp.route('/search', methods=['GET'])
@token_required
def search_users():
    name = request.args.get('name')
    users, message = g.user_service.search_users(name)
    if users is None:
        return bad_request_error(message)
    return jsonify(users), 200

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return bad_request_error("Invalid JSON")

    user, message = g.user_service.login(data)
    if user is None:
        return unauthorized_error(message)

    token = generate_token(user.id)
    return jsonify({'token': token}), 200
