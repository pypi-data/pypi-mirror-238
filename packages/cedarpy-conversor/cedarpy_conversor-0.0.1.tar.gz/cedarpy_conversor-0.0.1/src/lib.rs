use std::str::FromStr;

use pyo3::prelude::*;

/// Echo (return) the input string
#[pyfunction]
#[pyo3(signature = (s))]
fn echo(s: String) -> PyResult<String> {
    Ok(s)
}

#[pyfunction]
#[pyo3(signature = (policies))]
fn convert_json_to_cedar_policies(policies: String) -> PyResult<String> {
    let policies_json = serde_json::from_str(policies.as_str()).unwrap();
    match cedar_policy::Policy::from_json(None, policies_json) {
        Ok(p) => Ok(p.to_string()),
        Err(e) => {
            println!("❌ error converting json to cedar policies: {:?}", e);
            Err(pyo3::exceptions::PyValueError::new_err(e.to_string()))
        }
    }
}

#[pyfunction]
#[pyo3(signature = (policies))]
fn convert_cedar_policies_to_json(policies: String) -> PyResult<String> {
    let cedar_policies = cedar_policy::Policy::from_str(policies.as_str()).unwrap();
    match cedar_policies.to_json() {
        Ok(p) => Ok(p.to_string()),
        Err(e) => {
            println!("❌ error converting policies to json: {:?}", e);
            Err(pyo3::exceptions::PyValueError::new_err(e.to_string()))
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn _internal(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(echo, m)?)?;
    m.add_function(wrap_pyfunction!(convert_json_to_cedar_policies, m)?)?;
    m.add_function(wrap_pyfunction!(convert_cedar_policies_to_json, m)?)?;
    Ok(())
}
