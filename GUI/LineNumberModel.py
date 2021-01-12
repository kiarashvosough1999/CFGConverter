from PyQt5.QtCore import QAbstractListModel, Qt, pyqtSignal, pyqtSlot, QModelIndex


class LineNumberModel(QAbstractListModel):
    IndexRole = Qt.UserRole + 1
    personChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.indexx = 1

    @pyqtSlot(int, int, name="data", result="QString")
    def data(self, index, role=Qt.DisplayRole):
        if role == LineNumberModel.IndexRole:
            return self.indexx.__str__()

    def rowCount(self, parent=QModelIndex()):
        return self.indexx

    def roleNames(self):
        return {
            LineNumberModel.IndexRole: b'index'
        }

    @pyqtSlot(int, name="change_line_count")
    def change_line_count(self, count):
        if count > self.indexx:
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.indexx = count
            self.endInsertRows()
