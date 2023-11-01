//! Error types

use std::{
    backtrace::{Backtrace, BacktraceStatus},
    error::Error as StdError,
    fmt::{Debug, Display, Write},
};

use thiserror::Error;

use crate::value::SerializationError;

pub type Result<T> = std::result::Result<T, Error>;

/// Error and automatically captured backtrace
pub struct Error {
    kind: Box<ErrorKind>,
    backtrace: Backtrace,
}

impl Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Display::fmt(&self.kind, f)
    }
}

impl Debug for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        Debug::fmt(&self.kind, f)?;
        if self.backtrace.status() == BacktraceStatus::Captured {
            f.write_char('\n')?;
            Display::fmt(&self.backtrace, f)?;
        }
        Ok(())
    }
}

impl std::error::Error for Error {}

#[cfg(feature = "py")]
impl From<Error> for pyo3::PyErr {
    fn from(value: Error) -> pyo3::PyErr {
        // TODO select more accurate python error type
        pyo3::exceptions::PyException::new_err(value.to_string())
    }
}

impl From<Box<dyn StdError>> for Error {
    fn from(v: Box<dyn StdError>) -> Self {
        // TODO try to extract backtrace
        Error {
            kind: Box::new(ErrorKind::Other(v.to_string())),
            backtrace: Backtrace::capture(),
        }
    }
}

impl<T: Into<ErrorKind> + std::error::Error> From<T> for Error {
    fn from(v: T) -> Self {
        // capture backtrace if not already available
        let backtrace = std::error::request_value(&v).unwrap_or_else(Backtrace::capture);
        Error {
            kind: Box::new(v.into()),
            backtrace,
        }
    }
}

/// Internal error type
#[derive(Debug, Error)]
pub enum ErrorKind {
    #[error("Unsupported metadata: {0}")]
    UnsupportedMetadata(String),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
    #[cfg(feature = "json")]
    #[error("JSON error: {0}")]
    Json(#[from] serde_json::Error),
    #[cfg(feature = "neo4j")]
    #[error("Async error: {0}")]
    Neo4j(#[from] neo4rs::Error),
    #[cfg(feature = "neo4j")]
    #[error("Unsupported metadata format")]
    MetadataFormat,
    #[cfg(feature = "neo4j")]
    #[error("Invalid graph structure: {0}")]
    GraphStructure(String),
    #[error("Reading not supported by backend")]
    ReadUnsupported,
    #[error("Serialization error: {0}")]
    Serialization(#[from] SerializationError),
    #[error("Invalid UUID: {0}")]
    IdError(#[from] uuid::Error),
    #[error("Could not parse hex string: {0}")]
    HexParser(#[from] hex::FromHexError),
    #[error("{0}")]
    Other(String),
}
