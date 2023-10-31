# logger
from ..utils.logger import Logger

# pyqt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor

from ..recordings.config import UI_CODE_ERROR

import traceback
import re

REMAIN_COLOR = '#333333'
PATH_COLOR = '#1f77b4'
CODE_COLOR = '#33a02c'
EXCEPTION_COLOR = '#e31a1c'


class CodeErrorUi(QtWidgets.QDialog):
    def __init__(self):
        super(CodeErrorUi, self).__init__()
        uic.loadUi(UI_CODE_ERROR, self)

        self.errorText.clear()
        self.errorText.setTextColor(QColor(REMAIN_COLOR))
        self.highlight_traceback(str(traceback.format_exc()))

        self.showMaximized()

    def highlight_traceback(self, traceback_msg):
        path_pattern = re.compile(r'File ".*?"')
        code_pattern = re.compile(r'(?<=line )\d+')
        exception_pattern = re.compile(r'\b\w+Error\b')

        self.errorText.append(traceback_msg)

        path_format = QTextCharFormat()
        path_format.setForeground(QColor(PATH_COLOR))

        code_format = QTextCharFormat()
        code_format.setForeground(QColor(CODE_COLOR))

        exception_format = QTextCharFormat()
        exception_format.setForeground(QColor(EXCEPTION_COLOR))

        cursor = self.errorText.textCursor()

        for match in path_pattern.finditer(traceback_msg):
            cursor.setPosition(match.start())
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(match.group()))
            cursor.setCharFormat(path_format)

        for match in code_pattern.finditer(traceback_msg):
            cursor.setPosition(match.start())
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(match.group()))
            cursor.setCharFormat(code_format)

        for match in exception_pattern.finditer(traceback_msg):
            cursor.setPosition(match.start())
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(match.group()))
            cursor.setCharFormat(exception_format)

    @classmethod
    def show_exception(cls):
        ui = CodeErrorUi()
        ui.exec_()

