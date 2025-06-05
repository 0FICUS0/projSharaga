from database.storage import Storage  # импортируем слой хранения
from crypto.crypto_manager import CryptoManager  # импортируем шифратор

class NoteManager:
    def __init__(self, master_password: str, db_path: str):
        self.crypto = CryptoManager(master_password)
        self.storage = Storage(db_path)

    def add_note(self, title: str, content: str):
        encrypted_content = self.crypto.encrypt(content)
        self.storage.add_note(title, encrypted_content)

    def edit_note(self, note_id: int, title: str, content: str):
        encrypted_content = self.crypto.encrypt(content)
        self.storage.edit_note(note_id, title, encrypted_content)

    def delete_note(self, note_id: int):
        self.storage.delete_note(note_id)

    def get_all_notes(self):
        encrypted_notes = self.storage.get_all_notes()
        decrypted_notes = []
        for note in encrypted_notes:
            try:
                decrypted_content = self.crypto.decrypt(note['content'])
            except Exception:
                decrypted_content = "[Ошибка расшифровки]"
            decrypted_notes.append({
                'id': note['id'],
                'title': note['title'],
                'content': decrypted_content
            })
        return decrypted_notes

    def search_notes(self, query: str):
        results = []
        for note in self.get_all_notes():
            if query.lower() in note['title'].lower() or query.lower() in note['content'].lower():
                results.append(note)
        return results

    def get_note_by_id(self, note_id: int):
        """Возвращает одну расшифрованную заметку по её ID"""
        for note in self.get_all_notes():
            if note['id'] == note_id:
                return note
        return None
