from flask import Blueprint, request, jsonify, abort
from .database import get_db
import bcrypt
import re
import sqlite3

bp = Blueprint('routes', __name__)

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@bp.route('/')
def home():
    return jsonify({"status": "ok", "message": "User Management System"}), 200

@bp.route('/users', methods=['GET'])
def get_all_users():
    db = get_db()
    users = db.execute("SELECT id, name, email FROM users").fetchall()
    return jsonify([dict(user) for user in users]), 200

@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        abort(404)
    return jsonify(dict(user)), 200

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    db = get_db()
    try:
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({"message": "User created"}), 201

@bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get('name')
    email = data.get('email')

    if not all([name, email]):
        return jsonify({"error": "Missing required fields"}), 400

    if not re.match(EMAIL_REGEX, email):
        return jsonify({"error": "Invalid email format"}), 400

    db = get_db()
    try:
        result = db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    if result.rowcount == 0:
        abort(404)

    return jsonify({"message": "User updated"}), 200

@bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    result = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    if result.rowcount == 0:
        abort(404)
    return jsonify({"message": f"User {user_id} deleted"}), 200

@bp.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400

    db = get_db()
    users = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    return jsonify([dict(user) for user in users]), 200

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    user = db.execute("SELECT id, password FROM users WHERE email = ?", (email,)).fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    else:
        return jsonify({"status": "failed", "message": "Invalid credentials"}), 401
