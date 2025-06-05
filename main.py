import sys
import os
from PyQt5.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.admin_panel import AdminPanel
from ui.register_window import RegisterWindow

from users.user_manager import UserManager
from notes.note_manager import NoteManager

MASTER_KEY = "adminmasterkey"


# добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# глобальные окна и менеджер пользователей
windows = {}
user_manager = UserManager(master_key=MASTER_KEY)
os.makedirs("databases", exist_ok=True)


def main():
    app = QApplication(sys.argv)

    # Обработчик успешного входа
    def handle_login(username, password):
        user_data = user_manager.get_user(username)
        if user_data and user_data['is_admin']:
            print("[DEBUG] Вход за админа")
            windows['admin'] = AdminPanel(master_password=MASTER_KEY)
            windows['admin'].show()
        else:
            user_db_path = f"databases/{username}.db"
            note_manager = NoteManager(password, db_path=user_db_path)
            windows['main'] = MainWindow(note_manager, username)
            windows['main'].show()

        if 'login' in windows:
            windows['login'].close()

    # Обработчик окна регистрации
    def open_register():
        windows['register'] = RegisterWindow(user_manager, on_register_success=show_login)
        windows['register'].show()
        if 'login' in windows:
            windows['login'].close()

    # Отображение окна входа
    def show_login():
        windows['login'] = LoginWindow(
            user_manager,
            on_login_success=handle_login,
            on_admin_login=handle_login,  # уже не нужен, обработка через handle_login
            on_register=open_register
        )
        windows['login'].show()

    # Запуск с окна входа
    show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
