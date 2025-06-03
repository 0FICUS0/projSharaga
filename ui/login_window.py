from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from users.user_manager import UserManager
from notes.note_manager import NoteManager


class LoginWindow(QWidget):
    def __init__(self, on_login_success):
        super().__init__()
        self.setWindowTitle("Login")

        self.user_manager = UserManager()
        self.on_login_success = on_login_success

        # UI
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.status_label = QLabel()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.try_login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.user_manager.authenticate(username, password):
            note_manager = NoteManager(password, username=username)
            self.on_login_success(username, note_manager)
            self.close()
        else:
            self.status_label.setText("Неверный логин или пароль")

        # передаём управление наружу (main.py)
        self.on_login_success(username, password)

        # закрываем окно логина
        self.close()
