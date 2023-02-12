from nodes.numerical_test_node import TestNumericalNode

LISTBOX_MIMETYPE = "application/x-item"

NUM_NODE_TEST = 1
NUM_NODE_OUTPUT = 2

NUMERIC_NODES = {
    1: TestNumericalNode
}


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
    print("Numeric node registered")

    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class

    return decorator


def get_class_from_opcode(op_code):
    if op_code not in NUMERIC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return NUMERIC_NODES[op_code]
