import sys
import os
from PyQt5.QtWidgets import QApplication

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.admin_panel import AdminPanel
from ui.register_window import RegisterWindow

from users.user_manager import UserManager
from notes.note_manager import NoteManager

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

windows = {}
user_manager = UserManager()
os.makedirs("databases", exist_ok=True)

def show_login_window():
    windows['login'] = LoginWindow(
        user_manager,
        on_login_success=handle_login,
        on_admin_login=handle_login,
        on_register=open_register
    )
    windows['login'].show()

def handle_login(username, password):
    user_data = user_manager.get_user(username)
    if user_data and user_data['is_admin']:
        windows['admin'] = AdminPanel(master_password=password, on_close_callback=show_login_window)
        windows['admin'].show()
    else:
        user_db_path = f"databases/{username}.db"
        note_manager = NoteManager(password, db_path=user_db_path)
        windows['main'] = MainWindow(note_manager, username, on_close_callback=show_login_window)
        windows['main'].show()

    if 'login' in windows:
        windows['login'].close()

def open_register():
    windows['register'] = RegisterWindow(user_manager, on_register_success=show_login_window, on_close_callback=show_login_window)
    windows['register'].show()
    if 'login' in windows:
        windows['login'].close()

def main():
    app = QApplication(sys.argv)
    show_login_window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
