from PyQt5.QtWidgets import QMessageBox


def messageDefault(message):
    info_box = QMessageBox()
    info_box.setWindowIcon(QtGui.QIcon("icon-information"))
    info_box.setIcon(QMessageBox.Information)
    info_box.setWindowTitle("Informação")
    info_box.setText(f"{message}")
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
                """)
    info_box.exec_()


if __name__ == "__main__":
    messageDefault("Teste")
