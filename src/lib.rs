
use pyo3::prelude::*;
use current_platform::CURRENT_PLATFORM;

#[pyfunction]
fn platform() -> String {
    CURRENT_PLATFORM.to_string()
}

#[pymodule]
fn current_platform_rs(_py: Python, module: &PyModule) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(platform, module)?)?;

    Ok(())
}