import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QMessageBox
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRegExp, QThread, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap, QFontDatabase, QRegExpValidator, QIcon
from connDB import ConnectDB
from datetime import datetime


class ClienteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 753, 700)
        self.background.setStyleSheet("background: url(wallpaper.jpg)")

        self.labelNome = QLabel(self)
        self.labelNome.setGeometry(30, 80, 110, 45)
        self.labelNome.setText("Nome")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelNome.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelNome.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtNome = QLineEdit(self)
        self.txtNome.setGeometry(30, 120, 450, 30)
        self.txtNome.setPlaceholderText("Nome...")
        self.txtNome.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelCpf = QLabel(self)
        self.labelCpf.setGeometry(30, 200, 110, 45)
        self.labelCpf.setText("Cpf")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelCpf.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelCpf.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtCpf = QLineEdit(self)
        self.txtCpf.setInputMask("999.999.999-99")
        self.txtCpf.setGeometry(30, 245, 450, 30)
        self.txtCpf.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelEmail = QLabel(self)
        self.labelEmail.setGeometry(30, 320, 110, 45)
        self.labelEmail.setText("Email")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelEmail.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtEmail = QLineEdit(self)
        self.txtEmail.setGeometry(30, 360, 450, 30)
        self.txtEmail.setPlaceholderText("exemploemail@gmail.com")
        self.txtEmail.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelDataNasc = QLabel(self)
        self.labelDataNasc.setGeometry(30, 440, 230, 45)
        self.labelDataNasc.setText("Data de Nascimento")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelDataNasc.setStyleSheet(
            "font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelDataNasc.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtDataNasc = QLineEdit(self)
        self.txtDataNasc.setGeometry(30, 480, 450, 30)
        self.txtDataNasc.setInputMask("99/99/9999")
        self.txtDataNasc.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

    def insertData(self):
        try:
            conn = ConnectDB()
            conn.conecta()
            nome = self.txtNome.text().upper()
            cpf = self.txtCpf.text()
            email = self.txtEmail.text()
            if not "@" in email:
                print('Não tem @')
                return False
            dataNasc = datetime.strptime(str(self.txtDataNasc.text()), '%d/%m/%Y').strftime('%Y%m%d')
            print(dataNasc)
            # sql = f"insert into clientes (nome, cpf, email, datanasc) values ('Kaique Fischer', '123.456.789-89', 'kaique@kaique.com', 20230804)"
            sql = f"insert into clientes (nome, cpf, email, datanasc) values ('{nome}', '{cpf}', '{email}', {dataNasc})"
            conn.execute(sql)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False


class FuncionarioWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Tela de Cadastro de Funcionário")
        layout.addWidget(self.label)
        self.setLayout(layout)


class Cadastro(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastros")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(305, 10, 753, 700)

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 250, 700)
        self.container.setStyleSheet("background-color: #2c3e50")

        self.imgLogo = QLabel(self)
        self.imgLogo.setGeometry(20, 20, 100, 180)
        self.pixmap = QPixmap('title.png')
        self.pixmap = self.pixmap.scaled(200, 200)
        self.imgLogo.setPixmap(self.pixmap)
        self.imgLogo.resize(self.pixmap.width(), self.pixmap.height())

        self.cliente_button = QPushButton("Cliente", self.container)
        self.funcionario_button = QPushButton("Funcionário", self.container)

        self.cliente_button.clicked.connect(self.showCliente)
        self.funcionario_button.clicked.connect(self.showFuncionario)

        self.cliente_button.setStyleSheet(
            "QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; }"
            "QPushButton:hover { background-color: #2980b9; }"
        )

        self.funcionario_button.setStyleSheet(
            "QPushButton { background-color: #e74c3c; color: white; font-size: 16px; padding: 10px; border: none; }"
            "QPushButton:hover { background-color: #c0392b; }"
        )

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10, 200, 10, 300)  # Ajuste as margens inferior para mover o menu para cima
        menu_layout.addWidget(self.cliente_button)
        menu_layout.addWidget(self.funcionario_button)
        self.container.setLayout(menu_layout)

        self.stack = QStackedWidget(self)
        self.stack.setGeometry(250, 0, 503, 700)

        self.cliente_widget = ClienteWidget()
        self.funcionario_widget = FuncionarioWidget()

        self.stack.addWidget(self.cliente_widget)
        self.stack.addWidget(self.funcionario_widget)

        self.buttonSalvar = QPushButton("Salvar", self)
        self.buttonSalvar.setGeometry(390, 540, 200, 60)
        self.buttonSalvar.setStyleSheet("""
                                QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 10px}
                                QPushButton:hover { background-color: #2980b9; }
            """)

        self.buttonFechar = QPushButton("Fechar", self)
        self.buttonFechar.setGeometry(390, 620, 200, 60)
        self.buttonFechar.setStyleSheet("""
                                QPushButton { background-color: #FF0000; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 10px}
                                QPushButton:hover { background-color: #ff6961; }
            """)

        self.cliente_widget.txtNome.setFocus()
        self.buttonSalvar.clicked.connect(self.validateFields)
        self.buttonFechar.clicked.connect(self.closeWindow)

    def validateFields(self):
        validaCpf = None
        try:
            conn = ConnectDB()
            conn.conecta()
            sql = f"select cpf from clientes where cpf='{self.cliente_widget.txtCpf.text()}'"
            conn.execute(sql)
            cpfExist = conn.fetchone()
            validaCpf = cpfExist['cpf']
        except Exception as e:
            print(e)
        if self.cliente_widget.txtNome.text() == "" or self.cliente_widget.txtCpf.text() == "" or \
                self.cliente_widget.txtEmail.text() == "" or self.cliente_widget.txtDataNasc.text() == "":
            info_box = QMessageBox(self)
            info_box.setWindowIcon(QtGui.QIcon("icon-information"))
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Informação")
            info_box.setText("Preencha todos os campos!")
            info_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f4f4f4;
                    border: 2px solid #3498db;
                }
                QMessageBox QLabel {
                    color: #3498db;
                    font-size: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #3498db;
                    width: 70px;
                    color: white;
                    padding: 5px 20px;
                    border-radius: 5px;
                    margin: 0 auto
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980b9;
                }
                            /* Personalizar a barra de título */
                QHeaderView {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
                /* Personalizar os botões da barra de título */
                QHeaderView::section {
                    background-color: transparent;
                }
                QHeaderView::close-button, QHeaderView::minimize-button, QHeaderView::maximize-button {
                    background-color: transparent;
                    border: none;
                    margin: 2px;
                }
                QHeaderView::close-button:hover, QHeaderView::minimize-button:hover, QHeaderView::maximize-button:hover {
                    background-color: #e74c3c;
                }
            """)
            info_box.exec_()
            return

        if not "@" in self.cliente_widget.txtEmail.text():
            info_box = QMessageBox(self)
            info_box.setWindowIcon(QtGui.QIcon("icon-information"))
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Informação")
            info_box.setText("Endereço de email inválido.")
            info_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f4f4f4;
                    border: 2px solid #3498db;
                }
                QMessageBox QLabel {
                    color: #3498db;
                    font-size: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #3498db;
                    width: 70px;
                    color: white;
                    padding: 5px 20px;
                    border-radius: 5px;
                    margin: 0 auto
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980b9;
                }
                            /* Personalizar a barra de título */
                QHeaderView {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
                /* Personalizar os botões da barra de título */
                QHeaderView::section {
                    background-color: transparent;
                }
                QHeaderView::close-button, QHeaderView::minimize-button, QHeaderView::maximize-button {
                    background-color: transparent;
                    border: none;
                    margin: 2px;
                }
                QHeaderView::close-button:hover, QHeaderView::minimize-button:hover, QHeaderView::maximize-button:hover {
                    background-color: #e74c3c;
                }
            """)
            info_box.exec_()
            return

        if validaCpf:
            info_box = QMessageBox(self)
            info_box.setWindowIcon(QtGui.QIcon("icon-information"))
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Informação")
            info_box.setText("CPF já existe")
            info_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f4f4f4;
                    border: 2px solid #3498db;
                }
                QMessageBox QLabel {
                    color: #3498db;
                    font-size: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #3498db;
                    width: 70px;
                    color: white;
                    padding: 5px 20px;
                    border-radius: 5px;
                    margin: 0 auto
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980b9;
                }
                            /* Personalizar a barra de título */
                QHeaderView {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
                /* Personalizar os botões da barra de título */
                QHeaderView::section {
                    background-color: transparent;
                }
                QHeaderView::close-button, QHeaderView::minimize-button, QHeaderView::maximize-button {
                    background-color: transparent;
                    border: none;
                    margin: 2px;
                }
                QHeaderView::close-button:hover, QHeaderView::minimize-button:hover, QHeaderView::maximize-button:hover {
                    background-color: #e74c3c;
                }
            """)
            info_box.exec_()
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
            print(worker)
            worker.start()
            worker.validationFinished.connect(self.handleValidationResult)
        except Exception as e:
            print(e)

    def handleValidationResult(self, validados):
        if validados:
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            info_box = QMessageBox(self)
            info_box.setWindowIcon(QtGui.QIcon("icon-information"))
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Informação")
            info_box.setText("Cadastro efetuado com sucesso")
            info_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f4f4f4;
                    border: 2px solid #3498db;
                }
                QMessageBox QLabel {
                    color: #3498db;
                    font-size: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #3498db;
                    width: 70px;
                    color: white;
                    padding: 5px 20px;
                    border-radius: 5px;
                    margin: 0 auto
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980b9;
                }
                            /* Personalizar a barra de título */
                QHeaderView {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
                /* Personalizar os botões da barra de título */
                QHeaderView::section {
                    background-color: transparent;
                }
                QHeaderView::close-button, QHeaderView::minimize-button, QHeaderView::maximize-button {
                    background-color: transparent;
                    border: none;
                    margin: 2px;
                }
                QHeaderView::close-button:hover, QHeaderView::minimize-button:hover, QHeaderView::maximize-button:hover {
                    background-color: #e74c3c;
                }
            """)
            info_box.exec_()
            self.cliente_widget.txtNome.setText("")
            self.cliente_widget.txtCpf.setText("")
            self.cliente_widget.txtEmail.setText("")
            self.cliente_widget.txtDataNasc.setText("")
            self.cliente_widget.txtNome.setFocus()
        else:
            self.buttonSalvar.setEnabled(True)
            self.buttonFechar.setEnabled(True)
            info_box = QMessageBox(self)
            info_box.setWindowIcon(QtGui.QIcon("icon-critical"))
            info_box.setIcon(QMessageBox.Information)
            info_box.setWindowTitle("Erro")
            info_box.setText("Erro: Verifique os campos e tente novamente.")
            info_box.setStyleSheet("""
                QMessageBox {
                    background-color: #f4f4f4;
                    border: 2px solid #3498db;
                }
                QMessageBox QLabel {
                    color: #3498db;
                    font-size: 20px;
                }
                QMessageBox QPushButton {
                    background-color: #3498db;
                    width: 70px;
                    color: white;
                    padding: 5px 20px;
                    border-radius: 5px;
                    margin: 0 auto
                }
                QMessageBox QPushButton:hover {
                    background-color: #2980b9;
                }
                            /* Personalizar a barra de título */
                QHeaderView {
                    background-color: #3498db;
                    color: white;
                    padding: 5px;
                }
                /* Personalizar os botões da barra de título */
                QHeaderView::section {
                    background-color: transparent;
                }
                QHeaderView::close-button, QHeaderView::minimize-button, QHeaderView::maximize-button {
                    background-color: transparent;
                    border: none;
                    margin: 2px;
                }
                QHeaderView::close-button:hover, QHeaderView::minimize-button:hover, QHeaderView::maximize-button:hover {
                    background-color: #e74c3c;
                }
            """)
            info_box.exec_()

    def closeWindow(self):
        self.close()

    def showCliente(self):
        self.stack.setCurrentWidget(self.cliente_widget)

    def showFuncionario(self):
        self.stack.setCurrentWidget(self.funcionario_widget)


class WorkerThread(QThread):
    validationFinished = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        retorno = self.parent().cliente_widget.insertData()
        self.validationFinished.emit(retorno)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cad = Cadastro()
    cad.show()
    sys.exit(app.exec_())
