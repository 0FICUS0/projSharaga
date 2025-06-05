from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QMessageBox, QToolButton
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, user_manager, on_login_success, on_admin_login, on_register):
        super().__init__()
        self.setWindowTitle("🔐 Вход в систему")
        self.resize(400, 300)

        self.user_manager = user_manager
        self.on_login_success = on_login_success
        self.on_admin_login = on_admin_login
        self.on_register = on_register

        self.set_dark_theme()

        # Заголовок
        title_label = QLabel("Вход в систему")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        # Кнопка-глаз
        self.toggle_password_button = QToolButton()
        self.toggle_password_button.setText("👁️")
        self.toggle_password_button.setCheckable(True)
        self.toggle_password_button.setCursor(Qt.PointingHandCursor)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Поле пароля + глаз в одной строке
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password_button)

        # Кнопки входа/регистрации
        self.login_button = QPushButton("🔓 Войти")
        self.login_button.clicked.connect(self.try_login)

        self.register_button = QPushButton("📝 Зарегистрироваться")
        self.register_button.clicked.connect(self.on_register)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.login_button)
        btn_row.addWidget(self.register_button)

        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.username_input)
        layout.addLayout(password_layout)
        layout.addLayout(btn_row)
        layout.addStretch()
        self.setLayout(layout)

    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if self.user_manager.authenticate(username, password):
            if self.user_manager.is_admin(username):
                self.on_admin_login(username, password)
            else:
                self.on_login_success(username, password)
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def toggle_password_visibility(self):
        if self.toggle_password_button.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

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
