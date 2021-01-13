from pathlib import Path
from sys import platform
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QAction, QMenu, QMenuBar, QComboBox, \
    QPushButton, QMessageBox, QFileDialog
from Converter.CFG import CFG, showDialog
from Converter.ChomskyNF import ChomskyNF
from Converter.GenericNF import GenericNF
from Converter.GreibachNF import GreibachNF
from GUI.CodeEditor import CodeEditor
from GUI.ScrollLabel import ScrollLabel


class GUI(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs)
        self.grammer = CFG()
        self.menuBar = QMenuBar()
        self.form_widget = QWidget(self)
        self.grid_layout = QGridLayout(self.parentWidget())
        self.code_Editor = CodeEditor()
        self.combo_box = QComboBox()
        self.NF_button = QPushButton('is in NF')
        self.NF_button.clicked.connect(self.on_nf_clicked)
        self.convert_button = QPushButton('Convert')
        self.convert_button.clicked.connect(self.on_convert_clicked)
        self.simplify_button = QPushButton('Simplify')
        self.simplify_button.clicked.connect(self.on_simplify_button_clicked)
        self.result_scrolable_label = ScrollLabel()
        self.form_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.form_widget)
        self.init_menu_bar()
        self.init_gridlayout_items()
        self.init_comboBox()
        self.setWindowTitle("CFG Converter")

    def on_nf_clicked(self):
        if not self.code_Editor.is_input_available():
            showDialog(QMessageBox.Critical, 'there is no input')
            return
        self.grammer.loadFrom(self.code_Editor.toPlainText().splitlines())
        if self.combo_box.currentIndex() == 1:
            is_chomsky = ChomskyNF().isInNF(self.grammer)
            showDialog(QMessageBox.Information if is_chomsky else QMessageBox.Critical,
                       "It is already in Chomsky form" if is_chomsky else "It is  not in Chomsky form")
        else:
            is_grei = GreibachNF().isInNF(self.grammer)
            showDialog(QMessageBox.Information if is_grei else QMessageBox.Critical,
                       "It is already in Greibach form" if is_grei else "It is  not in greibach form")

    def on_convert_clicked(self):
        if not self.code_Editor.is_input_available():
            showDialog(QMessageBox.Critical, 'there is no input')
            return
        if self.combo_box.currentIndex() == 1:
            if not ChomskyNF().isInNF(self.grammer):
                self.result_scrolable_label.setText(ChomskyNF().convertToNF(self.grammer).__str__())
            else:
                showDialog(QMessageBox.Information, "It is already in Chomsky form")
        else:
            if not GreibachNF().isInNF(self.grammer):
                self.result_scrolable_label.setText(GreibachNF().convertToNF(self.grammer).__str__())
            else:
                showDialog(QMessageBox.Information, "It is already in Greibach form")

    def on_simplify_button_clicked(self):
        if not self.code_Editor.is_input_available():
            showDialog(QMessageBox.Critical, 'there is no input')
            return
        self.grammer.loadFrom(self.code_Editor.toPlainText().splitlines())
        self.result_scrolable_label.setText(GenericNF().simplifyCFG(self.grammer).__str__())

    def resizeEvent(self, event):
        self.result_scrolable_label.setMaximumHeight(event.size().height() * 1 / 5)

    def init_menu_bar(self):
        if platform == "darwin":
            self.menuBar.setNativeMenuBar(True)

        fileMenu = QMenu("&File", self)

        impAct = QAction('Import from file', self)
        impAct.triggered.connect(self.load_from_file_dialog)
        expAct = QAction('Export result to file', self)
        expAct.triggered.connect(self.export_Result)

        fileMenu.addAction(impAct)
        fileMenu.addAction(expAct)
        self.menuBar.addMenu(fileMenu)
        self.setMenuBar(self.menuBar)
        # self.menuBar.show()

    def load_from_file_dialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0]:
            f = open(filename[0], 'r')
            try:
                with f:
                    data = f.readlines()
                    self.code_Editor.setPlainText(''.join(data))
            finally:
                f.close()

    def init_comboBox(self):
        self.combo_box.addItems(['GreiBach', 'Chomsky'])

    def init_gridlayout_items(self):
        self.grid_layout.addWidget(self.combo_box, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.NF_button, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.convert_button, 0, 2, 1, 1)
        self.grid_layout.addWidget(self.simplify_button, 0, 3, 1, 1)
        self.grid_layout.addWidget(self.code_Editor, 1, 0, 1, 4)
        self.grid_layout.addWidget(self.result_scrolable_label, 2, 0, -1, 4)

    def export_Result(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)")
        my_file = Path(fileName)
        if my_file.is_file():
            file = open(fileName, 'w')
            try:
                with file:
                    if self.result_scrolable_label.get_text() and self.code_Editor.toPlainText():
                        file.write('input:\n\n' + self.result_scrolable_label.get_text() + '\n\n' +
                                   'output:\n\n' + self.code_Editor.toPlainText())
                    else:
                        showDialog(QMessageBox.Information, 'there is no result or input to save')
            finally:
                file.close()
