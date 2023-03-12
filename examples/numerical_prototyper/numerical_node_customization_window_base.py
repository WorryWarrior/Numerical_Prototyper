from qtpy import QtWidgets, QtCore, QtGui

from numerical_prototyper.numerical_method_customization_widget import NumericalMethodCustomizationWidget, \
    NumericalMethodCustomizationCommandList, NumericalMethodCustomizationPreviewWidget

INT_32_MAX = 2147483647
VARIABLE_NAME_REGEX = "[a-zA-Z]+[a-zA-Z_0-9]*"
FUNCTION_ARGS_REGEX = "[a-zA-Z]+([,][a-zA-Z ]+)*"
DOUBLE_VALUE_REGEX = "-?[0-9]*.?[0-9]+"

variableSet = set()


class NodeCustomizationWindowBase:
    title = ''

    def __init__(self, parameters):
        self.parameters = parameters
        [self.windowWidth, self.windowHeight] = self.getWindowDimensions()

    def openWindow(self, acceptCallback = None):
        if self.parameters is None:
            return True

        dialogWindow = QtWidgets.QDialog()

        dialogWindow.applyBtn = QtWidgets.QPushButton('Apply')
        cancelBtn = QtWidgets.QPushButton('Cancel')

        dialogWindow.applyBtn.setMinimumWidth(90)
        cancelBtn.setMinimumWidth(90)

        dialogWindow.applyBtn.clicked.connect(dialogWindow.accept)
        cancelBtn.clicked.connect(dialogWindow.reject)

        dialogWindow.content = QtWidgets.QVBoxLayout()
        dialogWindow.content.setContentsMargins(20, 10, 20, 10)
        dialogWindow.content.setAlignment(QtCore.Qt.AlignTop)
        contentGroupBox = QtWidgets.QGroupBox("Parameters")
        contentGroupBox.setLayout(dialogWindow.content)

        buttonRow = QtWidgets.QHBoxLayout()
        buttonRow.addStretch(1)
        buttonRow.addWidget(dialogWindow.applyBtn)
        buttonRow.addWidget(cancelBtn)

        dialogWindow.mainVLayout = QtWidgets.QVBoxLayout()
        dialogWindow.mainVLayout.addWidget(contentGroupBox)

        dialogWindow.setFixedWidth(self.windowWidth)
        dialogWindow.setFixedHeight(self.windowHeight)
        dialogWindow.setLayout(dialogWindow.mainVLayout)
        dialogWindow.setWindowTitle(self.title)

        dialogWindow = self.dressWindow(dialogWindow)

        dialogWindow.mainVLayout.addLayout(buttonRow)

        accepted = dialogWindow.exec_()

        dialogWindow.close()

        if accepted:
            self.extractParameters(dialogWindow)
            if acceptCallback is not None:
                acceptCallback()
            # self.updateDescription()
        return accepted

    def getParameterValue(self, key):
        if key in self.parameters:
            return self.parameters[key]

        return None

    def dressWindow(self, dialogWindow):
        return dialogWindow

    def extractParameters(self, dialogWindow):
        pass

    def getWindowDimensions(self) -> [int, int]:
        return [350, 350]

    def addRow(self, prompt, *args):
        setWidthOnTypes = [QtWidgets.QLineEdit, QtWidgets.QComboBox, QtWidgets.QPushButton, QtWidgets.QSlider]

        row = QtWidgets.QHBoxLayout()

        for widget in args:
            if type(widget) in setWidthOnTypes:
                widget.setFixedWidth(150)

            row.addWidget(widget)
        prompt.content.addLayout(row)


