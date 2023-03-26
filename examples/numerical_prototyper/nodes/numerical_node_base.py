from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_node import Node
from nodeeditor.node_graphics_node import QDMGraphicsNode
from numerical_prototyper.numerical_node_content import NumericalContent


class NumericalGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self._title_font = QFont("Ubuntu", 8)


class NumericalNode(Node):
    op_code = 0
    op_title = "---"
    content_label = ""
    content_label_objname = "numerical_node_label"

    GraphicsNode_class = NumericalGraphicsNode
    NodeContent_class = NumericalContent

    def __init__(self, scene, inputs=[2, 1], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.markDirty()

    def getScriptRepresentation(self) -> str: pass

    def debugOutputs(self):
        for nodeOutput in self.nodeOutputs:
            print(nodeOutput)

    def serialize(self):
        res = super().serialize()
        res['script_rep'] = self.getScriptRepresentation()
        return res

    def deserialize(self, data, hashmap={}, restore_id=True) :
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
