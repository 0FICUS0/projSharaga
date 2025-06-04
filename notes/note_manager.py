from database.storage import Storage  # импортируем слой хранения
from crypto.crypto_manager import CryptoManager # импортируем шифратор

class NoteManager:
    def __init__(self, master_password: str):
        # Инициализация менеджера заметок
        self.crypto = CryptoManager(master_password)  # создаём шифратор с мастер-паролем
        self.storage = Storage()  # создаём объект хранения (SQLite)

    def add_note(self, title: str, content: str):
        # Шифруем содержимое заметки
        encrypted_content = self.crypto.encrypt(content)
        # Сохраняем в базу данных: заголовок + зашифрованный текст
        self.storage.add_note(title, encrypted_content)

    def edit_note(self, note_id: int, title: str, content: str):
        # Шифруем новый текст заметки перед сохранением
        encrypted_content = self.crypto.encrypt(content)
        # Обновляем запись в БД
        self.storage.edit_note(note_id, title, encrypted_content)

    def delete_note(self, note_id: int):
        # Удаляем заметку по ID
        self.storage.delete_note(note_id)

    def get_all_notes(self):
        # Получаем список всех заметок из БД
        encrypted_notes = self.storage.get_all_notes()
        # Расшифровываем каждую заметку
        decrypted_notes = []
        for note in encrypted_notes:
            try:
                decrypted_content = self.crypto.decrypt(note['content'])  # пробуем расшифровать
            except Exception:
                decrypted_content = "[Ошибка расшифровки]"  # если не получилось — предупреждение
            decrypted_notes.append({
                'id': note['id'],
                'title': note['title'],
                'content': decrypted_content
            })
        return decrypted_notes

    def search_notes(self, query: str):
        # Ищем по всем заметкам (после расшифровки)
        results = []
        for note in self.get_all_notes():
            if query.lower() in note['title'].lower() or query.lower() in note['content'].lower():
                results.append(note)
        return results


if __name__ == "__main__":
    nm = NoteManager("mypassword")
    nm.add_note("Test Title", "Secret content here.")
    notes = nm.get_all_notes()
    print(notes)