class NumberInputNodeCustomizationWindow(NodeCustomizationWindowBase):
    title = "Number Input Node"

    valueParameterKey = '-Value'
    variableNameParameterKey = '-VariableName'
    variablePrintKey = '-PrintVariable'

    def __init__(self, parameters=None):
        super(NumberInputNodeCustomizationWindow, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.variableNameParameterKey: '',
                self.valueParameterKey: '',
                self.variablePrintKey: '',
            }

    def dressWindow(self, dialogWindow):
        
        dialogWindow.variableNameEdit = QtWidgets.QLineEdit()
        dialogWindow.variableNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.variableNameEdit.setText(str(self.parameters[self.variableNameParameterKey]))
        variableNameLabel = QtWidgets.QLabel('Variable Name ')
        self.addRow(dialogWindow, variableNameLabel, dialogWindow.variableNameEdit)

        dialogWindow.valueEdit = QtWidgets.QLineEdit()
        dialogWindow.valueEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(DOUBLE_VALUE_REGEX)))
        dialogWindow.valueEdit.setText(str(self.parameters[self.valueParameterKey]))
        valueLabel = QtWidgets.QLabel('Value ')
        self.addRow(dialogWindow, valueLabel, dialogWindow.valueEdit)

        dialogWindow.variablePrintBox = QtWidgets.QCheckBox()
        dialogWindow.variablePrintBox.setChecked(bool(self.parameters[self.variablePrintKey]))
        variablePrintLabel = QtWidgets.QLabel('Print Variable ')
        self.addRow(dialogWindow, variablePrintLabel, dialogWindow.variablePrintBox)

        return dialogWindow

    def extractParameters(self, dialogWindow):
        newParameters = {
            self.valueParameterKey: dialogWindow.valueEdit.text(),
            self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            self.variablePrintKey: dialogWindow.variablePrintBox.isChecked()
        }

        # addToSet(prompt)
        self.parameters.update(newParameters)

        return self.parameters


class FunctionInputNodeCustomizationWindow(NodeCustomizationWindowBase):
    title = "Function Input Node"

    valueParameterKey = '-Value'
    variableNameParameterKey = '-VariableName'
    variablePrintKey = '-PrintVariable'
    functionArgumentsKey = '-Args'

    def __init__(self, parameters=None):
        super(FunctionInputNodeCustomizationWindow, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.variableNameParameterKey: '',
                self.valueParameterKey: '',
                self.variablePrintKey: '',
                self.functionArgumentsKey: '',

            }

    def dressWindow(self, dialogWindow):
        dialogWindow.variableNameEdit = QtWidgets.QLineEdit()
        dialogWindow.variableNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.variableNameEdit.setText(str(self.parameters[self.variableNameParameterKey]))
        variableNameLabel = QtWidgets.QLabel('Function Name ')
        self.addRow(dialogWindow, variableNameLabel, dialogWindow.variableNameEdit)

        dialogWindow.functionArgumentEdit = QtWidgets.QLineEdit()
        dialogWindow.functionArgumentEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(FUNCTION_ARGS_REGEX)))
        dialogWindow.functionArgumentEdit.setText(str(self.parameters[self.functionArgumentsKey]))
        functionArgumentLabel = QtWidgets.QLabel('Function Arguments ')
        self.addRow(dialogWindow, functionArgumentLabel, dialogWindow.functionArgumentEdit)

        dialogWindow.valueEdit = QtWidgets.QLineEdit()
        dialogWindow.valueEdit.setText(str(self.parameters[self.valueParameterKey]))
        valueLabel = QtWidgets.QLabel('Value ')
        self.addRow(dialogWindow, valueLabel, dialogWindow.valueEdit)

        dialogWindow.variablePrintBox = QtWidgets.QCheckBox()
        dialogWindow.variablePrintBox.setChecked(bool(self.parameters[self.variablePrintKey]))
        variablePrintLabel = QtWidgets.QLabel('Print Function ')
        self.addRow(dialogWindow, variablePrintLabel, dialogWindow.variablePrintBox)

        return dialogWindow

    def extractParameters(self, dialogWindow):
        newParameters = {
            self.valueParameterKey: dialogWindow.valueEdit.text(),
            self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            self.variablePrintKey: dialogWindow.variablePrintBox.isChecked(),
            self.functionArgumentsKey: dialogWindow.functionArgumentEdit.text(),
        }

        # addToSet(prompt)
        self.parameters.update(newParameters)

        return self.parameters


