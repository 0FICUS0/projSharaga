import sqlite3

class Storage:
    def __init__(self, db_path="notes.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            ''')
            conn.commit()

    def add_note(self, title, content):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            conn.commit()

    def get_all_notes(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content FROM notes")
        rows = cursor.fetchall()
        conn.close()
        return [{'id': row[0], 'title': row[1], 'content': row[2]} for row in rows]


    def update_note(self, note_id, new_title, new_content):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (new_title, new_content, note_id))
            conn.commit()

    def delete_note(self, note_id):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()
