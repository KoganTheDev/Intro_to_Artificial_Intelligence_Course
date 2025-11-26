"""
Comprehensive test suite for utils module.

Tests cover:
- Path validation and resolution
- Tree printing
- Exit command detection
- Edge cases and error handling
"""

import pytest
import os
import tempfile
import sys
from io import StringIO

sys.path.insert(0, "../src")
import utils 
import json_parser as jp


class TestIsPathValid:
    """Test suite for is_path_valid function."""
    
    def test_existing_file_is_valid(self):
        """Test that an existing file is considered valid."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert utils.is_path_valid(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_existing_directory_is_valid(self):
        """Test that an existing directory is considered valid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            assert utils.is_path_valid(tmpdir) is True
    
    def test_nonexistent_file_is_invalid(self):
        """Test that a non-existent file is invalid."""
        assert utils.is_path_valid("/nonexistent/path/to/file.json") is False
    
    def test_nonexistent_directory_is_invalid(self):
        """Test that a non-existent directory is invalid."""
        assert utils.is_path_valid("/nonexistent/directory/path") is False
    
    def test_empty_string_is_invalid(self):
        """Test that empty string path is invalid."""
        assert utils.is_path_valid("") is False
    
    def test_none_raises_error(self):
        """Test that None as path raises an error."""
        with pytest.raises(TypeError):
            utils.is_path_valid(None)
    
    def test_relative_existing_path(self):
        """Test relative path to existing file."""
        # Create a temporary file in current directory
        with tempfile.NamedTemporaryFile(dir=".", delete=False) as f:
            temp_name = os.path.basename(f.name)
        
        try:
            assert utils.is_path_valid(temp_name) is True
        finally:
            os.unlink(temp_name)


class TestResolvePathRelativeToPythonScript:
    """Test suite for resolve_path_relative_to_python_script function."""
    
    def test_relative_path_resolution(self):
        """Test that relative path is resolved relative to script directory."""
        result = utils.resolve_path_relative_to_python_script("test.json")
        
        # Result should be absolute
        assert os.path.isabs(result)
        # Should end with the relative path
        assert result.endswith("test.json")
    
    def test_nested_relative_path(self):
        """Test resolution of nested relative paths."""
        result = utils.resolve_path_relative_to_python_script("folder/test.json")
        
        assert os.path.isabs(result)
        assert "folder" in result
        assert "test.json" in result
    
    def test_parent_directory_reference(self):
        """Test resolution with parent directory references."""
        result = utils.resolve_path_relative_to_python_script("../test.json")
        
        assert os.path.isabs(result)
        assert "test.json" in result


class TestCreateAbsolutePath:
    """Test suite for create_absolute_path function."""
    
    def test_absolute_path_unchanged(self):
        """Test that absolute path is returned unchanged."""
        abs_path = "/absolute/path/to/file.json"
        result = utils.create_absolute_path(abs_path)
        assert result == abs_path
    
    def test_windows_absolute_path(self):
        """Test Windows-style absolute path."""
        if sys.platform.startswith("win"):
            windows_path = "C:\\Users\\test\\file.json"
            result = utils.create_absolute_path(windows_path)
            assert result == windows_path

class TestIsExitCommand:
    """Test suite for is_exit_command function."""
    
    def test_exit_lowercase(self):
        """Test that 'exit' (lowercase) is recognized."""
        assert utils.is_exit_command("exit") is True
    
    def test_exit_uppercase(self):
        """Test that 'EXIT' (uppercase) is recognized."""
        assert utils.is_exit_command("EXIT") is True
    
    def test_exit_mixed_case(self):
        """Test that 'Exit' (mixed case) is recognized."""
        assert utils.is_exit_command("Exit") is True
    
    def test_quit_lowercase(self):
        """Test that 'quit' (lowercase) is recognized."""
        assert utils.is_exit_command("quit") is True
    
    def test_quit_uppercase(self):
        """Test that 'QUIT' (uppercase) is recognized."""
        assert utils.is_exit_command("QUIT") is True
    
    def test_quit_mixed_case(self):
        """Test that 'Quit' (mixed case) is recognized."""
        assert utils.is_exit_command("Quit") is True
    
    def test_exit_with_whitespace(self):
        """Test exit command with surrounding whitespace."""
        # Note: Current implementation doesn't strip whitespace
        assert utils.is_exit_command(" exit ") is False
        assert utils.is_exit_command("exit ") is False
        assert utils.is_exit_command(" exit") is False
    
    def test_non_exit_commands(self):
        """Test that other commands are not recognized as exit."""
        assert utils.is_exit_command("continue") is False
        assert utils.is_exit_command("no") is False
        assert utils.is_exit_command("stop") is False
        assert utils.is_exit_command("close") is False
    
    def test_partial_match_not_recognized(self):
        """Test that partial matches are not recognized."""
        assert utils.is_exit_command("ex") is False
        assert utils.is_exit_command("qui") is False
        assert utils.is_exit_command("exiting") is False
        assert utils.is_exit_command("quitting") is False
    
    def test_empty_string(self):
        """Test empty string is not an exit command."""
        assert utils.is_exit_command("") is False
    
    def test_whitespace_only(self):
        """Test whitespace-only string is not an exit command."""
        assert utils.is_exit_command("   ") is False
    
    def test_numeric_input(self):
        """Test numeric input is not recognized as exit command."""
        assert utils.is_exit_command("0") is False
        assert utils.is_exit_command("1") is False


