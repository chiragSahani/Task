import sqlite3
import bcrypt

def init_db_main(db_path='users.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS users')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    users = [
        ('John Doe', 'john@example.com', 'password123'),
        ('Jane Smith', 'jane@example.com', 'secret456'),
        ('Bob Johnson', 'bob@example.com', 'qwerty789')
    ]

    for name, email, password in users:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db_main()
    print("Database initialized with sample data")