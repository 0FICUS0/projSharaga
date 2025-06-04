from PyQt5.QtWidgets import QMainWindow, QWidget, QListWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, note_manager):
        super().__init__()
        self.note_manager = note_manager
        self.setWindowTitle("Менеджер заметок")
        self.setGeometry(100, 100, 800, 500)
        self.current_note_id = None


        # Виджеты
        self.note_list = QListWidget()
        self.title_edit = QLineEdit()
        self.text_edit = QTextEdit()

        self.create_button = QPushButton("Создать")
        self.save_button = QPushButton("Сохранить")
        self.delete_button = QPushButton("Удалить")

        # Layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.note_list)
        left_layout.addWidget(self.create_button)
        left_layout.addWidget(self.delete_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.title_edit)
        right_layout.addWidget(self.text_edit)
        right_layout.addWidget(self.save_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Связка событий
        self.note_list.itemClicked.connect(self.load_note)
        self.create_button.clicked.connect(self.create_note)
        self.save_button.clicked.connect(self.save_note)
        self.delete_button.clicked.connect(self.delete_note)
        

        # Загрузим заметки
        self.refresh_notes()

    def refresh_notes(self):
        self.note_list.clear()
        self.notes = self.note_manager.get_all_notes()
        for note in self.notes:
            self.note_list.addItem(note['title'])

    def load_note(self, item):
        index = self.note_list.row(item)
        note = self.notes[index]
        self.current_note_id = note["id"]
        self.title_edit.setText(note["title"])
        self.text_edit.setPlainText(note["content"])

    def create_note(self):
        self.title_edit.clear()
        self.text_edit.clear()
        self.current_note_id = None

    def save_note(self):
        title = self.title_edit.text()
        content = self.text_edit.toPlainText()

        if not title.strip():
            QMessageBox.warning(self, "Ошибка", "Заголовок не может быть пустым.")
            return

        if self.current_note_id is None:
            self.note_manager.add_note(title, content)
        else:
            self.note_manager.edit_note(self.current_note_id, title, content)

        self.refresh_notes()

    def delete_note(self):
        if self.current_note_id is not None:
            self.note_manager.delete_note(self.current_note_id)
            self.current_note_id = None
            self.title_edit.clear()
            self.text_edit.clear()
            self.refresh_notes()