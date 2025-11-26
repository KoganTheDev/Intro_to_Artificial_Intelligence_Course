"""
HW1.py

Parses a JSON description of a game tree into Node objects
and prints a concise summary and pretty-printed tree.
"""
import utils
import json_parser as jp
import json
import sys

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

def TEMP_REFACTOR(path):
    """
    Load a JSON tree file, parse it, and display it.
    
    Reads a JSON file from the given path, parses it into a tree structure,
    finds all leaf nodes, and prints the tree and leaf information.
    
    :param path: File path to the JSON tree file
    :raises FileNotFoundError: If the file does not exist
    :raises json.JSONDecodeError: If the JSON is malformed
    :raises Exception: For other unexpected errors during processing
    """
    #* ============== CAN BE REFACTORED =================== VVVV
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

    #* ============== CAN BE REFACTORED =================== ^^^^^^^


def main(args):
    initial_run_flag = True # For runs other than the initial run, don`t try using the args as input on the next try

    
    
    while True:
        # CMD arg as input
        if (initial_run_flag):
            if (len(args) > 0):
                print(f"Received arguments: {args}")
                path = args[0]
                
                if (utils.is_path_valid(path)): # Path valid
                    TEMP_REFACTOR(path)
                else: # Path given as argument is not valid
                    print(f"Argument: \"{path}\", is not a valid path")
            
            initial_run_flag = False

            # TODO: next step: implement JSON parsing and minMax
        
        #* ================== Main logic branch ==========================
        if not initial_run_flag:
            path = input("Enter JSON path or exit\\quit to exit\n")
            
            # If user wants to exit - check the raw input before resolving path
            if utils.is_exit_command(path):
                print("THANK YOU FOR USING OUR PROGRAM :)")
                return

            # Create the exact valid path to the JSON file
            path = utils.create_absolute_path(path)
            if (utils.is_path_valid(path)):
                print("Found valid path, running MiniMax")
                
                TEMP_REFACTOR(path)
                # TODO: run minimax
                
            else: # Not a valid path
                print("Please insert a valid JSON path")
                


            # Feature: Using custom function to find all of the JSON files recursevely in the folder.
            find_recursive = input("Do you want to find all of the JSON files in the current folder? Y/N\n")
            if (find_recursive.lower() == "y"):
                json_file_paths = jp.find_json_files(".")

                for path in json_file_paths:
                    TEMP_REFACTOR(path)
                                

if __name__ == "__main__":
    main(sys.argv[1:]) # Grab arguments if there are any
    
            
            
        
        
        