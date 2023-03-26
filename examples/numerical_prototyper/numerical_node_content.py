from PyQt5 import QtWidgets, QtGui, QtCore
from qtpy.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from nodeeditor.node_content_widget import QDMNodeContentWidget

DOUBLE_VALUE_REGEX = "-?[0-9]*.?[0-9]+"


class NumericalContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class EvaluateFunctionContent(QDMNodeContentWidget):

    def initUI(self):
        self.edit = QtWidgets.QLineEdit("", self)
        self.edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(DOUBLE_VALUE_REGEX)))
        self.edit.setAlignment(Qt.AlignRight)
        self.edit.setObjectName(self.node.content_label_objname)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            pass
            # dumpException(e)
        return res