class MatrixInputNodeCustomizationWindow(NodeCustomizationWindowBase):
    title = "Number Input Node"

    valueParameterKey = '-Value'
    variableNameParameterKey = '-VariableName'
    variableWidthDimensionValueKey = '-Width'
    variableHeightDimensionValueKey = '-Height'
    variablePrintKey = '-PrintVariable'

    def __init__(self, parameters=None):
        super(MatrixInputNodeCustomizationWindow, self).__init__(parameters)

        self.matrixExists = False
        self.matrixInputs = []
        self.matrixValues = []

        if self.parameters is None:
            self.parameters = {
                self.variableNameParameterKey: '',
                self.valueParameterKey: '',
                self.variableWidthDimensionValueKey: '',
                self.variableHeightDimensionValueKey: '',
                self.variablePrintKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.variableNameEdit = QtWidgets.QLineEdit()
        dialogWindow.variableNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.variableNameEdit.setText(str(self.parameters[self.variableNameParameterKey]))
        variableNameLabel = QtWidgets.QLabel('Variable Name ')
        self.addRow(dialogWindow, variableNameLabel, dialogWindow.variableNameEdit)

        dialogWindow.widthEdit = QtWidgets.QLineEdit()
        dialogWindow.widthEdit.setValidator(QtGui.QIntValidator(1, 9))
        dialogWindow.widthEdit.setText(str(self.parameters[self.variableWidthDimensionValueKey]))
        testLabel = QtWidgets.QLabel('Width ')
        self.addRow(dialogWindow, testLabel, dialogWindow.widthEdit)

        dialogWindow.heightEdit = QtWidgets.QLineEdit()
        dialogWindow.heightEdit.setValidator(QtGui.QIntValidator(1, 9))
        dialogWindow.heightEdit.setText(str(self.parameters[self.variableHeightDimensionValueKey]))
        testLabelTwo = QtWidgets.QLabel('Height ')
        self.addRow(dialogWindow, testLabelTwo, dialogWindow.heightEdit)

        dialogWindow.generateMatrixButton = QtWidgets.QPushButton("Generate matrix")
        dialogWindow.generateMatrixButton.pressed.connect(
            lambda: self.onMatrixDimensionChanged(dialogWindow, dialogWindow.widthEdit.text(),
                                                  dialogWindow.heightEdit.text())
        )

        dialogWindow.deleteMatrixButton = QtWidgets.QPushButton("Delete matrix")
        dialogWindow.deleteMatrixButton.pressed.connect(
            lambda: self.onMatrixDeleted(dialogWindow)
        )

        self.addRow(dialogWindow, dialogWindow.generateMatrixButton, dialogWindow.deleteMatrixButton)

        dialogWindow.variablePrintBox = QtWidgets.QCheckBox()
        dialogWindow.variablePrintBox.setChecked(bool(self.parameters[self.variablePrintKey]))
        variablePrintLabel = QtWidgets.QLabel('Print Variable ')
        self.addRow(dialogWindow, variablePrintLabel, dialogWindow.variablePrintBox)

        if len(self.parameters[self.valueParameterKey]) > 0:
            self.generateMatrixFields(dialogWindow)
            self.matrixExists = True

        return dialogWindow

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
            matrixFieldInput.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(DOUBLE_VALUE_REGEX)))

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
            matrixFieldInput.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(DOUBLE_VALUE_REGEX)))
            self.matrixInputs.append(matrixFieldInput)
            grid.addWidget(matrixFieldInput, *position)

        for i in range(len(inputsValues)):
            self.matrixInputs[i].setText(str(inputsValues[i]))

        dialogWindow.content.addLayout(grid)

    def getWindowDimensions(self) -> [int, int]:
        return [450, 450]

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
            self.valueParameterKey: self.getMatrixAsList(),
            self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            self.variableWidthDimensionValueKey: dialogWindow.widthEdit.text(),
            self.variableHeightDimensionValueKey: dialogWindow.heightEdit.text(),
            self.variablePrintKey: dialogWindow.variablePrintBox.isChecked()
        }

        # addToSet(prompt)
        self.parameters.update(newParameters)
        print(newParameters[self.valueParameterKey])
        return self.parameters


