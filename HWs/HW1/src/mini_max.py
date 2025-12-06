import json_parser as jp


def miniMax(node : jp.Node):
    """
    Run miniMax algorithm on a given node.
    The algorithm changes the node`s value in place

    @param node: Root node to run miniMax on
    """

    # Leaf → return value without recursion
    if node.type == "leaf":
        return node.value

    # Recursively evaluate children
    values = [miniMax(child) for child in node.children]

    if node.type == "max":
        node.value = max(values)
        return max(values)
    elif node.type == "min":
        node.value = min(values)
        return min(values)
    else:
        raise ValueError("Unknown node type:", node.type)
