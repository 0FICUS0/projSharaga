from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import sys

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Master Password")
        self.setGeometry(300, 300, 300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Master Password:")
        self.input = QLineEdit()
        self.input.setEchoMode(QLineEdit.Password)
        self.btn = QPushButton("Login")
        self.btn.clicked.connect(self.check_password)

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def check_password(self):
        pw = self.input.text()
        # 🔴 Пока проверка заглушка:
        if pw == "test":  # потом заменим на настоящую логику
            QMessageBox.information(self, "Success", "Correct password!")
            # Тут откроется основное окно потом
        else:
            QMessageBox.critical(self, "Error", "Wrong password!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
