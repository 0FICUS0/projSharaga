import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QTextEdit, QLineEdit, QLabel, QMessageBox, QInputDialog
)

# пока нет логики — фейковые данные
notes = {}

def start_app():
    app = QApplication(sys.argv)
    login_window = PasswordWindow()
    login_window.show()
    sys.exit(app.exec_())


class PasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Master Password")
        self.setGeometry(100, 100, 300, 100)
        layout = QVBoxLayout()

        self.label = QLabel("Enter master password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.check_password)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def check_password(self):
        # пока пароль не проверяется — просто открываем основное окно
        password = self.password_input.text()
        self.main_window = NotesWindow(password)
        self.main_window.show()
        self.close()


class NotesWindow(QWidget):
    def __init__(self, password):
        super().__init__()
        self.password = password  # пригодится позже
        self.setWindowTitle("Encrypted Notes")
        self.setGeometry(100, 100, 600, 400)

        layout = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()

        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_note)

        self.text_edit = QTextEdit()

        self.btn_new = QPushButton("New Note")
        self.btn_save = QPushButton("Save")
        self.btn_delete = QPushButton("Delete")

        self.btn_new.clicked.connect(self.new_note)
        self.btn_save.clicked.connect(self.save_note)
        self.btn_delete.clicked.connect(self.delete_note)

        left.addWidget(self.notes_list)
        left.addWidget(self.btn_new)
        left.addWidget(self.btn_save)
        left.addWidget(self.btn_delete)

        right.addWidget(self.text_edit)

        layout.addLayout(left)
        layout.addLayout(right)

        self.setLayout(layout)
        self.refresh_notes()

    def refresh_notes(self):
        self.notes_list.clear()
        for title in notes:
            self.notes_list.addItem(title)

    def load_note(self):
        selected = self.notes_list.currentItem()
        if selected:
            title = selected.text()
            content = notes.get(title, "")
            self.text_edit.setText(content)

    def new_note(self):
        title, ok = QInputDialog.getText(self, "New Note", "Enter note title:")
        if ok and title:
            notes[title] = ""
            self.refresh_notes()

    def save_note(self):
        selected = self.notes_list.currentItem()
        if selected:
            title = selected.text()
            notes[title] = self.text_edit.toPlainText()
        else:
            QMessageBox.warning(self, "No note selected", "Please select a note to save.")

    def delete_note(self):
        selected = self.notes_list.currentItem()
        if selected:
            title = selected.text()
            del notes[title]
            self.text_edit.clear()
            self.refresh_notes()
