//! Deserialization from [Value]

use log::trace;
use paste::paste;
use serde::{
    de::{
        value::{MapDeserializer, SeqDeserializer, StrDeserializer},
        EnumAccess, IntoDeserializer, VariantAccess,
    },
    forward_to_deserialize_any, Deserialize, Deserializer,
};
use thiserror::Error;

use crate::value::{Float, Value};

type Result<T> = std::result::Result<T, DeserializationError>;

#[derive(Debug, Error)]
pub enum DeserializationError {
    #[error("Remaining value: {0:?}")]
    RemainingValue(Value),
    #[error("Expected {0}, got {1:?}")]
    Unexpected(&'static str, Value),
    #[error("Empty input")]
    EmptyInput,
    #[error("Unsupported type: {0}")]
    Unsupported(&'static str),
    #[error("Other error: {0}")]
    Other(String),
}

impl serde::de::Error for DeserializationError {
    fn custom<T>(msg: T) -> Self
    where
        T: std::fmt::Display,
    {
        DeserializationError::Other(format!("{msg}"))
    }
}

impl<'a> IntoDeserializer<'a, DeserializationError> for &'a Value {
    type Deserializer = ValueDeserializer<'a>;

    fn into_deserializer(self) -> Self::Deserializer {
        ValueDeserializer::from_value(self)
    }
}

impl<'a> IntoDeserializer<'a, DeserializationError> for &'a String {
    type Deserializer = StrDeserializer<'a, DeserializationError>;

    fn into_deserializer(self) -> Self::Deserializer {
        StrDeserializer::new(self)
    }
}

#[derive(Clone)]
pub struct ValueDeserializer<'de> {
    input: &'de Value,
}

impl<'de> ValueDeserializer<'de> {
    fn from_value(input: &'de Value) -> Self {
        ValueDeserializer { input }
    }
}

pub fn from_value<'a, T>(v: &'a Value) -> Result<T>
where
    T: Deserialize<'a>,
{
    let deserializer = ValueDeserializer::from_value(v);
    T::deserialize(deserializer)
}

macro_rules! de_unsup {
    ($t:ident) => {
        paste! {
            fn [<deserialize_ $t>]<V>(self, _: V) -> Result<V::Value>
            where
                V: serde::de::Visitor<'de>,
            {
                Err(DeserializationError::Unsupported(stringify!($t)))
            }
        }
    };
}

impl<'de> Deserializer<'de> for ValueDeserializer<'de> {
    type Error = DeserializationError;

    fn deserialize_any<V>(mut self, visitor: V) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        match self.input {
            Value::Bool(x) => visitor.visit_bool(*x),
            Value::Char(x) => visitor.visit_char(*x),
            Value::Map(v) => visitor.visit_map(MapDeserializer::new(v.iter())),
            Value::Variant(name, value) => {
                self.input = value;
                visitor.visit_enum(Enum::new(Some(name), self))
            }
            Value::StructVariant(_name, value) => {
                visitor.visit_map(MapDeserializer::new(value.iter()))
            }
            Value::Float(Float(x)) => visitor.visit_f64(*x),
            Value::Int(x) => visitor.visit_i64(*x),
            Value::String(x) => visitor.visit_str(x),
            Value::Seq(v) => visitor.visit_seq(SeqDeserializer::new(v.iter())),
            Value::Unit => visitor.visit_unit(),
        }
    }

    forward_to_deserialize_any! {
        bool i8 i16 i32 i64 u8 u16 u32 u64 f32 f64 char str string
        unit unit_struct newtype_struct seq tuple
        tuple_struct map
    }

    de_unsup!(bytes);
    de_unsup!(byte_buf);
    de_unsup!(ignored_any);

    fn deserialize_enum<V>(
        self,
        _name: &'static str,
        _variants: &'static [&'static str],
        visitor: V,
    ) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        visitor.visit_enum(Enum::new(None, self))
    }

    fn deserialize_struct<V>(
        self,
        _name: &'static str,
        _fields: &'static [&'static str],
        visitor: V,
    ) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        self.deserialize_map(visitor)
    }

    fn deserialize_identifier<V>(self, visitor: V) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        match self.input {
            Value::String(s) | Value::StructVariant(s, _) | Value::Variant(s, _) => {
                visitor.visit_str(s)
            }
            Value::Char(c) => visitor.visit_char(*c),
            _ => Err(DeserializationError::Unexpected(
                "identifier",
                self.input.clone(),
            )),
        }
    }

    fn deserialize_option<V>(self, visitor: V) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        if let Value::Unit = self.input {
            visitor.visit_none()
        } else {
            visitor.visit_some(self)
        }
    }
}

struct Enum<'a, 'de: 'a> {
    name: Option<&'a str>,
    de: ValueDeserializer<'de>,
}

impl<'de, 'a> Enum<'a, 'de> {
    fn new(name: Option<&'a str>, de: ValueDeserializer<'de>) -> Self {
        Enum { name, de }
    }
}

impl<'de, 'a> EnumAccess<'de> for Enum<'a, 'de> {
    type Error = DeserializationError;
    type Variant = Self;

    fn variant_seed<V>(self, seed: V) -> Result<(V::Value, Self::Variant)>
    where
        V: serde::de::DeserializeSeed<'de>,
    {
        match self.name {
            Some(n) => {
                let val = seed.deserialize(StrDeserializer::<Self::Error>::new(n))?;
                Ok((val, self))
            }
            None => {
                // TODO separate variant access type to avoid cloning
                let val = seed.deserialize(self.de.clone())?;
                Ok((val, self))
            }
        }
    }
}

impl<'de, 'a> VariantAccess<'de> for Enum<'a, 'de> {
    type Error = DeserializationError;

    fn unit_variant(self) -> Result<()> {
        Ok(())
    }

    fn newtype_variant_seed<T>(self, _seed: T) -> Result<T::Value>
    where
        T: serde::de::DeserializeSeed<'de>,
    {
        trace!("newtype variant: {:?}", self.de.input);
        todo!()
    }

    fn tuple_variant<V>(mut self, _len: usize, visitor: V) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        trace!("tuple variant: {:?}", self.de.input);
        match self.de.input {
            Value::Variant(_, v) => self.de.input = v,
            v => return Err(DeserializationError::Unexpected("tuple variant", v.clone())),
        }
        self.de.deserialize_seq(visitor)
    }

    fn struct_variant<V>(self, _fields: &'static [&'static str], visitor: V) -> Result<V::Value>
    where
        V: serde::de::Visitor<'de>,
    {
        trace!("struct variant: {:?}", self.de.input);
        match self.de.input {
            Value::StructVariant(_, v) => visitor.visit_map(MapDeserializer::new(v.iter())),
            v => Err(DeserializationError::Unexpected("tuple variant", v.clone())),
        }
    }
}
