// parsing ast tree file
use pyo3::prelude::*;

/// Add decorators to functions in a Python file using Python's ast module.
#[pyfunction]
pub fn add_decorators_to_functions(py: Python, file_path: &str, decorator: &str) -> PyResult<String> {
    // Import Python's ast module to access AST parsing functionality
    // The ? operator propagates any import errors up to the caller
    let ast = py.import("ast")?;
    
    // Read the entire file content into a string
    // std::fs::read_to_string reads the file at the given path and returns the content as a String
    // map_err converts the std::io::Error into a PyIOError that Python can understand
    let content = std::fs::read_to_string(file_path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    
    // Parse the Python source code into an Abstract Syntax Tree (AST)
    // ast.parse() converts the raw Python source code string into a structured tree
    // representation that we can programmatically analyze
    // call_method1 calls the Python method "parse" with one argument (the content)
    let tree = ast.call_method1("parse", (content,))?;
    
    // Create an iterator that will walk through every node in the AST tree
    // ast.walk() is a Python generator that yields every node in the tree in depth-first order
    // This allows us to examine each node without having to implement our own tree traversal
    let walk_iter = ast.call_method1("walk", (tree.clone(),))?;
    
    // Iterate through each node in the AST
    // try_iter() converts the Python iterator into a Rust iterator that can handle errors
    for node in walk_iter.try_iter()? {
        // Extract the current node from the iterator result
        // The ? operator handles any errors that occur during iteration
        let node = node?;
        
        // Get the type name of the current AST node
        // Each AST node has a type (e.g., "FunctionDef", "ClassDef", "If", etc.)
        // get_type().name()? retrieves this type information as a string
        let node_type = node.get_type().name()?;
        
        // Check if this node represents a function definition
        // "FunctionDef" = regular function (def function_name():)
        // "AsyncFunctionDef" = asynchronous function (async def function_name():)
        if node_type == "FunctionDef" || node_type == "AsyncFunctionDef" {
            // Add decorator to the function's decorator list
            // First, get the decorator_list attribute from the function node
            if let Ok(decorator_list) = node.getattr("decorator_list") {
                // Create a new AST Name node for the decorator
                let name_node = ast.call_method1("Name", (decorator, ast.getattr("Load")?,))?;
                
                // Append the decorator to the function's decorator list
                decorator_list.call_method1("append", (name_node,))?;
            }
        }
    }
    
    // Convert the modified AST back to Python source code
    let modified_code = ast.call_method1("unparse", (tree,))?;
    let code_str: String = modified_code.extract()?;
    
    // Return the modified Python code
    Ok(code_str)
}

// change the get_functions_from_file( function to be add decorators to functions function. 
// add the parameter decorator: &str
// and also change the inside of the if statement to add this decorator to every function       if node_type == "FunctionDef" || node_type == "AsyncFunctionDef" {

/*
import os
import ast
import sys
import inspect

from graffito import graffiti

def emboss(elem: callable, name: str = "", checksum: str = ""):
    if os.path.exists(elem):
        src = open(elem, "r").read()
    else:
        src = inspect.getsource(elem)
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            if name == node.name:
                node.decorator_list.append(ast.Name(checksum))
    mod = ast.unparse(tree)
*/
