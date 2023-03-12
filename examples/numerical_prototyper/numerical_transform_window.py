import json

from qtpy import QtCore

import numerical_paths
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QPlainTextEdit, QAction, QToolBar
from qtpy.QtWidgets import QWidget

from treelib import Tree

from numerical_prototyper.intermediate_representation.numerical_edge_ir import EdgeIR
from numerical_prototyper.intermediate_representation.numerical_node_ir import NodeIR


class TransformWindow(QWidget):

    def __init__(self, data=None):
        super().__init__()
        self.layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        self.title = 'Create Script'

        self.script = ''
        self.convertToScript(data)

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

    def convertToScript(self, data):
        deserializedData = json.loads(data)
        [nodeIRs, edgeIRs] = self.deserialize(deserializedData)

        [isValid, nodeTree] = self.buildNodeTree(nodeIRs, edgeIRs)

        if not isValid:
            self.script = "Missing Output Node"
            self.editor.appendPlainText(self.script)
            return

        test = []
        for treeNode in nodeTree.expand_tree(mode=nodeTree.ZIGZAG):
            #print(self.getNodeByID(treeNode, nodeIRs).nodeName)
            test.append(treeNode)
            """
            nodeScriptRepresentation = self.getNodeByID(treeNode, nodeIRs).scriptRep
            if nodeScriptRepresentation is not None:
                self.addToScript(str(nodeScriptRepresentation))
                self.addNewLineToScript()
            """

        test.reverse()

        for treeNodeTest in test:
            nodeScriptRepresentation = self.getNodeByID(treeNodeTest, nodeIRs).scriptRep

            if nodeScriptRepresentation is not None:
                self.addToScript(str(nodeScriptRepresentation))
                self.addNewLineToScript()


        """
        for treeNode in nodeTree.expand_tree():
            nodeScriptRepresentation = self.getNodeByID(treeNode, nodeIRs).scriptRep

            if nodeScriptRepresentation is not None:
                self.addToScript(str(nodeScriptRepresentation))
                self.addNewLineToScript()
        """
            #print(self.getNodeByID(test, nodeIRs).nodeName)

        #nodeTree.show()

        self.editor.appendPlainText(self.script)

    def deserialize(self, data: dict, hashmap: dict = {}, restore_id: bool = True, *args, **kwargs):
        nodeIRs = []
        edgeIRs = []

        for node_data in data['nodes']:
            nodeIRs.append(NodeIR(
                nodeID=node_data['id'],
                nodeName=node_data['title'],
                inputIDs=self.getSocketIDs(node_data['inputs']),
                outputIDs=self.getSocketIDs(node_data['outputs']),
                scriptRep=node_data['script_rep']
            ))
            #self.addToScript(str(node_data))
            #self.addNewLineToScript()
            #self.addNewLineToScript()

        for edge_data in data['edges']:
            edgeIRs.append(EdgeIR(
                startID=edge_data['start'],
                endID=edge_data['end']
            ))
            #self.addToScript(str(edge_data))
            #self.addNewLineToScript()
            #self.addNewLineToScript()

        return [nodeIRs, edgeIRs]

    def getSocketIDs(self, socket_data):
        res = []

        for data in socket_data:
            res.append(data['id'])

        return res

    def buildNodeTree(self, nodeData: list, edgeData: list):
        nodeTree = Tree()
        # nodeDataCopy = nodeData
        detectedOutput = False

        for node in nodeData:
            if node.nodeName == "Output":
                nodeTree.create_node("Output", node.nodeID)
                # nodeDataCopy.remove(node)
                detectedOutput = True

        if not detectedOutput:
            return [False, None]

        treeConnections = []

        for edge in edgeData:
            [aa, bb] = self.getEdgeNodesByID(edge.startID, edge.endID, nodeData)
            treeConnections.append([aa, bb])

        emergencyCounter = 0

        while len(treeConnections) > 0 and emergencyCounter < 200:
            for treeConnection in treeConnections:
                if self.isNodeRegisteredInTree(nodeTree, treeConnection[0].nodeID):
                    nodeTree.create_node(treeConnection[1].nodeName, treeConnection[1].nodeID,
                                         parent=treeConnection[0].nodeID)
                    treeConnections.remove(treeConnection)
                else:
                    emergencyCounter += 1
                    continue

        return [True, nodeTree]

    def isNodeRegisteredInTree(self, tree: Tree, nodeID: int) -> bool:
        #print("Looking for node called " + nodeName)

        for treeNode in tree.nodes:
            #print(str(treeNode._get_identifier))
            if treeNode == nodeID:
                return True

        return False

    def getEdgeNodesByID(self, startNodeID, endNodeID, nodeData):
        startNodeName = None
        endNodeName = None

        for node in nodeData:
            for inputID in node.inputIDs:
                if inputID == endNodeID:
                    startNodeName = node
                    # startNodeName = node.nodeName
                    break

        for node in nodeData:
            for outputID in node.outputIDs:
                if outputID == startNodeID:
                    endNodeName = node
                    # endNodeName = node.nodeName
                    break

        return [startNodeName, endNodeName]

    def getNodeByID(self, targetNodeID, nodeData):
        for node in nodeData:
            if node.nodeID == targetNodeID:
                return node

        return None
    def addToScript(self, text):
        self.script += " " + text

    def addNewLineToScript(self):
        self.script += "\n"

    def saveScript(self):
        print("TODO")
