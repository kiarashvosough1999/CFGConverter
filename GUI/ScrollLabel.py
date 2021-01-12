from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class ScrollLabel(QScrollArea):


    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)

        self.label = QLabel(content)

        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.label.setWordWrap(True)

        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText('')
        self.label.setText(text)