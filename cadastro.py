import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QDialog
from PyQt5.QtGui import QPixmap, QFontDatabase


class Cadastro(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Cadastros")
        self.setStyleSheet("QDialog {background: url(wallpaper.jpg)}")
        self.resize(750, 650)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Cadastro()
    window.show()
    sys.exit(app.exec())
