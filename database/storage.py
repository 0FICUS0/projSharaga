import sqlite3

class Storage:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.ensure_tables_exist()

    def ensure_tables_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_note(self, title: str, content: str):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        self.conn.commit()

    def edit_note(self, note_id: int, title: str, content: str):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (title, content, note_id))
        self.conn.commit()

    def delete_note(self, note_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()

    def get_all_notes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title, content FROM notes")
        rows = cursor.fetchall()
        return [{'id': row[0], 'title': row[1], 'content': row[2]} for row in rows]