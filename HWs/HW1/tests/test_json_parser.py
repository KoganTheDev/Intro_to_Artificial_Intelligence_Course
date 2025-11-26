"""
Comprehensive test suite for json_parser module.

Tests cover:
- Node class creation and methods
- Tree parsing from dictionaries and JSON strings
- Validation and error handling
- Edge cases and potential bugs
- File operations for JSON discovery
"""

import pytest
import json
import os
import tempfile

import sys
sys.path.insert(0, "../src")
import json_parser as jp


class TestNode:
    """Test suite for Node class."""
    
    def test_node_leaf_creation(self):
        """Test creating a leaf node with value."""
        node = jp.Node(name="A", type="leaf", value=5)
        assert node.name == "A"
        assert node.type == "leaf"
        assert node.value == 5
        assert node.children == []
        assert node.parent is None
    
    def test_node_max_creation(self):
        """Test creating a max node."""
        node = jp.Node(name="B", type="max")
        assert node.name == "B"
        assert node.type == "max"
        assert node.value is None
        assert node.children == []
    
    def test_node_min_creation(self):
        """Test creating a min node."""
        node = jp.Node(name="C", type="min")
        assert node.name == "C"
        assert node.type == "min"
        assert node.value is None
        assert node.children == []
    
    def test_node_with_children(self):
        """Test creating a node with children."""
        child1 = jp.Node(name="D", type="leaf", value=3)
        child2 = jp.Node(name="E", type="leaf", value=7)
        parent = jp.Node(name="F", type="max", children=[child1, child2])
        
        assert len(parent.children) == 2
        assert parent.children[0] is child1
        assert parent.children[1] is child2
    
    def test_node_is_leaf_true(self):
        """Test is_leaf method returns True for leaf nodes."""
        node = jp.Node(name="A", type="leaf", value=10)
        assert node.is_leaf() is True
    
    def test_node_is_leaf_false_max(self):
        """Test is_leaf method returns False for max nodes."""
        node = jp.Node(name="A", type="max")
        assert node.is_leaf() is False
    
    def test_node_is_leaf_false_min(self):
        """Test is_leaf method returns False for min nodes."""
        node = jp.Node(name="A", type="min")
        assert node.is_leaf() is False
    
    def test_node_repr_leaf(self):
        """Test __repr__ for leaf node."""
        node = jp.Node(name="A", type="leaf", value=5)
        repr_str = repr(node)
        assert "Node" in repr_str
        assert "A" in repr_str
        assert "leaf" in repr_str
        assert "5" in repr_str
    
    def test_node_repr_max_with_children(self):
        """Test __repr__ for max node with children."""
        child1 = jp.Node(name="B", type="leaf", value=3)
        child2 = jp.Node(name="C", type="leaf", value=7)
        node = jp.Node(name="A", type="max", children=[child1, child2])
        repr_str = repr(node)
        assert "Node" in repr_str
        assert "A" in repr_str
        assert "max" in repr_str
        assert "2" in repr_str  # number of children
    
    def test_node_parent_assignment(self):
        """Test assigning parent to a node."""
        parent = jp.Node(name="A", type="max")
        child = jp.Node(name="B", type="leaf", value=5, parent=parent)
        assert child.parent is parent


class TestListLeaves:
    """Test suite for list_leaves function."""
    
    def test_single_leaf(self):
        """Test with a single leaf node."""
        node = jp.Node(name="A", type="leaf", value=5)
        leaves = jp.list_leaves(node)
        assert len(leaves) == 1
        assert leaves[0].name == "A"
        assert leaves[0].value == 5
    
    def test_multiple_leaves_simple_tree(self):
        """Test with simple tree containing multiple leaves."""
        leaf1 = jp.Node(name="B", type="leaf", value=3)
        leaf2 = jp.Node(name="C", type="leaf", value=7)
        root = jp.Node(name="A", type="max", children=[leaf1, leaf2])
        
        leaves = jp.list_leaves(root)
        assert len(leaves) == 2
        leaf_names = {l.name for l in leaves}
        assert leaf_names == {"B", "C"}
    
    def test_nested_tree_leaves(self):
        """Test with deeply nested tree."""
        leaf1 = jp.Node(name="D", type="leaf", value=5)
        leaf2 = jp.Node(name="E", type="leaf", value=-2)
        leaf3 = jp.Node(name="C", type="leaf", value=3)
        
        node_b = jp.Node(name="B", type="min", children=[leaf1, leaf2])
        root = jp.Node(name="A", type="max", children=[node_b, leaf3])
        
        leaves = jp.list_leaves(root)
        assert len(leaves) == 3
        leaf_values = {l.value for l in leaves}
        assert leaf_values == {5, -2, 3}
    
    def test_leaves_preserve_order(self):
        """Test that leaves are found in DFS order."""
        leaf1 = jp.Node(name="B", type="leaf", value=1)
        leaf2 = jp.Node(name="C", type="leaf", value=2)
        leaf3 = jp.Node(name="D", type="leaf", value=3)
        
        node_e = jp.Node(name="E", type="min", children=[leaf2, leaf3])
        root = jp.Node(name="A", type="max", children=[leaf1, node_e])
        
        leaves = jp.list_leaves(root)
        leaf_values = [l.value for l in leaves]
        assert leaf_values == [1, 2, 3]
    
    def test_no_leaves_error(self):
        """Test behavior when root has no leaves (edge case)."""
        root = jp.Node(name="A", type="max")
        leaves = jp.list_leaves(root)
        assert leaves == []


