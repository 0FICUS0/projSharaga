import os
import sqlite3
import hashlib

class UserManager:
    def __init__(self, users_db_path='users/users.db', db_dir='databases'):
        self.users_db_path = users_db_path
        self.db_dir = db_dir
        os.makedirs(os.path.dirname(users_db_path), exist_ok=True)
        os.makedirs(db_dir, exist_ok=True)
        self._init_users_table()

    def _init_users_table(self):
        with sqlite3.connect(self.users_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin INTEGER DEFAULT 0,
                    db_path TEXT
                )
            ''')
            conn.commit()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, is_admin=False, db_path=None):
        if db_path is None:
            db_path = os.path.join(self.db_dir, f"{username}.db")
        password_hash = self._hash_password(password)
        try:
            with sqlite3.connect(self.users_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, is_admin, db_path)
                    VALUES (?, ?, ?, ?)
                ''', (username, password_hash, int(is_admin), db_path))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Пользователь уже существует

    def delete_user(self, username):
        with sqlite3.connect(self.users_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT db_path FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                db_path = row[0]
                if os.path.exists(db_path):
                    os.remove(db_path)
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()

    def authenticate(self, username, password):
        password_hash = self._hash_password(password)
        with sqlite3.connect(self.users_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT username, is_admin, db_path FROM users
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            row = cursor.fetchone()
            if row:
                return {
                    'username': row[0],
                    'is_admin': bool(row[1]),
                    'db_path': row[2]
                }
            return None


if __name__ == "__main__":
    um = UserManager()
    if um.add_user("admin", "adminpass", is_admin=True, db_path=os.path.join("databases", "shared.db")):
        print("Admin user created")
    else:
        print("Admin already exists")
