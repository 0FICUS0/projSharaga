import sqlite3
import hashlib
import os

class UserManager:
    def __init__(self, user_db_path="users/users.db"):
        self.user_db_path = user_db_path
        os.makedirs(os.path.dirname(user_db_path), exist_ok=True)
        self.conn = sqlite3.connect(user_db_path)
        self._create_table()
        self._ensure_admin_exists()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                is_admin INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _ensure_admin_exists(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cur.fetchone()[0] == 0:
            self.add_user('admin', 'admin', is_admin=True)

    def add_user(self, username: str, password: str, is_admin=False):
        try:
            self.conn.execute(
                "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
                (username, self._hash_password(password), int(is_admin))
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_user(self, username: str):
        self.conn.execute("DELETE FROM users WHERE username = ?", (username,))
        self.conn.commit()
        db_path = f"data/{username}.db"
        if os.path.exists(db_path):
            os.remove(db_path)

    def authenticate(self, username: str, password: str) -> str | None:
        cur = self.conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and row[0] == self._hash_password(password):
            return f"data/{username}.db"
        return None
    
    def is_admin(self, username: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        return bool(row[0]) if row else False
    
    def get_user(self, username: str) -> dict | None:
        cur = self.conn.cursor()
        cur.execute("SELECT username, password_hash, is_admin FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row:
            return {
                "username": row[0],
                "password_hash": row[1],
                "is_admin": bool(row[2])
            }
        return None
    
    def get_all_users(self) -> list:
        cur = self.conn.cursor()
        cur.execute("SELECT username, is_admin FROM users")
        rows = cur.fetchall()
        return [{'username': row[0], 'is_admin': bool(row[1])} for row in rows]
