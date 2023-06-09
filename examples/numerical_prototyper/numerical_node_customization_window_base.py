import json
from copy import deepcopy

from PyQt5.QtWidgets import QAction
from qtpy import QtWidgets, QtCore, QtGui

from numerical_prototyper import numerical_global, numerical_paths
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

    def openWindow(self, acceptCallback=None):
        if self.parameters is None:
            return True

        dialogWindow = QtWidgets.QDialog()

        dialogWindow.applyBtn = QtWidgets.QPushButton('Apply')
        cancelBtn = QtWidgets.QPushButton('Cancel')

        dialogWindow.applyBtn.setMinimumWidth(90)
        cancelBtn.setMinimumWidth(90)

        # dialogWindow.applyBtn.clicked.connect(dialogWindow.accept)
        dialogWindow.applyBtn.clicked.connect(lambda: self.onApplyButtonPressed(dialogWindow))
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

    def onApplyButtonPressed(self, dialogWindow):
        return dialogWindow.accept()

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
    title = "Matrix Input Node"

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
    title = "Configurable Logic Node"

    functionNameKey = "-FunctionName"
    stateKey = "-State"

    def __init__(self, inputs, outputs, parameters=None):
        super(FunctionZeroSearchNodeCustomizationWindow, self).__init__(parameters)

        self.inputs = inputs
        self.outputs = outputs
        self.declarationText = ''
        self.callText = ''
        self.previewWidget = None

        if self.parameters is None:
            self.parameters = {
                self.functionNameKey: '',
                self.stateKey: '',
            }

    def getWindowDimensions(self) -> [int, int]:
        return [1000, 800]

    def dressWindow(self, dialogWindow):
        dialogWindow.functionNameInput = QtWidgets.QLineEdit()
        dialogWindow.functionNameInput.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.functionNameInput.setText(str(self.parameters[self.functionNameKey]))

        testLayout = QtWidgets.QHBoxLayout()
        previewWidget = NumericalMethodCustomizationPreviewWidget(self.inputs, self.outputs,
                                                                  dialogWindow.functionNameInput)
        previewWidget.setReadOnly(True)
        self.previewWidget = previewWidget
        dialogWindow.commandListWidget = NumericalMethodCustomizationCommandList(previewWidget)
        commandTabWidget = NumericalMethodCustomizationWidget(parent=dialogWindow.commandListWidget)

        dialogWindow.functionNameInput.textChanged.connect(dialogWindow.commandListWidget.changePreviewText)
        dialogWindow.functionNameInput.textChanged.connect(lambda: self.updateCallText(dialogWindow))
        previewWidget.textChanged.connect(self.updateDeclarationText)

        testLayout.addWidget(previewWidget)
        testLayout.addWidget(dialogWindow.commandListWidget)
        testLayout.addWidget(commandTabWidget)

        commandTabWidget.initUI()

        dialogWindow.commandListWidget.loadData(self.parameters[self.stateKey])

        self.addRow(dialogWindow, QtWidgets.QLabel('Method Name '), dialogWindow.functionNameInput)
        dialogWindow.content.addLayout(testLayout)

        menuBar = QtWidgets.QMenuBar(dialogWindow)
        fileMenu = menuBar.addMenu('&File')
        loadAction = QtWidgets.QAction('&Load', fileMenu,
                                       triggered=lambda: self.loadListWidget(dialogWindow.commandListWidget))
        saveAction = QtWidgets.QAction('&Save', fileMenu,
                                       triggered=lambda: self.saveListWidget(dialogWindow.commandListWidget))
        saveAsBlockAction = QtWidgets.QAction('&Save as Block', fileMenu,
                                              triggered=lambda: self.saveListWidgetAsBlock(
                                                  dialogWindow.commandListWidget))

        fileMenu.addAction(loadAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsBlockAction)
        menuBar.show()

        return dialogWindow

    def updateDeclarationText(self):
        self.declarationText = self.previewWidget.toPlainText()

    def updateCallText(self, dialogWindow):
        res = ''
        res += f'{dialogWindow.functionNameInput.text()}('

        for i in range(len(self.inputs)):
            res += f'input_{i}'

            if i != len(self.inputs) - 1:
                res += ', '

        res += ')'

        self.callText = res

    def getCallText(self, args):
        res = self.callText

        for i in range(len(args)):
            res = res.replace(f'input_{i}', args[i])

        return res

    def extractParameters(self, dialogWindow):
        newParameters = {
            self.functionNameKey: dialogWindow.functionNameInput.text(),
            self.stateKey: dialogWindow.commandListWidget.getSaveData(),
        }

        self.parameters.update(newParameters)

        return self.parameters

    def loadListWidget(self, listWidget):
        reply = QtWidgets.QMessageBox.question(listWidget, 'Warning',
                                               "Continue?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No |
                                               QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
        if reply != QtWidgets.QMessageBox.Yes:
            return False

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=listWidget,
                                                            caption="Load method logic",
                                                            filter="Method Logic (*.logic)",
                                                            directory=numerical_paths.saveDirectory)
        if filename == "":
            return False

        try:
            loadData = json.load(open(filename))
        except IOError:
            return

        listWidget.loadData(deepcopy(loadData))

    def saveListWidget(self, listWidget):
        numerical_global.ensurePathExists(numerical_paths.saveDirectory)
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=listWidget,
                                                            caption="Save method logic",
                                                            filter="Method Logic (*.logic)",
                                                            directory=numerical_paths.saveDirectory)
        if filename == "":
            return False

        saveData = listWidget.getSaveData()
        json.dump(saveData, open(filename, 'w'), sort_keys=False, indent=3, separators=(',', ': '))

    def saveListWidgetAsBlock(self, listWidget):
        numerical_global.ensurePathExists(numerical_paths.saveDirectory)
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=listWidget,
                                                            caption="Save method logic as block",
                                                            filter="Method Logic (*.block)",
                                                            directory=numerical_paths.saveDirectory)
        if filename == "":
            return False

        saveData = listWidget.getSaveTextData()
        json.dump(saveData, open(filename, 'w'), sort_keys=False, indent=3, separators=(',', ': '))