from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QApplication


class SquareLabel(QLabel):
    def __init__(self, parent=None):
        super(SquareLabel, self).__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(223, 230, 248))
        self.setPalette(p)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        print("On Hover")# event.pos().x(), event.pos().y()

    def mousePressEvent(self, event):
        print(event)


class SuperEdit(QWidget):
    def __init__(self, data, parent=None):
        super(SuperEdit, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

        for name in data:
            label = SquareLabel(self)
            label.setText(name)
            layout.addWidget(label)


if __name__ == '__main__':
    names = ['Name 1', 'Name 2', 'Name 3']
    app = QApplication([])
    editor = SuperEdit(names)
    editor.show()
    app.exec_()
