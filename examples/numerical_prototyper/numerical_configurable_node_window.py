from PyQt5.QtCore import Qt

from numerical_prototyper.numerical_node_customization_window_base import NodeCustomizationWindowBase
from qtpy import QtWidgets

INPUT_OUTPUT_MAX_COUNT = 5
INPUT_OUTPUT_TYPES = ['Number', 'Function', 'Matrix', 'Boolean', 'Complex Number']

class NumericalConfigurableNodeWindow(NodeCustomizationWindowBase):
    title = "Node Configuration Window"

    # valueParameterKey = '-Value'
    # variableNameParameterKey = '-VariableName'
    # variableWidthDimensionValueKey = '-Width'
    # variableHeightDimensionValueKey = '-Height'
    # variablePrintKey = '-PrintVariable'

    def __init__(self, parameters=None):
        super(NumericalConfigurableNodeWindow, self).__init__(parameters)

        self.matrixExists = False
        self.matrixInputs = []
        self.matrixValues = []

        if self.parameters is None:
            self.parameters = {
                # self.variableNameParameterKey: '',
                # self.valueParameterKey: '',
                # self.variableWidthDimensionValueKey: '',
                # self.variableHeightDimensionValueKey: '',
                # self.variablePrintKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.inputLayout = QtWidgets.QVBoxLayout()
        dialogWindow.inputLayout.setAlignment(Qt.AlignTop)

        dialogWindow.outputLayout = QtWidgets.QVBoxLayout()
        dialogWindow.outputLayout.setAlignment(Qt.AlignTop)

        dialogWindow.inputOutputLayout = QtWidgets.QHBoxLayout()
        dialogWindow.inputOutputLayout.addLayout(dialogWindow.inputLayout)
        dialogWindow.inputOutputLayout.addLayout(dialogWindow.outputLayout)

        dialogWindow.inputCountEdit = QtWidgets.QComboBox()
        for i in range(INPUT_OUTPUT_MAX_COUNT): dialogWindow.inputCountEdit.addItem(str(i))
        inputCountLabel = QtWidgets.QLabel('Input Node Number')
        self.addRow(dialogWindow, inputCountLabel, dialogWindow.inputCountEdit)

        dialogWindow.inputCountEdit.currentIndexChanged.connect(
            lambda: self.onInputCountChanged(dialogWindow)
        )

        dialogWindow.outputCountEdit = QtWidgets.QComboBox()
        for i in range(INPUT_OUTPUT_MAX_COUNT): dialogWindow.outputCountEdit.addItem(str(i))
        outputCountLabel = QtWidgets.QLabel('Output Node Number')
        self.addRow(dialogWindow, outputCountLabel, dialogWindow.outputCountEdit)

        dialogWindow.outputCountEdit.currentIndexChanged.connect(
            lambda: self.onOutputCountChanged(dialogWindow)
        )

        dialogWindow.content.addLayout(dialogWindow.inputOutputLayout)

        return dialogWindow

    def onInputCountChanged(self, dialogWindow):
        self.clearLayout(dialogWindow.inputLayout)
        for i in range(int(dialogWindow.inputCountEdit.currentIndex())):
            inputOption = QtWidgets.QComboBox()
            for j in range(len(INPUT_OUTPUT_TYPES)): inputOption.addItem(INPUT_OUTPUT_TYPES[j])
            inputOptionLayout = QtWidgets.QHBoxLayout()
            inputOptionLayout.addWidget(QtWidgets.QLabel(f'Input {i + 1}'))
            inputOptionLayout.addWidget(inputOption)
            inputOptionLayout.setAlignment(Qt.AlignLeft)
            dialogWindow.inputLayout.addLayout(inputOptionLayout)


    def onOutputCountChanged(self, dialogWindow):
        self.clearLayout(dialogWindow.outputLayout)
        for i in range(int(dialogWindow.outputCountEdit.currentIndex())):
            outputOption = QtWidgets.QComboBox()
            for j in range(len(INPUT_OUTPUT_TYPES)): outputOption.addItem(INPUT_OUTPUT_TYPES[j])
            outputOptionLayout = QtWidgets.QHBoxLayout()
            outputOptionLayout.addWidget(QtWidgets.QLabel(f'Output {i + 1}'))
            outputOptionLayout.addWidget(outputOption)
            outputOptionLayout.setAlignment(Qt.AlignLeft)
            dialogWindow.outputLayout.addLayout(outputOptionLayout)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def onMatrixDeleted(self, dialogWindow):
        self.parameters[self.valueParameterKey] = ''

        for matrixInput in self.matrixInputs:
            matrixInput.deleteLater()

        self.matrixInputs = []
        self.matrixExists = False

    def onMatrixDimensionChanged(self, dialogWindow, widthValue, heightValue):
        if self.matrixExists or widthValue == '' or heightValue == '':
            return

        width = int(widthValue)
        height = int(heightValue)

        grid = QtWidgets.QGridLayout()

        positions = [(i, j) for i in range(height) for j in range(width)]

        self.matrixInputs = []

        for position in positions:
            matrixFieldInput = QtWidgets.QLineEdit()

            self.matrixInputs.append(matrixFieldInput)

            grid.addWidget(matrixFieldInput, *position)

        dialogWindow.content.addLayout(grid)
        self.matrixExists = True

    def generateMatrixFields(self, dialogWindow):
        width = int(self.parameters[self.variableWidthDimensionValueKey])
        height = int(self.parameters[self.variableHeightDimensionValueKey])
        inputsValues = self.parameters[self.valueParameterKey]

        grid = QtWidgets.QGridLayout()

        positions = [(i, j) for i in range(height) for j in range(width)]

        self.matrixInputs = []

        for position in positions:
            matrixFieldInput = QtWidgets.QLineEdit()
            self.matrixInputs.append(matrixFieldInput)
            grid.addWidget(matrixFieldInput, *position)

        for i in range(len(inputsValues)):
            self.matrixInputs[i].setText(str(inputsValues[i]))

        dialogWindow.content.addLayout(grid)

    def getWindowDimensions(self) -> [int, int]:
        return [350, 350]

    def getMatrixAsList(self):
        res = []

        for matrixInput in self.matrixInputs:
            appendedText = matrixInput.text()
            if appendedText.strip() != '':
                res.append(matrixInput.text())
            else:
                res.append('0')

        return res

    def extractParameters(self, dialogWindow):
        newParameters = {
            # self.valueParameterKey: self.getMatrixAsList(),
            # self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            # self.variableWidthDimensionValueKey: dialogWindow.widthEdit.text(),
            # self.variableHeightDimensionValueKey: dialogWindow.heightEdit.text(),
            # self.variablePrintKey: dialogWindow.variablePrintBox.isChecked()
        }

        # addToSet(prompt)
        self.parameters.update(newParameters)
        return self.parameters
