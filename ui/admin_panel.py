from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QLabel, QTextEdit, QPushButton, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from users.user_manager import UserManager
from notes.note_manager import NoteManager


class AdminPanel(QWidget):
    def __init__(self, master_password, on_close_callback):
        super().__init__()
        self.setWindowTitle("Админ-панель")
        self.resize(1000, 600)

        self.master_password = master_password
        self.user_manager = UserManager(master_key=master_password)
        self.note_manager_cache = {}  # кэш NoteManager'ов
        self.users_data = {}  # username -> encrypted_password
        
        print("[DEBUG] AdminPanel master password:", self.master_password)

        self.set_dark_theme()

        self.users_list = QListWidget()
        self.users_list.setMinimumWidth(250)
        self.users_list.itemClicked.connect(self.load_user_notes)

        self.notes_view = QTextEdit()
        self.notes_view.setReadOnly(True)

        self.info_label = QLabel("Выберите пользователя для просмотра заметок и пароля")
        self.info_label.setFont(QFont("Segoe UI", 10))
        self.info_label.setStyleSheet("padding: 5px;")

        self.refresh_button = QPushButton("🔄 Обновить список")
        self.refresh_button.clicked.connect(self.load_users)

        self.on_close_callback = on_close_callback

        left_panel = QVBoxLayout()
        left_panel.addWidget(self.refresh_button)
        left_panel.addWidget(self.users_list)

        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.info_label)
        right_panel.addWidget(self.notes_view)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.load_users()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(60, 60, 60))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.Highlight, QColor(100, 100, 255))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QListWidget {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
            }
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

    def load_users(self):
        self.users_list.clear()
        self.users_data = {}
        users = self.user_manager.get_all_users()
        for user in users:
            username = user['username']
            encrypted_pw = user['password_encrypted']
            is_admin = user['is_admin']
            try:
                decrypted_pw = self.user_manager.decrypt_password(encrypted_pw)
            except Exception:
                decrypted_pw = "[Ошибка расшифровки]"

            self.users_data[username] = {
                'encrypted': encrypted_pw,
                'decrypted': decrypted_pw
            }

            label = f"{username} (админ)" if is_admin else username
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, username)
            self.users_list.addItem(item)


    def load_user_notes(self, item):
        username = item.data(Qt.UserRole)
        db_path = f"databases/{username}.db"

        try:
            user_info = self.users_data.get(username)
            decrypted_pw = user_info['decrypted']

            if username not in self.note_manager_cache:
                self.note_manager_cache[username] = NoteManager(decrypted_pw, db_path)

            note_manager = self.note_manager_cache[username]
            notes = note_manager.get_all_notes()

            if notes:
                output = f"Заметки пользователя {username}:\n\n"
                for note in notes:
                    output += f"📌 {note['title']}\n{note['content']}\n{'-' * 40}\n"
            else:
                output = f"У пользователя {username} нет заметок."

            self.info_label.setText(f"Пользователь: {username} | Пароль: {decrypted_pw}")
            self.notes_view.setText(output)

        except Exception as e:
            self.info_label.setText(f"[Ошибка] Не удалось загрузить данные: {e}")
            self.notes_view.clear()


    def closeEvent(self, event):
        self.on_close_callback()
        event.accept()


