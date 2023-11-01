#![feature(error_generic_member_access, doc_auto_cfg)]
//! This library provides backend and format agnostic data storage for simulation results coupled with metadata about the used [Software] and the simulation [Run]
//!
//! The main use case is the following
//!
//! 1. generate data on a cluster and save it with JSON backend
//! 1. transfer data to Neo4j backend
//! 1. directly use Neo4j to select data
//!
//! Therefore the main goal is a simple solution for writing data and there are no plans to support advanched search or query features.
//!
//! Data storage is not handled by the database, only associated metadata.
//!
//! Currently two backends are included:
//! * [Json](db::json::Json), which saves everything in JSON files
//! * [Neo4j](db::neo4j::Neo4j), which uses a Neo4j database as backend (write only)
//!
//! Custom backends can be implemented via the [Database](db::Database) and [DatabaseSession](db::DatabaseSession) traits.
//! Sessions are meant to associate a [Dataset]s specific [Run] of a [Software].
//! [Dataset]s are references to data stored in a file of any arbitrary format.
//!
//! ## Features
//!
//! * `json` enable [Json](db::json::Json) backend
//! * `neo4j` enable [Neo4j](db::neo4j::Neo4j) backend
//! * `sha` enable [sha2] support for automatic hash calculations
//! * `arbitrary` enable support for [arbitrary] (required for tests)
//!
//! ## Example
//!
//! This creates a [Json](db::json::Json) based [Database](db::Database) and writes some arbitraty data to it.
//! Note that in order to create a session, usually the [vergen_session] macro will suffice.
//!
//! ```
//! use std::io::Write;
//! use serde::Serialize;
//! use simuldb::prelude::*;
//!
//! // Define a metadata type
//! #[derive(Debug, Serialize)]
//! struct Metadata {
//!     a: usize,
//!     b: String,
//! }
//!
//! fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     # std::env::set_current_dir(format!("{}/..", env!("CARGO_MANIFEST_DIR")))?; // change to top level directory
//!     // Create or open database
//!     let mut json = Json::new("output/json");
//!
//!     // Start new session which will contain references to the datasets
//!     let software = Software::new("example", "1.0", "now");
//!     let run = Run::new("here", "now");
//!     let session = Session::new(software, run);
//!     let mut json_session = json.add_session(session)?;
//!
//!     // Create a directory for the result data
//!     std::fs::create_dir_all("output/data")?;
//!
//!     // Generate some data and add it to the database
//!     for a in 0_usize..10 {
//!         // A DataWriter can be used to automatically calculate
//!         // the hash of a file and create a Dataset from it
//!         let mut writer = DatasetWriter::new("output/data")?;
//!
//!         // Write some data to the output file
//!         writeln!(writer, "a^2 = {}", a.pow(2))?;
//!
//!         // Generate metadata to associate with it
//!         let metadata = Metadata {
//!             a,
//!             b: "squaring".to_string(),
//!         };
//!
//!         // Add the corresponding dataset to the database
//!         let dataset = writer.finalize(metadata)?;
//!         json_session.add_dataset(&dataset)?;
//!     }
//!
//!     Ok(())
//! }
//! ```

use std::{collections::BTreeMap, fmt::Debug, fs::File, io::Read, path::Path};

#[cfg(feature = "arbitrary")]
use arbitrary::Arbitrary;
pub use chrono;
use log::*;
#[cfg(feature = "neo4j")]
pub use neo4rs;
#[cfg(feature = "py")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use value::Map;

use crate::{
    error::{ErrorKind, Result},
    value::{Value, ValueSerializer},
};

/// Commonly used structs, traits and macros
pub mod prelude {
    #[cfg(feature = "json")]
    pub use crate::db::json::Json;
    #[cfg(feature = "neo4j")]
    pub use crate::db::neo4j::Neo4j;
    #[cfg(feature = "sha")]
    pub use crate::db::DatasetWriter;
    pub use crate::{
        db::{Database, DatabaseSession},
        vergen_session, Dataset, Run, Session, Software,
    };
}

pub mod db;
pub mod error;
pub mod value;

/// Generate version for usage with [vergen_session]
#[macro_export]
#[cfg(feature = "git")]
macro_rules! vergen_version {
    () => {{
        concat!(env!("CARGO_PKG_VERSION"), "-", env!("VERGEN_GIT_SHA")).to_string()
    }};
}
/// Generate version for usage with [vergen_session]
#[macro_export]
#[cfg(not(feature = "git"))]
macro_rules! vergen_version {
    () => {{
        env!("CARGO_PKG_VERSION").to_string()
    }};
}

