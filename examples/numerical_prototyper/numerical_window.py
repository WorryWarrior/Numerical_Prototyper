from nodeeditor.utils import loadStylesheets

import numerical_paths
from numerical_transform_window import TransformWindow
from numerical_sub_window import NumericalSubWindow
from qtpy import QtGui, QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDockWidget, QAction
from nodeeditor.node_editor_window import NodeEditorWindow
from numerical_drag_listbox import QDMDragListbox


class NumericalWindow(NodeEditorWindow):

    def initUI(self):
        loadStylesheets(numerical_paths.editor_stylesheet_file)

        self.setWindowTitle("Numerical Analysis Prototyper")
        self.nodeeditor = self.__class__.NodeEditorWidget_class(self)
        self.nodeeditor.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.nodeeditor)

        self.test = NumericalSubWindow()
        self.setCentralWidget(self.test)

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createTransformButton()


    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createMenus(self):
        super().createMenus()

    def createActions(self):
        super().createActions()

    def createTransformButton(self):
        toolbar = self.addToolBar("MainToolbar")
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        transformAction = QAction(QtGui.QIcon(numerical_paths.run_app), 'Create Script', self)
        transformAction.triggered.connect(lambda: self.createScript())
        toolbar.addAction(transformAction)

    def createScript(self):
        self.converter = TransformWindow()
        self.converter.show()
