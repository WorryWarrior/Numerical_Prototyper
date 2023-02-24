import json

from nodeeditor.utils import loadStylesheets

import numerical_paths
from numerical_transform_window import TransformWindow
from numerical_sub_window import NumericalSubWindow
from qtpy import QtGui, QtCore
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDockWidget, QAction
from nodeeditor.node_editor_window import NodeEditorWindow
from numerical_drag_listbox import QDMDragListbox

from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node,
    edge_cannot_connect_input_and_output_of_different_type
)

# Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_different_type)


class NumericalWindow(NodeEditorWindow):

    def initUI(self):
        loadStylesheets(numerical_paths.editor_stylesheet_file)

        self.setWindowTitle("Numerical Analysis Prototyper")
        self.nodeeditor = self.__class__.NodeEditorWidget_class(self)
        self.nodeeditor.scene.addHasBeenModifiedListener(self.setTitle)
        self.setCentralWidget(self.nodeeditor)

        self.nodeEditorSubwindow = NumericalSubWindow()
        self.setCentralWidget(self.nodeEditorSubwindow)

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createTransformButton()

        # self.showMaximized()

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
        a = json.dumps(self.nodeEditorSubwindow.scene.serialize(), indent=4)
        self.converter = TransformWindow(a)
        self.converter.show()
