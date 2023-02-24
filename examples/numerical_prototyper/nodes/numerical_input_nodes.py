from PyQt5.QtWidgets import QLabel

from nodeeditor.node_content_widget import QDMNodeContentWidget

#from numerical_prototyper.nodes.numerical_node_base import NumericalNode, NumericalGraphicsNode
#from numerical_prototyper.numerical_conf import register_numeric_node, NUM_NODE_OUTPUT
# from numerical_prototyper.numerical_conf import NUM_NODE_OUTPUT, register_numeric_node
#from numerical_prototyper.numerical_node_customization_window_base import InputNodeCustomizationWindow


class TestNumericalInputNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.valueLabel = QLabel("", self)
        self.valueLabel.setObjectName(self.node.content_label_objname)



