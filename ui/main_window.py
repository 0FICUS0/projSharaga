from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, note_manager):
        super().__init__()
        self.note_manager = note_manager
        self.setWindowTitle("Менеджер заметок")

        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)