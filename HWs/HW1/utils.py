def pretty_print(root, indent=0):
    prefix = "  " * indent
    if root.is_leaf():
        print(f"{prefix}- {root.name} (leaf) value={root.value}")
    else:
        print(f"{prefix}- {root.name} ({root.type})")
        for c in root.children:
            pretty_print(c, indent + 1)