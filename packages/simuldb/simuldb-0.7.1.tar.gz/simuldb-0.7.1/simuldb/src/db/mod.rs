//! Database backends
//!
//! This module contains both database backends and generic traits to represent them.

use std::{
    fmt::Debug,
    fs::{create_dir_all, File},
    io::{Seek, Write},
    path::{Path, PathBuf},
};

use log::info;
use serde::Serialize;
use uuid::Uuid;

use crate::{Dataset, Session};

#[cfg(feature = "json")]
pub mod json;
#[cfg(feature = "neo4j")]
pub mod neo4j;

#[cfg(test)]
mod testutils;

/// Database backend
///
/// Storage backend for the database.
// TODO allow deletion of sessions
pub trait Database: Debug {
    type Error: std::error::Error;

    /// Add a session to the database
    fn add_session(
        &mut self,
        session: Session,
    ) -> Result<Box<dyn DatabaseSession<Error = Self::Error>>, Self::Error>;

    /// Get an interation over sessions in the database
    #[allow(clippy::type_complexity)]
    fn get_sessions(
        &self,
    ) -> Result<Vec<Box<dyn DatabaseSession<Error = Self::Error>>>, Self::Error>;
}

impl<E> Database for Box<dyn Database<Error = E>>
where
    E: std::error::Error,
{
    type Error = E;

    fn add_session(
        &mut self,
        session: Session,
    ) -> Result<Box<dyn DatabaseSession<Error = Self::Error>>, Self::Error> {
        (**self).add_session(session)
    }

    fn get_sessions(
        &self,
    ) -> Result<Vec<Box<dyn DatabaseSession<Error = Self::Error>>>, Self::Error> {
        (**self).get_sessions()
    }
}

/// Database session
///
/// This represents access to a single session stored in the database
// TODO allow deletions of datasets
pub trait DatabaseSession: Debug {
    type Error: std::error::Error;

    /// Get session information
    fn session(&self) -> &Session;
    /// Add a dataset to the database
    fn add_dataset(&mut self, dataset: &Dataset) -> Result<(), Self::Error>;
    /// Get iterator over datasets in the session
    fn get_datasets(&self) -> Result<Vec<Dataset>, Self::Error>;
}

/// Wrapper for easier [Dataset] generation
///
/// This type can be used to write data to a file and then automatically generate an id and calculate a hash for the file.
/// The hash algorithm used is SHA-512 (see also [Dataset::from_file]).
///
/// This type implements [Write] and [Seek] and therefor can be used together with things like [serde_json::to_writer] or similar functions.
///
/// # Example
/// ```
/// # use simuldb::prelude::*;
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// #     std::env::set_current_dir(format!("{}/..", env!("CARGO_MANIFEST_DIR")))?; // change to top level directory
/// #     let mut json = Json::new("output/json");
/// #     let software = Software::new("example", "1.0", "now");
/// #     let run = Run::new("here", "now");
/// #     let session = Session::new(software, run);
/// #     let mut dbsession = json.add_session(session)?;
/// let mut writer = DatasetWriter::new("output/data")?;
/// serde_json::to_writer(&mut writer, &[0, 1, 2])?;
/// let dataset = writer.finalize(())?;
/// dbsession.add_dataset(&dataset)?;
/// #     Ok(())
/// # }
/// ```
#[cfg(feature = "sha")]
pub struct DatasetWriter {
    id: Uuid,
    file: File,
    path: PathBuf,
}

#[cfg(feature = "sha")]
impl DatasetWriter {
    /// Create new writer
    ///
    /// This generates an id uses this as a filename to create a file in `folder`.
    /// If the path did not exist before, parent folders are created.
    pub fn new<P: AsRef<Path>>(folder: P) -> Result<Self, std::io::Error> {
        let mut path: PathBuf = folder.as_ref().into();
        let id = Uuid::new_v4();
        create_dir_all(&path)?;
        path.push(format!("{id}"));
        let file = File::create(&path)?;
        Ok(Self { id, file, path })
    }

    /// Generate [Dataset]
    ///
    /// This uses [Dataset::from_file] to calculate a SHA-512 hash and generate a [Dataset].
    ///
    /// # Arguments
    ///
    /// * `metadata`: associated metadata, has to serializable to a [Map](crate::value::Value::Map)
    pub fn finalize<S: Serialize + Debug>(
        self,
        metadata: S,
    ) -> Result<Dataset, crate::error::Error> {
        Dataset::from_file(self.path, metadata, Some(self.id))
    }
}

#[cfg(feature = "sha")]
impl Write for DatasetWriter {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        self.file.write(buf)
    }

    fn flush(&mut self) -> std::io::Result<()> {
        self.file.flush()
    }
}

#[cfg(feature = "sha")]
impl Seek for DatasetWriter {
    fn seek(&mut self, pos: std::io::SeekFrom) -> std::io::Result<u64> {
        self.file.seek(pos)
    }
}

/// Transfer data from one [Database] to another
///
/// This function iterates over all sessions and the contained [Dataset]s and transfers the information.
/// No data is cleared, so if the target session was not empty before, the contents will differ.
pub fn transfer<A: Database + Debug, B: Database + Debug>(
    a: &A,
    b: &mut B,
) -> Result<(), Box<dyn std::error::Error>>
where
    A::Error: 'static,
    B::Error: 'static,
{
    info!("Transfering from {a:?} to {b:?}");
    for session in a.get_sessions()? {
        info!("Transfering session {:?}", session.session());
        let mut session_b = b.add_session(session.session().clone())?;
        for dataset in session.get_datasets()? {
            info!("Transfering dataset {dataset:?}");
            session_b.add_dataset(&dataset)?;
        }
    }
    Ok(())
}
