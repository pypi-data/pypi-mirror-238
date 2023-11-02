use std::str::FromStr;

use serde::{Deserialize, Serialize};
use pyo3::{prelude::*, types::PyDict};

/// Echo (return) the input string
#[pyfunction]
#[pyo3(signature = (s))]
fn echo(s: String) -> PyResult<String> {
    Ok(s)
}

#[pyfunction]
#[pyo3(signature = (policies))]
fn convert_json_to_cedar_policies(policies: String) -> PyResult<String> {
    let policies_json = match serde_json::from_str::<serde_json::Value>(policies.as_str()) {
        Ok(json) => json,
        Err(e) => {
            let error = format!("❌ error parsing json: {:?}", e);
            return Err(pyo3::exceptions::PyValueError::new_err(error));
        }
    };
    match cedar_policy::Policy::from_json(None, policies_json) {
        Ok(p) => Ok(p.to_string()),
        Err(e) => {
            let error = format!("❌ error converting json to cedar policies: {:?}", e);
            Err(pyo3::exceptions::PyValueError::new_err(error))
        }
    }
}

#[pyfunction]
#[pyo3(signature = (policies))]
fn convert_cedar_policies_to_json(policies: String) -> PyResult<String> {
    let cedar_policies = match cedar_policy::Policy::from_str(policies.as_str()) {
        Ok(p) => p,
        Err(e) => {
            let error = format!("❌ error parsing cedar policies: {:?}", e);
            return Err(pyo3::exceptions::PyValueError::new_err(error));
        }
    };
    match cedar_policies.to_json() {
        Ok(p) => Ok(p.to_string()),
        Err(e) => {
            let error = format!("❌ error converting policies to json: {:?}", e);
            Err(pyo3::exceptions::PyValueError::new_err(error))
        }
    }
}

#[derive(Debug, PartialEq, Clone, Serialize, Deserialize)]
struct EntityTypeAndName {
    entity_id: String,
    entity_type: String,
}

impl IntoPy<PyObject> for EntityTypeAndName {
    fn into_py(self, py: Python) -> PyObject {
        let dict = PyDict::new(py);
        dict.set_item("entity_id", self.entity_id).unwrap();
        dict.set_item("entity_type", self.entity_type).unwrap();
        dict.into()
    }
}



#[pyfunction]
#[pyo3(signature = (entity))]
fn get_entity_type_and_id(entity: String) -> PyResult<EntityTypeAndName> {
    let cedar_entity = match cedar_policy::EntityUid::from_str(&entity) {
        Ok(e) => e,
        Err(e) => {
            let error = format!("❌ error parsing entity: {:?}", e);
            return Err(pyo3::exceptions::PyValueError::new_err(error));
        }
    };

    Ok(EntityTypeAndName {
        entity_id: cedar_entity.id().to_string(),
        entity_type: cedar_entity.type_name().to_string(),
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn _internal(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(echo, m)?)?;
    m.add_function(wrap_pyfunction!(convert_json_to_cedar_policies, m)?)?;
    m.add_function(wrap_pyfunction!(convert_cedar_policies_to_json, m)?)?;
    m.add_function(wrap_pyfunction!(get_entity_type_and_id, m)?)?;
    Ok(())
}
