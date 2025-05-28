import sqlite3
import datetime
from crypto.encryption import derive_key, encrypt_note, decrypt_note, generate_salt

print("note_manager загружен")

class NoteManager:
    def __init__(self, db_path="notes.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    ciphertext BLOB NOT NULL,
                    salt BLOB NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

    def add_note(self, title: str, text: str, password: str):
        salt = generate_salt()
        key = derive_key(password, salt)
        encrypted_text = encrypt_note(text, key)
        created_at = datetime.datetime.now().isoformat()

        with self.conn:
            self.conn.execute("""
                INSERT INTO notes (title, ciphertext, salt, created_at)
                VALUES (?, ?, ?, ?)
            """, (title, encrypted_text, salt, created_at))

    def get_note(self, note_id: int, password: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, ciphertext, salt FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if row:
            title, ciphertext, salt = row
            key = derive_key(password, salt)
            decrypted_text = decrypt_note(ciphertext, key)
            return f"{title}\n{decrypted_text}"
        else:
            return "[!] Note not found"

    def list_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, created_at FROM notes")
        return cursor.fetchall()
