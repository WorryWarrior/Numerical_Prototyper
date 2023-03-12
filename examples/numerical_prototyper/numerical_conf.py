from PyQt5.QtGui import QFont

from numerical_prototyper.nodes.numerical_input_nodes import TestNumericalInputNodeContent
from numerical_prototyper.nodes.numerical_node_base import NumericalNode, NumericalGraphicsNode
from numerical_prototyper.numerical_node_customization_window_base import NumberInputNodeCustomizationWindow, \
    FunctionInputNodeCustomizationWindow, EvaluateFunctionNodeCustomizationWindow, MatrixInputNodeCustomizationWindow, \
    FunctionZeroSearchNodeCustomizationWindow

LISTBOX_MIMETYPE = "application/x-item"

NUM_NODE_INPUT_NUMBER = 1
NUM_NODE_INPUT_FUNCTION = 2
NUM_NODE_INPUT_MATRIX = 3
NUM_NODE_EVALUATE_FUNCTION = 4
NUM_NODE_TRANSPOSE = 5
NUM_NODE_CONDITION_NUMBER = 6
NUM_NODE_ZERO_SEARCH = 7
NUM_NODE_ADD = 8

"""
NUM_NONE_SUBTRACT = 6
NUM_NODE_MULTIPLY = 7
NUM_NODE_DIVIDE = 8
NUM_NODE_SQUARE_ROOT = 9
NUM_NODE_POWER = 10
NUM_NODE_ABS = 11
"""

NUM_NODE_OUTPUT = 20

NUMERIC_NODES = {
}

ANONYMOUS_INPUT_COUNTER = 0


class ConfException(Exception): pass


class InvalidNodeRegistration(ConfException): pass


class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in NUMERIC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, NUMERIC_NODES[op_code]
        ))
    NUMERIC_NODES[op_code] = class_reference


def register_numeric_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class

    return decorator


def get_class_from_opcode(op_code):
    if op_code not in NUMERIC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return NUMERIC_NODES[op_code]


@register_numeric_node(NUM_NODE_EVALUATE_FUNCTION)
class EvaluateFunctionNode(NumericalNode):
    op_code = NUM_NODE_EVALUATE_FUNCTION
    op_title = "Evaluate function"

    def __init__(self, scene):
        super().__init__(scene, inputs=[2, 1], outputs=[1])
        self.customizationWindow = EvaluateFunctionNodeCustomizationWindow()
        self.functionName = ''
        self.argumentName = ''
        self.useVariable = False
        self.printOutput = False
        self.variableName = ''
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.functionName == '' or self.argumentName == '':
            return res

        if self.variableName != '':
            res += f'{self.variableName} = '

        res += f'{str(self.functionName)}({self.argumentName})'

        if not self.printOutput:
            res += ";"

        return res

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)

        if retrievedVariableName is not None:
            self.variableName = retrievedVariableName

        retrievedUseVariableValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.useVariableKey)
        self.useVariable = retrievedUseVariableValue

        retrievedPrintOutputValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.printOutputKey)
        self.printOutput = retrievedPrintOutputValue

        if self.variableName == '':
            outputValue = f'{str(self.functionName)}({self.argumentName})'
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]

        self.markDescendantsDirty()

    def onInputChanged(self, socket: None):
        self.eval()

    def onMarkedDirty(self):
        self.eval()

    def eval(self, index=0):

        if self.getInput(0) is None or self.getInput(1) is None:
            self.functionName = None
            self.argumentName = None
            return

        self.functionName = self.getInput(0).nodeOutputs[0]
        self.argumentName = self.getInput(1).nodeOutputs[0]

        if self.variableName == '' or not self.useVariable:
            outputValue = f'{str(self.functionName)}({self.argumentName})'
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]


@register_numeric_node(NUM_NODE_TRANSPOSE)
class TransposeMatrixNode(NumericalNode):
    op_code = NUM_NODE_TRANSPOSE
    op_title = "Transpose matrix"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[0])
        self.customizationWindow = EvaluateFunctionNodeCustomizationWindow()
        self.matrixValue = ''
        self.useVariable = False
        self.printOutput = False
        self.variableName = ''
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.matrixValue == '':
            return res

        if self.variableName != '':
            res += f'{self.variableName} = '

        res += f'{self.matrixValue}\''

        if not self.printOutput:
            res += ";"

        return res

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)

        if retrievedVariableName is not None:
            self.variableName = retrievedVariableName

        retrievedUseVariableValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.useVariableKey)
        self.useVariable = retrievedUseVariableValue

        retrievedPrintOutputValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.printOutputKey)
        self.printOutput = retrievedPrintOutputValue

        if self.variableName == '':
            outputValue = f'{self.matrixValue}\''
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]

        self.markDescendantsDirty()

    def onInputChanged(self, socket: None):
        self.eval()

    def onMarkedDirty(self):
        self.eval()

    def eval(self, index=0):

        if self.getInput(0) is None:
            self.matrixValue = None
            return

        self.matrixValue = self.getInput(0).nodeOutputs[0]

        if self.variableName == '' or not self.useVariable:
            outputValue = f'{self.matrixValue}\''
        else:
            outputValue = self.variableName

        if self.matrixValue.strip() == '':
            outputValue = ''

        self.nodeOutputs = [outputValue]


