import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFontDatabase
from connDB import ConnectDB
from message import messageDefault
from datetime import datetime


class ClienteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 750, 712)
        self.background.setStyleSheet("background: url(assets/wallpaper.jpg)")

        self.labelNome = QLabel(self)
        self.labelNome.setGeometry(30, 80, 110, 45)
        self.labelNome.setText("Nome")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelNome.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff")
        self.labelNome.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtNome = QLineEdit(self)
        self.txtNome.setGeometry(30, 120, 450, 30)
        self.txtNome.setPlaceholderText("Nome...")
        self.txtNome.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

        # ---------------------------------------------------

        self.labelCpf = QLabel(self)
        self.labelCpf.setGeometry(30, 200, 110, 45)
        self.labelCpf.setText("Cpf")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelCpf.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff;")
        self.labelCpf.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtCpf = QLineEdit(self)
        self.txtCpf.setInputMask("999.999.999-99")
        self.txtCpf.setGeometry(30, 245, 450, 30)
        self.txtCpf.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

        # ---------------------------------------------------

        self.labelEmail = QLabel(self)
        self.labelEmail.setGeometry(30, 320, 110, 45)
        self.labelEmail.setText("Email")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelEmail.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff;")
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtEmail = QLineEdit(self)
        self.txtEmail.setGeometry(30, 360, 450, 30)
        self.txtEmail.setPlaceholderText("exemploemail@gmail.com")
        self.txtEmail.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

        # ---------------------------------------------------

        self.labelDataNasc = QLabel(self)
        self.labelDataNasc.setGeometry(30, 440, 230, 45)
        self.labelDataNasc.setText("Data de Nascimento")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelDataNasc.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff;")
        self.labelDataNasc.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtDataNasc = QLineEdit(self)
        self.txtDataNasc.setGeometry(30, 480, 450, 30)
        self.txtDataNasc.setInputMask("99/99/9999")
        self.txtDataNasc.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

    def insertData(self):
        conn = ConnectDB()
        try:
            conn.conecta()
            nome = self.txtNome.text()
            cpf = self.txtCpf.text()
            email = self.txtEmail.text()
            dataNasc = datetime.strptime(str(self.txtDataNasc.text()), '%d/%m/%Y').strftime('%Y%m%d')
            sql = f"insert into clientes (nome, cpf, email, datanasc) values ('{nome}', '{cpf}', '{email}', {dataNasc})"
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.desconecta()


class FuncionarioWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Tela de Cadastro de Funcionário")
        layout.addWidget(self.label)
        self.setLayout(layout)


