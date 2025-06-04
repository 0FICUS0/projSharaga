from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from users.user_manager import UserManager

class LoginWindow(QWidget):
    def __init__(self, user_manager, on_login_success, on_admin_login, on_register):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.user_manager = user_manager
        self.on_login_success = on_login_success
        self.on_admin_login = on_admin_login
        self.on_register = on_register

        self.username_label = QLabel("Логин:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.try_login)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.on_register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.user_manager.authenticate(username, password):
            if self.user_manager.is_admin(username):
                self.on_admin_login()
            else:
                self.on_login_success(username, password)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
