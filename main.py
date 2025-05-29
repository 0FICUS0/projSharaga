import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from notes.note_manager import NoteManager

def main():
    app = QApplication(sys.argv)

    # Callback при успешном вводе пароля
    def handle_login(master_password):
        note_manager = NoteManager(master_password)
        main_window = MainWindow(note_manager)
        main_window.show()

    # Показываем окно входа
    login_window = LoginWindow(handle_login)
    login_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
