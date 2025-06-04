from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QTextEdit, QLineEdit, QLabel, QMessageBox, QInputDialog, QComboBox
)

class MainWindow(QMainWindow):
    def __init__(self, note_manager, username):
        super().__init__()
        self.note_manager = note_manager
        self.username = username
        self.notes = []

        self.setWindowTitle(f"Заметки пользователя: {username}")
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Поиск и сортировка
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(self.search_notes)
        self.sort_box = QComboBox()
        self.sort_box.addItems(["По заголовку (А-Я)", "По заголовку (Я-А)"])
        self.sort_box.currentIndexChanged.connect(self.sort_notes)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.sort_box)
        main_layout.addLayout(search_layout)

        # Список заметок
        self.note_list = QListWidget()
        self.note_list.itemClicked.connect(self.load_note)
        main_layout.addWidget(self.note_list)

        # Кнопки действий
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Создать")
        self.save_button = QPushButton("Сохранить")
        self.delete_button = QPushButton("Удалить")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        main_layout.addLayout(button_layout)

        self.add_button.clicked.connect(self.add_note)
        self.save_button.clicked.connect(self.save_note)
        self.delete_button.clicked.connect(self.delete_note)

        # Поле редактирования текста
        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit)

        self.selected_note_id = None
        self.refresh_notes()

    def refresh_notes(self):
        self.notes = self.note_manager.get_all_notes()
        self.show_notes(self.notes)

    def show_notes(self, notes):
        self.note_list.clear()
        for note in notes:
            self.note_list.addItem(note['title'])

    def search_notes(self):
        query = self.search_input.text()
        if query:
            results = self.note_manager.search_notes(query)
            self.show_notes(results)
        else:
            self.refresh_notes()

    def sort_notes(self):
        current = self.sort_box.currentIndex()
        if current == 0:
            self.notes.sort(key=lambda n: n['title'])
        else:
            self.notes.sort(key=lambda n: n['title'], reverse=True)
        self.show_notes(self.notes)

    def load_note(self, item):
        title = item.text()
        for note in self.notes:
            if note['title'] == title:
                self.text_edit.setText(note['content'])
                self.selected_note_id = note['id']
                break

    def add_note(self):
        title, ok = QInputDialog.getText(self, "Новая заметка", "Введите заголовок:")
        if ok and title:
            self.note_manager.add_note(title, "")
            self.refresh_notes()

    def save_note(self):
        if self.selected_note_id is None:
            QMessageBox.warning(self, "Нет заметки", "Выберите заметку для сохранения")
            return
        title = self.note_list.currentItem().text()
        content = self.text_edit.toPlainText()
        self.note_manager.edit_note(self.selected_note_id, title, content)
        self.refresh_notes()

    def delete_note(self):
        if self.selected_note_id is None:
            QMessageBox.warning(self, "Нет заметки", "Выберите заметку для удаления")
            return
        self.note_manager.delete_note(self.selected_note_id)
        self.text_edit.clear()
        self.selected_note_id = None
        self.refresh_notes()
