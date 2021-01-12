import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFontMetrics, QPainter, QColor, QTextFormat
from PyQt5.QtWidgets import QTextEdit, QPlainTextEdit
from GUI.LineNumberArea import LineNumberArea


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)
        self.connect_signals_to_slots()
        self.updateLineNumberAreaWidth(0)

    def connect_signals_to_slots(self):
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def lineNumberAreaWidth(self):
        """ This method has been slightly modified (use of log and uses actual
        font rather than standart.) """
        n_lines = self.blockCount()
        digits = np.ceil(np.log10(n_lines)) + 1
        return digits * QFontMetrics(self.font()).width('9') + 3

    def updateLineNumberAreaWidth(self, _):
        # print('CodeEditor.updateLineNumberAreaWidth: margin = {}'.format(self.lineNumberAreaWidth()))
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        # print('CodeEditor.updateLineNumberArea: rect = {}, dy = {}'.format(rect, dy))

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        # print('CodeEditor.updateLineNumberArea: rect.contains(self.viewport().rect()) = {}'.format(
        #     rect.contains(self.viewport().rect())))
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))
        # self.lineNumberAreaPaintEvent(event)

    def lineNumberAreaPaintEvent(self, event):
        # print('CodeEditor.lineNumberAreaPaintEvent')
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = QFontMetrics(self.font()).height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)
