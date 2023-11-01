use std::collections::BTreeMap;

use arbitrary::{Arbitrary, Result, Unstructured};
use log::info;
use serde::{Deserialize, Serialize};
use test_log::test;

use crate::value::{de::from_value, ValueSerializer};

#[derive(Debug, Serialize, Deserialize, Arbitrary, PartialEq, Eq, PartialOrd, Ord)]
struct ComplexStruct {
    uint: u32,
    tuple: (u8, u16, u32, i8, i16, i32, i64, isize),
    optional_bool: Option<bool>,
    cplx_enum: ComplexEnum,
    map: BTreeMap<String, ComplexStruct>,
    vec: Vec<String>,
    string: String,
}

#[derive(Debug, Serialize, Deserialize, Arbitrary, Hash, PartialEq, Eq, PartialOrd, Ord)]
enum ComplexEnum {
    A,
    B(i64, u8),
    C {},
    D { a: u32, b: Box<ComplexEnum> },
}

fn serialize_complex_struct(u: &mut Unstructured<'_>) -> Result<()> {
    let s: ComplexStruct = u.arbitrary()?;
    let _value = s
        .serialize(ValueSerializer)
        .expect("Failed to serialize complex struct");
    Ok(())
}

#[test]
fn test_serialize_complex_struct() {
    arbtest::builder()
        .budget_ms(10_000)
        .run(serialize_complex_struct);
}

fn arbitrary_json_value(u: &mut Unstructured<'_>) -> Result<serde_json::Value> {
    let v: crate::value::Value = u.arbitrary()?;
    Ok(serde_json::to_value(v).expect("Could not serialize value to JSON"))
}

fn json_value_round_trip(u: &mut Unstructured<'_>) -> Result<()> {
    let v: serde_json::Value = normalize(arbitrary_json_value(u)?);
    info!("Testing round trip for {v:#?}");
    let ser = v
        .serialize(ValueSerializer)
        .expect("Could not serialize value");
    info!("Serialized to {ser:?}");
    let v2: serde_json::Value = from_value(&ser).expect("Could not serialize value");
    info!("Got {v2:#?}");
    assert!(values_equal(&v, &v2));
    Ok(())
}

fn normalize(a: serde_json::Value) -> serde_json::Value {
    match a {
        serde_json::Value::Number(n) => serde_json::Value::Number(match n.as_i64() {
            Some(x) => x.into(),
            None => serde_json::value::Number::from_f64(n.as_f64().unwrap_or_default()).unwrap_or(
                serde_json::value::Number::from_f64(0.).expect("Failed to create number"),
            ),
        }),
        serde_json::Value::Array(x) => {
            serde_json::Value::Array(x.into_iter().map(normalize).collect())
        }
        serde_json::Value::Object(x) => {
            serde_json::Value::Object(x.into_iter().map(|(k, v)| (k, normalize(v))).collect())
        }
        _ => a,
    }
}

fn values_equal(a: &serde_json::Value, b: &serde_json::Value) -> bool {
    match (a, b) {
        (serde_json::Value::Number(n), serde_json::Value::Number(m)) => {
            if let (Some(x), Some(y)) = (n.as_i64(), m.as_i64()) {
                return x == y;
            }
            if let (Some(x), Some(y)) = (n.as_u64(), m.as_u64()) {
                return x == y;
            }
            if let (Some(x), Some(y)) = (n.as_f64(), m.as_f64()) {
                return x == y;
            }
            false
        }
        _ => a == b,
    }
}

#[test]
fn test_serde_json_round_trip() {
    arbtest::builder()
        .budget_ms(10_000)
        .run(json_value_round_trip);
}

fn struct_round_trip(u: &mut Unstructured<'_>) -> Result<()> {
    let v: ComplexStruct = u.arbitrary()?;
    info!("Testing round trip for {v:#?}");
    let ser = v
        .serialize(ValueSerializer)
        .expect("Could not serialize value");
    info!("Serialized to {ser:#?}");
    let v2: ComplexStruct = from_value(&ser).expect("Could not serialize complex struct");
    info!("Got {v2:#?}");
    assert_eq!(&v, &v2);
    Ok(())
}

#[test]
fn test_struct_round_trip() {
    arbtest::builder().budget_ms(10_000).run(struct_round_trip);
}
