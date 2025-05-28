from note_manager import NoteManager

print("импорт удался")  

manager = NoteManager()

password = "my_secret"

# Создаём заметку
manager.add_note("Моя первая заметка", "Это текст, который зашифруется.", password)

# Показываем список
for note in manager.list_notes():
    print(f"[{note[0]}] {note[1]} ({note[2]})")

# Расшифровываем первую
print("\n>> Расшифрованная заметка:")
print(manager.get_note(1, password))
