from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QToolButton
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class RegisterWindow(QWidget):
    def __init__(self, user_manager, on_register_success, on_close_callback):
        super().__init__()
        self.setWindowTitle("📝 Регистрация")
        self.resize(400, 320)


        self.on_close_callback = on_close_callback
        self.user_manager = user_manager
        self.on_register_success = on_register_success

        self.set_dark_theme()

        title_label = QLabel("Регистрация нового пользователя")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))

        # Логин
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        # Пароль
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Глаз для пароля
        self.toggle_password_button = QToolButton()
        self.toggle_password_button.setText("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)

        # Повтор пароля
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Повторите пароль")
        self.confirm_input.setEchoMode(QLineEdit.Password)

        # Кнопка регистрации
        self.register_button = QPushButton("✅ Зарегистрироваться")
        self.register_button.clicked.connect(self.register_user)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.username_input)
        layout.addLayout(password_layout)
        layout.addWidget(self.confirm_input)
        layout.addWidget(self.register_button)
        layout.addStretch()
        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Ошибка", "Пароли не совпадают.")
            return

        success = self.user_manager.add_user(username, password)
        if success:
            QMessageBox.information(self, "Успешно", "Регистрация прошла успешно.")
            self.on_register_success()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует.")

    def toggle_password_visibility(self):
        mode = QLineEdit.Normal if self.toggle_password_button.isChecked() else QLineEdit.Password
        self.password_input.setEchoMode(mode)
        self.confirm_input.setEchoMode(mode)

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

            QLineEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
                padding: 6px;
            }

            QPushButton, QToolButton {
                background-color: #444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }

            QPushButton:hover, QToolButton:hover {
                background-color: #555;
            }

            QPushButton:pressed, QToolButton:pressed {
                background-color: #666;
            }
        """)


    def closeEvent(self, event):
        self.on_close_callback()
        event.accept()