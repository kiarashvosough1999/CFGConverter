from sys import argv
from PyQt5.QtWidgets import QApplication
from GUI import GUI

if __name__ == '__main__':
    app = QApplication(argv)
    x = GUI()
    x.show()
    app.exec_()