/// Generate session object automatically by extracting data from environment variables provided by Cargo and vergen
///
/// This requires setting up a suitable build script that enables VERGEN_BUILD_TIMESTAMP (see the examples folder).
/// If the `git` feature is set, the version number will also contain the short SHA hash of the current commit (this requires VERGEN_GIT_SHA).
///
/// The following build script can be used to set up the required configuration:
///
/// ```rust,ignore
/// use vergen::EmitBuilder;
///
/// fn main() -> Result<(), Box<dyn std::error::Error>> {
///     println!("cargo:rerun-if-changed=build.rs");
///     EmitBuilder::builder()
///         .build_timestamp()
///         .git_sha(true)
///         .emit()?;
///     Ok(())
/// }
/// ```
#[macro_export]
macro_rules! vergen_session {
    () => {{
        ::simuldb::Session {
            software: ::simuldb::Software {
                name: env!("CARGO_CRATE_NAME").to_string(),
                version: ::simuldb::vergen_version!(),
                compile_time: env!("VERGEN_BUILD_TIMESTAMP").to_string(),
            },
            run: ::simuldb::Run {
                date: ::simuldb::chrono::offset::Utc::now().to_rfc3339(),
                host: ::hostname::get()
                    .ok()
                    .and_then(|x| x.into_string().ok())
                    .unwrap_or_default(),
            },
        }
    }};
}

/// Combination of [Software] and [Run] metadata associated with the data of one run
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Hash, PartialOrd, Ord)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
#[cfg_attr(feature = "py", pyclass(set_all, get_all))]
pub struct Session {
    /// Used software
    pub software: Software,
    /// Run information
    pub run: Run,
}

impl Session {
    pub fn new(software: Software, run: Run) -> Self {
        Self { software, run }
    }
}

#[cfg(feature = "py")]
#[pymethods]
impl Session {
    #[new]
    fn py_new(software: Software, run: Run) -> Self {
        Self::new(software, run)
    }

    fn __repr__(&self) -> String {
        format!(
            "Session(software={}-{}, run={})",
            self.software.name, self.software.version, self.run.date
        )
    }
}

/// [Run] metadata containing information about the machine and the start time
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Hash, PartialOrd, Ord)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
#[cfg_attr(feature = "py", pyclass(set_all, get_all))]
pub struct Run {
    /// Start time of run
    pub date: String,
    /// Hostname of machine
    pub host: String,
}

impl Run {
    pub fn new<S, T>(date: S, host: T) -> Self
    where
        S: ToString,
        T: ToString,
    {
        Self {
            date: date.to_string(),
            host: host.to_string(),
        }
    }
}

#[cfg(feature = "py")]
#[pymethods]
impl Run {
    #[new]
    fn py_new(date: &str, host: &str) -> Self {
        Self::new(date, host)
    }

    fn __repr__(&self) -> String {
        format!("Run(date={}, host={})", self.date, self.host)
    }
}

/// Version information about the used [Software]
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Hash, PartialOrd, Ord)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
#[cfg_attr(feature = "py", pyclass(set_all, get_all))]
pub struct Software {
    /// Name of software
    pub name: String,
    /// Version of software
    pub version: String,
    /// Compilation time
    pub compile_time: String,
}

impl Software {
    /// Create new [Software]
    ///
    /// # Arguments
    ///
    /// * `name` name of software
    /// * `version` version of software
    /// * `compile_time` compilation time
    pub fn new<S, T, U>(name: S, version: T, compile_time: U) -> Self
    where
        S: ToString,
        T: ToString,
        U: ToString,
    {
        Self {
            name: name.to_string(),
            version: version.to_string(),
            compile_time: compile_time.to_string(),
        }
    }
}

#[cfg(feature = "py")]
#[pymethods]
impl Software {
    #[new]
    fn py_new(name: &str, version: &str, compile_time: &str) -> Self {
        Self::new(name, version, compile_time)
    }

    fn __repr__(&self) -> String {
        format!(
            "Software(name={}, version={}, compile_time={})",
            self.name, self.version, self.compile_time
        )
    }
}

/// Reference to one data file
///
/// This stores an `id` to identify to file, a `hash` to verify it and some metadata that is associated with the data.
/// Note that this does not specify exactly where the file is stored.
///
/// By default [sha2] is used to generate a SHA-512 hash of the file if the `sha` feature is enabled.
/// Manually calculating the hash and using `from_hash` allows for other hash functions as long as the hash is representable as [`Vec<u8>`](Vec).
///
/// Every time that is serializable into a [Map] can be used as metadata.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, PartialOrd, Ord)]
#[cfg_attr(feature = "arbitrary", derive(Arbitrary))]
#[cfg_attr(feature = "py", pyclass)]
pub struct Dataset {
    /// Id of file
    pub id: Uuid,
    /// Hash of file
    pub hash: Vec<u8>,
    /// Metadata associated with dataset
    metadata: Map,
}

