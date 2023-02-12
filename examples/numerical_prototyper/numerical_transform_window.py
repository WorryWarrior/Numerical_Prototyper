from qtpy import QtCore

import numerical_paths
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QPlainTextEdit, QAction, QToolBar
from qtpy.QtWidgets import QWidget


class TransformWindow(QWidget):

    def __init__(self, data=None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        self.title = 'Create Script'

        self.initUI()
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)

    def initUI(self):
        self.layout.addWidget(self.editor)
        self.setWindowTitle(self.title)

        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(12)
        self.editor.setFont(fixedFont)

        saveAction = QAction(QIcon(numerical_paths.save_file), "Save Script", self)
        saveAction.triggered.connect(lambda: self.saveScript())

        toolbar = QToolBar()
        toolbar.addAction(saveAction)
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

        self.layout.setMenuBar(toolbar)
        self.setLayout(self.layout)

        self.show()

    def saveScript(self):
        print("TODO")
