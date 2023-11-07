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

stylesheet = '''
    QTreeWidget::Item{
        color: black;
        border-bottom: 1px solid #d2d2d2;
        border-top: 1px solid #d2d2d2;
        border-right: 1px solid #d2d2d2;
    }
    QTreeWidget::Item:selected {
        background-color: #94c9e4;
    }
'''


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
        self.closeButton.clicked.connect(self.closeWindow)

        # ------------------------------------------------------

        self.detalhar = QCheckBox(self)
        self.detalhar.setText("Detalhar")
        self.detalhar.setStyleSheet("font-size: 12px; font-family: Arial")
        self.detalhar.setGeometry(280, 28, 70, 23)

        # ------------------------------------------------------

        self.lblData = QLabel(self)
        self.lblData.setText("Data(inicial/final)")
        self.lblData.setStyleSheet("font-size: 13px; font-family: Arial")
        self.lblData.setGeometry(23, 25, 150, 25)

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
        self.dataInicio.setDisplayFormat("dd/MM/yyyy")
        self.dataInicio.setGeometry(20, 50, 90, 25)
        self.setFirstDayOfTheMonth()

        self.dataFim = QDateEdit(self)
        self.dataFim.setCalendarPopup(True)
        self.dataFim.setStyleSheet("""
                QDateEdit {
                    border: 2px solid #0078d4; /* Cor da borda */
                    border-radius: 3px; /* Borda arredondada */
                    padding: 3px;
                }
            """)
        self.dataFim.setDisplayFormat("dd/MM/yyyy")
        self.dataFim.setGeometry(140, 50, 90, 25)
        self.setToday()

        # ------------------------------------------------------

        self.filtroBarbeiro = QComboBox(self)
        self.filtroBarbeiro.addItem("")
        self.filtroBarbeiro.setEditable(True)
        try:
            conn = ConnectDB()
            conn.conecta()
            sql = "select id_barbeiro, nome from barbeiro"
            conn.execute(sql)
            barbeiros = conn.fetchall()
            for barbeiro in barbeiros:
                self.filtroBarbeiro.addItem(f"{barbeiro['id_barbeiro']} - {barbeiro['nome']}")
        except Exception as e:
            print(e)
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
        self.buscarBtn.clicked.connect(self.searchFaturamento)

        # ------------------------------------------------------

        self.treeWidgetFaturamento = QTreeWidget(self)
        self.treeWidgetFaturamento.setGeometry(5, 110, 740, 567)
        self.treeWidgetFaturamento.setColumnCount(5)
        self.treeWidgetFaturamento.setColumnWidth(0, 150)
        self.treeWidgetFaturamento.setColumnWidth(1, 170)
        self.treeWidgetFaturamento.setColumnWidth(2, 120)
        self.treeWidgetFaturamento.setColumnWidth(3, 215)
        self.treeWidgetFaturamento.setColumnWidth(4, 60)
        self.treeWidgetFaturamento.setHeaderLabels(["Data", "Cliente", "Cliente_doc", "Servico", "Valor"])
        self.treeWidgetFaturamento.header().setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.treeWidgetFaturamento.header().setStyleSheet("""
                                font: bold 11px; 
                                text-align: center; 
                                font-family: Arial; 
                                border: 1px solid #d3d3d3;
                                background-color: #f1f1f1;
        """)
        self.treeWidgetFaturamento.setStyleSheet(stylesheet)

        # ------------------------------------------------------

        self.lblFaturamentoTotal = QLabel(self)
        self.lblFaturamentoTotal.setText("Total R$")
        self.lblFaturamentoTotal.setStyleSheet("font-size: 14px; border: 1px solid grey; font-family: Arial")
        self.lblFaturamentoTotal.setGeometry(0, 683, 100, 24)

        self.lblValorFaturamentoTotal = QLabel(self)
        self.lblValorFaturamentoTotal.setText("0.00")
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

    def searchFaturamento(self):
        self.treeWidgetFaturamento.clear()
        try:
            dataIncial = datetime.strptime(self.dataInicio.text(), "%d/%m/%Y").strftime("%Y%m%d")
            dataFinal = datetime.strptime(self.dataFim.text(), "%d/%m/%Y").strftime("%Y%m%d")
            busca = self.filtroBarbeiro.currentText().split("-") if self.filtroBarbeiro.currentText() else None
            conn = ConnectDB()
            conn.conecta()
            if self.detalhar.isChecked():
                if busca is None:
                    sql = f"""
                            select agendamentos.data_hora as dia, 
                            agendamentos.nome_cliente as cliente,
                            agendamentos.cpf_cliente as cpf,
                            servicos.nome_servico as servico,
                            servicos.valor_servico as venda
                            from agendamentos
                            join servicos on agendamentos.id_servico = servicos.id
                            join barbeiro on agendamentos.id_barbeiro = barbeiro.id_barbeiro
                            where agendamentos.status=1 and 
                            agendamentos.data_hora between {dataIncial} and {dataFinal}235959
                            order by agendamentos.data_hora
                            """
                else:
                    id_barb = int(busca[0])
                    sql = f"""
                            select agendamentos.data_hora as dia, 
                            agendamentos.nome_cliente as cliente,
                            agendamentos.cpf_cliente as cpf,
                            servicos.nome_servico as servico,
                            servicos.valor_servico as venda
                            from agendamentos
                            join servicos on agendamentos.id_servico = servicos.id
                            join barbeiro on agendamentos.id_barbeiro = barbeiro.id_barbeiro
                            where agendamentos.status=1 and 
                            agendamentos.data_hora between {dataIncial} and {dataFinal}235959 and
                            agendamentos.id_barbeiro={id_barb}
                            order by agendamentos.data_hora
                            """
                conn.execute(sql)
                rows = conn.fetchall()
                valorTotal = 0
                if rows:
                    for row in rows:
                        dia = datetime.strptime(str(row['dia']), "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M:%S")
                        cliente = row['cliente']
                        cpf = row['cpf']
                        servico = row['servico']
                        valor = f"{row['venda']:.2f}"
                        item = QTreeWidgetItem(self.treeWidgetFaturamento)
                        item.setText(0, str(dia))
                        item.setText(1, str(cliente))
                        item.setText(2, str(cpf))
                        item.setText(3, str(servico))
                        item.setText(4, str(valor))

                        item.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)
                        valorTotal += float(valor)
                    self.lblValorFaturamentoTotal.setText(f"{valorTotal:.2f}")
                else:
                    messageDefault("Nenhum registro encontrado")
                return True
            else:
                if busca is None:
                    sql = f"""
                            select date_format(agendamentos.data_hora, '%Y/%m/%d') as dia, sum(servicos.valor_servico) as total_acum
                            from agendamentos
                            join servicos on agendamentos.id_servico = servicos.id
                            where agendamentos.status=1 and agendamentos.data_hora between {dataIncial} and {dataFinal}235959
                            group by date_format(agendamentos.data_hora, '%Y/%m/%d') 
                            order by date_format(agendamentos.data_hora, '%Y/%m/%d');
                            """
                else:
                    id_barb = int(busca[0])
                    sql = f"""
                            select date_format(agendamentos.data_hora, '%Y/%m/%d') as dia, sum(servicos.valor_servico) as total_acum
                            from agendamentos
                            join servicos on agendamentos.id_servico = servicos.id
                            join barbeiro on agendamentos.id_barbeiro = barbeiro.id_barbeiro
                            where agendamentos.status=1 and agendamentos.data_hora between {dataIncial} and {dataFinal}235959
                            and agendamentos.id_barbeiro={id_barb}
                            group by date_format(agendamentos.data_hora, '%Y/%m/%d') 
                            order by date_format(agendamentos.data_hora, '%Y/%m/%d');
                            """
                conn.execute(sql)
                rows = conn.fetchall()
                valorTotal = 0
                if rows:
                    for row in rows:
                        dia = datetime.strptime(row['dia'], "%Y/%m/%d").strftime("%d/%m/%Y")
                        valor = f"{row['total_acum']:.2f}"
                        item = QTreeWidgetItem(self.treeWidgetFaturamento)
                        item.setText(0, str(dia))
                        item.setText(1, "*")
                        item.setText(2, "*")
                        item.setText(3, "*")
                        item.setText(4, str(valor))

                        item.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
                        item.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)
                        valorTotal += float(valor)
                    self.lblValorFaturamentoTotal.setText(f"{valorTotal:.2f}")
                else:
                    messageDefault("Nenhum registro encontrado")
                return True
        except Exception as e:
            print(e)

    def closeWindow(self):
        self.close()

    def setToday(self):
        today = QDate().currentDate().toString("dd/MM/yyyy")
        formatToday = QDate().fromString(today, "dd/MM/yyyy")
        self.dataFim.setDate(formatToday)

    def setFirstDayOfTheMonth(self):
        mes_ano = QDate().currentDate().toString("MM/yyyy")
        listMes = mes_ano.split("/")
        listMes.insert(0, "01")
        diaUmDoMes = "/".join(listMes)
        formatDay = QDate().fromString(diaUmDoMes, "dd/MM/yyyy")
        self.dataInicio.setDate(formatDay)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Relatorio()
    window.show()
    app.exec_()
