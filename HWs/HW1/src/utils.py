import os

def pretty_print(root, indent=0):
    """
    Recursively print a tree structure in a formatted, indented manner.
    
    :param root: Root node of the tree to print
    :param indent: Current indentation level (default: 0)
    """
    prefix = "  " * indent
    if root.is_leaf():
        print(f"{prefix}- {root.name} (leaf) value={root.value}")
    else:
        print(f"{prefix}- {root.name} ({root.type})")
        for c in root.children:
            pretty_print(c, indent + 1)

def resolve_path_relative_to_python_script(path):
    """
    Resolve a relative path to an absolute path based on the script's directory.
    
    :param path: Relative path to resolve
    :return: Absolute path combining script directory and provided path
    """
    # Find the path to the directory that contains the file (this module)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # If empty path, return the script directory
    if not path:
        return script_dir

    # If an absolute path was provided, return it unchanged
    if os.path.isabs(path):
        return path

    # Candidate 1: file relative to the script (src) directory
    candidate_src = os.path.join(script_dir, path)
    if os.path.exists(candidate_src):
        return os.path.abspath(candidate_src)

    # Candidate 2: file in the project root (parent of src)
    project_root = os.path.dirname(script_dir)
    candidate_root = os.path.join(project_root, path)
    if os.path.exists(candidate_root):
        return os.path.abspath(candidate_root)

    # Fallback: return argument as is so it fails on is_path_valid() in main
    return path
            
def create_absolute_path(path):
    """
    Convert a path to an absolute path.
    
    If the path is relative, resolve it relative to the script directory.
    If the path is absolute, return it unchanged.
    
    :param path: Path to convert (relative or absolute)
    :return: Absolute path
    """
    if path is None:
        return None

    if not os.path.isabs(path):
        # Resolve using the helper which tries src/ then project root
        resolved_path = resolve_path_relative_to_python_script(path)
    else:
        resolved_path = path

    return resolved_path
            
def is_path_valid(path):
    """
    Check if the given path exists.
    
    :param path: Path to validate
    :return: True if path exists, False otherwise
    """
    
    return os.path.exists(path)

def is_exit_command(command):
    """
    Check if the given command is an exit command.
    
    Recognized exit commands are 'exit' and 'quit' (case-insensitive).
    
    :param command: User input command to check
    :return: True if command is 'exit' or 'quit', False otherwise
    """
    exit_commands = {"exit", "quit"}
    
    return (command.lower() in exit_commands)
