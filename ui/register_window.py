from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class RegisterWindow(QWidget):
    def __init__(self, user_manager, on_register_success):
        super().__init__()
        self.setWindowTitle("Регистрация пользователя")
        self.user_manager = user_manager
        self.on_register_success = on_register_success

        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register)

        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return
        if self.user_manager.add_user(username, password):
            QMessageBox.information(self, "Успех", "Пользователь создан")
            self.on_register_success()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")
