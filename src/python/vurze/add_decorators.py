"""Automatically add cryptographic decorators to all functions and classes in a python file."""

import ast
import copy
from vurze import generate_signature
from .setup import get_private_key

def add_decorators_to_functions(file_path: str) -> str:
    """
    Parse a Python file, add decorators to all functions and classes, and return the modified code.
    
    Args:
        file_path: Path to the Python file to process
        
    Returns:
        Modified Python source code as a string
    """
    # Read the entire file content into a string
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Parse the Python source code into an Abstract Syntax Tree (AST)
    tree = ast.parse(content)
    
    # Split content into lines for manipulation
    lines = content.split('\n')
    
    # First pass: Remove existing vurze decorators
    lines_to_remove = set()
    for node in ast.walk(tree):
        if type(node).__name__ in ("FunctionDef", "AsyncFunctionDef", "ClassDef"):
            if hasattr(node, 'decorator_list'):
                for decorator in node.decorator_list:
                    is_vurze_decorator = False
                    
                    if isinstance(decorator, ast.Name):
                        if decorator.id.startswith("vurze"):
                            is_vurze_decorator = True
                    elif isinstance(decorator, ast.Attribute):
                        if isinstance(decorator.value, ast.Name) and decorator.value.id == "vurze":
                            is_vurze_decorator = True
                    elif isinstance(decorator, ast.Call):
                        func = decorator.func
                        if isinstance(func, ast.Attribute):
                            if isinstance(func.value, ast.Name) and func.value.id == "vurze":
                                is_vurze_decorator = True
                        elif isinstance(func, ast.Name) and func.id.startswith("vurze"):
                            is_vurze_decorator = True
                    
                    if is_vurze_decorator:
                        # Mark this line for removal (convert to 0-indexed)
                        lines_to_remove.add(decorator.lineno - 1)
    
    # Remove the marked lines (in reverse order to preserve indices)
    for line_idx in sorted(lines_to_remove, reverse=True):
        del lines[line_idx]
    
    # Re-parse the content after removing decorators to get updated line numbers
    modified_content = '\n'.join(lines)
    tree = ast.parse(modified_content)
    
    # Collect all functions/classes with their signatures (in reverse order to modify from bottom up)
    decorators_to_add = []
    
    # Iterate through each node in the AST
    for node in ast.walk(tree):
        node_type = type(node).__name__
        
        if node_type in ("FunctionDef", "AsyncFunctionDef", "ClassDef"):
            # Extract the complete source code of this function/class for hashing
            node_clone = copy.deepcopy(node)
            
            # Filter out vurze decorators
            if hasattr(node_clone, 'decorator_list'):
                filtered_decorators = []
                
                for decorator in node_clone.decorator_list:
                    should_keep = True
                    
                    if isinstance(decorator, ast.Name):
                        if decorator.id.startswith("vurze"):
                            should_keep = False
                    elif isinstance(decorator, ast.Attribute):
                        if isinstance(decorator.value, ast.Name) and decorator.value.id == "vurze":
                            should_keep = False
                    elif isinstance(decorator, ast.Call):
                        func = decorator.func
                        if isinstance(func, ast.Attribute):
                            if isinstance(func.value, ast.Name) and func.value.id == "vurze":
                                should_keep = False
                        elif isinstance(func, ast.Name) and func.id.startswith("vurze"):
                            should_keep = False
                    
                    if should_keep:
                        filtered_decorators.append(decorator)
                
                node_clone.decorator_list = filtered_decorators
            
            # Convert the filtered node back to source code
            module_wrapper = ast.Module(body=[node_clone], type_ignores=[])
            function_source = ast.unparse(module_wrapper)
            
            # Generate hash and signature
            try:
                private_key = get_private_key()
            except (FileNotFoundError, ValueError) as e:
                raise RuntimeError(f"Cannot add decorators: {e}. Please run 'vurze init' first.")
            
            try:
                signature = generate_signature(function_source, private_key)
            except Exception as e:
                raise RuntimeError(f"Failed to generate signature: {e}")
            
            # Store the line number and signature
            # Find the line where the decorator should be added (before the def/class line)
            # Account for existing decorators
            decorator_line = node.lineno - 1
            if hasattr(node, 'decorator_list') and node.decorator_list:
                decorator_line = node.decorator_list[0].lineno - 1
            
            decorators_to_add.append((decorator_line, node.col_offset, signature))
    
    # Sort in reverse order to add from bottom to top (preserves line numbers)
    decorators_to_add.sort(reverse=True)
    
    # Add decorators to the lines
    for line_idx, col_offset, signature in decorators_to_add:
        indent = ' ' * col_offset
        decorator_line = f"{indent}@vurze._{signature}()"
        lines.insert(line_idx, decorator_line)
    
    # Join lines back together
    modified_code = '\n'.join(lines)
    
    return modified_code
