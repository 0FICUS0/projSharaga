import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from notes.note_manager import NoteManager
from users.user_manager import UserManager

windows = {}

def main():
    app = QApplication(sys.argv)

    # Callback при успешном вводе пароля
    def handle_login(username, password):
        note_manager = NoteManager(password, username=username)
        windows['main'] = MainWindow(note_manager)
        windows['main'].show()

        windows['login'] = LoginWindow(on_login_success=handle_login)
        windows['login'].show()



        

    # Показываем окно входа
    login_window = LoginWindow(handle_login)
    login_window.show()

    

    windows['login'] = LoginWindow(handle_login)
    windows['login'].show()
    windows['login'].close()

    

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