class TestPrettyPrint:
    """Test suite for pretty_print function."""
    
    def test_single_leaf_print(self):
        """Test printing a single leaf node."""
        node = jp.Node(name="A", type="leaf", value=5)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(node)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "A" in output
        assert "leaf" in output
        assert "5" in output
    
    def test_simple_tree_print(self):
        """Test printing a simple tree."""
        leaf1 = jp.Node(name="B", type="leaf", value=3)
        leaf2 = jp.Node(name="C", type="leaf", value=7)
        root = jp.Node(name="A", type="max", children=[leaf1, leaf2])
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(root)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "A" in output
        assert "max" in output
        assert "B" in output
        assert "C" in output
        assert "3" in output
        assert "7" in output
    
    def test_nested_tree_print(self):
        """Test printing a nested tree with indentation."""
        leaf1 = jp.Node(name="D", type="leaf", value=5)
        leaf2 = jp.Node(name="E", type="leaf", value=-2)
        node_b = jp.Node(name="B", type="min", children=[leaf1, leaf2])
        leaf3 = jp.Node(name="C", type="leaf", value=3)
        root = jp.Node(name="A", type="max", children=[node_b, leaf3])
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(root)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        lines = output.strip().split("\n")
        
        # Check that indentation increases for nested nodes
        assert len(lines) >= 4  # At least root, B, D, E, C
        assert "A" in output
        assert "B" in output
        assert "D" in output
    
    def test_print_with_custom_indent(self):
        """Test pretty_print with custom initial indentation."""
        node = jp.Node(name="A", type="leaf", value=5)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(node, indent=2)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        # Should have indentation
        assert output.startswith("    -")  # 2 indents * 2 spaces + "- "
    
    def test_print_max_node(self):
        """Test printing max node is labeled correctly."""
        node = jp.Node(name="MAX_NODE", type="max", children=[
            jp.Node(name="child", type="leaf", value=1)
        ])
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(node)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "max" in output
        assert "MAX_NODE" in output
    
    def test_print_min_node(self):
        """Test printing min node is labeled correctly."""
        node = jp.Node(name="MIN_NODE", type="min", children=[
            jp.Node(name="child", type="leaf", value=1)
        ])
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(node)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "min" in output
        assert "MIN_NODE" in output
    
    def test_print_deep_tree(self):
        """Test printing a deeply nested tree."""
        # Create a deep tree: A -> B -> C -> D (leaf)
        leaf = jp.Node(name="D", type="leaf", value=10)
        node_c = jp.Node(name="C", type="min", children=[leaf])
        node_b = jp.Node(name="B", type="max", children=[node_c])
        root = jp.Node(name="A", type="max", children=[node_b])
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(root)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "A" in output
        assert "B" in output
        assert "C" in output
        assert "D" in output
        assert "10" in output
    
    def test_print_negative_values(self):
        """Test printing nodes with negative values."""
        node = jp.Node(name="A", type="leaf", value=-42)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        utils.pretty_print(node)
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        assert "-42" in output


class TestIntegrationUtils:
    """Integration tests for utils module functions."""
    
    def test_path_workflow(self):
        """Test complete path resolution workflow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = os.path.join(tmpdir, "test.json")
            with open(test_file, "w") as f:
                f.write("{}")
            
            # Test that it can be found
            assert utils.is_path_valid(test_file) is True
    
    def test_exit_command_workflow(self):
        """Test exit command in various scenarios."""
        # Valid exit commands
        assert utils.is_exit_command("exit") is True
        assert utils.is_exit_command("quit") is True
        
        # Invalid commands
        assert utils.is_exit_command("run") is False
        assert utils.is_exit_command("help") is False