class Cadastro(QDialog):
    def __init__(self, permissao, parent=None):
        super().__init__(parent)
        self.permissao = permissao
        self.setWindowTitle("Cadastros")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.resize(750, 712)
        self.center_dialog()

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 250, 712)
        self.container.setStyleSheet("background-color: #2c3e50")

        self.imgLogo = QLabel(self)
        self.imgLogo.setGeometry(20, 20, 100, 180)
        self.pixmap = QPixmap('assets/logo.png')
        self.pixmap = self.pixmap.scaled(200, 200)
        self.imgLogo.setPixmap(self.pixmap)
        self.imgLogo.resize(self.pixmap.width(), self.pixmap.height())

        self.clienteButton = QPushButton("Cliente", self.container)
        self.clienteButton.clicked.connect(self.showCliente)

        self.clienteButton.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )

        menuLayout = QVBoxLayout()
        menuLayout.setContentsMargins(10, 200, 10, 300)  # Ajuste as margens inferior para mover o menu para cima
        menuLayout.addWidget(self.clienteButton)

        if self.permissao == 1:
            self.funcionarioButton = QPushButton("Funcionário", self.container)
            self.funcionarioButton.clicked.connect(self.showFuncionario)
            menuLayout.addWidget(self.funcionarioButton)
            self.funcionarioButton.setStyleSheet(
                "QPushButton { background-color: #e74c3c; color: white; font-size: 16px; padding: 10px; border: none; }"
                "QPushButton:hover { background-color: #c0392b; }"
            )
        else:
            pass

        self.container.setLayout(menuLayout)

        self.stack = QStackedWidget(self)
        self.stack.setGeometry(250, 0, 503, 712)

        self.clienteWidget = ClienteWidget()
        self.funcionarioWidget = FuncionarioWidget()

        self.stack.addWidget(self.clienteWidget)
        self.stack.addWidget(self.funcionarioWidget)

        self.buttonSalvar = QPushButton("Salvar", self)
        self.buttonSalvar.setGeometry(390, 540, 200, 60)
        self.buttonSalvar.setStyleSheet("""
                                QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 10px}
                                QPushButton:hover { background-color: #2980b9; }
            """)

        self.buttonFechar = QPushButton("Fechar", self)
        self.buttonFechar.setGeometry(390, 630, 200, 60)
        self.buttonFechar.setStyleSheet("""
                                QPushButton { background-color: #FF0000; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 10px}
                                QPushButton:hover { background-color: #ff6961; }
            """)

        self.clienteWidget.txtNome.setFocus()
        self.buttonSalvar.clicked.connect(self.validateFields)
        self.buttonFechar.clicked.connect(self.closeWindow)

    def validateFields(self):
        validaCpf = None
        try:
            conn = ConnectDB()
            conn.conecta()
            sql = f"select cpf from clientes where cpf='{self.clienteWidget.txtCpf.text()}'"
            conn.execute(sql)
            cpfExist = conn.fetchone()
            validaCpf = cpfExist['cpf']
        except Exception as e:
            print(e)
        if self.clienteWidget.txtNome.text() == "" or self.clienteWidget.txtCpf.text() == "" or \
                self.clienteWidget.txtEmail.text() == "" or self.clienteWidget.txtDataNasc.text() == "":
            messageDefault("Preencha todos os campos!")
            return

        if not "@" in self.clienteWidget.txtEmail.text():
            messageDefault("Endereço de email inválido")
            return

        if validaCpf:
            messageDefault("CPF já cadastrado")
            return

        self.saveData()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            pass

    def saveData(self):
        try:
            self.buttonSalvar.setDisabled(True)
            self.buttonFechar.setDisabled(True)
            worker = WorkerThread(self)
            worker.start()
            worker.validationFinished.connect(self.handleValidationResult)
        except Exception as e:
            print(e)

    def handleValidationResult(self, validados):
        if validados:
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            messageDefault("Cadastro efetuado com sucesso")
            self.clienteWidget.txtNome.setText("")
            self.clienteWidget.txtCpf.setText("")
            self.clienteWidget.txtEmail.setText("")
            self.clienteWidget.txtDataNasc.setText("")
            self.clienteWidget.txtNome.setFocus()
        else:
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            messageDefault("Erro: Verifique os campos e tente novamente.")

    def closeWindow(self):
        self.close()

    def showCliente(self):
        self.stack.setCurrentWidget(self.clienteWidget)

    def showFuncionario(self):
        self.stack.setCurrentWidget(self.funcionarioWidget)

    # Centraliza a janela no meio da tela
    def center_dialog(self):
        # Obtém o tamanho da tela
        screenGeo = QApplication.desktop().availableGeometry()

        # Obtém o retângulo da geometria do diálogo
        dialogGeo = self.frameGeometry()

        # Calcula a posição para centralizar o diálogo
        centerPoint = screenGeo.center()
        dialogGeo.moveCenter(centerPoint)

        self.move(dialogGeo.topLeft())  # Move o diálogo para a posição calculada


class WorkerThread(QThread):
    validationFinished = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        retorno = self.parent().clienteWidget.insertData()
        self.validationFinished.emit(retorno)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cad = Cadastro()
    cad.show()
    sys.exit(app.exec_())
