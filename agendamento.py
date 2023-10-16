import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLineEdit, \
    QHBoxLayout, QTreeWidget, QTreeWidgetItem, QScrollArea, QFrame, QComboBox, QDateEdit, \
    QDateTimeEdit
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, QEvent, QDateTime, QTimer, QDate
from PyQt5.QtGui import QPixmap
from datetime import datetime, timedelta
from connDB import ConnectDB
from message import messageDefault

stylesheetTreeWidgts = '''
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


class AgendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.tempo = 0
        self.horas = 0
        self.ultAgendamento = None
        self.nome = None
        self.cpf = None
        self.idServico = 0

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 20, 20)
        self.layout.setSpacing(10)  # Adicionando espaçamento entre os widgets

        self.nomeLabel = QLabel("Nome:")
        self.nomeLabel.setStyleSheet("color: #fff")
        self.nomeInput = QLineEdit()
        self.nomeInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")
        self.nomeInput.installEventFilter(self)
        # self.nomeInput.textChanged.connect(self.textChangedUpperCase)

        # ----------------------------------------------------------------

        self.cpfLabel = QLabel("CPF:")
        self.cpfLabel.setStyleSheet("color: #fff")
        self.cpfInput = QLineEdit()
        self.cpfInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")
        self.cpfInput.setInputMask("999.999.999-99")
        self.cpfInput.installEventFilter(self)

        # ----------------------------------------------------------------

        self.servicoLayout = QHBoxLayout()
        self.servicoLabel = QLabel("Serviço:")
        self.servicoLabel.setStyleSheet("color: #fff")
        self.servicoInput = QLineEdit()
        self.servicoInput.setReadOnly(True)
        self.servicoInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")
        self.servicoButton = QPushButton("Selecionar")
        self.servicoButton.resize(80, 23)
        self.servicoButton.setStyleSheet("""
                        QPushButton {
                            border-radius: 3px; 
                            background-color: #3498db; 
                            color: #fff; 
                            padding: 6px
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
        """)
        self.servicoLayout.addWidget(self.servicoLabel)
        self.servicoLayout.addWidget(self.servicoInput)
        self.servicoLayout.addWidget(self.servicoButton)

        self.valorLabel = QLabel("Valor:")
        self.valorLabel.setStyleSheet("color: #fff")
        self.valorInput = QLineEdit()
        self.valorInput.setReadOnly(True)
        self.valorInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")

        self.tempoLayout = QHBoxLayout()

        self.tempoLabel = QLabel("Tempo:")
        self.tempoLabel.setStyleSheet("color: #fff")
        self.tempoInput = QLineEdit()
        self.tempoInput.setReadOnly(True)
        self.tempoInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")

        self.barbeiroLabel = QLabel("Barbeiro")
        self.barbeiroLabel.setStyleSheet("color: #fff")
        self.barbeiroInput = QComboBox()
        self.barbeiroInput.setStyleSheet("color: #fff; background-color: #262D37; border: 2px solid #fff")

        try:
            conn = ConnectDB()
            conn.conecta()
            sqlBarbeiros = "select id_barbeiro, nome from barbeiro"
            conn.execute(sqlBarbeiros)
            barbeiros = conn.fetchall()
            self.barbeiroInput.addItem("")
            for barbeiro in barbeiros:
                self.barbeiroInput.addItem(f"{barbeiro['id_barbeiro']} - {barbeiro['nome']}")
        except Exception as e:
            print(e)
            pass

        self.tempoLayout.addWidget(self.valorLabel)
        self.tempoLayout.addWidget(self.valorInput)
        self.tempoLayout.addWidget(self.tempoLabel)
        self.tempoLayout.addWidget(self.tempoInput)
        # self.tempoLayout.addWidget(self.barbeiroLabel)
        # self.tempoLayout.addWidget(self.barbeiroInput)

        # ----------------------------------------------------------------

        self.dateTime = QDateTime.currentDateTime()
        self.dataLabel = QLabel("Data:")
        self.dataLabel.setStyleSheet("color: #fff")

        self.diaInput = QLineEdit()
        self.diaInput.setStyleSheet("border-radius: 0px;")
        self.diaInput.setText(f"{self.dateTime.toString('dd')}")
        self.diaInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.diaInput.setMaxLength(2)

        self.diaIncreaseButton = QPushButton(self)
        self.diaIncreaseButton.setText("+")
        self.diaIncreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.diaIncreaseButton.setGeometry(0, 443, 154, 25)
        self.diaIncreaseButton.clicked.connect(lambda: self.increase(self.diaInput))

        self.diaDecreaseButton = QPushButton(self)
        self.diaDecreaseButton.setText("-")
        self.diaDecreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.diaDecreaseButton.setGeometry(0, 495, 154, 23)
        self.diaDecreaseButton.clicked.connect(lambda: self.decrease(self.diaInput))

        self.diaInput.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.mesInput = QLineEdit()
        self.mesInput.setStyleSheet("border-radius: 0px;")
        self.mesInput.setText(f"{self.dateTime.toString('MM')}")
        self.mesInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.mesInput.setMaxLength(2)

        self.mesIncreaseButton = QPushButton(self)
        self.mesIncreaseButton.setText("+")
        self.mesIncreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.mesIncreaseButton.setGeometry(164, 443, 155, 25)
        self.mesIncreaseButton.clicked.connect(lambda: self.increase(self.mesInput))

        self.mesDecreaseButton = QPushButton(self)
        self.mesDecreaseButton.setText("-")
        self.mesDecreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.mesDecreaseButton.setGeometry(164, 495, 155, 23)
        self.mesDecreaseButton.clicked.connect(lambda: self.decrease(self.mesInput))

        self.mesInput.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.anoInput = QLineEdit()
        self.anoInput.setStyleSheet("border-radius: 0px;")
        self.anoInput.setText(f"{self.dateTime.toString('yyyy')}")
        self.anoInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)
        self.anoInput.setMaxLength(4)

        self.anoIncreaseButton = QPushButton(self)
        self.anoIncreaseButton.setText("+")
        self.anoIncreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.anoIncreaseButton.setGeometry(329, 443, 154, 25)
        self.anoIncreaseButton.clicked.connect(lambda: self.increase(self.anoInput))

        self.anoDecreaseButton = QPushButton(self)
        self.anoDecreaseButton.setText("-")
        self.anoDecreaseButton.setStyleSheet("border-radius: 3px; background-color: #3498db; color: #fff;")
        self.anoDecreaseButton.setGeometry(329, 495, 154, 23)
        self.anoDecreaseButton.clicked.connect(lambda: self.decrease(self.anoInput))

        self.anoInput.textChanged.connect(self.textChangedFields)

        # ----------------------------------------------------------------

        self.horaLabel = QLabel("Horário:")
        self.horaLabel.setStyleSheet("color: #fff")
        self.horaInput = QLineEdit()
        self.horaInput.setMaxLength(2)
        self.horaInput.setText(str(self.dateTime.toString("hh")))
        self.horaInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)

        self.horaInput.textChanged.connect(self.textChangedFields)

        self.separator = QLabel(":")
        self.separator.setStyleSheet("font-size: 20px")
        self.separator.setStyleSheet("color: #fff")

        self.minutoInput = QLineEdit()
        self.minutoInput.setMaxLength(2)
        self.minutoInput.setText(str(self.dateTime.toString("mm")))
        self.minutoInput.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignCenter)

        self.defaultButton = QPushButton()
        self.defaultButton.setText("Redefinir hora")
        self.defaultButton.resize(80, 23)
        self.defaultButton.setStyleSheet("""
                        QPushButton {
                            border-radius: 3px; 
                            background-color: #3498db; 
                            color: #fff; 
                            padding: 6px
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
        """)

        self.minutoInput.textChanged.connect(self.textChangedFields)

        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.iniTimer)
        # self.timer.setInterval(10000)
        # self.timer.start()

        # ----------------------------------------------------------------

        self.agendarButton = QPushButton("Agendar")
        self.cancelarButton = QPushButton("Cancelar")

        self.agendarButton.setStyleSheet("""
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

        self.cancelarButton.setStyleSheet("""
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

        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.diaInput)
        dataLayout.addWidget(self.mesInput)
        dataLayout.addWidget(self.anoInput)

        horaLayout = QHBoxLayout()
        horaLayout.addWidget(self.horaInput)
        horaLayout.addWidget(self.separator)
        horaLayout.addWidget(self.minutoInput)
        horaLayout.addWidget(self.defaultButton)

        self.layout.addWidget(self.nomeLabel)
        self.layout.addWidget(self.nomeInput)
        self.layout.addWidget(self.cpfLabel)
        self.layout.addWidget(self.cpfInput)
        self.layout.addLayout(self.servicoLayout)
        # self.layout.addWidget(self.valorLabel)
        # self.layout.addWidget(self.valorInput)
        self.layout.addLayout(self.tempoLayout)
        # self.layout.addWidget(self.tempoLabel)
        # self.layout.addWidget(self.tempoInput)
        self.layout.addWidget(self.barbeiroLabel)
        self.layout.addWidget(self.barbeiroInput)
        self.layout.addWidget(self.dataLabel)
        self.layout.addLayout(dataLayout)
        self.layout.addWidget(self.horaLabel)
        self.layout.addLayout(horaLayout)

        self.layout.addWidget(self.agendarButton)
        self.layout.addWidget(self.cancelarButton)

        self.servicoButton.clicked.connect(self.openServices)
        self.defaultButton.clicked.connect(self.clickedDefaultHourCurrent)
        self.agendarButton.clicked.connect(self.clickSchedule)

        self.setLayout(self.layout)

    # Abre a tela de serviços prestados pelo o usuario
    def openServices(self):
        try:
            self.services = QDialog(self)
            self.services.setFixedSize(420, 300)
            self.services.setWindowTitle("Serviços")
            self.services.setStyleSheet("""
                background-color: white;
                font-size: 14px;
                font-weight: bold;
            """)

            titleLabel = QLabel("Serviços")
            titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px")

            scrollArea = QScrollArea(self.services)
            scrollArea.setGeometry(0, 40, 420, 300)

            scrollContent = QWidget()
            scrollLayout = QVBoxLayout(scrollContent)

            conn = ConnectDB()
            conn.conecta()
            sqlServices = "select * from servicos"
            conn.execute(sqlServices)
            services = conn.fetchall()
            for service in services:
                nome = service["nome_servico"]
                valorFormatado = f"{service['valor_servico']:.2f}".replace(".", ",")
                tempo = service["tempo_servico"]
                horas = "m" if service["horas"] == "minutos" else "h"
                layout = QHBoxLayout()
                label = QLabel(f"{nome}\nR$ {valorFormatado} - {tempo}{horas}")
                label.setStyleSheet("padding: 10px")
                label.setFixedWidth(250)  # Limita a largura máxima do rótulo

                button = QPushButton("Confirmar")
                button.setStyleSheet("""
                    background-color: #3498db;
                    color: white;
                    padding: 5px 10px;
                    border: none;
                    border-radius: 3px;
                    font-weight: bold;
                """)
                button.setFixedSize(100, 30)
                button.clicked.connect(lambda checked, s=service: self.onServiceSelected(s))

                layout.addWidget(label)
                layout.addWidget(button)
                scrollLayout.addLayout(layout)

                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                scrollLayout.addWidget(line)

            scrollArea.setWidget(scrollContent)

            main_layout = QVBoxLayout(self.services)
            main_layout.addWidget(titleLabel)
            main_layout.addWidget(scrollArea)

            self.services.exec_()
        except Exception as e:
            print(e)

    # Serviço selecionado e seta os textos nas variaveis da classe
    def onServiceSelected(self, servico):
        nome = servico["nome_servico"]
        valorFormatado = f"{servico['valor_servico']:.2f}".replace(".", ",")
        self.idServico = servico["id"]
        self.tempo = servico["tempo_servico"]
        self.horas = "m" if servico["horas"] == "minutos" else "h"
        self.servicoInput.setText(str(nome))
        self.valorInput.setText(str(valorFormatado))
        self.tempoInput.setText(f"{str(self.tempo)}{str(self.horas)}")
        self.services.close()

    # Confirmação de agendamento de cliente e salva no BD
    def clickSchedule(self):
        nomeCliente = self.nomeInput.text()
        cpfCliente = self.cpfInput.text()
        servico = self.servicoInput.text()
        valor = self.valorInput.text()
        horas = self.horaInput.text()
        minutos = self.minutoInput.text()
        dt = datetime.strptime(f"{self.anoInput.text()}{self.mesInput.text()}{self.diaInput.text()}{horas}{minutos}00",
                               "%Y%m%d%H%M%S")

        previsao = datetime.strptime(str(dt + timedelta(minutes=self.tempo)), "%Y-%m-%d %H:%M:%S").strftime(
            "%Y%m%d%H%M%S") \
            if self.horas == "m" else datetime.strptime(str(dt + timedelta(hours=self.tempo)),
                                                        "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")

        data = datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")
        barberList = self.barbeiroInput.currentText().split("-")
        barberId = barberList[0]
        conn = ConnectDB()
        conn.conecta()
        if nomeCliente == "" or cpfCliente == "..-" or servico == "" or valor == "" or self.tempo == "" or barberId == "":
            messageDefault('Preencha todos os campos!')
            return
        try:
            sqlVerificarAgendamento = f"select * from agendamentos where data_hora={data} and id_barbeiro={barberId}"
            conn.execute(sqlVerificarAgendamento)
            agendamento = conn.fetchone()
            if agendamento:
                messageDefault("Este horário já esta agendado, verifique outro horário ou barbeiro")
                return
            sqlInsert = f"""
                    insert into agendamentos
                    (id_servico, nome_cliente, cpf_cliente, data_hora, previsao, status, id_barbeiro)
                    values
                    (%s, %s, %s, %s, %s, %s, %s)
                    """
            val = (self.idServico, nomeCliente, cpfCliente, data, previsao, 0, barberId)
            conn.execute(sqlInsert, val)
            conn.commit()

            messageDefault("Agendamento realizado com sucesso!")

            self.nomeInput.setText("")
            self.cpfInput.setText("")
            self.servicoInput.setText("")
            self.valorInput.setText("")
            self.tempoInput.setText("")
            self.barbeiroInput.setCurrentIndex(0)
            self.timer.timeout.connect(self.iniTimer)
            self.timer.setInterval(0)
            self.timer.start()

        except Exception as e:
            print(f"Erro: {e}")

        finally:
            conn.desconecta()

    # Aumenta o número que recebe
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

        if self.diaInput.text() == "32":
            self.diaInput.setText("01")

        if self.mesInput.text() == "13":
            self.mesInput.setText("01")

    # Diminui o número que recebe
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

        if self.diaInput.text() == "00":
            self.diaInput.setText("31")

        if self.mesInput.text() == "00":
            self.mesInput.setText("12")

    # Faz a validação dos numeros dos campos de data/hora
    def textChangedFields(self):
        dateCurrent = int(self.dateTime.toString('yyyy'))
        if not self.diaInput.text().isdigit() or not self.mesInput.text().isdigit() or not self.anoInput.text().isdigit():
            self.diaInput.setText("01")
            self.mesInput.setText("01")
            self.anoInput.setText(str(dateCurrent))
            return

        else:
            dayText = int(self.diaInput.text())
            monthText = int(self.mesInput.text())
            yearText = int(self.anoInput.text())
            if dayText > 31:
                self.diaInput.setText("01")

            elif monthText > 12:
                self.mesInput.setText("01")

            elif yearText < dateCurrent:
                messageDefault("Ano inválido!")
                self.anoInput.setText(str(dateCurrent))

        if not self.horaInput.text().isdigit() or not self.minutoInput.text().isdigit():
            self.timer.timeout.connect(self.iniTimer)
            self.timer.setInterval(0)
            self.timer.start()
            return
        else:
            hourText = int(self.horaInput.text())
            minuteText = int(self.minutoInput.text())

            if hourText > 24:
                try:
                    self.timer.timeout.connect(self.iniTimer)
                    self.timer.setInterval(0)
                    self.timer.start()
                except Exception as e:
                    self.horaInput.setText("24")

            elif minuteText > 59:
                try:
                    self.timer.timeout.connect(self.iniTimer)
                    self.timer.setInterval(0)
                    self.timer.start()
                except Exception as e:
                    self.minutoInput.setText("59")

    # Realize a redefinição do horario atual
    def clickedDefaultHourCurrent(self):
        self.timer.timeout.connect(self.iniTimer)
        self.timer.setInterval(0)
        self.timer.start()

    # Define o horario atual nas variaveis de texto da classe
    def hourCurrent(self):
        try:
            # self.timer.start(10000)
            time = QDateTime.currentDateTime()
            hourCurrent = time.toString("hh")
            minuteCurrent = time.toString("mm")
            self.horaInput.setText(str(hourCurrent))
            self.minutoInput.setText(str(minuteCurrent))
        except Exception as e:
            self.horaInput.setText("24")
            self.minutoInput.setText("59")

    # Inicializa uma tread para rodar em segundo plano e faz a atualização de hora automatico na aplicação
    # desabilitada atualizacao automatica
    def iniTimer(self):
        self.timer.stop()
        worker = WorkerTreadTime(self)
        worker.start()
        worker.finished.connect(self.hourCurrent)

    # Faz a busca de um cliente no BD apartir de um cpf passado
    def searchClientByCpf(self, cpf):
        try:
            conn = ConnectDB()
            conn.conecta()
            sql = f"select nome from clientes where cpf='{cpf}'"
            conn.execute(sql)
            row = conn.fetchone()
            if row:
                nomeClient = row['nome']
                self.nomeInput.setText(nomeClient)
            else:
                messageDefault("Cadastro não encontrado")
                self.nomeInput.setText("")
        except Exception as e:
            exc_type, exc_value = sys.exc_info()
            print("Tipo de exceção:", exc_type)
            print("Mensagem de erro:", exc_value)

    # Abre uma janela com NOME e CPF e busca um cliente pelo nome passado
    def showTreeWidget(self, name):
        try:
            self.treeWidget = QTreeWidget(self)
            self.treeWidget.itemSelectionChanged.connect(self.selectedItem)
            self.treeWidget.installEventFilter(self)
            if name.text() == "" or name.text().isdigit():
                self.treeWidget.clear()
                messageDefault("Nenhum registo encontrado")
            else:
                conn = ConnectDB()
                conn.conecta()
                sql = f"select nome, cpf from clientes where nome like '%{name.text()}%' limit 100"
                conn.execute(sql)
                rows = conn.fetchall()
                if rows:
                    itemCount = 0
                    self.treeWidget.setColumnCount(2)
                    self.treeWidget.setHeaderLabels(['Nome', 'CPF'])
                    self.treeWidget.setColumnWidth(0, 250)
                    self.treeWidget.setColumnWidth(1, 100)
                    self.treeWidget.setGeometry(0, 110, 483, 200)
                    self.treeWidget.header().setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    self.treeWidget.setStyleSheet("QScrollBar {height:0px;}")
                    self.treeWidget.setStyleSheet("QScrollBar {width:0px;}")

                    for row in rows:
                        itemCount += 1
                        client = QTreeWidgetItem(self.treeWidget)
                        nome = str(row['nome'])
                        cpf = str(row['cpf'])
                        client.setText(0, nome)
                        client.setText(1, cpf)
                        client.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
                        self.treeWidget.setFocus()
                    self.treeWidget.show()
                self.nome = rows[0]['nome']
                self.cpf = rows[0]['cpf']
        except Exception as e:
            print(e)

    # Função criada para receber o valor de texto e ser retornada no campo nome o texto em maiúsculo
    # desabilitado
    def textChangedUpperCase(self, txt):
        up_text = txt.upper()
        self.nomeInput.setText(up_text)

    # Caso a janela que realize a busca de cliente por nome esteje aberta/instanciada apertando 'ESC' a janela é fechada
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if hasattr(self, 'treeWidget') and self.treeWidget.isVisible():
                self.treeWidget.close()
        else:
            super().keyPressEvent(event)

    # Com a janela de busca de cliente por nome aberta a linha selecionada é pego os valores de texto e definido nos
    # atributos da classe
    def selectedItem(self):
        getSelect = self.treeWidget.selectedItems()
        if getSelect:
            baseNode = getSelect[0]
            getChildNome = baseNode.text(0)
            getChildCpf = baseNode.text(1)
            self.nome = str(getChildNome)
            self.cpf = str(getChildCpf)

    # Faz a verificação de quais objetos estão com foco e quais teclas estão sendo pressionadas assim realiza chamadas de
    # funções/ações e etc
    def eventFilter(self, obj, e):
        if obj == self.cpfInput:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
                    self.searchClientByCpf(self.cpfInput.text())
                    return True
        if obj == self.nomeInput:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
                    self.showTreeWidget(self.nomeInput)  # Chamando a função para adicionar o QTreeWidget
                    return True

        if hasattr(self, 'treeWidget') and self.treeWidget.isVisible():
            if obj == self.treeWidget:
                if e.type() == QEvent.KeyPress:
                    if e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
                        self.nomeInput.setText(self.nome)
                        self.cpfInput.setText(self.cpf)
                        self.treeWidget.close()
                        return True
        return False


class AgendamentosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.idServico = 0
        self.idAgendamento = 0
        self.horas = 0
        self.tempoServico = 0

        self.title = QLabel(self)
        self.title.setText("Agendamentos")
        self.title.setStyleSheet("font-size: 25px; font-weight: bold; font-family: Arial, sans-serif; color: #fff")
        self.title.setGeometry(0, 30, 200, 50)

        # ------------------------------------------------------------

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
        self.closeButton.setGeometry(460, 0, 40, 25)

        # ------------------------------------------------------------

        self.dataEdit = QDateEdit(self)
        self.dataEdit.setCalendarPopup(True)
        self.dataEdit.setStyleSheet("""
                QDateEdit {
                    border: 2px solid #0078d4; /* Cor da borda */
                    border-radius: 5px; /* Borda arredondada */
                    padding: 3px;
                }
            """)
        self.dataEdit.setDisplayFormat("dd/MM/yyyy")
        self.dataEdit.setGeometry(0, 100, 100, 30)
        self.setToday()

        self.nomeInput = QLineEdit(self)
        self.nomeInput.setGeometry(105, 98, 270, 35)

        self.searchDataButton = QPushButton(self)
        self.searchDataButton.setText("Buscar")
        self.searchDataButton.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.searchDataButton.setGeometry(380, 100, 100, 30)

        # ------------------------------------------------------------

        self.treeWidgetAgendamentos = QTreeWidget(self)
        self.treeWidgetAgendamentos.setGeometry(0, 150, 480, 540)
        self.treeWidgetAgendamentos.setColumnCount(8)
        self.treeWidgetAgendamentos.setHeaderLabels(
            ["Cliente", "Serviço", "Valor", "Barbeiro", "Horário", "Previsão de Término", "", "", ""])
        self.treeWidgetAgendamentos.setColumnWidth(0, 250)
        self.treeWidgetAgendamentos.setColumnWidth(1, 160)
        self.treeWidgetAgendamentos.setColumnWidth(2, 70)
        self.treeWidgetAgendamentos.setColumnWidth(3, 180)
        self.treeWidgetAgendamentos.setColumnWidth(4, 145)
        self.treeWidgetAgendamentos.setColumnWidth(5, 145)
        self.treeWidgetAgendamentos.setColumnWidth(6, 50)
        self.treeWidgetAgendamentos.setColumnWidth(7, 50)
        self.treeWidgetAgendamentos.setColumnWidth(8, 50)
        self.treeWidgetAgendamentos.header().setDefaultAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.treeWidgetAgendamentos.header().setStyleSheet("""
                                font: bold 12px; 
                                text-align: center; 
                                font-family: Helvetica; 
                                border: 1px solid #d3d3d3;
                                background-color: #f1f1f1;
        """)
        self.treeWidgetAgendamentos.setStyleSheet(stylesheetTreeWidgts)
        self.searchDataButton.clicked.connect(self.searchDateAgendamento)

    # Define a data atual
    def setToday(self):
        today = QDate().currentDate().toString("dd/MM/yyyy")
        formatToday = QDate().fromString(today, "dd/MM/yyyy")
        self.dataEdit.setDate(formatToday)

    def searchDateAgendamento(self):
        try:
            conn = ConnectDB()
            conn.conecta()
            nameClient = self.nomeInput.text()
            date = datetime.strptime(str(self.dataEdit.text()), "%d/%m/%Y").strftime("%Y%m%d")
            sql = f"""
                select a.id_agendamento, a.nome_cliente, s.nome_servico, s.valor_servico, a.id_servico, b.nome, a.data_hora, 
                a.previsao, s.horas, s.tempo_servico
                from agendamentos a
                inner join servicos s on a.id_servico=s.id
                inner join barbeiro b on a.id_barbeiro=b.id_barbeiro
                where data_hora between {date} and {date}235959 and
                nome_cliente like coalesce('%{nameClient}%', '') and status=0
                order by data_hora
            """
            conn.execute(sql)
            clients = conn.fetchall()
            if clients:
                clientCount = 0
                self.treeWidgetAgendamentos.clear()
                image_layout = QHBoxLayout()
                image_layout.setAlignment(Qt.AlignCenter)
                for client in clients:
                    clientCount += 1
                    agendamento = QTreeWidgetItem(self.treeWidgetAgendamentos)
                    idAgendamento = str(client['id_agendamento'])
                    idServico = str(client['id_servico'])
                    nomeClient = str(client['nome_cliente'])
                    servico = str(client['nome_servico'])
                    horas_minutos = str(client['horas'])
                    tempo = client['tempo_servico']
                    valor = client['valor_servico']
                    nomeBarbeiro = str(client['nome'])
                    data = datetime.strptime(str(client['data_hora']), "%Y-%m-%d %H:%M:%S").strftime(
                        "%d-%m-%Y %H:%M:%S") if client['data_hora'] else ""
                    previsao = datetime.strptime(str(client['previsao']), "%Y-%m-%d %H:%M:%S").strftime(
                        "%d-%m-%Y %H:%M:%S") if client['previsao'] else ""
                    agendamento.setText(0, nomeClient)
                    agendamento.setText(1, servico)
                    agendamento.setText(2, f"R$ {float(valor):.2f}")
                    agendamento.setText(3, nomeBarbeiro)
                    agendamento.setText(4, data)
                    agendamento.setText(5, previsao)

                    pixmap1 = QPixmap('assets/icon-critical.ico')
                    pixmap1 = pixmap1.scaled(26, 26)
                    lblImageDelete = QLabel()
                    lblImageDelete.setPixmap(pixmap1)
                    lblImageDelete.setAlignment(Qt.AlignCenter)

                    pixmap2 = QPixmap('assets/icon-edit.ico')
                    pixmap2 = pixmap2.scaled(25, 25)
                    lblImageUpdate = QLabel()
                    lblImageUpdate.setPixmap(pixmap2)
                    lblImageUpdate.setAlignment(Qt.AlignCenter)

                    pixmap3 = QPixmap('assets/icon-check.ico')
                    pixmap3 = pixmap3.scaled(25, 25)
                    lblImageCheck = QLabel()
                    lblImageCheck.setPixmap(pixmap3)
                    lblImageCheck.setAlignment(Qt.AlignCenter)

                    lblImageCheck.mousePressEvent = lambda event, label=idAgendamento: self.checkAgendamento(label)
                    lblImageDelete.mousePressEvent = lambda event, label=idAgendamento: self.deleteAgendamento(label)
                    lblImageUpdate.mousePressEvent = lambda event, label=idAgendamento, label2=idServico, label3=tempo, label4=horas_minutos: \
                        self.updateAgendamento(label, label2, label3, label4)

                    self.treeWidgetAgendamentos.setItemWidget(agendamento, 6, lblImageCheck)
                    self.treeWidgetAgendamentos.setItemWidget(agendamento, 7, lblImageDelete)
                    self.treeWidgetAgendamentos.setItemWidget(agendamento, 8, lblImageUpdate)
            else:
                self.treeWidgetAgendamentos.clear()
                messageDefault("Não há agendamentos!")

        except Exception as e:
            messageDefault("Erro ao buscar agendamentos")
            print(e)

    def openServices(self):
        try:
            self.services = QDialog(self)
            self.services.setFixedSize(420, 300)
            self.services.setWindowTitle("Serviços")
            self.services.setStyleSheet("""
                background-color: white;
                font-size: 14px;
                font-weight: bold;
            """)

            titleLabel = QLabel("Serviços")
            titleLabel.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px")

            scrollArea = QScrollArea(self.services)
            scrollArea.setGeometry(0, 40, 420, 300)

            scrollContent = QWidget()
            scrollLayout = QVBoxLayout(scrollContent)

            conn = ConnectDB()
            conn.conecta()
            sqlServices = "select * from servicos"
            conn.execute(sqlServices)
            services = conn.fetchall()
            for service in services:
                nome = service["nome_servico"]
                valorFormatado = f"{service['valor_servico']:.2f}".replace(".", ",")
                tempo = service["tempo_servico"]
                horas = "m" if service["horas"] == "minutos" else "h"
                layout = QHBoxLayout()
                label = QLabel(f"{nome}\nR$ {valorFormatado} - {tempo}{horas}")
                label.setStyleSheet("padding: 10px")
                label.setFixedWidth(250)  # Limita a largura máxima do rótulo

                button = QPushButton("Confirmar")
                button.setStyleSheet("""
                    background-color: #3498db;
                    color: white;
                    padding: 5px 10px;
                    border: none;
                    border-radius: 3px;
                    font-weight: bold;
                """)
                button.setFixedSize(100, 30)
                button.clicked.connect(lambda checked, s=service: self.onServiceSelected(s))

                layout.addWidget(label)
                layout.addWidget(button)
                scrollLayout.addLayout(layout)

                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setFrameShadow(QFrame.Sunken)
                scrollLayout.addWidget(line)

            scrollArea.setWidget(scrollContent)

            main_layout = QVBoxLayout(self.services)
            main_layout.addWidget(titleLabel)
            main_layout.addWidget(scrollArea)

            self.services.exec_()
        except Exception as e:
            print(e)

    def onServiceSelected(self, servico):
        nome = servico["nome_servico"]
        valorFormatado = f"{servico['valor_servico']:.2f}".replace(".", ",")
        self.idServico = servico["id"]
        self.tempoServico = servico["tempo_servico"]
        self.horas = "m" if servico["horas"] == "minutos" else "h"
        self.servicoLineEdit.setText(str(nome))
        self.valorLineEdit.setText(str(valorFormatado))
        self.tempoLineEdit.setText(f"{str(self.tempoServico)}{str(self.horas)}")
        self.services.close()

    def deleteAgendamento(self, idAgendamento):
        try:
            conn = ConnectDB()
            conn.conecta()
            sqlDelete = f"delete from agendamentos where id_agendamento={idAgendamento}"
            conn.execute(sqlDelete)
            conn.commit()
            self.searchDateAgendamento()
            messageDefault("Agendamento excluído")
        except Exception as e:
            print(e)

    def updateAgendamento(self, idAgendamento, idServico, tempoServico, horas_minutos):
        self.idAgendamento = idAgendamento
        self.idServico = idServico
        self.tempoServico = tempoServico
        self.horas = horas_minutos
        try:
            conn = ConnectDB()
            conn.conecta()

            # -----------------------------------------------------

            sqlAgendamentos = f"""
                    select a.id_agendamento, a.nome_cliente, s.nome_servico, s.valor_servico, s.tempo_servico, 
                    s.horas, b.nome, b.id_barbeiro, a.data_hora, a.previsao
                    from agendamentos a
                    inner join servicos s on a.id_servico=s.id
                    inner join barbeiro b on a.id_barbeiro=b.id_barbeiro
                    where id_agendamento={idAgendamento}
            """
            conn.execute(sqlAgendamentos)
            agendamentos = conn.fetchall()
            nomeClient = agendamentos[0]["nome_cliente"]
            servico = agendamentos[0]["nome_servico"]
            valor = agendamentos[0]["valor_servico"]
            tempo = agendamentos[0]["tempo_servico"]
            horas = "m" if agendamentos[0]["horas"] == "minutos" else "h"
            idBarbeiro = agendamentos[0]["id_barbeiro"]
            nomeBarbeiro = agendamentos[0]["nome"]
            dataDoServico = agendamentos[0]["data_hora"]
            dataFormatada = datetime.strptime(str(dataDoServico), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M")
            qDate = QDateTime.fromString(dataFormatada, "dd-MM-yyyy HH:mm")

            # -----------------------------------------------------

            sqlBarbeiros = "select id_barbeiro, nome from barbeiro"
            conn.execute(sqlBarbeiros)
            barbeiros = conn.fetchall()

            # -----------------------------------------------------

            self.showDialog = QDialog(self)
            self.showDialog.setFixedSize(420, 300)
            self.showDialog.setWindowTitle("Informações de Agendamento")

            # -----------------------------------------------------

            layout = QVBoxLayout(self.showDialog)
            layoutServico = QHBoxLayout()
            layoutTempoeValor = QHBoxLayout()
            layoutHorario = QHBoxLayout()

            # -----------------------------------------------------

            lblNome = QLabel("Cliente:")
            lblNome.setStyleSheet("color: #fff")
            self.nomeLineEdit = QLineEdit()
            self.nomeLineEdit.setText(nomeClient)
            self.nomeLineEdit.setDisabled(True)

            # -----------------------------------------------------

            lblServico = QLabel("Serviço:")
            lblServico.setStyleSheet("color: #fff")
            self.servicoLineEdit = QLineEdit()
            self.servicoLineEdit.setText(servico)
            self.servicoLineEdit.setDisabled(True)

            # -----------------------------------------------------

            lblTempo = QLabel("Tempo:")
            lblTempo.setStyleSheet("color: #fff")
            self.tempoLineEdit = QLineEdit()
            self.tempoLineEdit.setText(f"{tempo}{horas}")
            self.tempoLineEdit.setDisabled(True)

            # -----------------------------------------------------

            lblValor = QLabel("Valor:")
            lblValor.setStyleSheet("color: #fff")
            self.valorLineEdit = QLineEdit()
            self.valorLineEdit.setText(f"{float(valor):.2f}")
            self.valorLineEdit.setDisabled(True)

            # -----------------------------------------------------

            lblBarbeiro = QLabel("Barbeiro:")
            lblBarbeiro.setStyleSheet("color: #fff")
            self.barbeiroLineEdit = QComboBox()

            self.barbeiroLineEdit.addItem(f"{idBarbeiro} - {nomeBarbeiro}")
            for barbeiro in barbeiros:
                if barbeiro['nome'] == nomeBarbeiro:
                    continue
                self.barbeiroLineEdit.addItem(f"{barbeiro['id_barbeiro']} - {barbeiro['nome']}")

            # -----------------------------------------------------

            servicoButton = QPushButton("Selecionar")
            servicoButton.resize(80, 23)
            servicoButton.setStyleSheet("""
                            QPushButton {
                                border-radius: 3px; 
                                background-color: #3498db; 
                                color: #fff; 
                                padding: 6px
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
            """)

            # -----------------------------------------------------

            confirmButton = QPushButton("Confirmar")
            confirmButton.resize(80, 23)
            confirmButton.setStyleSheet("""
                            QPushButton {
                                border-radius: 3px; 
                                background-color: #3498db; 
                                color: #fff; 
                                padding: 6px
                            }
                            QPushButton:hover {
                                background-color: #2980b9;
                            }
            """)

            # -----------------------------------------------------

            layoutServico.addWidget(lblServico)
            layoutServico.addWidget(self.servicoLineEdit)
            layoutServico.addWidget(servicoButton)

            layoutTempoeValor.addWidget(lblTempo)
            layoutTempoeValor.addWidget(self.tempoLineEdit)
            layoutTempoeValor.addWidget(lblValor)
            layoutTempoeValor.addWidget(self.valorLineEdit)

            lblHorario = QLabel("Horário:")
            self.horarioDateTimeEdit = QDateTimeEdit()
            self.horarioDateTimeEdit.setDateTime(qDate)
            self.horarioDateTimeEdit.setDisplayFormat("dd-MM-yyyy HH:mm")
            self.horarioDateTimeEdit.setCalendarPopup(True)

            layoutHorario.addWidget(lblHorario)
            layoutHorario.addWidget(self.horarioDateTimeEdit)

            layout.addWidget(lblNome)
            layout.addWidget(self.nomeLineEdit)
            layout.addWidget(lblBarbeiro)
            layout.addWidget(self.barbeiroLineEdit)
            layout.addLayout(layoutServico)
            layout.addLayout(layoutTempoeValor)
            layout.addLayout(layoutHorario)
            layout.addWidget(confirmButton)

            servicoButton.clicked.connect(self.openServices)
            confirmButton.clicked.connect(self.confirmUpdateAgendamento)

            self.showDialog.exec_()

        except Exception as e:
            print(e)

    def checkAgendamento(self, idAgendamento):
        conn = ConnectDB()
        conn.conecta()
        try:
            sql = f"UPDATE agendamentos SET status=1 where id_agendamento={idAgendamento}"
            conn.execute(sql)
            conn.commit()
            self.searchDateAgendamento()
            messageDefault("Serviço realizado! ✓")
        except Exception as e:
            messageDefault("Erro ao atualizar status de agendamento")
            print(e)
        finally:
            conn.desconecta()

    def confirmUpdateAgendamento(self):
        conn = ConnectDB()
        conn.conecta()
        try:
            dataAlterada = datetime.strptime(str(self.horarioDateTimeEdit.text()), "%d-%m-%Y %H:%M").strftime("%Y%m%d%H%M%S")
            dataFormatada = datetime.strptime(str(self.horarioDateTimeEdit.text()), "%d-%m-%Y %H:%M")
            previsaoTermino = datetime.strptime(str(dataFormatada + timedelta(minutes=self.tempoServico)),
                                                "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S") \
                if self.horas == "m" or self.horas == "minutos" else datetime.strptime(str(dataFormatada + timedelta(hours=self.tempoServico)),
                                                            "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")
            barberList = self.barbeiroLineEdit.currentText().split("-")
            barberId = barberList[0]
            sql = f"""
                SELECT *
                FROM `agendamentos` 
                where id_servico={self.idServico} and data_hora={dataAlterada} and id_barbeiro={barberId}
            """
            conn.execute(sql)
            verification = conn.fetchall()
            if verification:
                messageDefault("Nada foi alterado")
                return
            sql = f"""
                UPDATE agendamentos 
                SET id_barbeiro={barberId}, id_servico={self.idServico}, data_hora={dataAlterada}, previsao={previsaoTermino}
                where id_agendamento={self.idAgendamento}
            """
            conn.execute(sql)
            conn.commit()
            messageDefault("Reagendamento realizado com sucesso")
            self.searchDateAgendamento()
            self.showDialog.close()
        except Exception as e:
            messageDefault("Ocorreu um erro ao reagendar")
            print(e)
        finally:
            conn.desconecta()


class WorkerTreadTime(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.window = parent

    def run(self):
        try:
            pass
        except Exception as e:
            self.parent().horaInput.setText("24")
            self.parent().minutoInput.setText("59")


class Agendamento(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cadastros")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("""
        QDialog {
            background-color: #262D37;
        }
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

        self.buttonAgendar = QPushButton("Agendar", self.container)
        self.buttonAgendamentos = QPushButton("Agendamentos", self.container)

        self.buttonAgendar.clicked.connect(self.showAgendar)
        self.buttonAgendamentos.clicked.connect(self.showAgendamentos)

        self.buttonAgendar.setStyleSheet("""
                QPushButton { 
                    background-color: #282828; 
                    color: white; 
                    font-size: 
                    16px; 
                    padding: 10px; 
                    border: 2px solid #fff; 
                    border-radius: 5px; 
                    width: 100px
                    }
                QPushButton:hover { 
                    background-color: #474747;
                }"""
        )

        self.buttonAgendamentos.setStyleSheet("""
                QPushButton { 
                    background-color: #282828; 
                    color: white; 
                    font-size: 
                    16px; 
                    padding: 10px; 
                    border: 2px solid #fff; 
                    border-radius: 5px; 
                    width: 100px
                    }
                QPushButton:hover { 
                    background-color: #474747; }"""
        )

        menuLayout = QVBoxLayout()
        menuLayout.setContentsMargins(10, 30, 10, 500)  # Ajuste as margens inferior para mover o menu para cima
        menuLayout.addWidget(self.buttonAgendar)
        menuLayout.addWidget(self.buttonAgendamentos)
        self.container.setLayout(menuLayout)

        self.stack = QStackedWidget(self)
        self.stack.setGeometry(250, 0, 503, 712)

        self.agendarWidget = AgendarWidget()
        self.agendamentosWidget = AgendamentosWidget()
        self.agendarWidget.cancelarButton.clicked.connect(self.closeWindow)
        self.agendamentosWidget.closeButton.clicked.connect(self.closeWindow)

        self.stack.addWidget(self.agendarWidget)
        self.stack.addWidget(self.agendamentosWidget)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            pass

    def closeWindow(self):
        self.close()

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

    def showAgendar(self):
        self.stack.setCurrentWidget(self.agendarWidget)

    def showAgendamentos(self):
        self.agendamentosWidget.treeWidgetAgendamentos.clear()
        self.stack.setCurrentWidget(self.agendamentosWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Agendamento()
    dialog.show()
    sys.exit(app.exec_())
