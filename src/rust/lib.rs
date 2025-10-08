use pyo3::prelude::*;

mod parser;
use parser::add_decorators_to_functions;

/// A Python module implemented in Rust.
#[pymodule]
fn _vurze(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_decorators_to_functions, m)?)?;
    Ok(())
}
