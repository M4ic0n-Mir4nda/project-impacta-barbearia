import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from cadastro import Cadastro
from connDB import ConnectDB
from message import messageDefault
from agendamento import Agendamento
from cadastroServico import CadastroServico
from relatorio import Relatorio


class MainWindow(QMainWindow):
    def __init__(self, nome="", permissao=0):
        super().__init__()
        self.nome = nome
        self.permissao = permissao
        self.setWindowTitle("Studio Beard")
        self.resize(750, 650)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowIcon(QtGui.QIcon("assets/iconBarber.ico"))
        self.setStyleSheet("QMainWindow {background: url(assets/wallpaper.jpg)}")
        QFontDatabase.addApplicationFont("GreatVibes-Regular.ttf")

        # ------------------------------------------------------

        self.lblUserLogin = QLabel(self)
        self.lblUserLogin.setGeometry(10, 10, 250, 50)
        self.lblUserLogin.setStyleSheet("background-color: #282828; border-radius: 5px")

        self.lblNomeUser = QLabel(self)
        self.lblNomeUser.setGeometry(69, 0, 180, 50)
        self.lblNomeUser.setStyleSheet("color: #fff; font-size: 14px; font-family: Arial")
        self.lblNomeUser.setText(self.nome)

        self.btnDeslogar = QPushButton(self)
        self.btnDeslogar.setGeometry(69, 37, 20, 20)
        self.btnDeslogar.setText("Sair")
        self.btnDeslogar.setStyleSheet("""
                    QPushButton {
                        color: #fff; 
                        border: none; 
                        background-color: #282828
                    }
                    QPushButton:hover {
                        background-color: #474747;
                    }
        """)

        self.imgUser = QLabel(self)
        self.imgUser.setGeometry(15, 13, 70, 70)
        self.imgUser.setStyleSheet("border-radius: 5px;")
        self.imgUser.setMouseTracking(True)
        self.pixmap = QPixmap('assets/imgUser.png')
        self.pixmap = self.pixmap.scaled(45, 45)
        self.imgUser.setPixmap(self.pixmap)
        self.imgUser.resize(self.pixmap.width(), self.pixmap.height())

        self.btnDeslogar.clicked.connect(self.deslogar)

        # ------------------------------------------------------

        self.lblServico = QPushButton(self)
        self.lblServico.setGeometry(160, 100, 150, 180)
        self.lblServico.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextServico = QLabel(self)
        self.lblTextServico.setText("Serviços")
        self.lblTextServico.setGeometry(195, 160, 100, 180)
        self.lblTextServico.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgNavalha = QLabel(self)
        self.imgNavalha.setGeometry(185, 120, 200, 180)
        self.imgNavalha.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.imgNavalha.setMouseTracking(True)
        self.pixmap = QPixmap('assets/imgNavalha.png')
        self.pixmap = self.pixmap.scaled(100, 100)
        self.imgNavalha.setPixmap(self.pixmap)
        self.imgNavalha.resize(self.pixmap.width(), self.pixmap.height())
        self.imgNavalha.mousePressEvent = self.pressCadastroServico

        # ------------------------------------------------------

        self.lblAgendamento = QLabel(self)
        self.lblAgendamento.setGeometry(450, 100, 150, 180)
        self.lblAgendamento.setStyleSheet("background-color: #282828; border-radius: 5px;")
        self.lblTextAgendamento = QLabel(self)
        self.lblTextAgendamento.setText("Agendamentos")
        self.lblTextAgendamento.setGeometry(460, 160, 130, 180)
        self.lblTextAgendamento.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

        self.imgCadeira = QLabel(self)
        self.imgCadeira.setGeometry(480, 120, 350, 100)
        self.pixmap = QPixmap('assets/imgCadeira.png')
        self.pixmap = self.pixmap.scaled(100, 100)
        self.imgCadeira.setPixmap(self.pixmap)
        self.imgCadeira.resize(self.pixmap.width(), self.pixmap.height())
        self.imgCadeira.mousePressEvent = self.pressAgendamento

        # ------------------------------------------------------

        try:
            if self.permissao == 1:
                self.lblCadastro = QLabel(self)
                self.lblCadastro.setGeometry(160, 410, 150, 180)
                self.lblCadastro.setStyleSheet("background-color: #282828; border-radius: 5px;")
                self.lblTextCadastro = QLabel(self)
                self.lblTextCadastro.setText("Cadastro")
                self.lblTextCadastro.setGeometry(190, 470, 100, 180)
                self.lblTextCadastro.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

                self.imgRegister = QLabel(self)
                self.imgRegister.setGeometry(200, 450, 350, 100)
                self.pixmap = QPixmap('assets/imgRegister.png')
                self.pixmap = self.pixmap.scaled(75, 75)
                self.imgRegister.setPixmap(self.pixmap)
                self.imgRegister.resize(self.pixmap.width(), self.pixmap.height())
                self.imgRegister.mousePressEvent = self.pressCadastro

                # ------------------------------------------------------

                self.lblRelatorios = QLabel(self)
                self.lblRelatorios.setGeometry(450, 410, 150, 180)
                self.lblRelatorios.setStyleSheet("background-color: #282828; border-radius: 5px;")
                self.lblTextRelatorios = QLabel(self)
                self.lblTextRelatorios.setText("Relátorios")
                self.lblTextRelatorios.setGeometry(475, 470, 130, 180)
                self.lblTextRelatorios.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

                self.imgRelatorios = QLabel(self)
                self.imgRelatorios.setGeometry(475, 430, 350, 100)
                self.pixmap = QPixmap('assets/imgRelatorio.png')
                self.pixmap = self.pixmap.scaled(105, 105)
                self.imgRelatorios.setPixmap(self.pixmap)
                self.imgRelatorios.resize(self.pixmap.width(), self.pixmap.height())
                self.imgRelatorios.mousePressEvent = self.pressRelatorio
            else:
                self.lblCadastro = QLabel(self)
                self.lblCadastro.setGeometry(300, 410, 150, 180)
                self.lblCadastro.setStyleSheet("background-color: #282828; border-radius: 5px;")
                self.lblTextCadastro = QLabel(self)
                self.lblTextCadastro.setText("Cadastro")
                self.lblTextCadastro.setGeometry(330, 470, 100, 180)
                self.lblTextCadastro.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

                self.imgRegister = QLabel(self)
                self.imgRegister.setGeometry(343, 450, 350, 100)
                self.pixmap = QPixmap('assets/imgRegister.png')
                self.pixmap = self.pixmap.scaled(75, 75)
                self.imgRegister.setPixmap(self.pixmap)
                self.imgRegister.resize(self.pixmap.width(), self.pixmap.height())
                self.imgRegister.mousePressEvent = self.pressCadastro
        except Exception as e:
            self.lblCadastro = QLabel(self)
            self.lblCadastro.setGeometry(160, 410, 150, 180)
            self.lblCadastro.setStyleSheet("background-color: #282828; border-radius: 5px;")
            self.lblTextCadastro = QLabel(self)
            self.lblTextCadastro.setText("Cadastro")
            self.lblTextCadastro.setGeometry(190, 470, 100, 180)
            self.lblTextCadastro.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

            self.imgRegister = QLabel(self)
            self.imgRegister.setGeometry(200, 450, 350, 100)
            self.pixmap = QPixmap('assets/imgRegister.png')
            self.pixmap = self.pixmap.scaled(75, 75)
            self.imgRegister.setPixmap(self.pixmap)
            self.imgRegister.resize(self.pixmap.width(), self.pixmap.height())
            self.imgRegister.mousePressEvent = self.pressCadastro

            # ------------------------------------------------------

            self.lblRelatorios = QLabel(self)
            self.lblRelatorios.setGeometry(450, 410, 150, 180)
            self.lblRelatorios.setStyleSheet("background-color: #282828; border-radius: 5px;")
            self.lblTextRelatorios = QLabel(self)
            self.lblTextRelatorios.setText("Relátorios")
            self.lblTextRelatorios.setGeometry(475, 470, 130, 180)
            self.lblTextRelatorios.setStyleSheet("font-size: 30px; color: #fff; font-family: 'Great Vibes', cursive;")

            self.imgRelatorios = QLabel(self)
            self.imgRelatorios.setGeometry(475, 430, 350, 100)
            self.pixmap = QPixmap('assets/imgRelatorio.png')
            self.pixmap = self.pixmap.scaled(105, 105)
            self.imgRelatorios.setPixmap(self.pixmap)
            self.imgRelatorios.resize(self.pixmap.width(), self.pixmap.height())
            self.imgRelatorios.mousePressEvent = self.pressRelatorio

    def pressCadastroServico(self, event):
        windowCadService = CadastroServico()
        windowCadService.exec()

    def pressCadastro(self, event):
        windowCad = Cadastro(self.permissao)
        windowCad.exec()

    def pressAgendamento(self, event):
        windowAgendamento = Agendamento(self)
        windowAgendamento.exec()

    def pressRelatorio(self, event):
        windowRelatorio = Relatorio()
        windowRelatorio.exec()

    def deslogar(self):
        self.permissao = 0
        self.nome = ""
        self.close()
        login.show()