class TestParseTreeFromDict:
    """Test suite for parse_tree_from_dict function."""
    
    def test_valid_simple_tree(self):
        """Test parsing a valid simple tree."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "leaf", "value": 3},
                "C": {"type": "leaf", "value": 7}
            }
        }
        root = jp.parse_tree_from_dict(data)
        assert root.name == "A"
        assert root.type == "max"
        assert len(root.children) == 2
    
    def test_valid_complex_tree(self):
        """Test parsing the example tree from tree.json."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "min", "children": ["D", "E"]},
                "C": {"type": "leaf", "value": 3},
                "D": {"type": "leaf", "value": 5},
                "E": {"type": "leaf", "value": -2}
            }
        }
        root = jp.parse_tree_from_dict(data)
        
        assert root.name == "A"
        leaves = jp.list_leaves(root)
        assert len(leaves) == 3
        leaf_values = {l.value for l in leaves}
        assert leaf_values == {3, 5, -2}
    
    def test_missing_root_key(self):
        """Test error handling when 'root' key is missing."""
        data = {
            "nodes": {
                "A": {"type": "leaf", "value": 5}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_missing_nodes_key(self):
        """Test error handling when 'nodes' key is missing."""
        data = {
            "root": "A"
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_input_not_dict(self):
        """Test error handling when input is not a dictionary."""
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict("not a dict")
        
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict([1, 2, 3])
    
    def test_nodes_not_dict(self):
        """Test error handling when 'nodes' is not a dictionary."""
        data = {
            "root": "A",
            "nodes": ["A", "B", "C"]
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_node_spec_not_dict(self):
        """Test error handling when node spec is not a dictionary."""
        data = {
            "root": "A",
            "nodes": {
                "A": "invalid"
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_missing_type_in_node(self):
        """Test error handling when node is missing 'type'."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"children": ["B"]}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_leaf_missing_value(self):
        """Test error handling when leaf node is missing 'value'."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "leaf"}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_non_leaf_missing_children(self):
        """Test error handling when max/min node is missing 'children'."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max"}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_children_not_list(self):
        """Test error handling when 'children' is not a list."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": "B"}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_undefined_child_reference(self):
        """Test error handling when child is referenced but not defined."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                # B is not defined
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_root_not_in_nodes(self):
        """Test error handling when root is not found in nodes."""
        data = {
            "root": "A",
            "nodes": {
                "B": {"type": "leaf", "value": 5}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_leaf_with_children_error(self):
        """Test error handling when leaf node has children."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "leaf", "value": 5, "children": ["B"]},
                "B": {"type": "leaf", "value": 3}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_max_node_without_children_error(self):
        """Test error handling when max node has no children."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": []}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_min_node_without_children_error(self):
        """Test error handling when min node has no children."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "min", "children": []}
            }
        }
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_dict(data)
    
    def test_negative_leaf_values(self):
        """Test parsing tree with negative leaf values."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "leaf", "value": -5},
                "C": {"type": "leaf", "value": -10}
            }
        }
        root = jp.parse_tree_from_dict(data)
        leaves = jp.list_leaves(root)
        leaf_values = {l.value for l in leaves}
        assert leaf_values == {-5, -10}
    
    def test_zero_leaf_value(self):
        """Test parsing tree with zero value leaf."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 0}
            }
        }
        root = jp.parse_tree_from_dict(data)
        leaves = jp.list_leaves(root)
        assert leaves[0].value == 0
    
    def test_large_leaf_value(self):
        """Test parsing tree with large leaf values."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 999999999}
            }
        }
        root = jp.parse_tree_from_dict(data)
        leaves = jp.list_leaves(root)
        assert leaves[0].value == 999999999
    
    def test_float_leaf_value(self):
        """Test parsing tree with float leaf values."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 3.14}
            }
        }
        root = jp.parse_tree_from_dict(data)
        leaves = jp.list_leaves(root)
        assert leaves[0].value == 3.14
    
    def test_parent_child_links(self):
        """Test that parent-child relationships are properly established."""
        data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "leaf", "value": 3},
                "C": {"type": "leaf", "value": 7}
            }
        }
        root = jp.parse_tree_from_dict(data)
        
        # Check that children have correct parent
        for child in root.children:
            assert child.parent is root


