import sqlite3
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    name: str
    email: str
    password: str = field(repr=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_row(row):
        return User(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password=row["password"]
        )

    @staticmethod
    def get_by_id(db, user_id):
        row = db.execute("SELECT id, name, email, password FROM users WHERE id = ?", (user_id,)).fetchone()
        if row:
            return User.from_row(row)
        return None

    @staticmethod
    def get_by_email(db, email):
        row = db.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            return User.from_row(row)
        return None

    @staticmethod
    def get_all(db):
        rows = db.execute("SELECT id, name, email, password FROM users").fetchall()
        return [User.from_row(row) for row in rows]

    @staticmethod
    def create(db, name, email, password_hash):
        try:
            cursor = db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password_hash))
            db.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def update(db, user_id, name, email):
        try:
            result = db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
            db.commit()
            return result.rowcount > 0
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def delete(db, user_id):
        result = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        return result.rowcount > 0

    @staticmethod
    def search_by_name(db, name):
        rows = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
            } for row in rows
        ]
