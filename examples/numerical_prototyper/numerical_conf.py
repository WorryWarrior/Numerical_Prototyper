import random

from numerical_prototyper.nodes.numerical_input_nodes import TestNumericalInputNodeContent
from numerical_prototyper.nodes.numerical_node_base import NumericalNode, NumericalGraphicsNode
from numerical_prototyper.numerical_node_customization_window_base import NumberInputNodeCustomizationWindow, \
    FunctionInputNodeCustomizationWindow, EvaluateFunctionNodeCustomizationWindow

LISTBOX_MIMETYPE = "application/x-item"

NUM_NODE_EVALUATE_FUNCTION = 1
NUM_NODE_INPUT_NUMBER = 2
NUM_NODE_INPUT_FUNCTION = 3
NUM_NODE_OUTPUT = 10

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
class TestNumericalNode(NumericalNode):
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


@register_numeric_node(NUM_NODE_INPUT_NUMBER)
class TestNumericalInputNode(NumericalNode):
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

        res += f'{str(self.inputVariableName)} = {str(self.inputValue)}'

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
            self.content.valueLabel.setText(str(retrievedValue))
            self.content.valueLabel.adjustSize()

        retrievedVariableName = self.customizationWindow.getParameterValue(
            self.customizationWindow.variableNameParameterKey)
        if retrievedVariableName is not None:
            self.inputVariableName = retrievedVariableName

        retrievedVariablePrintValue = self.customizationWindow.getParameterValue(
            self.customizationWindow.variablePrintKey)
        self.printVariable = retrievedVariablePrintValue

        self.nodeOutputs = [str(self.inputVariableName)]
        self.markDescendantsDirty()


@register_numeric_node(NUM_NODE_INPUT_FUNCTION)
class TestNumericalInputNode(NumericalNode):
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

        if self.inputValue == '':
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
            self.content.valueLabel.setText(str(retrievedValue))
            self.content.valueLabel.adjustSize()

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
        self.markDescendantsDirty()


@register_numeric_node(NUM_NODE_OUTPUT)
class TestNumericalInputNode(NumericalNode):
    op_code = NUM_NODE_OUTPUT
    op_title = "Output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[0, 1, 2], outputs=[])
