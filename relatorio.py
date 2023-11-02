import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QHBoxLayout, QTreeWidget, QTreeWidgetItem, QScrollArea, QFrame, QComboBox, QDateEdit, \
    QDateTimeEdit, QCheckBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, QEvent, QDateTime, QTimer, QDate
from PyQt5.QtGui import QPixmap
from datetime import datetime, timedelta
from connDB import ConnectDB
from message import messageDefault


class Relatorio(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Relatório de Faturamento")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog {background-color: #ececec}")
        self.resize(750, 712)
        self.center_dialog()

        self.closeButton = QPushButton(self)
        self.closeButton.setText("X")
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                font-size: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.closeButton.setGeometry(710, 0, 40, 25)

        # ------------------------------------------------------

        self.detalhar = QCheckBox(self)
        self.detalhar.setText("Detalhar")
        self.detalhar.setStyleSheet("font-size: 12px; font-family: Arial")
        self.detalhar.setGeometry(100, 28, 70, 23)

        # ------------------------------------------------------

        self.lblData = QLabel(self)
        self.lblData.setText("Data")
        self.lblData.setStyleSheet("font-size: 13px; font-family: Arial")
        self.lblData.setGeometry(23, 25, 70, 25)

        # ------------------------------------------------------

        self.dataInicio = QDateEdit(self)
        self.dataInicio.setCalendarPopup(True)
        self.dataInicio.setStyleSheet("""
                QDateEdit {
                    border: 2px solid #0078d4; /* Cor da borda */
                    border-radius: 3px; /* Borda arredondada */
                    padding: 3px;
                }
            """)
        self.dataInicio.setGeometry(20, 50, 90, 25)

        self.dataFim = QDateEdit(self)
        self.dataFim.setCalendarPopup(True)
        self.dataFim.setStyleSheet("""
                QDateEdit {
                    border: 2px solid #0078d4; /* Cor da borda */
                    border-radius: 3px; /* Borda arredondada */
                    padding: 3px;
                }
            """)
        self.dataFim.setGeometry(140, 50, 90, 25)

        # ------------------------------------------------------

        self.filtroBarbeiro = QComboBox(self)
        self.filtroBarbeiro.addItem("")
        self.filtroBarbeiro.setEditable(True)
        self.filtroBarbeiro.addItem("Maicon Miranda Santana")
        self.filtroBarbeiro.setStyleSheet("font-size: 12px; font-family: Arial")
        self.filtroBarbeiro.setGeometry(280, 50, 230, 25)

        self.line = self.filtroBarbeiro.lineEdit()
        self.line.setAlignment(Qt.AlignCenter)
        self.line.setReadOnly(True)

        # ------------------------------------------------------

        self.buscarBtn = QPushButton(self)
        self.buscarBtn.setGeometry(550, 45, 130, 35)
        self.buscarBtn.setText("Buscar")
        self.buscarBtn.setStyleSheet("""
                            QPushButton {
                                border-radius: 3px; 
                                background-color: #3498db; 
                                color: #fff; 
                                padding: 6px;
                                font-size: 12px;
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
            """)

        # ------------------------------------------------------

        self.treeWidgetFaturamento = QTreeWidget(self)
        self.treeWidgetFaturamento.setGeometry(5, 110, 740, 567)
        self.treeWidgetFaturamento.setColumnCount(6)
        self.treeWidgetFaturamento.setColumnWidth(0, 105)
        self.treeWidgetFaturamento.setColumnWidth(1, 105)
        self.treeWidgetFaturamento.setColumnWidth(2, 160)
        self.treeWidgetFaturamento.setColumnWidth(3, 120)
        self.treeWidgetFaturamento.setColumnWidth(4, 140)
        self.treeWidgetFaturamento.setColumnWidth(5, 100)
        self.treeWidgetFaturamento.setHeaderLabels(["Data", "Hora", "Cliente", "Cliente_doc", "Servico", "Valor"])
        self.treeWidgetFaturamento.header().setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        # ------------------------------------------------------

        self.lblFaturamentoTotal = QLabel(self)
        self.lblFaturamentoTotal.setText("Total R$")
        self.lblFaturamentoTotal.setStyleSheet("font-size: 14px; border: 1px solid grey; font-family: Arial")
        self.lblFaturamentoTotal.setGeometry(0, 683, 100, 24)

        self.lblValorFaturamentoTotal = QLabel(self)
        self.lblValorFaturamentoTotal.setText("20.569.59")
        self.lblValorFaturamentoTotal.setStyleSheet("font-size: 14px; border: 1px solid grey; font-family: Arial")
        self.lblValorFaturamentoTotal.setGeometry(100, 683, 100, 24)
        self.lblValorFaturamentoTotal.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)

        # ------------------------------------------------------

        self.rodape = QLabel(self)
        self.rodape.lower()
        self.rodape.setStyleSheet("border: 1px solid grey; background-color: #f6f6f6")
        self.rodape.setGeometry(0, 683, 750, 25)

        # ------------------------------------------------------

    def center_dialog(self):
        # Obtém o tamanho da tela
        screenGeo = QApplication.desktop().availableGeometry()

        # Obtém o retângulo da geometria do diálogo
        dialogGeo = self.frameGeometry()

        # Calcula a posição para centralizar o diálogo
        centerPoint = screenGeo.center()
        dialogGeo.moveCenter(centerPoint)

        self.move(dialogGeo.topLeft())  # Move o diálogo para a posição calculada


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Relatorio()
    window.show()
    app.exec_()