@register_numeric_node(NUM_NODE_CONDITION_NUMBER)
class ConditionNumberNode(NumericalNode):
    op_code = NUM_NODE_CONDITION_NUMBER
    op_title = "Find Condition Number"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0], outputs=[1])
        self.customizationWindow = EvaluateFunctionNodeCustomizationWindow()
        self.matrixValue = ''
        self.useVariable = False
        self.printOutput = False
        self.variableName = ''
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.matrixValue == '':
            return res

        if self.variableName != '':
            res += f'{self.variableName} = '

        res += f'cond({self.matrixValue})'

        if not self.printOutput:
            res += ";"

        return res

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)

        if retrievedVariableName is not None:
            self.variableName = retrievedVariableName

        retrievedUseVariableValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.useVariableKey)
        self.useVariable = retrievedUseVariableValue

        retrievedPrintOutputValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.printOutputKey)
        self.printOutput = retrievedPrintOutputValue

        if self.variableName == '':
            outputValue = f'cond({self.matrixValue})'
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]

        self.markDescendantsDirty()

    def onInputChanged(self, socket: None):
        self.eval()

    def onMarkedDirty(self):
        self.eval()

    def eval(self, index=0):

        if self.getInput(0) is None:
            self.matrixValue = None
            return

        self.matrixValue = self.getInput(0).nodeOutputs[0]

        if self.variableName == '' or not self.useVariable:
            outputValue = f'cond({self.matrixValue})'
        else:
            outputValue = self.variableName

        if self.matrixValue.strip() == '':
            outputValue = ''

        self.nodeOutputs = [outputValue]


@register_numeric_node(NUM_NODE_ADD)
class AddNumbersNode(NumericalNode):
    op_code = NUM_NODE_ADD
    op_title = "Add Numbers"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1], outputs=[1])
        self.customizationWindow = EvaluateFunctionNodeCustomizationWindow()
        self.firstNumberName = ''
        self.secondNumberName = ''
        self.useVariable = False
        self.printOutput = False
        self.variableName = ''
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.firstNumberName == '' or self.secondNumberName == '':
            return res

        if self.variableName != '':
            res += f'{self.variableName} = '

        res += f'{str(self.firstNumberName)} + {self.secondNumberName}'

        if not self.printOutput:
            res += ";"

        return res

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)

        if retrievedVariableName is not None:
            self.variableName = retrievedVariableName

        retrievedUseVariableValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.useVariableKey)
        self.useVariable = retrievedUseVariableValue

        retrievedPrintOutputValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.printOutputKey)
        self.printOutput = retrievedPrintOutputValue

        if self.variableName == '':
            outputValue = f'{str(self.firstNumberName)} + {self.secondNumberName}'
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]

        self.markDescendantsDirty()

    def onInputChanged(self, socket: None):
        self.eval()

    def onMarkedDirty(self):
        self.eval()

    def eval(self, index=0):

        if self.getInput(0) is None or self.getInput(1) is None:
            self.firstNumberName = None
            self.secondNumberName = None
            return

        self.firstNumberName = self.getInput(0).nodeOutputs[0]
        self.secondNumberName = self.getInput(1).nodeOutputs[0]

        if self.variableName == '' or not self.useVariable:
            outputValue = f'{str(self.firstNumberName)} + {self.secondNumberName}'
        else:
            outputValue = self.variableName

        self.nodeOutputs = [outputValue]


@register_numeric_node(NUM_NODE_INPUT_NUMBER)
class NumberInputNode(NumericalNode):
    op_code = NUM_NODE_INPUT_NUMBER
    op_title = "Number Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.customizationWindow = NumberInputNodeCustomizationWindow()
        self.inputValue = ''
        self.inputVariableName = None
        self.printVariable = False
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.inputValue == '':
            return res

        if self.inputVariableName != '':
            res += f'{str(self.inputVariableName)} = '

        res += f'{str(self.inputValue)}'

        if not self.printVariable:
            res += ";"

        return res

    def initInnerClasses(self):
        self.content = TestNumericalInputNodeContent(self)
        self.grNode = NumericalGraphicsNode(self)

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedValue = self.customizationWindow.getParameterValue(self.customizationWindow.valueParameterKey)
        if retrievedValue is not None:
            self.inputValue = retrievedValue

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)
        if retrievedVariableName is not None:
            self.inputVariableName = retrievedVariableName

        retrievedVariablePrintValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.variablePrintKey)
        self.printVariable = retrievedVariablePrintValue

        if self.inputVariableName != '':
            self.nodeOutputs = [str(self.inputVariableName)]
        else:
            self.nodeOutputs = [str(self.inputValue)]

        self.content.valueLabel.setText(self.inputValue)
        self.content.valueLabel.setFont(QFont('Arial', 12))
        self.content.valueLabel.adjustSize()

        self.markDescendantsDirty()


