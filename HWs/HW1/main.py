"""
HW1.py

Parses a JSON description of a game tree into Node objects
and prints a concise summary and pretty-printed tree.
"""
import utils
import json_parser as jp
import json

'''
sample_json = ''
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

if __name__ == "__main__":
    json_file_paths = jp.find_json_files(".")

    for path in json_file_paths:
        try:
          with open(path, 'r', encoding='utf-8') as f:
                json_string = f.read()
              
                root = jp.parse_tree_from_json_string(json_string)      
                utils.pretty_print(root)
                # Tree was generated on the line above
                # TODO: Run Minimax on the generated tree
                print("\n[demo] Pretty-printed tree:")
                utils.pretty_print(root)

                leaves = jp.list_leaves(root)
                print("\n[demo] Leaves and their values:")
                for lf in leaves:
                    print(f"  - {lf.name}: {lf.value}")

                print(f"\n[demo] Root: {root.name}, total leaves: {len(leaves)}")

        except FileNotFoundError:
            print(f"Error: File not found at {path}")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from file: {path}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {path}: {e}") 
            
            
        
        
        