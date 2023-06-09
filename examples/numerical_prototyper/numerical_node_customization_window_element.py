import json

from qtpy import QtWidgets, QtCore, QtGui

import numerical_prototyper.numerical_paths
from numerical_prototyper.numerical_node_customization_window_base import NodeCustomizationWindowBase, \
    VARIABLE_NAME_REGEX


class NumericalCustomizationWindowElementBase(NodeCustomizationWindowBase):
    icon = ''
    description = ''
    textValue = ''

    def dressWidget(self, newWidget):
        newWidget.setTitle(self.title)
        newWidget.setDescription(self.description)
        # newWidget.setIcon(self.icon)
        return newWidget

    def loadTextValue(self):
        pass

    def getSaveData(self):
        commandSave = {'type': self.__class__.__name__,
                       'parameters': self.parameters}
        return commandSave


class IfElement(NumericalCustomizationWindowElementBase):
    title = 'if'
    icon = ''
    textValue = 'if'

    conditionLeftValueKey = '-ConditionLeftValue'
    conditionRightValueKey = '-ConditionRightValue'
    conditionSignKey = '-ConditionSignKey'
    conditionTypeKey = '-ConditionType'

    conditionSigns = ['==', '~=', '>', '>=', '<', '<=']

    def __init__(self, parameters=None):
        super(IfElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.conditionLeftValueKey: '',
                self.conditionRightValueKey: '',
                self.conditionSignKey: 0,
                self.conditionTypeKey: 0,
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.conditionLeftValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionLeftValueEdit.setText(str(self.parameters[self.conditionLeftValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Left Value'), dialogWindow.conditionLeftValueEdit)

        dialogWindow.conditionSignEdit = QtWidgets.QComboBox()
        dialogWindow.conditionSignEdit.addItem('Equal')
        dialogWindow.conditionSignEdit.addItem('Not Equal')
        dialogWindow.conditionSignEdit.addItem('Greater than')
        dialogWindow.conditionSignEdit.addItem('Greater or equal')
        dialogWindow.conditionSignEdit.addItem('Less than')
        dialogWindow.conditionSignEdit.addItem('Less or equal')
        dialogWindow.conditionSignEdit.setCurrentIndex(self.parameters[self.conditionSignKey])
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Sign'), dialogWindow.conditionSignEdit)

        dialogWindow.conditionRightValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionRightValueEdit.setText(str(self.parameters[self.conditionRightValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Right Value'), dialogWindow.conditionRightValueEdit)

        dialogWindow.conditionTypeEdit = QtWidgets.QComboBox()
        dialogWindow.conditionTypeEdit.addItem('If')
        dialogWindow.conditionTypeEdit.addItem('If-Else')
        dialogWindow.conditionTypeEdit.addItem('If-Elseif-Else')
        dialogWindow.conditionTypeEdit.setCurrentIndex(self.parameters[self.conditionTypeKey])
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Structure'), dialogWindow.conditionTypeEdit)

        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'if {dialogWindow.conditionLeftValueEdit.text()} '
        res += self.conditionSigns[dialogWindow.conditionSignEdit.currentIndex()]
        res += f' {dialogWindow.conditionRightValueEdit.text()}'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'if {self.parameters[self.conditionLeftValueKey]} '
        res += self.conditionSigns[self.parameters[self.conditionSignKey]]
        res += f' {self.parameters[self.conditionRightValueKey]}'
        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.conditionLeftValueKey: dialogWindow.conditionLeftValueEdit.text(),
            self.conditionRightValueKey: dialogWindow.conditionRightValueEdit.text(),
            self.conditionSignKey: dialogWindow.conditionSignEdit.currentIndex(),
            self.conditionTypeKey: dialogWindow.conditionTypeEdit.currentIndex(),
        }
        self.parameters.update(newParameters)

        return self.parameters


class WhileElement(NumericalCustomizationWindowElementBase):
    title = 'While'
    icon = ''
    textValue = 'while'

    conditionLeftValueKey = '-ConditionLeftValue'
    conditionRightValueKey = '-ConditionRightValue'
    conditionSignKey = '-ConditionSignKey'

    conditionSigns = ['==', '~=', '>', '>=', '<', '<=']

    def __init__(self, parameters=None):
        super(WhileElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.conditionLeftValueKey: '',
                self.conditionRightValueKey: '',
                self.conditionSignKey: 0,
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.conditionLeftValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionLeftValueEdit.setText(str(self.parameters[self.conditionLeftValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Left Value'), dialogWindow.conditionLeftValueEdit)

        dialogWindow.conditionSignEdit = QtWidgets.QComboBox()
        dialogWindow.conditionSignEdit.addItem('Equal')
        dialogWindow.conditionSignEdit.addItem('Not Equal')
        dialogWindow.conditionSignEdit.addItem('Greater than')
        dialogWindow.conditionSignEdit.addItem('Greater or equal')
        dialogWindow.conditionSignEdit.addItem('Less than')
        dialogWindow.conditionSignEdit.addItem('Less or equal')
        dialogWindow.conditionSignEdit.setCurrentIndex(self.parameters[self.conditionSignKey])
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Structure'), dialogWindow.conditionSignEdit)

        dialogWindow.conditionRightValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionRightValueEdit.setText(str(self.parameters[self.conditionRightValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Right Value'), dialogWindow.conditionRightValueEdit)

        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'while {dialogWindow.conditionLeftValueEdit.text()} '
        res += self.conditionSigns[dialogWindow.conditionSignEdit.currentIndex()]
        res += f' {dialogWindow.conditionRightValueEdit.text()}'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'while {self.parameters[self.conditionLeftValueKey]} '
        res += self.conditionSigns[self.parameters[self.conditionSignKey]]
        res += f' {self.parameters[self.conditionRightValueKey]}'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.conditionLeftValueKey: dialogWindow.conditionLeftValueEdit.text(),
            self.conditionRightValueKey: dialogWindow.conditionRightValueEdit.text(),
            self.conditionSignKey: dialogWindow.conditionSignEdit.currentIndex(),
        }
        self.parameters.update(newParameters)

        return self.parameters


class ForElement(NumericalCustomizationWindowElementBase):
    title = 'For'
    icon = ''
    textValue = 'for'

    loopVariableNameKey = '-LoopVariableName'
    loopStartValueKey = '-LoopStartValue'
    loopLimitValueKey = '-LoopLimitValue'
    loopStepValueKey = '-LoopStepValue'
    isInvertedValue = '-IsInverted'

    def __init__(self, parameters=None):
        super(ForElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.loopVariableNameKey: '',
                self.loopStartValueKey: '',
                self.loopLimitValueKey: '',
                self.loopStepValueKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.loopVariableEdit = QtWidgets.QLineEdit()
        dialogWindow.loopVariableEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.loopVariableEdit.setText(str(self.parameters[self.loopVariableNameKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Loop Variable Name'), dialogWindow.loopVariableEdit)

        dialogWindow.loopStartEdit = QtWidgets.QLineEdit()
        dialogWindow.loopStartEdit.setText(str(self.parameters[self.loopStartValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Loop Start Value'), dialogWindow.loopStartEdit)

        dialogWindow.loopLimitEdit = QtWidgets.QLineEdit()
        dialogWindow.loopLimitEdit.setText(str(self.parameters[self.loopLimitValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Loop Limit Value'), dialogWindow.loopLimitEdit)

        dialogWindow.loopStepEdit = QtWidgets.QLineEdit()
        dialogWindow.loopStepEdit.setText(str(self.parameters[self.loopStepValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Loop Step'), dialogWindow.loopStepEdit)

        return dialogWindow

    def onApplyButtonPressed(self, dialogWindow):

        if dialogWindow.loopVariableEdit.text().strip() == '':
            return

        dialogWindow.accept()

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'for {dialogWindow.loopVariableEdit.text()} = '

        res += f'{dialogWindow.loopStartEdit.text()}:'

        if int(dialogWindow.loopStepEdit.text()) != 1:
            res += f'{dialogWindow.loopStepEdit.text()}:'

        res += f'{dialogWindow.loopLimitEdit.text()}'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'for {self.parameters[self.loopVariableNameKey]} = '

        res += f'{self.parameters[self.loopStepValueKey]}:'

        if int(self.parameters[self.loopStepValueKey]) != 1:
            res += f'{self.parameters[self.loopStepValueKey]}:'

        res += f'{self.parameters[self.loopLimitValueKey]}'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.loopVariableNameKey: dialogWindow.loopVariableEdit.text(),
            self.loopStartValueKey: dialogWindow.loopStartEdit.text(),
            self.loopLimitValueKey: dialogWindow.loopLimitEdit.text(),
            self.loopStepValueKey: dialogWindow.loopStepEdit.text()
        }
        self.parameters.update(newParameters)

        return self.parameters


class VariableElement(NumericalCustomizationWindowElementBase):
    title = 'Var'
    description = 'Assign Variable'
    icon = ''

    assignedVariableKey = '-AssignedVariable'
    assignedValueKey = '-AssignedValue'

    def __init__(self, parameters=None):
        super(VariableElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.assignedVariableKey: '',
                self.assignedValueKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.assignedVariableEdit = QtWidgets.QLineEdit()
        #dialogWindow.assignedVariableEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.assignedVariableEdit.setText(str(self.parameters[self.assignedVariableKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Assigned Variable'), dialogWindow.assignedVariableEdit)

        dialogWindow.assignedValueEdit = QtWidgets.QLineEdit()
        dialogWindow.assignedValueEdit.setText(str(self.parameters[self.assignedValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Assigned Value'), dialogWindow.assignedValueEdit)

        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'{dialogWindow.assignedVariableEdit.text()} = {dialogWindow.assignedValueEdit.text()};'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'{self.parameters[self.assignedVariableKey]} = {self.parameters[self.assignedValueKey]};'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.assignedVariableKey: dialogWindow.assignedVariableEdit.text(),
            self.assignedValueKey: dialogWindow.assignedValueEdit.text(),
        }
        self.parameters.update(newParameters)

        return self.parameters


class MethodElement(NumericalCustomizationWindowElementBase):
    title = 'Method'
    description = 'Assign Method Output'
    icon = ''

    methodName = ''
    methodContent = ''

    assignedVariableKey = '-AssignedVariable'
    assignedMethodParametersKey = '-AssignedMethodParameters'
    assignedMethodPathKey = '-AssignedMethodPath'
    assignedMethodDeclarationListKey = '-ListAssignedMethodDeclaration'
    assignedMethodNameKey = '-AssignedMethodName'
    assignedMethodContentKey = '-AssignedMethodContent'

    def __init__(self, parameters=None):
        super(MethodElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.assignedVariableKey: '',
                self.assignedMethodParametersKey: '',
                self.assignedMethodPathKey: '',
                self.assignedMethodDeclarationListKey: '',
                self.assignedMethodNameKey: '',
                self.assignedMethodContentKey: ''
            }

    def dressWindow(self, dialogWindow):
        self.methodName = self.parameters[self.assignedMethodNameKey]
        self.methodContent = self.parameters[self.assignedMethodContentKey]

        dialogWindow.assignedVariableEdit = QtWidgets.QLineEdit()
        dialogWindow.assignedVariableEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
        dialogWindow.assignedVariableEdit.setText(str(self.parameters[self.assignedVariableKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Assigned Variable'), dialogWindow.assignedVariableEdit)

        dialogWindow.assignedValueEdit = QtWidgets.QLineEdit()
        dialogWindow.assignedValueEdit.setText(str(self.parameters[self.assignedMethodParametersKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Method Parameters'), dialogWindow.assignedValueEdit)

        dialogWindow.fileOpenBtn = QtWidgets.QPushButton()
        dialogWindow.pathEdit = QtWidgets.QLineEdit()
        dialogWindow.fileOpenBtn.setText("...")
        dialogWindow.fileOpenBtn.clicked.connect(lambda: self.browse_block(dialogWindow))
        dialogWindow.fileOpenBtn.setFixedWidth(25)
        dialogWindow.fileOpenBtn.setFixedHeight(25)

        dialogWindow.pathEdit.setText(str(self.parameters[self.assignedMethodPathKey]))

        pathLabel = QtWidgets.QLabel('Filename ')
        row = QtWidgets.QHBoxLayout()
        row.addWidget(pathLabel)
        row.addWidget(dialogWindow.pathEdit)
        row.addWidget(dialogWindow.fileOpenBtn)
        dialogWindow.content.addLayout(row)

        dialogWindow.declarationListBox = QtWidgets.QCheckBox()
        dialogWindow.declarationListBox.setChecked(bool(self.parameters[self.assignedMethodDeclarationListKey]))
        declarationListLabel = QtWidgets.QLabel('List Declaration ')
        self.addRow(dialogWindow, declarationListLabel, dialogWindow.declarationListBox)

        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'{dialogWindow.assignedVariableEdit.text()} = ' \
               f'{self.methodName}({dialogWindow.assignedValueEdit.text()});'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'{self.parameters[self.assignedVariableKey]} = ' \
               f'{self.parameters[self.assignedMethodNameKey]}({self.parameters[self.assignedMethodParametersKey]});'

        self.textValue = res

    def deserializeBlock(self, jsonDataPath):
        return json.load(open(jsonDataPath))

    def browse_block(self, prompt):
        chosenFile, _ = QtWidgets.QFileDialog.getOpenFileName(parent=prompt,
                                                              caption="Open method logic",
                                                              filter="Block (*.block)",
                                                              directory=numerical_prototyper.numerical_paths
                                                              .saveDirectory)
        if chosenFile == "":
            return
        prompt.pathEdit.setText(str(chosenFile))

        blockData = self.deserializeBlock(str(chosenFile))
        self.methodName = blockData['name']
        self.methodContent = blockData['content']

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.assignedVariableKey: dialogWindow.assignedVariableEdit.text(),
            self.assignedMethodParametersKey: dialogWindow.assignedValueEdit.text(),
            self.assignedMethodPathKey: dialogWindow.pathEdit.text(),
            self.assignedMethodDeclarationListKey: dialogWindow.declarationListBox.isChecked(),
            self.assignedMethodNameKey: self.methodName,
            self.assignedMethodContentKey: self.methodContent
        }
        self.parameters.update(newParameters)
        return self.parameters


class OpenBlockElement(NumericalCustomizationWindowElementBase):
    title = '{'
    textValue = ''

    def __init__(self, parameters=None):
        super(OpenBlockElement, self).__init__(parameters)

    def dressWindow(self, dialogWindow):
        pass


class CloseBlockElement(NumericalCustomizationWindowElementBase):
    title = '}'
    textValue = 'end'

    def __init__(self, parameters=None):
        super(CloseBlockElement, self).__init__(parameters)

    def dressWindow(self, dialogWindow):
        pass


class CloseBlockSilentlyElement(NumericalCustomizationWindowElementBase):
    title = '}'
    textValue = ''

    def __init__(self, parameters=None):
        super(CloseBlockSilentlyElement, self).__init__(parameters)

    def dressWindow(self, dialogWindow):
        pass


class BreakElement(NumericalCustomizationWindowElementBase):
    title = 'Break'
    textValue = 'break'

    def __init__(self, parameters=None):
        super(BreakElement, self).__init__(parameters)

    def dressWindow(self, dialogWindow):
        pass


class ElseElement(NumericalCustomizationWindowElementBase):
    title = 'Else'
    textValue = 'else'

    def __init__(self, parameters=None):
        super(ElseElement, self).__init__(parameters)

    def dressWindow(self, dialogWindow):
        pass


class ElseIfElement(NumericalCustomizationWindowElementBase):
    title = 'ElseIf'
    textValue = 'elseif'

    conditionLeftValueKey = '-ConditionLeftValue'
    conditionRightValueKey = '-ConditionRightValue'
    conditionSignKey = '-ConditionSignKey'

    conditionSigns = ['==', '~=', '>', '>=', '<', '<=']

    def __init__(self, parameters=None):
        super(ElseIfElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.conditionLeftValueKey: '',
                self.conditionRightValueKey: '',
                self.conditionSignKey: 0,
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.conditionLeftValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionLeftValueEdit.setText(str(self.parameters[self.conditionLeftValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Left Value'), dialogWindow.conditionLeftValueEdit)

        dialogWindow.conditionSignEdit = QtWidgets.QComboBox()
        dialogWindow.conditionSignEdit.addItem('Equal')
        dialogWindow.conditionSignEdit.addItem('Not Equal')
        dialogWindow.conditionSignEdit.addItem('Greater than')
        dialogWindow.conditionSignEdit.addItem('Greater or equal')
        dialogWindow.conditionSignEdit.addItem('Less than')
        dialogWindow.conditionSignEdit.addItem('Less or equal')
        dialogWindow.conditionSignEdit.setCurrentIndex(self.parameters[self.conditionSignKey])
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Sign'), dialogWindow.conditionSignEdit)

        dialogWindow.conditionRightValueEdit = QtWidgets.QLineEdit()
        dialogWindow.conditionRightValueEdit.setText(str(self.parameters[self.conditionRightValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Condition Right Value'), dialogWindow.conditionRightValueEdit)
        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'elseif {dialogWindow.conditionLeftValueEdit.text()} '
        res += self.conditionSigns[dialogWindow.conditionSignEdit.currentIndex()]
        res += f' {dialogWindow.conditionRightValueEdit.text()}'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'elseif {self.parameters[self.conditionLeftValueKey]} '
        res += self.conditionSigns[self.parameters[self.conditionSignKey]]
        res += f' {self.parameters[self.conditionRightValueKey]}'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.conditionLeftValueKey: dialogWindow.conditionLeftValueEdit.text(),
            self.conditionRightValueKey: dialogWindow.conditionRightValueEdit.text(),
            self.conditionSignKey: dialogWindow.conditionSignEdit.currentIndex(),
        }
        self.parameters.update(newParameters)

        return self.parameters


class LogElement(NumericalCustomizationWindowElementBase):
    title = 'Log'
    textValue = 'disp'

    loggedValueKey = '-LoggedValue'

    def __init__(self, parameters=None):
        super(LogElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.loggedValueKey: '',
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.loggedValueEdit = QtWidgets.QLineEdit()
        dialogWindow.loggedValueEdit.setText(str(self.parameters[self.loggedValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Logged Value'), dialogWindow.loggedValueEdit)
        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'disp({dialogWindow.loggedValueEdit.text()});'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'disp({self.parameters[self.loggedValueKey]});'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.loggedValueKey: dialogWindow.loggedValueEdit.text(),
        }
        self.parameters.update(newParameters)

        return self.parameters


class PlotElement(NumericalCustomizationWindowElementBase):
    title = 'Plot'
    textValue = 'plot'

    xValueKey = '-xValue'
    yValueKey = '-yValue'

    def __init__(self, parameters=None):
        super(PlotElement, self).__init__(parameters)

        if self.parameters is None:
            self.parameters = {
                self.xValueKey: '',
                self.yValueKey: ''
            }

    def dressWindow(self, dialogWindow):
        dialogWindow.xValueEdit = QtWidgets.QLineEdit()
        dialogWindow.xValueEdit.setText(str(self.parameters[self.xValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('X Value'), dialogWindow.xValueEdit)

        dialogWindow.yValueEdit = QtWidgets.QLineEdit()
        dialogWindow.yValueEdit.setText(str(self.parameters[self.yValueKey]))
        self.addRow(dialogWindow, QtWidgets.QLabel('Y Value'), dialogWindow.yValueEdit)

        return dialogWindow

    def setTextValue(self, dialogWindow):
        res = ''

        res += f'plot({dialogWindow.xValueEdit.text()}, {dialogWindow.yValueEdit.text()});'

        self.textValue = res

    def loadTextValue(self):
        res = ''

        res += f'plot({self.parameters[self.xValueKey]}, {self.parameters[self.yValueKey]});'

        self.textValue = res

    def extractParameters(self, dialogWindow):
        self.setTextValue(dialogWindow)

        newParameters = {
            self.xValueKey: dialogWindow.xValueEdit.text(),
            self.yValueKey: dialogWindow.yValueEdit.text()
        }
        self.parameters.update(newParameters)

        return self.parameters



