from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QTextEdit,
    QLineEdit, QLabel, QSplitter, QSizePolicy, QFrame
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont


class MainWindow(QWidget):
    def __init__(self, note_manager, username, on_close_callback):
        super().__init__()
        self.note_manager = note_manager
        
        self.username = username
        self.setWindowTitle("Encrypted Notes - Obsidian Style")
        self.resize(1000, 600)

        self.set_dark_theme()

        # Панель с заметками
        self.notes_list = QListWidget()
        self.notes_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.notes_list.setMinimumWidth(250)
        self.notes_list.itemClicked.connect(self.display_note)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Поиск...")
        self.search_input.textChanged.connect(self.search_notes)

        # Левая колонка (поиск + список)
        self.left_panel = QVBoxLayout()
        self.left_panel.addWidget(self.search_input)
        self.left_panel.addWidget(self.notes_list)

        left_widget = QWidget()
        left_widget.setLayout(self.left_panel)

        # Редактор
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Заголовок заметки...")
        self.title_input.setFont(QFont("Segoe UI", 12, QFont.Bold))

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Содержимое заметки...")

        # Верхние кнопки
        self.save_button = QPushButton("💾 Сохранить")
        self.delete_button = QPushButton("🗑️ Удалить")
        self.new_button = QPushButton("➕ Новая")

        self.save_button.clicked.connect(self.save_note)
        self.delete_button.clicked.connect(self.delete_note)
        self.new_button.clicked.connect(self.new_note)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.new_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)

        # Центральная область
        self.editor_layout = QVBoxLayout()
        self.editor_layout.addWidget(self.title_input)
        self.editor_layout.addWidget(self.text_edit)
        self.editor_layout.addLayout(buttons_layout)

        right_widget = QWidget()
        right_widget.setLayout(self.editor_layout)

        # Разделение экрана
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        self.current_note_id = None
        self.refresh_notes_list()


        #Закрытие окна
        self.on_close_callback = on_close_callback

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

            QLineEdit, QTextEdit, QListWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #3c3c3c;
                border-radius: 6px;
                padding: 6px;
            }

            QLineEdit:focus, QTextEdit:focus, QListWidget:focus {
                border: 1px solid #5a5aff;
                background-color: #2f2f3a;
            }

            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
            }

            QPushButton:hover {
                background-color: #555;
            }

            QPushButton:pressed {
                background-color: #666;
            }
        """)


    # --- Логика редактирования
    def refresh_notes_list(self):
        self.notes_list.clear()
        for note in self.note_manager.get_all_notes():
            item = QListWidgetItem(note['title'])
            item.setData(Qt.UserRole, note['id'])  # сохраняем ID
            self.notes_list.addItem(item)


    def display_note(self, item):
        note_id = item.data(Qt.UserRole)  # получаем ID из item
        note = self.note_manager.get_note_by_id(note_id)
        if note:
            self.current_note_id = note['id']
            self.title_input.setText(note['title'])
            self.text_edit.setText(note['content'])


    def save_note(self):
        title = self.title_input.text().strip()
        content = self.text_edit.toPlainText()
        if self.current_note_id:
            self.note_manager.edit_note(self.current_note_id, title, content)
        else:
            self.note_manager.add_note(title, content)
        self.refresh_notes_list()
        self.clear_editor()

    def delete_note(self):
        if self.current_note_id:
            self.note_manager.delete_note(self.current_note_id)
            self.refresh_notes_list()
            self.clear_editor()

    def new_note(self):
        self.current_note_id = None
        self.clear_editor()

    def clear_editor(self):
        self.title_input.clear()
        self.text_edit.clear()

    def search_notes(self, query):
        results = self.note_manager.search_notes(query)
        self.notes_list.clear()
        for note in results:
            item = QListWidgetItem(note['title'])
            item.setData(Qt.UserRole, note['id'])  # тоже сохраняем ID
            self.notes_list.addItem(item)


    def closeEvent(self, event):
        self.on_close_callback()
        event.accept()


