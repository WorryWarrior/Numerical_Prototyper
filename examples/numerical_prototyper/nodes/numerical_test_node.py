#from numerical_prototyper.numerical_conf import register_numeric_node, NUM_NODE_TEST
from numerical_prototyper.nodes.numerical_node_base import NumericalNode
from numerical_prototyper.numerical_transform_window import TransformWindow


#@register_numeric_node(NUM_NODE_TEST)
class TestNumericalNode(NumericalNode):
    op_code = 1
    op_title = "Overriden Test"
