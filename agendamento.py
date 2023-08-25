import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QMessageBox, QComboBox, QHBoxLayout
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRegExp, QThread, QEvent, pyqtSignal, QDateTime, QTimer
from PyQt5.QtGui import QPixmap, QFontDatabase, QRegExpValidator, QIcon
from connDB import ConnectDB
from datetime import datetime

def dataAtual():
    dateTime = QDateTime.currentDateTime()
    dateDisplay = dateTime.toString("hh:ss")
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
        self.cpf_input.setInputMask("999.999.999-99")
        self.cpf_input.installEventFilter(self)

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

        self.dateTime = QDateTime.currentDateTime()
        self.data_label = QLabel("Data:")

        self.dia_input = QLineEdit()
        self.dia_input.setText(f"{self.dateTime.toString('dd')}")
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

        self.dia_input.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.mes_input = QLineEdit()
        self.mes_input.setText(f"{self.dateTime.toString('MM')}")
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

        self.mes_input.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.ano_input = QLineEdit()
        self.ano_input.setText(f"{self.dateTime.toString('yyyy')}")
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

        self.ano_input.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.hora_label = QLabel("Horário:")
        self.hora_input = QLineEdit()
        self.hora_input.setMaxLength(2)
        self.hora_input.setText(str(self.dateTime.toString("hh")))
        self.hora_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)

        self.hora_input.textChanged.connect(self.textChangedFields)

        self.separator = QLabel(":")
        self.separator.setStyleSheet("font-size: 20px")

        self.minuto_input = QLineEdit()
        self.minuto_input.setMaxLength(2)
        self.minuto_input.setText(str(self.dateTime.toString("mm")))
        self.minuto_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)

        self.default_button = QPushButton()
        self.default_button.setText("Redefinir hora")
        self.default_button.resize(80, 23)
        self.default_button.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff; padding: 7px")

        self.default_button.clicked.connect(self.clickedDefaultHourCurrent)

        self.minuto_input.textChanged.connect(self.textChangedFields)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.iniTimer)
        self.timer.setInterval(10000)
        self.timer.start()

        # ----------------------------------------------------------------

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
        hora_layout.addWidget(self.separator)
        hora_layout.addWidget(self.minuto_input)
        hora_layout.addWidget(self.default_button)

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
        if increase < 10:
            listValue = list(str(increase))
            listValue.insert(0, "0")
            incrementZero = "".join(listValue)
            input_field.setText(incrementZero)
        else:
            input_field.setText(str(increase))

        if self.dia_input.text() == "32":
            self.dia_input.setText("01")

        if self.mes_input.text() == "13":
            self.mes_input.setText("01")

    def decrease(self, input_field):
        valueText = input_field.text()
        decrease = int(valueText) - 1
        if decrease < 10:
            listValue = list(str(decrease))
            listValue.insert(0, "0")
            incrementZero = "".join(listValue)
            input_field.setText(incrementZero)
        else:
            input_field.setText(str(decrease))

        if self.dia_input.text() == "00":
            self.dia_input.setText("31")

        if self.mes_input.text() == "00":
            self.mes_input.setText("12")

    def textChangedFields(self):
        dateCurrent = int(self.dateTime.toString('yyyy'))
        if not self.dia_input.text().isdigit() or not self.mes_input.text().isdigit() or not self.ano_input.text().isdigit():
            self.dia_input.setText("01")
            self.mes_input.setText("01")
            self.ano_input.setText(str(dateCurrent))
            return

        else:
            dayText = int(self.dia_input.text())
            monthText = int(self.mes_input.text())
            yearText = int(self.ano_input.text())
            if dayText > 31:
                self.dia_input.setText("01")

            elif monthText > 12:
                self.mes_input.setText("01")

            elif yearText < dateCurrent:
                info_box = QMessageBox(self)
                info_box.setWindowIcon(QtGui.QIcon("icon-information"))
                info_box.setIcon(QMessageBox.Information)
                info_box.setWindowTitle("Informação")
                info_box.setText("Ano inválido!")
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
                self.ano_input.setText(str(dateCurrent))

        if not self.hora_input.text().isdigit() or not self.minuto_input.text().isdigit():
            self.timer.timeout.connect(self.iniTimer)
            self.timer.setInterval(0)
            self.timer.start()
            return
        else:
            hourText = int(self.hora_input.text())
            minuteText = int(self.minuto_input.text())

            if hourText > 24:
                try:
                    self.timer.timeout.connect(self.iniTimer)
                    self.timer.setInterval(0)
                    self.timer.start()
                except Exception as e:
                    self.hora_input.setText("24")

            elif minuteText > 59:
                try:
                    self.timer.timeout.connect(self.iniTimer)
                    self.timer.setInterval(0)
                    self.timer.start()
                except Exception as e:
                    self.minuto_input.setText("59")

    def clickedDefaultHourCurrent(self):
        self.timer.timeout.connect(self.iniTimer)
        self.timer.setInterval(0)
        self.timer.start()

    def hourCurrent(self):
        try:
            self.timer.start(10000)
            time = QDateTime.currentDateTime()
            hourCurrent = time.toString("hh")
            minuteCurrent = time.toString("mm")
            self.hora_input.setText(str(hourCurrent))
            self.minuto_input.setText(str(minuteCurrent))
        except Exception as e:
            self.hora_input.setText("24")
            self.minuto_input.setText("59")

    def iniTimer(self):
        self.timer.stop()
        self.worker = WorkerTreadTime(self)
        self.worker.start()
        self.worker.finished.connect(self.hourCurrent)

    def eventFilter(self, obj, e):
        if obj == self.cpf_input:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
                    print(self.cpf_input.text())
                    return True
        return False


class AgendamentosWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel("Tela de Cadastro de Funcionário")
        layout.addWidget(self.label)
        self.setLayout(layout)


class WorkerTreadTime(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        try:
            pass
        except Exception as e:
            self.parent().hora_input.setText("24")
            self.parent().minuto_input.setText("59")


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

    def center_dialog(self):
        # Obtém o tamanho da tela
        screen_geo = QApplication.desktop().availableGeometry()

        # Obtém o retângulo da geometria do diálog
        dialog_geo = self.frameGeometry()

        # Calcula a posição para centralizar o diálog
        center_point = screen_geo.center()
        dialog_geo.moveCenter(center_point)

        self.move(dialog_geo.topLeft())  # Move o diálog para a posição calculada

    def showAgendar(self):
        self.stack.setCurrentWidget(self.agendar_widget)

    def showAgendamentos(self):
        self.stack.setCurrentWidget(self.agendamentos_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Agendamento()
    dialog.show()
    sys.exit(app.exec_())


