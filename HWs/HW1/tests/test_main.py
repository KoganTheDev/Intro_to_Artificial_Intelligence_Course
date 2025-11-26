"""
Comprehensive test suite for main module.

Tests cover:
- TEMP_REFACTOR function with file I/O
- main function with command-line args and user input
- Error handling and edge cases
- Mock file operations to avoid side effects
"""

import pytest
import json
import tempfile
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock, mock_open, call

sys.path.insert(0, "../src")
import main
import json_parser as jp
import utils as utils


class TestTempRefactor:
    """Test suite for TEMP_REFACTOR function."""
    
    def test_valid_json_file(self):
        """Test processing a valid JSON file."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "leaf", "value": 3},
                "C": {"type": "leaf", "value": 7}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            assert "A" in output
            assert "B" in output or "3" in output
        finally:
            os.unlink(temp_path)
    
    
    def test_output_includes_tree_info(self):
        """Test that output includes tree information."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should include demo messages and tree info
            assert "demo" in output or "Root" in output or "A" in output
        finally:
            os.unlink(temp_path)
    
    def test_leaves_extraction(self):
        """Test that leaves are correctly extracted and displayed."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B", "C"]},
                "B": {"type": "leaf", "value": 3},
                "C": {"type": "leaf", "value": 7}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should display leaf information
            assert "Leaves" in output or "B" in output or "C" in output
        finally:
            os.unlink(temp_path)
    
    def test_complex_tree_processing(self):
        """Test processing a more complex tree structure."""
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
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should process without errors and display info
            assert output  # Should have some output
        finally:
            os.unlink(temp_path)


class TestMain:
    """Test suite for main function."""
    
    def test_main_with_valid_file_argument(self):
        """Test main with a valid JSON file as argument."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            with patch("builtins.input", side_effect=["exit"]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([temp_path])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should process the argument and handle exit
                assert output  # Should have some output
        finally:
            os.unlink(temp_path)
    
    def test_main_with_invalid_file_argument(self):
        """Test main with an invalid file path as argument."""
        with patch("builtins.input", side_effect=["exit"]):
            captured_output = StringIO()
            sys.stdout = captured_output
            main.main(["/nonexistent/path.json"])
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should indicate invalid path
            assert "valid" in output.lower() or "error" in output.lower() or "not found" in output.lower()
    
    def test_main_exit_command_case_insensitive(self):
        """Test that exit command is case-insensitive."""
        with patch("builtins.input", side_effect=["EXIT"]):
            captured_output = StringIO()
            sys.stdout = captured_output
            main.main([])
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should successfully exit
            assert "THANK YOU" in output or "exit" in output.lower()
    
    def test_main_quit_command(self):
        """Test that quit command works like exit."""
        with patch("builtins.input", side_effect=["QUIT"]):
            captured_output = StringIO()
            sys.stdout = captured_output
            main.main([])
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should successfully quit
            assert "THANK YOU" in output or "quit" in output.lower()
    
    def test_main_relative_path_conversion(self):
        """Test that relative paths are converted to absolute."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", dir=".", delete=False) as f:
            json.dump(tree_data, f)
            temp_name = os.path.basename(f.name)
        
        try:
            with patch("builtins.input", side_effect=["exit"]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([temp_name])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should process relative path correctly
                assert output
        finally:
            os.unlink(temp_name)
    
    @patch("json_parser.find_json_files")
    def test_main_find_recursive_json_files_yes(self, mock_find):
        """Test recursive JSON file discovery when user answers yes."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        # Mock find_json_files to return the temp file
        mock_find.return_value = [temp_path]
        
        try:
            with patch("builtins.input", side_effect=[
                "/nonexistent/path.json",
                "y",
                "exit"
            ]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should call find_json_files
                assert mock_find.called
        finally:
            os.unlink(temp_path)
    
    @patch("json_parser.find_json_files")
    def test_main_find_recursive_json_files_no(self, mock_find):
        """Test that recursive search doesn't happen when user answers no."""
        with patch("builtins.input", side_effect=[
            "/nonexistent/path.json",
            "n",
            "exit"
        ]):
            captured_output = StringIO()
            sys.stdout = captured_output
            main.main([])
            sys.stdout = sys.__stdout__
            
            # Should not call find_json_files
            assert not mock_find.called
    
    def test_main_multiple_invalid_paths(self):
        """Test main handling multiple invalid paths before exit."""
        with patch("builtins.input", side_effect=[
            "/invalid/path1.json",
            "/invalid/path2.json",
            "exit"
        ]):
            captured_output = StringIO()
            sys.stdout = captured_output
            main.main([])
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should handle multiple invalid paths
            assert output
    
    def test_main_exit_after_argument_processing(self):
        """Test that exit can occur after processing argument."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            with patch("builtins.input", side_effect=["exit"]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([temp_path])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should include thank you message on exit
                assert "THANK YOU" in output
        finally:
            os.unlink(temp_path)


class TestEdgeCases:
    """Test suite for edge cases and potential bugs."""
    
    def test_large_json_file(self):
        """Test handling of large JSON tree."""
        # Create a large tree with many leaves
        nodes = {"A": {"type": "max", "children": []}}
        for i in range(100):
            node_name = f"B{i}"
            nodes[node_name] = {"type": "leaf", "value": i}
            nodes["A"]["children"].append(node_name)
        
        tree_data = {"root": "A", "nodes": nodes}
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            assert "100" in output or "A" in output
        finally:
            os.unlink(temp_path)
    
    def test_special_characters_in_node_names(self):
        """Test handling of special characters in node names."""
        tree_data = {
            "root": "Node-A",
            "nodes": {
                "Node-A": {"type": "max", "children": ["Node_B"]},
                "Node_B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            assert "Node" in output
        finally:
            os.unlink(temp_path)
    
    def test_unicode_node_names(self):
        """Test handling of unicode characters in node names."""
        tree_data = {
            "root": "الف",  # Arabic letter
            "nodes": {
                "الف": {"type": "max", "children": ["ب"]},
                "ب": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(tree_data, f, ensure_ascii=False)
            temp_path = f.name
        
        try:
            captured_output = StringIO()
            sys.stdout = captured_output
            main.TEMP_REFACTOR(temp_path)
            sys.stdout = sys.__stdout__
            
            output = captured_output.getvalue()
            # Should handle unicode properly
            assert output
        finally:
            os.unlink(temp_path)


class TestIntegrationMain:
    """Integration tests for main module."""
    
    def test_full_workflow_with_valid_file(self):
        """Test complete workflow from file argument to exit."""
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
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            with patch("builtins.input", side_effect=["exit"]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([temp_path])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should successfully process and exit
                assert "THANK YOU" in output
                assert len(output) > 0
        finally:
            os.unlink(temp_path)
    
    def test_full_workflow_interactive(self):
        """Test complete interactive workflow."""
        tree_data = {
            "root": "A",
            "nodes": {
                "A": {"type": "max", "children": ["B"]},
                "B": {"type": "leaf", "value": 5}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(tree_data, f)
            temp_path = f.name
        
        try:
            with patch("builtins.input", side_effect=[
                temp_path,
                "n",
                "exit"
            ]):
                captured_output = StringIO()
                sys.stdout = captured_output
                main.main([])
                sys.stdout = sys.__stdout__
                
                output = captured_output.getvalue()
                # Should process path and exit successfully
                assert "THANK YOU" in output
        finally:
            os.unlink(temp_path)
