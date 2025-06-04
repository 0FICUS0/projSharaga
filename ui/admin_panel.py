from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QLineEdit,
    QLabel, QMessageBox, QHBoxLayout
)

from users.user_manager import UserManager

class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ-панель пользователей")
        self.user_manager = UserManager()

        # Основной layout
        layout = QVBoxLayout()

        # Заголовок
        layout.addWidget(QLabel("Список пользователей:"))

        # Список пользователей
        self.user_list = QListWidget()
        layout.addWidget(self.user_list)

        # Кнопки удаления и обновления
        btn_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Обновить список")
        self.refresh_button.clicked.connect(self.load_users)
        btn_layout.addWidget(self.refresh_button)

        self.delete_button = QPushButton("Удалить выбранного")
        self.delete_button.clicked.connect(self.delete_selected_user)
        btn_layout.addWidget(self.delete_button)

        layout.addLayout(btn_layout)

        # Добавление нового пользователя (GUI)
        layout.addWidget(QLabel("Добавить нового пользователя:"))
        self.new_username = QLineEdit()
        self.new_username.setPlaceholderText("Имя пользователя")
        layout.addWidget(self.new_username)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("Пароль")
        self.new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password)

        self.admin_checkbox = QPushButton("Добавить как администратора")
        self.admin_checkbox.setCheckable(True)
        layout.addWidget(self.admin_checkbox)

        self.add_button = QPushButton("Создать пользователя")
        self.add_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        self.user_list.clear()
        users = self.user_manager.get_all_users()
        for u in users:
            is_admin = "[admin]" if u['is_admin'] else ""
            self.user_list.addItem(f"{u['username']} {is_admin}")

    def delete_selected_user(self):
        selected = self.user_list.currentItem()
        if selected:
            username = selected.text().split()[0]
            if username == "admin":
                QMessageBox.warning(self, "Ошибка", "Нельзя удалить пользователя admin")
                return
            self.user_manager.delete_user(username)
            QMessageBox.information(self, "Успешно", f"Пользователь {username} удалён")
            self.load_users()

    def add_user(self):
        username = self.new_username.text().strip()
        password = self.new_password.text().strip()
        is_admin = self.admin_checkbox.isChecked()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")
            return

        success = self.user_manager.add_user(username, password, is_admin)
        if success:
            QMessageBox.information(self, "Успешно", f"Пользователь {username} создан")
            self.load_users()
            self.new_username.clear()
            self.new_password.clear()
            self.admin_checkbox.setChecked(False)
        else:
            QMessageBox.warning(self, "Ошибка", f"Пользователь {username} уже существует")
