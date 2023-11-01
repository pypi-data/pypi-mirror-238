//! Generic serialization target
//!
//! This module contains a generic [Value] struct that can be used as a serialization target (similar to [serde_json]s [Value](serde_json::Value)).

use std::collections::BTreeMap;

#[cfg(feature = "arbitrary")]
use arbitrary::Arbitrary;
#[cfg(feature = "py")]
use pyo3::{
    prelude::*,
    types::{PyDict, PyNone},
};
use serde::{Deserialize, Serialize};

pub use de::{from_value, DeserializationError, ValueDeserializer};
pub use ser::{SerializationError, ValueSerializer};

#[cfg(test)]
mod test;

mod de;
mod ser;

/// Generic serialization target type
///
/// The available fields correspond to [serde]s internal data representation.
///
/// # Drawbacks
///
/// There is no destinction between different integer or float types, so numbers that cannot be represented by `i64` or `f64` are not supported.
/// Also structs are also represented as [Map](Value::Map).
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
#[serde(untagged)]
pub enum Value {
    /// Scalar bool value
    Bool(bool),
    /// Scalar string value
    String(String),
    /// Scalar char value
    Char(char),
    /// Map from a [String] key to [Value]
    Map(Map),
    /// Scalar enum variant
    Variant(String, Box<Value>),
    /// Struct enum variant
    StructVariant(String, Map),
    /// Scalar integer value
    Int(i64),
    /// Scalar float value
    Float(Float),
    /// List of [Value]s
    Seq(Vec<Value>),
    /// Unit type
    Unit,
}

pub type Map = BTreeMap<String, Value>;

/// Custom float wrapper
///
/// This custom wrapper allows the implementation of comparisons and orderings.
/// These are **not** meant to be consistent for numeric values.
/// Equality for this time is defined by equal bit representations.
/// This is especially important special values like NaN and infinity.
/// Ordering is done by utilizing [PartialOrd] and ordering the byte representation as a fallback.
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
pub struct Float(pub f64);

impl PartialEq for Float {
    fn eq(&self, other: &Self) -> bool {
        self.0.to_bits() == other.0.to_bits()
    }
}

impl Eq for Float {}

impl PartialOrd for Float {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Float {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.partial_cmp(other)
            .unwrap_or_else(|| self.0.to_bits().cmp(&other.0.to_bits()))
    }
}

impl From<Float> for f64 {
    fn from(value: Float) -> Self {
        value.0
    }
}

impl From<Float> for f32 {
    fn from(value: Float) -> Self {
        value.0 as f32
    }
}

impl<T> From<Option<T>> for Value
where
    T: Into<Value>,
{
    fn from(value: Option<T>) -> Self {
        match value {
            None => Value::Unit,
            Some(x) => x.into(),
        }
    }
}

#[cfg(feature = "py")]
#[derive(FromPyObject)]
enum PyValue {
    /// Scalar bool value
    Bool(bool),
    /// Scalar string value
    String(String),
    /// Scalar char value
    Char(char),
    /// Map from a [String] key to [Value]
    Map(BTreeMap<String, PyValue>),
    /// Scalar integer value
    Int(i64),
    /// Scalar float value
    Float(f64),
    /// List of [Value]s
    Seq(Vec<PyValue>),
}

// TODO add support for classes
#[cfg(feature = "py")]
impl From<PyValue> for Value {
    fn from(value: PyValue) -> Self {
        match value {
            PyValue::Bool(x) => Value::Bool(x),
            PyValue::String(x) => Value::String(x),
            PyValue::Char(x) => Value::Char(x),
            PyValue::Map(x) => Value::Map(x.into_iter().map(|(k, v)| (k, v.into())).collect()),
            PyValue::Int(x) => Value::Int(x),
            PyValue::Float(x) => Value::Float(Float(x)),
            PyValue::Seq(x) => Value::Seq(x.into_iter().map(Value::from).collect()),
        }
    }
}

#[cfg(feature = "py")]
impl<'source> FromPyObject<'source> for Value {
    fn extract(ob: &'source PyAny) -> PyResult<Self> {
        let py_value = PyValue::extract(ob)?;
        Ok(py_value.into())
    }
}
#[cfg(feature = "py")]
impl IntoPy<PyObject> for Value {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Value::Bool(x) => x.into_py(py),
            Value::String(x) => x.into_py(py),
            Value::Char(x) => x.into_py(py),
            Value::Int(x) => x.into_py(py),
            Value::Float(Float(x)) => x.into_py(py),
            Value::Map(x) => {
                let res = PyDict::new(py);
                for (k, v) in x {
                    res.set_item(k, v.into_py(py)).ok().unwrap();
                }
                res.into_py(py)
            }
            Value::Seq(s) => s
                .into_iter()
                .map(|x| x.into_py(py))
                .collect::<Vec<_>>()
                .into_py(py),
            Value::Unit => PyNone::get(py).into_py(py),
            Value::Variant(_, _) | Value::StructVariant(_, _) => unimplemented!(),
        }
    }
}
