from qtpy import QtWidgets, QtCore, QtGui

INT_32_MAX = 2147483647
VARIABLE_NAME_REGEX = "[a-zA-Z]+[a-zA-Z_0-9]*"
FUNCTION_ARGS_REGEX = "[a-zA-Z]+([,][a-zA-Z ]+)*"
DOUBLE_VALUE_REGEX = "-?[0-9]*.?[0-9]+"


class NodeCustomizationWindowBase:
    title = ''

    def __init__(self, parameters):
        self.parameters = parameters

    def openWindow(self):
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

        dialogWindow.setFixedWidth(350)
        dialogWindow.setFixedHeight(350)
        dialogWindow.setLayout(dialogWindow.mainVLayout)
        dialogWindow.setWindowTitle(self.title)

        dialogWindow = self.dressWindow(dialogWindow)

        dialogWindow.mainVLayout.addLayout(buttonRow)

        accepted = dialogWindow.exec_()

        dialogWindow.close()

        if accepted:
            self.extractParameters(dialogWindow)
            #self.updateDescription()
        return accepted

    def getParameterValue(self, key):
        if key in self.parameters:
            return self.parameters[key]

        return None

    def dressWindow(self, dialogWindow):
        return dialogWindow

    def extractParameters(self, dialogWindow):
        pass

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

        #addToSet(prompt)
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

        #addToSet(prompt)
        self.parameters.update(newParameters)

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
        dialogWindow.printOutputBox.setChecked(bool(self.parameters[self.useVariableKey]))
        printOutputLabel = QtWidgets.QLabel('Print Output ')
        self.addRow(dialogWindow, printOutputLabel, dialogWindow.printOutputBox)

        return dialogWindow

    def extractParameters(self, dialogWindow):
        newParameters = {
            self.variableNameParameterKey: dialogWindow.variableNameEdit.text(),
            self.useVariableKey: dialogWindow.useVariableBox.isChecked(),
            self.printOutputKey: dialogWindow.printOutputBox.isChecked(),
                         }

        #addToSet(prompt)
        self.parameters.update(newParameters)

        return self.parameters