class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 750, 712)
        self.setStyleSheet("background-color: #2c3e50")
        self.setWindowIcon(QtGui.QIcon("assets/iconBarber.ico"))
        self.setWindowTitle("Login")
        self.resize(700, 500)
        self.center_dialog()

        self.labelLogin = QLabel(self)
        self.labelLogin.setGeometry(25, 330, 150, 50)
        self.labelLogin.setText("Login:")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelLogin.setStyleSheet(
            "font-size: 25px; color: #fcfafa; font-family: 'ariel', cursive;")
        self.labelLogin.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtLogin = QLineEdit(self)
        self.txtLogin.setGeometry(65, 380, 200, 30)
        self.txtLogin.setPlaceholderText("Login de acesso...")
        self.txtLogin.setStyleSheet(
            "border: 3px solid #fcfafa; border-radius: 5px; font-size: 15px; color: #fcfafa; font-family: Arial")

        # ---------------------------------------------------

        self.labelSenha = QLabel(self)
        self.labelSenha.setGeometry(400, 330, 150, 50)
        self.labelSenha.setText("Senha:")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelSenha.setStyleSheet(
            "font-size: 25px; color: #fcfafa; font-family: 'ariel', cursive;")
        self.labelSenha.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtSenha = QLineEdit(self)
        self.txtSenha.setEchoMode(QLineEdit.Password)
        self.txtSenha.setGeometry(435, 380, 200, 30)
        self.txtSenha.setPlaceholderText("Senha...")
        self.txtSenha.setStyleSheet(
            "border: 3px solid #fcfafa; border-radius: 5px; font-size: 15px; color: #fcfafa; font-family: Arial")

        # ---------------------------------------------------

        entrar = QPushButton("ENTRAR", self)
        entrar.setGeometry(300, 430, 100, 30)
        entrar.setStyleSheet("""
                QPushButton {
                        border: 3px solid #fcfafa; 
                        border-radius: 5px; 
                        font-size: 12px;
                        font: bold; 
                        color: #fcfafa
                }
                QPushButton:hover {
                        background-color: #415B75;
                }
        """)
        entrar.clicked.connect(self.efetuarLogin)

        # ---------------------------------------------------

        self.logo = QLabel(self)
        self.logo.setGeometry(90, 25, 600, 300)
        self.logo.setPixmap(QtGui.QPixmap('assets/logo.png'))

    def efetuarLogin(self):
        conn = ConnectDB()
        if self.txtLogin.text() == "" or self.txtSenha.text() == "":
            messageDefault("Preencha os campos!")
            return True
        try:
            conn.conecta()
            nome = self.txtLogin.text().lower()
            senha = self.txtSenha.text().lower()
            sql = f"SELECT nome, senha, permissao FROM barbeiro where nome='{nome}' and senha='{senha}'"
            conn.execute(sql)
            usuario = conn.fetchone()
            if usuario:
                if nome == usuario['nome'].lower() and senha == usuario['senha'].lower():
                    self.close()
                    self.txtLogin.setText("")
                    self.txtSenha.setText("")
                    main = MainWindow(usuario['nome'], usuario['permissao'])
                    main.show()
            else:
                messageDefault("Usuario Invalido")
                return
        except Exception as e:
            print(e)
            messageDefault("Ocorreu algum erro")
            return False
        finally:
            conn.desconecta()

    def center_dialog(self):
        # Obtém o tamanho da tela
        screenGeo = QApplication.desktop().availableGeometry()

        # Obtém o retângulo da geometria do diálogo
        dialogGeo = self.frameGeometry()

        # Calcula a posição para centralizar o diálogo
        centerPoint = screenGeo.center()
        dialogGeo.moveCenter(centerPoint)

        self.move(dialogGeo.topLeft())  # Move o diálogo para a posição calculada


app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
login = Login()
login.show()
app.exec()
