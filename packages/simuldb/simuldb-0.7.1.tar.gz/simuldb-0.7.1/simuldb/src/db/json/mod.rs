//! JSON backed database

use std::{
    fs::{self, File},
    hash::{Hash, Hasher},
    path::PathBuf,
};

use highway::HighwayHasher;
use log::*;
#[cfg(feature = "py")]
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

use crate::{
    db::{Database, DatabaseSession},
    error::{Error, Result},
    value::{Float, Value},
    Dataset, Session,
};

#[cfg(test)]
mod test;

impl TryFrom<Value> for serde_json::Value {
    type Error = Error;

    fn try_from(value: Value) -> Result<Self> {
        match value {
            Value::Bool(x) => Ok(x.into()),
            Value::Char(x) => Ok(x.to_string().into()),
            Value::Map(x) => {
                let mut res = serde_json::Map::with_capacity(x.len());
                for (k, v) in &x {
                    res.insert(k.clone(), v.clone().try_into()?);
                }
                Ok(serde_json::Value::Object(res))
            }
            Value::Variant(x, _) => Ok(x.into()),
            Value::StructVariant(_, _) => todo!(),
            Value::Float(Float(x)) => Ok(x.into()),
            Value::Int(x) => Ok(x.into()),
            Value::String(x) => Ok(x.into()),
            Value::Seq(x) => {
                let y: Result<Vec<serde_json::Value>> =
                    x.into_iter().map(|x| x.try_into()).collect();
                Ok(serde_json::Value::Array(y?))
            }
            Value::Unit => Ok(().into()),
        }
    }
}

/// JSON backend
///
/// All data is saved in JSON files inside `json_folder`.
/// The session information is stored directly there with its hash (calculated with [HighwayHasher] for reprociblity) as a hex strings as filename.
/// This hash is also used to create a subfolder where all datasets are stored.
/// For those, the id is used as a filename.
///
/// A folder with one session and five datasets could look like this:
/// ```text
/// 9F03105D9451CC3A.json
/// 9F03105D9451CC3A
/// 9F03105D9451CC3A/96ae94e6-cc1a-4621-999c-32a72741e4e8.json
/// 9F03105D9451CC3A/4eac9469-09a4-484c-a7cd-b1aa37d91a6c.json
/// 9F03105D9451CC3A/b9b446a3-78a9-4fe5-b4c1-530759e33282.json
/// 9F03105D9451CC3A/a33a95e6-afd7-4cdf-8e66-54180a77312f.json
/// 9F03105D9451CC3A/c04a2a79-7b13-413f-8f35-523259937101.json
/// ```
#[derive(Debug, Clone, Serialize, Deserialize)]
#[cfg_attr(feature = "py", pyclass)]
pub struct Json {
    json_folder: PathBuf,
}

impl Json {
    /// Create new JSON backend
    ///
    /// # Arguments
    ///
    /// * `json_folder` folder that will contain all JSON files
    pub fn new<P: Into<PathBuf>>(json_folder: P) -> Self {
        Self {
            json_folder: json_folder.into(),
        }
    }
}

// TODO writing
#[cfg(feature = "py")]
#[pymethods]
impl Json {
    #[new]
    fn py_new(json_folder: String) -> Self {
        Self::new(json_folder)
    }

    fn get_sessions(&self) -> Result<Vec<JsonSession>> {
        self.get_json_sessions()
    }

    fn add_session(&mut self, session: Session) -> Result<JsonSession> {
        self.add_json_session(session)
    }

    fn __repr__(&self) -> String {
        format!("Json(path={})", self.json_folder.display())
    }
}

impl Database for Json {
    type Error = Error;

    fn add_session(
        &mut self,
        session: Session,
    ) -> Result<Box<dyn DatabaseSession<Error = Self::Error>>> {
        Ok(Box::new(self.add_json_session(session)?))
    }

    fn get_sessions(&self) -> Result<Vec<Box<dyn DatabaseSession<Error = Self::Error>>>> {
        Ok(self
            .get_json_sessions()?
            .into_iter()
            .map(|x| Box::new(x) as Box<dyn DatabaseSession<Error = Self::Error>>)
            .collect())
    }
}

