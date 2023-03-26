from qtpy import QtWidgets, QtCore, QtGui

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

    conditionLeftValueKey = '-ConditionLeftValue'
    conditionRightValueKey = '-ConditionRightValue'
    conditionSignKey = '-ConditionSignKey'

    conditionSigns = ['==', '~=', '>', '>=', '<', '<=']

    def __init__(self, parameters=None):
        super(ForElement, self).__init__(parameters)

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
        dialogWindow.assignedVariableEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(VARIABLE_NAME_REGEX)))
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
