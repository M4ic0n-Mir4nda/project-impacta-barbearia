import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QPixmap, QFontDatabase, QRegExpValidator


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
        self.labelNome.setStyleSheet("font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelNome.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtNome = QLineEdit(self)
        self.txtNome.setGeometry(30, 120, 450, 30)
        self.txtNome.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelCpf = QLabel(self)
        self.labelCpf.setGeometry(30, 200, 110, 45)
        self.labelCpf.setText("Cpf")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelCpf.setStyleSheet("font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelCpf.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtCpf = QLineEdit(self)
        '''rx = QtCore.QRegExp("[0-9]{10}")  # +++
        val = QRegExpValidator(rx)  # +++
        self.txtCpf.setValidator(val)'''
        self.txtCpf.setGeometry(30, 245, 450, 30)
        self.txtCpf.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelEmail = QLabel(self)
        self.labelEmail.setGeometry(30, 320, 110, 45)
        self.labelEmail.setText("Email")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelEmail.setStyleSheet("font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtEmail = QLineEdit(self)
        self.txtEmail.setGeometry(30, 360, 450, 30)
        self.txtEmail.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")

        # ---------------------------------------------------

        self.labelDataNasc = QLabel(self)
        self.labelDataNasc.setGeometry(30, 440, 230, 45)
        self.labelDataNasc.setText("Data de Nascimento")
        QFontDatabase.addApplicationFont("Pacifico-Regular.ttf")
        self.labelDataNasc.setStyleSheet("font-size: 24px; background-color: #282828; color: #fff; font-family: 'Pacifico', cursive;")
        self.labelDataNasc.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.txtDataNasc = QLineEdit(self)
        self.txtDataNasc.setGeometry(30, 480, 450, 30)
        self.txtDataNasc.setStyleSheet("border: 3px solid #282828; border-radius: 5px; font-size: 15px")


class FuncionarioWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Tela de Cadastro de Funcionário")
        layout.addWidget(self.label)
        self.setLayout(layout)


class Cadastro(QDialog):
    def __init__(self, parent):
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
        self.buttonSalvar.setGeometry(390, 580, 200, 60)
        self.buttonSalvar.setStyleSheet("""
                                QPushButton { background-color: #3498db; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 10px}
                                QPushButton:hover { background-color: #2980b9; }
            """)

        self.buttonSalvar.clicked.connect(self.saveData)

    def saveData(self):
        print('Teste')
        self.close()

    def showCliente(self):
        self.stack.setCurrentWidget(self.cliente_widget)

    def showFuncionario(self):
        self.stack.setCurrentWidget(self.funcionario_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Cadastro()
    ex.show()
    sys.exit(app.exec_())
