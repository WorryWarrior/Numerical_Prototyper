from PyQt5.QtWidgets import QLabel

from nodeeditor.node_content_widget import QDMNodeContentWidget


class TestNumericalInputNodeContent(QDMNodeContentWidget):
    def initUI(self):
        self.valueLabel = QLabel("", self)
        self.valueLabel.setObjectName(self.node.content_label_objname)