class TestParseTreeFromJsonString:
    """Test suite for parse_tree_from_json_string function."""
    
    def test_valid_json_string(self):
        """Test parsing valid JSON string."""
        json_str = json.dumps({
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        })
        root = jp.parse_tree_from_json_string(json_str)
        assert root.name == "A"
    
    def test_malformed_json(self):
        """Test error handling with malformed JSON."""
        with pytest.raises(json.JSONDecodeError):
            jp.parse_tree_from_json_string("{ invalid json }")
    
    def test_empty_json_string(self):
        """Test error handling with empty JSON string."""
        with pytest.raises(json.JSONDecodeError):
            jp.parse_tree_from_json_string("")
    
    def test_valid_json_invalid_tree_structure(self):
        """Test error when JSON is valid but tree structure is invalid."""
        json_str = json.dumps({"invalid": "structure"})
        with pytest.raises(jp.JSONTreeParserError):
            jp.parse_tree_from_json_string(json_str)


class TestFindJsonFiles:
    """Test suite for find_json_files function."""
    
    def test_find_single_json_file(self):
        """Test finding a single JSON file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = os.path.join(tmpdir, "test.json")
            with open(json_path, "w") as f:
                f.write("{}")
            
            found = jp.find_json_files(tmpdir)
            assert len(found) == 1
            assert json_path in found
    
    def test_find_multiple_json_files(self):
        """Test finding multiple JSON files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple JSON files
            json1 = os.path.join(tmpdir, "test1.json")
            json2 = os.path.join(tmpdir, "test2.json")
            
            with open(json1, "w") as f:
                f.write("{}")
            with open(json2, "w") as f:
                f.write("{}")
            
            found = jp.find_json_files(tmpdir)
            assert len(found) == 2
    
    def test_find_json_in_subdirectories(self):
        """Test recursive search in subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "subdir")
            os.makedirs(subdir)
            
            json_path = os.path.join(subdir, "test.json")
            with open(json_path, "w") as f:
                f.write("{}")
            
            found = jp.find_json_files(tmpdir)
            assert len(found) == 1
            assert json_path in found
    
    def test_find_json_ignores_non_json_files(self):
        """Test that non-JSON files are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create JSON and non-JSON files
            json_file = os.path.join(tmpdir, "test.json")
            txt_file = os.path.join(tmpdir, "test.txt")
            
            with open(json_file, "w") as f:
                f.write("{}")
            with open(txt_file, "w") as f:
                f.write("not json")
            
            found = jp.find_json_files(tmpdir)
            assert len(found) == 1
            assert json_file in found
            assert txt_file not in found
    
    def test_no_json_files_raises_error(self):
        """Test error when no JSON files are found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(FileNotFoundError):
                jp.find_json_files(tmpdir)
    
    def test_finds_json_with_different_nesting_levels(self):
        """Test finding JSON files at different nesting levels."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create files at different depths
            json1 = os.path.join(tmpdir, "level1.json")
            subdir1 = os.path.join(tmpdir, "sub1")
            subdir2 = os.path.join(subdir1, "sub2")
            os.makedirs(subdir2)
            json2 = os.path.join(subdir1, "level2.json")
            json3 = os.path.join(subdir2, "level3.json")
            
            with open(json1, "w") as f:
                f.write("{}")
            with open(json2, "w") as f:
                f.write("{}")
            with open(json3, "w") as f:
                f.write("{}")
            
            found = jp.find_json_files(tmpdir)
            assert len(found) == 3


class TestRaiseNoJsonFilesFound:
    """Test suite for raise_no_json_files_found function."""
    
    def test_raises_file_not_found_error(self):
        """Test that the function raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            jp.raise_no_json_files_found("/some/path")
    
    def test_error_message_contains_path(self):
        """Test that error message contains the directory path."""
        try:
            jp.raise_no_json_files_found("/test/path")
        except FileNotFoundError as e:
            assert "/test/path" in str(e)


class TestJSONTreeParserError:
    """Test suite for JSONTreeParserError exception."""
    
    def test_exception_is_exception_subclass(self):
        """Test that JSONTreeParserError is an Exception subclass."""
        assert issubclass(jp.JSONTreeParserError, Exception)
    
    def test_raise_and_catch_error(self):
        """Test raising and catching JSONTreeParserError."""
        with pytest.raises(jp.JSONTreeParserError):
            raise jp.JSONTreeParserError("Test error message")


class TestIntegration:
    """Integration tests for the whole parsing pipeline."""
    
    def test_parse_from_file(self):
        """Test parsing a complete JSON tree from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tree_data = {
                "root": "A",
                "nodes": {
                    "A": {"type": "max", "children": ["B", "C"]},
                    "B": {"type": "min", "children": ["D", "E"]},
                    "C": {"type": "leaf", "value": 3},
                    "D": {"type": "leaf", "value": 5},
                    "E": {"type": "leaf", "value": -2}
                }
            }
            
            json_path = os.path.join(tmpdir, "tree.json")
            with open(json_path, "w") as f:
                json.dump(tree_data, f)
            
            # Read and parse
            with open(json_path, "r") as f:
                json_str = f.read()
            
            root = jp.parse_tree_from_json_string(json_str)
            leaves = jp.list_leaves(root)
            
            assert root.name == "A"
            assert len(leaves) == 3
            assert {l.value for l in leaves} == {3, 5, -2}
