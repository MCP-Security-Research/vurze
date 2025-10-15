"""Automatically add decorators to all functions and classes in a python file."""

import ast
import copy


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
    
    # Iterate through each node in the AST
    # ast.walk() returns an iterator that yields every node in the tree
    for node in ast.walk(tree):
        # Get the type name of the current AST node
        # Each AST node has a type (e.g., "FunctionDef", "ClassDef", "If", etc.)
        node_type = type(node).__name__
        
        # Check if this node represents a function or class definition
        # "FunctionDef" = regular function (def function_name():)
        # "AsyncFunctionDef" = asynchronous function (async def function_name():)
        # "ClassDef" = class definition (class ClassName:)
        if node_type in ("FunctionDef", "AsyncFunctionDef", "ClassDef"):
            
            # Extract the complete source code of this function/class for hashing
            # Step 1: Create a deep copy of the node to avoid modifying the original
            try:
                node_clone = copy.deepcopy(node)
            except Exception:
                # If deepcopy fails, try to create a copy through unparsing and reparsing
                source = ast.unparse(node)
                node_clone = ast.parse(source)
            
            # Step 2: Get decorator_list and filter out vurze decorators
            if hasattr(node_clone, 'decorator_list'):
                filtered_decorators = []
                
                for decorator in node_clone.decorator_list:
                    # Check if decorator is a Name node with id attribute
                    if isinstance(decorator, ast.Name) and hasattr(decorator, 'id'):
                        # Keep decorator if it doesn't start with "vurze"
                        if not decorator.id.startswith("vurze"):
                            filtered_decorators.append(decorator)
                    else:
                        # If not a simple Name, keep it (could be a decorator with args)
                        filtered_decorators.append(decorator)
                
                # Replace decorator_list with filtered version
                node_clone.decorator_list = filtered_decorators
            
            # Step 3: Convert the filtered node back to source code
            function_source = ast.unparse(node_clone)
            
            # Step 4: Generate hash of the function/class source code
            '''
            // generate keypair --> this only is done once???
            // generate sig package
            '''
            # Step 5: Create decorator with the hash embedded (format: @vurze._<hash>())
            # decorator_name = f"vurze._{hash_value}"
            # vurze.protect(x, x, x)
            
            # Get the decorator_list attribute from the original function node
            if hasattr(node, 'decorator_list'):
                # Create a new AST Name node for the decorator
                # This creates the equivalent of: @vurze._<hash>()
                name_node = ast.Name(id=decorator_name, ctx=ast.Load())
                call_node = ast.Call(func=name_node, args=[], keywords=[])
                
                # Insert the decorator at the beginning of the decorator list
                node.decorator_list.insert(0, call_node)
    
    # Convert the modified AST back to Python source code
    modified_code = ast.unparse(tree)
    
    # Return the modified Python code
    return modified_code