impl Json {
    pub fn add_json_session(&mut self, session: Session) -> Result<JsonSession> {
        let mut hasher = HighwayHasher::default();
        session.hash(&mut hasher);
        let hash = format!("{:016X}", hasher.finish());
        let filename = format!("{hash}.json");
        info!("Hashed session {session:?} as {hash}");

        let mut path = self.json_folder.clone();
        fs::create_dir_all(&path)?;
        path.push(filename);
        let file = File::create(path)?;
        serde_json::to_writer(file, &session)?;

        let session_path = self.json_folder.clone();
        Ok(JsonSession::new(session, session_path))
    }

    pub fn get_json_sessions(&self) -> Result<Vec<JsonSession>> {
        let session_path = self.json_folder.clone();
        let res = fs::read_dir(&self.json_folder)
            .into_iter()
            .flatten()
            .filter_map(|x| x.ok())
            .inspect(|x| debug!("Trying to open session at {}", x.path().display()))
            .filter_map(|x| File::open(x.path()).ok())
            .filter_map(|x| -> Option<Session> {
                match serde_json::from_reader(x) {
                    Ok(x) => Some(x),
                    Err(e) => {
                        info!("Failed to deserialize session: {}", e);
                        None
                    }
                }
            })
            .map(move |x| JsonSession::new(x, session_path.clone()))
            .collect();
        Ok(res)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[cfg_attr(feature = "py", pyclass(get_all))]
/// Session representation in JSON backend
pub struct JsonSession {
    /// Session information
    session: Session,
    /// Folder with datasets
    path: PathBuf,
}

// TODO writing
#[cfg(feature = "py")]
#[pymethods]
impl JsonSession {
    #[getter]
    fn get_software(&self) -> crate::Software {
        self.session.software.clone()
    }

    #[getter]
    fn get_run(&self) -> crate::Run {
        self.session.run.clone()
    }

    fn __repr__(&self) -> String {
        format!(
            "JsonSession(software={}-{}, run={}, path={})",
            self.session.software.name,
            self.session.software.version,
            self.session.run.date,
            self.path.display()
        )
    }

    #[pyo3(name = "add_dataset")]
    fn py_add_dataset(&mut self, dataset: &Dataset) -> Result<()> {
        self.add_dataset(dataset)
    }

    #[pyo3(name = "get_datasets")]
    fn py_get_datasets(&self) -> Result<Vec<Dataset>> {
        self.get_datasets()
    }
}

impl JsonSession {
    /// Create new JSON session
    ///
    /// # Arguments
    ///
    /// * `session` session information
    /// * `path` folder with datasets
    pub fn new<P: Into<PathBuf>>(session: Session, path: P) -> Self {
        let mut path = path.into();
        let mut hasher = HighwayHasher::default();
        session.hash(&mut hasher);
        let hash = format!("{:016X}", hasher.finish());
        path.push(hash);
        Self { session, path }
    }
}

impl DatabaseSession for JsonSession {
    type Error = Error;

    fn session(&self) -> &Session {
        &self.session
    }

    fn add_dataset(&mut self, dataset: &crate::Dataset) -> Result<()> {
        info!("Adding dataset: {dataset:?}");
        let mut filename = self.path.clone();
        fs::create_dir_all(&filename)?;
        filename.push(format!("{}.json", dataset.id));
        debug!("Writing dataset to {}", filename.display());
        let file = File::create(&filename)?;
        serde_json::to_writer(file, &dataset)?;
        Ok(())
    }

    fn get_datasets(&self) -> Result<Vec<Dataset>> {
        debug!("Looking for datasets at {}", self.path.display());
        let res = fs::read_dir(&self.path)
            .into_iter()
            .flatten()
            .filter_map(|x| x.ok())
            .map(|x| File::open(x.path()))
            .filter_map(|x| x.ok())
            .filter_map(|x| -> Option<Dataset> { serde_json::from_reader(x).ok() })
            .collect();
        Ok(res)
    }
}