class EvaluateFunctionNodeCustomizationWindow(NodeCustomizationWindowBase):
    title = "Evaluate Function Node"

    variableNameParameterKey = '-VariableName'
    useVariableKey = '-UseVariable'
    printOutputKey = '-PrintOutput'

    def __init__(self, parameters=None):
        super(EvaluateFunctionNodeCustomizationWindow, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.variableNameParameterKey: '',
                self.useVariableKey: '',
                self.printOutputKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.useVariableBox = QtWidgets.QCheckBox()
        dialogWindow.useVariableBox.setChecked(bool(self.parameters[self.useVariableKey]))
        variablePrintLabel = QtWidgets.QLabel('Use Variable ')
        self.addRow(dialogWindow, variablePrintLabel, dialogWindow.useVariableBox)

        dialogWindow.variableNameEdit = QtWidgets.QLineEdit()
        dialogWindow.variableNameEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.variableNameEdit.setText(str(self.parameters[self.variableNameParameterKey]))
        variableNameLabel = QtWidgets.QLabel('Variable Name ')
        self.addRow(dialogWindow, variableNameLabel, dialogWindow.variableNameEdit)

        dialogWindow.printOutputBox = QtWidgets.QCheckBox()
        dialogWindow.printOutputBox.setChecked(bool(self.parameters[self.printOutputKey]))
        printOutputLabel = QtWidgets.QLabel('Print Output ')
        self.addRow(dialogWindow, printOutputLabel, dialogWindow.printOutputBox)

        return dialogWindow

    def extractParameters(self, dialogWindow):
        newParameters = {
            self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            self.useVariableKey: dialogWindow.useVariableBox.isChecked(),
            self.printOutputKey: dialogWindow.printOutputBox.isChecked(),
        }

        # addToSet(prompt)
        self.parameters.update(newParameters)

        return self.parameters


class FunctionZeroSearchNodeCustomizationWindow(NodeCustomizationWindowBase):
    title = "Function Zero Search"

    def __init__(self, inputs, outputs, parameters=None):
        super(FunctionZeroSearchNodeCustomizationWindow, self).__init__(parameters)

        self.inputs = inputs
        self.outputs = outputs

        if self.parameters is None:
            self.parameters = {

            }

    def getWindowDimensions(self) -> [int, int]:
        return [1000, 800]

    def dressWindow(self, dialogWindow):
        functionNameInput = QtWidgets.QLineEdit()
        functionNameInput.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))


        testLayout = QtWidgets.QHBoxLayout()
        testPreviewWidget = NumericalMethodCustomizationPreviewWidget(self.inputs, self.outputs, functionNameInput)
        testPreviewWidget.setReadOnly(True)
        testListWidget = NumericalMethodCustomizationCommandList(testPreviewWidget)
        testListWidgetTwo = NumericalMethodCustomizationWidget(parent=testListWidget)

        functionNameInput.textChanged.connect(testListWidget.changePreviewText)

        testLayout.addWidget(testPreviewWidget)
        testLayout.addWidget(testListWidget)
        testLayout.addWidget(testListWidgetTwo)

        testListWidgetTwo.initUI()

        self.addRow(dialogWindow, QtWidgets.QLabel('Method Name '), functionNameInput)
        dialogWindow.content.addLayout(testLayout)

        return dialogWindow
