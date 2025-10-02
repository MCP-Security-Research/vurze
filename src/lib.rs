use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn vurze(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(get_functions_from_file, m)?)?;
    Ok(())
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// Extract function names from a Python file using Python's ast module.
#[pyfunction]
fn get_functions_from_file(py: Python, file_path: &str) -> PyResult<Vec<String>> {
    // Import Python's ast module
    let ast = py.import("ast")?;
    
    // Read the file content
    let content = std::fs::read_to_string(file_path)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(e.to_string()))?;
    
    // Parse the Python code into an AST
    let tree = ast.call_method1("parse", (content,))?;
    
    // Walk through the AST and collect function names
    let mut function_names = Vec::new();
    let walk_iter = ast.call_method1("walk", (tree,))?;
    
    for node in walk_iter.try_iter()? {
        let node = node?;
        let node_type = node.get_type().name()?;
        
        if node_type == "FunctionDef" || node_type == "AsyncFunctionDef" {
            if let Ok(name) = node.getattr("name") {
                let name_str: String = name.extract()?;
                function_names.push(name_str);
            }
        }
    }
    
    Ok(function_names)
}



/*
example python code that does this: 

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