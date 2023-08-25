import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtCore import Qt
from cadastro import Cadastro
from agendamento import Agendamento
from connDB import ConnectDB


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barber Shop")
        self.resize(750, 650)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setStyleSheet("QMainWindow {background: url(wallpaper.jpg)}")
        QFontDatabase.addApplicationFont("GreatVibes-Regular.ttf")

        # ------------------------------------------------------

        self.lblNavalha = QPushButton(self)
        self.lblNavalha.setGeometry(160, 100, 150, 180)
        self.lblNavalha.setText("Teste")
        self.lblNavalha.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextNavalha = QLabel(self)
        self.lblTextNavalha.setText("Serviços")
        self.lblTextNavalha.setGeometry(195, 160, 100, 180)
        self.lblTextNavalha.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgNavalha = QLabel(self)
        self.imgNavalha.setGeometry(185, 120, 200, 180)
        self.imgNavalha.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.pixmap = QPixmap('imgNavalha.png')
        self.pixmap = self.pixmap.scaled(100, 100)
        self.imgNavalha.setPixmap(self.pixmap)
        self.imgNavalha.resize(self.pixmap.width(), self.pixmap.height())

        # ------------------------------------------------------

        self.lblAgendamento = QLabel(self)
        self.lblAgendamento.setGeometry(450, 100, 150, 180)
        self.lblAgendamento.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextAgendamento = QLabel(self)
        self.lblTextAgendamento.setText("Agendamentos")
        self.lblTextAgendamento.setGeometry(460, 160, 130, 180)
        self.lblTextAgendamento.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgAgendamento = QLabel(self)
        self.imgAgendamento.setGeometry(480, 120, 350, 100)
        self.pixmap = QPixmap('imgCadeira.png')
        self.pixmap = self.pixmap.scaled(100, 100)
        self.imgAgendamento.setPixmap(self.pixmap)
        self.imgAgendamento.resize(self.pixmap.width(), self.pixmap.height())
        self.imgAgendamento.mousePressEvent = self.pressAgendamento

        # ------------------------------------------------------

        self.lblCadastro = QLabel(self)
        self.lblCadastro.setGeometry(160, 410, 150, 180)
        self.lblCadastro.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextCadastro = QLabel(self)
        self.lblTextCadastro.setText("Cadastro")
        self.lblTextCadastro.setGeometry(190, 470, 100, 180)
        self.lblTextCadastro.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgUser = QLabel(self)
        self.imgUser.setGeometry(200, 450, 350, 100)
        self.pixmap = QPixmap('imgUser.png')
        self.pixmap = self.pixmap.scaled(75, 75)
        self.imgUser.setPixmap(self.pixmap)
        self.imgUser.resize(self.pixmap.width(), self.pixmap.height())
        self.imgUser.mousePressEvent = self.pressCadastro

        # ------------------------------------------------------

        self.lblAbout = QLabel(self)
        self.lblAbout.setGeometry(450, 410, 150, 180)
        self.lblAbout.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextAbout = QLabel(self)
        self.lblTextAbout.setText("Sobre nós")
        self.lblTextAbout.setGeometry(475, 470, 130, 180)
        self.lblTextAbout.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgAbout = QLabel(self)
        self.imgAbout.setGeometry(490, 450, 350, 100)
        self.pixmap = QPixmap('imgAbout.png')
        self.pixmap = self.pixmap.scaled(75, 75)
        self.imgAbout.setPixmap(self.pixmap)
        self.imgAbout.resize(self.pixmap.width(), self.pixmap.height())

    def pressCadastro(self, event):
        windowCad = Cadastro(self)
        windowCad.exec()

    def pressAgendamento(self, event):
        windowAgendamento = Agendamento(self)
        windowAgendamento.exec()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