/// Generate [Map] object from serializable metadata.
///
/// This will serialize it as [Value] first and then extract the [Map].
/// Unit types are also supported and will be serialized as an empty map.
/// If `metadata` serializes to anything except a map, an error of kind [UnsupportedMetadata](error::ErrorKind::UnsupportedMetadata) is returned.
pub fn serialize_metadata<S: Serialize + Debug>(metadata: S) -> Result<Map> {
    match metadata.serialize(ValueSerializer) {
        Ok(Value::Map(map)) => Ok(map),
        Ok(Value::Unit) => Ok(BTreeMap::new()),
        Ok(_) => Err(ErrorKind::UnsupportedMetadata(format!("{metadata:?} is not a map",)).into()),
        Err(e) => Err(ErrorKind::UnsupportedMetadata(format!("{e}")).into()),
    }
}

impl Dataset {
    /// Generate dataset object from externally calculated `hash`
    ///
    /// If no id is specified, a random one will be generated
    ///
    /// # Arguments
    /// * `hash`: hash of the data file
    /// * `metadata`: associated metadata, has to be serializable to a [Map]
    /// * `id`: id of the file
    pub fn from_hash<S: Serialize + Debug>(
        hash: Vec<u8>,
        metadata: S,
        id: Option<Uuid>,
    ) -> Result<Self> {
        let id = id.unwrap_or_else(Uuid::new_v4);

        debug!("Serializing metadata: {metadata:?}");
        let metadata = serialize_metadata(metadata)?;
        Ok(Dataset { id, hash, metadata })
    }

    /// Generate dataset object by calulating the SHA-512 hash of an existing file
    ///
    /// If no id is specified, a random one will be generated
    ///
    /// # Arguments
    /// * `path`: path to the data file
    /// * `metadata`: associated metadata, has to be serializable to a [Map]
    /// * `id`: id of the file
    #[cfg(feature = "sha")]
    pub fn from_file<P: AsRef<Path>, S: Serialize + Debug>(
        path: P,
        metadata: S,
        id: Option<Uuid>,
    ) -> Result<Self> {
        use sha2::{Digest, Sha512};

        let id = id.unwrap_or_else(Uuid::new_v4);

        let hash = {
            let mut hasher = Sha512::new();
            let mut buffer = Vec::new();
            File::open(path)?.read_to_end(&mut buffer)?;
            hasher.update(buffer);
            hasher.finalize().as_slice().to_vec()
        };

        debug!("Serializing metadata: {metadata:?}");
        let metadata = serialize_metadata(metadata)?;
        Ok(Dataset { id, hash, metadata })
    }
}

#[cfg(feature = "py")]
#[pymethods]
impl Dataset {
    #[new]
    fn py_new(
        id: Option<&str>,
        metadata: Option<BTreeMap<String, Value>>,
        hash: Option<&str>,
        path: Option<&str>,
    ) -> Result<Dataset> {
        let id = id.map(Uuid::parse_str).transpose()?;
        match (hash, path) {
            (Some(hash), None) => Self::from_hash(hex::decode(hash)?, metadata, id),
            (None, Some(path)) => Self::from_file(path, metadata, id),
            _ => Err(ErrorKind::Other(
                "Exactly one of hash and path has to be specified".to_string(),
            )
            .into()),
        }
    }

    fn __repr__(&self) -> String {
        format!("Dataset(id={}, hash={})", self.id, hex::encode(&self.hash))
    }

    #[getter]
    fn get_id(&self) -> String {
        self.id.to_string()
    }

    #[getter]
    fn get_hash(&self) -> String {
        hex::encode(&self.hash)
    }

    #[getter]
    fn get_metadata(&self) -> Result<Value> {
        Ok(Value::Map(serialize_metadata(&self.metadata)?))
    }
}

// TODO test for python
#[cfg(feature = "py")]
#[pymodule]
fn simuldb(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Session>()?;
    m.add_class::<Software>()?;
    m.add_class::<Run>()?;
    m.add_class::<Dataset>()?;

    #[cfg(feature = "json")]
    {
        m.add_class::<db::json::Json>()?;
        m.add_class::<db::json::JsonSession>()?;
    }

    #[cfg(feature = "neo4j")]
    {
        m.add_class::<db::neo4j::Neo4j>()?;
        m.add_class::<db::neo4j::Neo4jSession>()?;
    }

    Ok(())
}