@register_numeric_node(NUM_NODE_INPUT_FUNCTION)
class FunctionInputNode(NumericalNode):
    op_code = NUM_NODE_INPUT_FUNCTION
    op_title = "Function Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[2])
        self.customizationWindow = FunctionInputNodeCustomizationWindow()
        self.inputValue = ''
        self.inputVariableName = ''
        self.printVariable = False
        self.functionArgs = None
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if self.inputValue == '' or self.inputVariableName == '':
            return res

        if self.inputVariableName != '':
            res += f'{str(self.inputVariableName)} = '

        res += f'@({str(self.functionArgs)}){str(self.inputValue)}'

        if not self.printVariable:
            res += ";"

        return res

    def initInnerClasses(self):
        self.content = TestNumericalInputNodeContent(self)
        self.grNode = NumericalGraphicsNode(self)

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedValue = self.customizationWindow.getParameterValue(self.customizationWindow.valueParameterKey)
        if retrievedValue is not None:
            self.inputValue = retrievedValue

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)
        if retrievedVariableName is not None:
            self.inputVariableName = retrievedVariableName

        retrievedArgsName = self.customizationWindow.getParameterValue(
            self.customizationWindow.functionArgumentsKey)
        if retrievedArgsName is not None:
            self.functionArgs = retrievedArgsName

        retrievedVariablePrintValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.variablePrintKey)
        self.printVariable = retrievedVariablePrintValue

        self.nodeOutputs = [str(self.inputVariableName)]

        self.content.valueLabel.setText(self.inputValue)
        self.content.valueLabel.setFont(QFont('Arial', 12))
        self.content.valueLabel.adjustSize()

        self.markDescendantsDirty()


@register_numeric_node(NUM_NODE_INPUT_MATRIX)
class MatrixInputNode(NumericalNode):
    op_code = NUM_NODE_INPUT_MATRIX
    op_title = "Matrix Input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[0])
        self.customizationWindow = MatrixInputNodeCustomizationWindow()
        self.matrixWidth = 0
        self.matrixHeight = 0
        self.matrixValues = []
        self.inputVariableName = ''
        self.printVariable = False
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        if len(self.matrixValues) <= 0:
            return res

        if self.inputVariableName != '':
            res += f'{str(self.inputVariableName)} = '

        res += self.getMatrixRepresentation()

        if not self.printVariable:
            res += ";"

        return res

    def initInnerClasses(self):
        self.content = TestNumericalInputNodeContent(self)
        self.grNode = NumericalGraphicsNode(self)

    def getMatrixRepresentation(self):
        res = ''
        res += '['

        for i in range(len(self.matrixValues)):
            res += f'{self.matrixValues[i]} '

            if (i + 1) % self.matrixWidth == 0:
                res += '; '

        res += ']'
        return res

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        retrievedValues = self.customizationWindow.getParameterValue(self.customizationWindow.valueParameterKey)
        self.matrixValues = retrievedValues

        retrievedWidth = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableWidthDimensionValueKey)
        if retrievedWidth.strip() != '':
            self.matrixWidth = int(retrievedWidth)

        retrievedHeight = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableHeightDimensionValueKey)
        if retrievedHeight.strip() != '':
            self.matrixHeight = int(retrievedHeight)

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)
        if retrievedVariableName is not None:
            self.inputVariableName = retrievedVariableName

        retrievedVariablePrintValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.variablePrintKey)
        self.printVariable = retrievedVariablePrintValue

        if str(self.inputVariableName).strip() == '':
            self.nodeOutputs = [self.getMatrixRepresentation()]
        else:
            self.nodeOutputs = [str(self.inputVariableName)]

        if len(self.matrixValues) <= 0:
            self.nodeOutputs = ['']

        # self.nodeOutputs = [self.getScriptRepresentation()]
        self.markDescendantsDirty()


@register_numeric_node(NUM_NODE_OUTPUT)
class OutputNode(NumericalNode):
    op_code = NUM_NODE_OUTPUT
    op_title = "Output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 1, 2], outputs=[])


@register_numeric_node(NUM_NODE_ZERO_SEARCH)
class FunctionZeroSearchNode(NumericalNode):
    op_code = NUM_NODE_ZERO_SEARCH
    op_title = "Bisection"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1, 1, 2], outputs=[1])
        self.customizationWindow = FunctionZeroSearchNodeCustomizationWindow(inputs=[1, 1, 2], outputs=[1])
        self.inputValue = ''
        self.inputVariableName = None
        self.printVariable = False
        self.nodeOutputs = [""]

    def getScriptRepresentation(self):
        res = ""

        return res

    def initInnerClasses(self):
        self.content = TestNumericalInputNodeContent(self)
        self.grNode = NumericalGraphicsNode(self)

    def onDoubleClicked(self, event):
        self.customizationWindow.openWindow()

        self.markDescendantsDirty()
