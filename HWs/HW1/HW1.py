"""
HW1.py

Parses a JSON description of a game tree into Node objects
and prints a concise summary and pretty-printed tree.
"""
import json


class Node:
    def __init__(self, name, type, children=None, value=None, parent=None):
        self.name = name
        self.type = type
        self.children = children if children is not None else []
        self.value = value
        self.parent = parent

    def is_leaf(self):
        return self.type == "leaf"

    def __repr__(self):  # concise repr for prints
        if self.is_leaf():
            return f"Node({self.name!r}, leaf, value={self.value})"
        return f"Node({self.name!r}, {self.type}, children={len(self.children)})"


class JSONTreeParserError(Exception):
    pass


def parse_tree_from_dict(data):
    """Parse a dictionary (loaded JSON) describing a tree and return the root Node.

    Expected format:
    {
      "root": "A",
      "nodes": {
        "A": { "type": "max", "children": ["B", "C"] },
        "B": { "type": "min", "children": ["D", "E"] },
        "C": { "type": "leaf", "value": 3 },
        "D": { "type": "leaf", "value": 5 },
        "E": { "type": "leaf", "value": -2 }
      }
    }

    This function only builds the Node graph and performs validation.
    """
    if not isinstance(data, dict):
        raise JSONTreeParserError("Input data must be a dictionary (parsed JSON).")

    if "root" not in data or "nodes" not in data:
        raise JSONTreeParserError("JSON must contain 'root' and 'nodes' keys.")

    root_name = data["root"]
    nodes_def = data["nodes"]

    if not isinstance(nodes_def, dict):
        raise JSONTreeParserError("'nodes' must be a dictionary mapping names to node specs.")

    # First pass: create Node objects without linking children
    nodes = {}
    print("[parser] Creating node objects...")
    for name, spec in nodes_def.items():
        if not isinstance(spec, dict) or "type" not in spec:
            raise JSONTreeParserError(f"Node spec for '{name}' must be a dict with a 'type'.")
        ntype = spec["type"]
        if ntype == "leaf":
            if "value" not in spec:
                raise JSONTreeParserError(f"Leaf node '{name}' missing 'value'.")
            node = Node(name=name, type="leaf", value=spec["value"])
        else:
            # max/min expected to have children
            if "children" not in spec:
                raise JSONTreeParserError(f"Non-leaf node '{name}' missing 'children'.")
            node = Node(name=name, type=ntype)
        nodes[name] = node
        print(f"  created: {node}")

    # Second pass: link children
    print("[parser] Linking children references...")
    for name, spec in nodes_def.items():
        node = nodes[name]
        if node.is_leaf():
            continue
        child_names = spec.get("children", [])
        if not isinstance(child_names, list):
            raise JSONTreeParserError(f"'children' for node '{name}' must be a list.")
        for cname in child_names:
            if cname not in nodes:
                raise JSONTreeParserError(f"Child '{cname}' referenced by '{name}' not defined in nodes.")
            child_node = nodes[cname]
            node.children.append(child_node)
            if child_node.parent is None:
                child_node.parent = node
        print(f"  linked {name} -> {[c.name for c in node.children]}")

    if root_name not in nodes:
        raise JSONTreeParserError(f"Root '{root_name}' not found among nodes.")

    root = nodes[root_name]

    # Basic validation: ensure leaf nodes have no children and non-leaf nodes have children
    print("[parser] Validating node constraints...")
    for n in nodes.values():
        if n.is_leaf() and n.children:
            raise JSONTreeParserError(f"Leaf node '{n.name}' has children defined.")
        if n.type in ("max", "min") and not n.children:
            raise JSONTreeParserError(f"Node '{n.name}' of type '{n.type}' must have children.")

    print(f"[parser] Parsed tree root: {root.name}, total nodes: {len(nodes)}")
    return root


def parse_tree_from_json_string(json_text):
    data = json.loads(json_text)
    return parse_tree_from_dict(data)


def list_leaves(root):
    leaves = []

    def dfs(n):
        if n.is_leaf():
            leaves.append(n)
        for c in n.children:
            dfs(c)

    dfs(root)
    return leaves


def pretty_print(root, indent=0):
    prefix = "  " * indent
    if root.is_leaf():
        print(f"{prefix}- {root.name} (leaf) value={root.value}")
    else:
        print(f"{prefix}- {root.name} ({root.type})")
        for c in root.children:
            pretty_print(c, indent + 1)


if __name__ == "__main__":
    # Demo using the example from the assignment attachment
    sample_json = '''
    {
      "root": "A",
      "nodes": {
        "A": { "type": "max", "children": ["B", "C"] },
        "B": { "type": "min", "children": ["D", "E"] },
        "C": { "type": "leaf", "value": 3 },
        "D": { "type": "leaf", "value": 5 },
        "E": { "type": "leaf", "value": -2 }
      }
    }
    '''

    print("[demo] Loading sample JSON and building tree...")
    root = parse_tree_from_json_string(sample_json)

    print("\n[demo] Pretty-printed tree:")
    pretty_print(root)

    leaves = list_leaves(root)
    print("\n[demo] Leaves and their values:")
    for lf in leaves:
        print(f"  - {lf.name}: {lf.value}")

    print(f"\n[demo] Root: {root.name}, total leaves: {len(leaves)}")
