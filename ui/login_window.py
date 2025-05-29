from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow
import sys

class LoginWindow(QMainWindow):
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success

        self.setWindowTitle("Вход по мастер-паролю")

        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)

        self.label = QLabel("Введите мастер-пароль:")

        self.button = QPushButton("Войти")
        self.button.clicked.connect(self.try_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def try_login(self):
        password = self.input.text()
        # тут можно добавить проверку пароля, пока просто передаём его
        self.on_login_success(password)
        self.close()
