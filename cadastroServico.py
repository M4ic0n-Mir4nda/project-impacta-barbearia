import sys
import locale
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QMessageBox, QComboBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRegExp, QThread, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap, QFontDatabase, QRegExpValidator, QIcon
from connDB import ConnectDB
from datetime import datetime
from message import messageDefault


def fDecimal(num):
    num = num.replace(",", "")
    num = num.replace(".", "")
    num = str(num).zfill(3)  # f"{num:03}"
    a = num[0:-2]
    b = num[-2:]
    num = a + "." + b
    valor = f"{float(num):.2f}".replace(".", ",")
    return valor


class CadastroServiceWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 750, 712)
        self.background.setStyleSheet("background: url(assets/wallpaper.jpg)")

        self.labelNomeServico = QLabel(self)
        self.labelNomeServico.setGeometry(30, 80, 200, 45)
        self.labelNomeServico.setText("Nome do Serviço")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelNomeServico.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff;")
        self.labelNomeServico.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtNome = QLineEdit(self)
        self.txtNome.setGeometry(30, 120, 450, 30)
        self.txtNome.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial; font-family: Arial")

        # ---------------------------------------------------

        self.labelTmpServico = QLabel(self)
        self.labelTmpServico.setGeometry(30, 260, 200, 45)
        self.labelTmpServico.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.labelTmpServico.setText("Tempo do Serviço")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelTmpServico.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff")
        self.txtTmpServico = QLineEdit(self)
        rx = QtCore.QRegExp("[/\d+\,?\d*/5]{2}")
        val = QRegExpValidator(rx)  # +++
        self.txtTmpServico.setValidator(val)
        self.txtTmpServico.setGeometry(30, 300, 355, 30)
        self.txtTmpServico.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtTmpServico.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

        self.box = QComboBox(self)
        self.box.setGeometry(400, 300, 80, 28)
        self.box.setStyleSheet("""
                    color: #fff; 
                    background-color: #282828;
                    border: 2px solid #fff; 
                    border-radius: 5px; 
                    font-size: 14px;
                    font-family: Arial;
        """)
        self.box.addItem("")
        self.box.addItem("minutos")
        self.box.addItem("horas")

        # ---------------------------------------------------

        self.labelValor = QLabel(self)
        self.labelValor.setGeometry(30, 440, 200, 45)
        self.labelValor.setText("Valor do Serviço")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelValor.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff")
        self.labelValor.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtValor = QLineEdit(self)
        self.txtValor.setGeometry(30, 480, 450, 30)
        self.txtValor.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtValor.setText("0,00")
        self.txtValor.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px; font-family: Arial")

        # ---------------------------------------------------

    def insertData(self):
        conn = ConnectDB()
        try:
            conn.conecta()
            nomeServico = self.txtNome.text()
            tempoServico = self.txtTmpServico.text()
            horas_minutos = self.box.currentText()
            valor = self.txtValor.text().replace(",", ".")
            val = (nomeServico, valor, tempoServico, horas_minutos)
            sql = f"""
                insert into servicos (nome_servico, valor_servico, tempo_servico, horas) values
                (%s, %s, %s, %s)
            """
            conn.execute(sql, val)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            conn.desconecta()


class CadastroServico(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        self.cadastroButton = QPushButton("Cadastrar", self.container)

        self.cadastroButton.clicked.connect(self.showCadastroServicos)

        self.cadastroButton.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )

        menuLayout = QVBoxLayout()
        menuLayout.setContentsMargins(10, 200, 10, 300)  # Ajuste as margens inferior para mover o menu para cima
        menuLayout.addWidget(self.cadastroButton)
        self.container.setLayout(menuLayout)

        self.stack = QStackedWidget(self)
        self.stack.setGeometry(250, 0, 503, 712)

        self.cadastroServiceWidget = CadastroServiceWidget()

        self.stack.addWidget(self.cadastroServiceWidget)

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

        self.cadastroServiceWidget.txtNome.setFocus()
        self.cadastroServiceWidget.txtValor.textChanged.connect(self.txtValorServico_textChanged)
        self.buttonSalvar.clicked.connect(self.saveData)
        self.buttonFechar.clicked.connect(self.closeWindow)

    def saveData(self):
        if self.cadastroServiceWidget.txtNome.text() == "" or self.cadastroServiceWidget.txtTmpServico.text() == "" or \
                self.cadastroServiceWidget.box.currentText() == "" or self.cadastroServiceWidget.txtValor.text() == "":
            messageDefault("Preencha todos os campos!")
            return
        tempoServico = int((self.cadastroServiceWidget.txtTmpServico.text()))
        if tempoServico < 5 and self.cadastroServiceWidget.box.currentText() == "minutos":
            messageDefault("Tempo do serviço precisa ser no minímo de 5 minutos")
            return
        if self.cadastroServiceWidget.txtValor.text() == "0,00":
            messageDefault("Defina algum valor para o serviço")
            return
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
            pass
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            messageDefault("Cadastro efetuado com sucesso")
            self.cadastroServiceWidget.txtNome.setText("")
            self.cadastroServiceWidget.txtTmpServico.setText("")
            self.cadastroServiceWidget.box.setCurrentIndex(0)
            self.cadastroServiceWidget.txtValor.setText("")
        else:
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            messageDefault("Erro: Verifique os campos e tente novamente")

    def txtValorServico_textChanged(self):
        text = self.cadastroServiceWidget.txtValor.text()
        self.cadastroServiceWidget.txtValor.setText(fDecimal(text))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            pass

    def closeWindow(self):
        self.close()

    def showCadastroServicos(self):
        self.stack.setCurrentWidget(self.cadastroServiceWidget)

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
        retorno = self.parent().cadastroServiceWidget.insertData()
        self.validationFinished.emit(retorno)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cad = CadastroServico()
    cad.show()
    sys.exit(app.exec_())
