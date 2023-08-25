import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QMessageBox, QComboBox, QHBoxLayout
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRegExp, QThread, QEvent, pyqtSignal, QDateTime
from PyQt5.QtGui import QPixmap, QFontDatabase, QRegExpValidator, QIcon
from connDB import ConnectDB
from datetime import datetime


def dataAtual():
    dateTime = QDateTime.currentDateTime()
    dateDisplay = dateTime.toString("dd/MM/yyyy")
    print(dateDisplay)


class AgendarWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 20, 20)
        self.layout.setSpacing(10)  # Adicionando espaçamento entre os widgets

        self.nome_label = QLabel("Nome:")
        self.nome_input = QLineEdit()

        # ----------------------------------------------------------------

        self.cpf_label = QLabel("CPF:")
        self.cpf_input = QLineEdit()

        # ----------------------------------------------------------------

        self.servico_layout = QHBoxLayout()
        self.servico_label = QLabel("Serviço:")
        self.servico_input = QLineEdit()
        self.servico_input.setReadOnly(True)
        self.servico_btn = QPushButton("Selecionar")
        self.servico_layout.addWidget(self.servico_label)
        self.servico_layout.addWidget(self.servico_input)
        self.servico_layout.addWidget(self.servico_btn)

        self.valor_label = QLabel("Valor:")
        self.valor_input = QLineEdit()
        self.valor_input.setReadOnly(True)

        self.tempo_label = QLabel("Tempo:")
        self.tempo_input = QLineEdit()
        self.tempo_input.setReadOnly(True)

        # ----------------------------------------------------------------

        dateTime = QDateTime.currentDateTime()
        self.data_label = QLabel("Data:")

        self.dia_input = QLineEdit()
        self.dia_input.setText(f"{dateTime.toString('dd')}")
        self.dia_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.dia_input.setMaxLength(2)

        self.dia_increase_btn = QPushButton(self)
        self.dia_increase_btn.setText("+")
        self.dia_increase_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.dia_increase_btn.setGeometry(1, 453, 153, 23)
        self.dia_increase_btn.clicked.connect(lambda: self.increase(self.dia_input))

        self.dia_decrease_btn = QPushButton(self)
        self.dia_decrease_btn.setText("-")
        self.dia_decrease_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.dia_decrease_btn.setGeometry(1, 505, 153, 23)
        self.dia_decrease_btn.clicked.connect(lambda: self.decrease(self.dia_input))

        # ----------------------------------------------------------------

        self.mes_input = QLineEdit()
        self.mes_input.setText(f"{dateTime.toString('MM')}")
        self.mes_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.mes_input.setMaxLength(2)

        self.mes_increase_btn = QPushButton(self)
        self.mes_increase_btn.setText("+")
        self.mes_increase_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.mes_increase_btn.setGeometry(165, 453, 154, 23)
        self.mes_increase_btn.clicked.connect(lambda: self.increase(self.mes_input))

        self.mes_decrease_btn = QPushButton(self)
        self.mes_decrease_btn.setText("-")
        self.mes_decrease_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.mes_decrease_btn.setGeometry(165, 505, 154, 23)
        self.mes_decrease_btn.clicked.connect(lambda: self.decrease(self.mes_input))

        # ----------------------------------------------------------------

        self.ano_input = QLineEdit()
        self.ano_input.setText(f"{dateTime.toString('yyyy')}")
        self.ano_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.ano_input.setMaxLength(4)

        self.ano_increase_btn = QPushButton(self)
        self.ano_increase_btn.setText("+")
        self.ano_increase_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.ano_increase_btn.setGeometry(329, 453, 154, 23)
        self.ano_increase_btn.clicked.connect(lambda: self.increase(self.ano_input))

        self.ano_decrease_btn = QPushButton(self)
        self.ano_decrease_btn.setText("-")
        self.ano_decrease_btn.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.ano_decrease_btn.setGeometry(329, 505, 154, 23)
        self.ano_decrease_btn.clicked.connect(lambda: self.decrease(self.ano_input))

        # ----------------------------------------------------------------

        self.hora_label = QLabel("Horário:")
        self.hora_input = QLineEdit()
        self.hora_input.setMaxLength(2)
        self.minuto_input = QLineEdit()
        self.minuto_input.setMaxLength(2)

        self.agendar_btn = QPushButton("Agendar")
        self.cancelar_btn = QPushButton("Cancelar")

        self.agendar_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        self.cancelar_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        self.servico_btn.clicked.connect(self.select_servico)

        data_layout = QHBoxLayout()
        data_layout.addWidget(self.dia_input)
        data_layout.addWidget(self.mes_input)
        data_layout.addWidget(self.ano_input)

        hora_layout = QHBoxLayout()
        hora_layout.addWidget(self.hora_input)
        hora_layout.addWidget(self.minuto_input)

        self.layout.addWidget(self.nome_label)
        self.layout.addWidget(self.nome_input)
        self.layout.addWidget(self.cpf_label)
        self.layout.addWidget(self.cpf_input)
        self.layout.addLayout(self.servico_layout)
        self.layout.addWidget(self.valor_label)
        self.layout.addWidget(self.valor_input)
        self.layout.addWidget(self.tempo_label)
        self.layout.addWidget(self.tempo_input)
        self.layout.addWidget(self.data_label)
        self.layout.addLayout(data_layout)
        self.layout.addWidget(self.hora_label)
        self.layout.addLayout(hora_layout)

        self.layout.addWidget(self.agendar_btn)
        self.layout.addWidget(self.cancelar_btn)

        self.setLayout(self.layout)

    def select_servico(self):
        print('Teste')

    def increase(self, input_field):
        valueText = input_field.text()
        increase = int(valueText) + 1
        input_field.setText(str(increase))

    def decrease(self, input_field):
        valueText = input_field.text()
        decrease = int(valueText) - 1
        input_field.setText(str(decrease))


class AgendamentosWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Tela de Cadastro de Funcionário")
        layout.addWidget(self.label)
        self.setLayout(layout)


class Agendamento(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastros")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("""
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }

        QLabel {
            color: #333;
        }

        QLineEdit, QComboBox {
            background-color: #f5f5f5;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
        }"""
        )
        self.resize(750, 712)
        self.center_dialog()

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 220, 712)
        self.container.setStyleSheet("background-color: #2c3e50")

        self.button_agendar = QPushButton("Agendar", self.container)
        self.button_agendamentos = QPushButton("Agendamentos", self.container)

        self.button_agendar.clicked.connect(self.showAgendar)
        self.button_agendamentos.clicked.connect(self.showAgendamentos)

        self.button_agendar.setStyleSheet(
            "QPushButton { background-color: #282828; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 5px; width: 100px}"
            "QPushButton:hover { background-color: #474747; }"
        )

        self.button_agendamentos.setStyleSheet(
            "QPushButton { background-color: #282828; color: white; font-size: 16px; padding: 10px; border: none; border-radius: 5px }"
            "QPushButton:hover { background-color: #474747; }"
        )

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10, 30, 10, 500)  # Ajuste as margens inferior para mover o menu para cima
        menu_layout.addWidget(self.button_agendar)
        menu_layout.addWidget(self.button_agendamentos)
        self.container.setLayout(menu_layout)

        self.stack = QStackedWidget(self)
        self.stack.setGeometry(250, 0, 503, 712)

        self.agendar_widget = AgendarWidget()
        self.agendamentos_widget = AgendamentosWidget()

        self.stack.addWidget(self.agendar_widget)
        self.stack.addWidget(self.agendamentos_widget)

        '''self.buttonSalvar = QPushButton("Salvar", self)
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
            """)'''
        dataAtual()

    def center_dialog(self):
        # Obtém o tamanho da tela
        screen_geo = QApplication.desktop().availableGeometry()

        # Obtém o retângulo da geometria do diálogo
        dialog_geo = self.frameGeometry()

        # Calcula a posição para centralizar o diálogo
        center_point = screen_geo.center()
        dialog_geo.moveCenter(center_point)

        self.move(dialog_geo.topLeft())  # Move o diálogo para a posição calculada

    def showAgendar(self):
        self.stack.setCurrentWidget(self.agendar_widget)

    def showAgendamentos(self):
        self.stack.setCurrentWidget(self.agendamentos_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Agendamento()
    dialog.show()
    sys.exit(app.exec_())


