import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTreeWidget com imagens clicáveis")
        self.setGeometry(100, 100, 400, 300)

        self.treeWidget = QTreeWidget(self)
        self.setCentralWidget(self.treeWidget)

        self.treeWidget.setColumnCount(2)
        self.treeWidget.setHeaderLabels(["Item", ""])
        self.treeWidget.setColumnWidth(0, 250)

        # Criar um item da árvore com duas imagens clicáveis
        item1 = QTreeWidgetItem(self.treeWidget, ["Item 1"])
        image_widget = QWidget()
        image_layout = QHBoxLayout()

        # Carregar a primeira imagem (substitua 'path_imagem1.png' pelo caminho da sua primeira imagem)
        pixmap1 = QPixmap('icon-critical.ico')
        pixmap1 = pixmap1.scaled(30, 30)
        label1 = QLabel()
        label1.setPixmap(pixmap1)
        label1.mousePressEvent = lambda event, label="imagem1": self.on_image_clicked(label)
        image_layout.addWidget(label1)

        # Carregar a segunda imagem (substitua 'path_imagem2.png' pelo caminho da sua segunda imagem)
        pixmap2 = QPixmap('icon-information.ico')
        pixmap2 = pixmap2.scaled(26, 26)
        label2 = QLabel()
        label2.setPixmap(pixmap2)
        label2.mousePressEvent = lambda event, label="imagem2": self.on_image_clicked(label)
        image_layout.addWidget(label2)

        image_widget.setLayout(image_layout)
        image_layout.setAlignment(Qt.AlignCenter)
        self.treeWidget.setItemWidget(item1, 1, image_widget)

    def on_image_clicked(self, label):
        print(f"Imagem clicada: {label}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
