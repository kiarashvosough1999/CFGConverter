import sys
from os.path import dirname, join
from sys import platform
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, QAction, QMenu, QMenuBar, QComboBox, \
    QPushButton
from GUI.CodeEditor import CodeEditor
from GUI.ScrollLabel import ScrollLabel


def show_window():
    app = QApplication(sys.argv)
    x = GUI()
    x.show()
    app.exec_()


class GUI(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        # self.statusBar().showMessage('Ready')
        self.menuBar = QMenuBar()
        self.form_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.parentWidget())
        self.code_Editor = CodeEditor()
        self.combo_box = QComboBox()
        self.NF_button = QPushButton('is in NF')
        self.convert_button = QPushButton('Convert')
        self.result_scrolable_label = ScrollLabel()
        self.form_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.form_widget)
        self.init_menu_bar()
        self.init_gridlayout_items()
        self.init_comboBox()
        self.setWindowTitle("CFG Converter")

    def resizeEvent(self, event):
        self.result_scrolable_label.setMaximumHeight(event.size().height() * 1 / 5)

    def init_menu_bar(self):
        if platform == "darwin":
            self.menuBar.setNativeMenuBar(True)

        fileMenu = QMenu("&File", self)

        impAct = QAction('Import from file', self)
        expAct = QAction('Export result to file',self)

        fileMenu.addAction(impAct)
        fileMenu.addAction(expAct)
        self.menuBar.addMenu(fileMenu)
        self.setMenuBar(self.menuBar)
        # self.menuBar.show()

    def init_comboBox(self):
        self.combo_box.addItems(['GreiBach', 'Chomsky'])

    def init_gridlayout_items(self):
        self.grid_layout.addWidget(self.combo_box, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.NF_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.convert_button, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.code_Editor, 1, 0, 1, 3)
        self.grid_layout.addWidget(self.result_scrolable_label, 2, 0, -1, 3)

    def get_qml_path(self):
        return join(dirname(__file__), 'MainForm/MainForm.qml')

    # def show(self, text):
    #     print(text)

    # def start_app(self):
    #     app = QGuiApplication(sys.argv)
    #     engine = QQmlApplicationEngine()
    #     x = LineNumberModel()
    #     # y = ObjectManager()
    #     # engine.setContextForObject(y,QQmlContext=QQmlContext())
    #     engine.rootContext().setContextProperty('lineNumberModel', x)
    #     # engine.rootContext().setContextProperty('manager', y)
    #     engine.load(abspath(self.get_qml_path()))
    #
    #     win = engine.rootObjects()[0]
    #     win.textUpdated.connect(self.show)
    #     # button = win.findChild(QObject, "myButton")
    #     # print(button.property("text"))
    #     #
    #     # @pyqtSlot(str, name="myFunction")
    #     # def myFunction(text):
    #     #     print(text)
    #
    #     # l = QTextEdit("jk")
    #     # button.textChanged.connect()
    #
    #
    #
    #     if not engine.rootObjects():
    #         sys.exit(-1)
    #     sys.exit(app.exec())

# class ObjectManager(QObject):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._qobjects = []
#
#     @property
#     def qobjects(self):
#         return self._qobjects
#
#     @pyqtSlot(QObject, name="add_qobject")
#     def add_qobject(self, obj):
#         if obj is not None:
#             obj.destroyed.connect(self._handle_destroyed)
#             self.qobjects.append(obj)
#         print(self.qobjects[0].objectName())
#         print(self.qobjects)
#
#     def _handle_destroyed(self):
#         self._qobjects = [o for o in self.qobjects if shiboken2.isValid(o)]
