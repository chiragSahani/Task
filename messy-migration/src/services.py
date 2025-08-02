import bcrypt
import re
from .models import User
from .auth import generate_token

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

class UserService:
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        users = User.get_all(self.db)
        return [user.to_dict() for user in users]

    def get_user_by_id(self, user_id):
        user = User.get_by_id(self.db, user_id)
        if user:
            return user.to_dict()
        return None

    def create_user(self, data):
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return None, "Missing required fields"

        if not re.match(EMAIL_REGEX, email):
            return None, "Invalid email format"

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_id = User.create(self.db, name, email, hashed_password)
        if not user_id:
            return None, "Email already exists"

        new_user = User.get_by_id(self.db, user_id)
        return new_user.to_dict(), "User created"

    def update_user(self, user_id, data, current_user):
        if user_id != current_user.id:
             return None, "Permission denied"

        name = data.get('name')
        email = data.get('email')

        if not all([name, email]):
            return None, "Missing required fields"

        if not re.match(EMAIL_REGEX, email):
            return None, "Invalid email format"

        user = User.get_by_id(self.db, user_id)
        if not user:
            return None, "User not found"

        success = User.update(self.db, user_id, name, email)
        if not success:
            return None, "Email already exists"

        updated_user = User.get_by_id(self.db, user_id)
        return updated_user.to_dict(), "User updated"

    def delete_user(self, user_id, current_user):
        if user_id != current_user.id:
            return False, "Permission denied"

        success = User.delete(self.db, user_id)
        return success, "User deleted" if success else "User not found"

    def search_users(self, name):
        if not name:
            return None, "Please provide a name to search"
        users = User.search_by_name(self.db, name)
        return users, "Users found"

    def login(self, data):
        email = data.get('email')
        password = data.get('password')

        if not all([email, password]):
            return None, "Missing required fields"

        user = User.get_by_email(self.db, email)

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            return user, "Login successful"

        return None, "Invalid credentials"
