import sqlite3
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str

    @staticmethod
    def from_row(row):
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password=row["password"]
        )

def get_user_by_id(db, user_id):
    row = db.execute("SELECT id, name, email, password FROM users WHERE id = ?", (user_id,)).fetchone()
    if row:
        return User.from_row(row)
    return None

def get_all_users(db):
    rows = db.execute("SELECT id, name, email, password FROM users").fetchall()
    return [User.from_row(row) for row in rows]
