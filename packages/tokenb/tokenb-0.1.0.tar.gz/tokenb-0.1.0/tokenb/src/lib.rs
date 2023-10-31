use pyo3::prelude::*;

mod implc;

use implc::{load_from_file, TokenBTokenizer};

/// A Python module implemented in Rust.
#[pymodule]
fn tokenb(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_from_file, m)?)?;
    m.add_class::<TokenBTokenizer>()?;
    Ok(())
}
