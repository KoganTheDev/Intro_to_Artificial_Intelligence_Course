import os
import glob
import errno
import json

class Node:
    def __init__(self, name, type, children=None, value=None, parent=None):
        """
        Initialize a tree node.
        
        :param name: Unique identifier for the node
        :param type: Node type ('leaf', 'max', or 'min')
        :param children: List of child Node objects (default: empty list)
        :param value: Value of the node (only for leaf nodes)
        :param parent: Parent Node object (default: None)
        """
        self.name = name
        self.type = type
        self.children = children if children is not None else []
        self.value = value
        self.parent = parent

    def is_leaf(self):
        """
        Check if the node is a leaf node.
        
        :return: True if node is a leaf, False otherwise
        """
        return self.type == "leaf"

    def __repr__(self):  # concise repr for prints
        """
        Return a concise string representation of the node.
        
        :return: String representation of the node
        """
        if self.is_leaf():
            return f"Node({self.name!r}, leaf, value={self.value})"
        return f"Node({self.name!r}, {self.type}, children={len(self.children)})"


def list_leaves(root):
    """
    Recursively traverse the tree and return all leaf nodes.
    
    :param root: Root node of the tree
    :return: List of all leaf nodes found in the tree
    """
    leaves = []

    def dfs(n):
        if n.is_leaf():
            leaves.append(n)
        for c in n.children:
            dfs(c)

    dfs(root)
    return leaves

class JSONTreeParserError(Exception):
    pass

def raise_no_json_files_found(start_directory):
    """
    Raise a FileNotFoundError when no JSON files are found.
    
    :param start_directory: Directory where search was performed
    :raises FileNotFoundError: Always raises with appropriate errno
    """
    error_message = f"No JSON files found in directory: {start_directory}"
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), error_message)

def find_json_files(start_directory):
    """
    Find all JSON files recursively in a directory.
    
    :param start_directory: Starting directory for recursive search
    :return: List of absolute paths to all JSON files found
    :raises FileNotFoundError: If no JSON files are found in the directory tree
    """
    full_pattern = os.path.join(start_directory, "**", "*.json")
    found_files = glob.glob(full_pattern, recursive=True)
    
    found_files = [f for f in glob.glob(full_pattern, recursive=True) if os.path.isfile(f)] 
    
    if not found_files:
        raise_no_json_files_found(start_directory)
    
    return found_files

def parse_tree_from_dict(data):
    """
    Parse a dictionary (loaded JSON) describing a tree and return the root Node.

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

    This function builds the Node graph, validates structure and constraints.
    
    :param data: Dictionary parsed from JSON containing tree structure
    :return: Root node of the constructed tree
    :raises JSONTreeParserError: If data format is invalid or constraints are violated
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
            # Leaf nodes must have a value and must not declare children
            if "value" not in spec:
                raise JSONTreeParserError(f"Leaf node '{name}' missing 'value'.")
            if "children" in spec:
                raise JSONTreeParserError(f"Leaf node '{name}' must not have 'children' specified.")
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
    """
    Parse a JSON string describing a tree and return the root Node.
    
    :param json_text: JSON string containing tree structure
    :return: Root node of the constructed tree
    :raises JSONTreeParserError: If JSON format is invalid or tree constraints are violated
    :raises json.JSONDecodeError: If JSON text is malformed
    """
    data = json.loads(json_text)
    return parse_tree_from_dict(data)

