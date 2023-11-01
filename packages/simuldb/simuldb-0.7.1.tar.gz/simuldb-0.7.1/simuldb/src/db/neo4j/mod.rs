//! Neo4j backed database

use std::{
    collections::{BTreeMap, VecDeque},
    fmt::{Debug, Formatter},
    sync::Arc,
};

use neo4rs::{query, Config, Graph, Node, Query, RowStream};
#[cfg(feature = "py")]
use pyo3::prelude::*;
use tokio::runtime::Runtime;
use uuid::Uuid;

use crate::{
    db::{Database, DatabaseSession},
    error::{Error, ErrorKind},
    value::{Float, Map, Value},
    Dataset, Run, Session, Software,
};

#[cfg(test)]
mod test;

pub type Result<T> = std::result::Result<T, Error>;

#[derive(Clone)]
#[cfg_attr(feature = "py", pyclass)]
/// Neo4j backend
///
/// Currently, only writing is supported.
///
/// Add metadata is saved as nodes in a Neo4j database.
/// Software and runs are saved as nodes and linked to datasets with relations of type `uses` and `part_of` respectively.
///
/// # Metadata storage
///
/// Metadata can be of any type that can be serializable to a map, including arbitrarily nested types.
/// Neo4j does not support values that are maps themselves.
/// To circumvent this, each leaf of the metadata tree is saved as a separate node containing the path to it and its value.
pub struct Neo4j {
    /// Neo4j configuration
    config: Config,
    /// Neo4j connection
    graph: Arc<Graph>,
    /// Async runtime
    rt: Arc<Runtime>,
}

impl Debug for Neo4j {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "Neo4j ({:?})", self.config)
    }
}

impl Neo4j {
    /// Create new Neo4j backend
    ///
    /// # Arguments
    ///
    /// * `config` Neo4j connection configuration
    pub fn new(config: Config) -> Result<Self> {
        let rt = Arc::new(Runtime::new()?);
        Ok(Neo4j {
            graph: Arc::new(rt.block_on(Graph::connect(config.clone()))?),
            config,
            rt,
        })
    }

    /// Run query on graph and ignore result
    pub fn run(&self, q: Query) -> Result<()> {
        Ok(self.rt.block_on(async { self.graph.run(q).await })?)
    }

    /// Run query on graph and return results
    pub fn execute(&self, q: Query) -> Result<RowStream> {
        Ok(self.rt.block_on(async { self.graph.execute(q).await })?)
    }
}

// TODO writing
#[cfg(feature = "py")]
#[pymethods]
impl Neo4j {
    #[new]
    #[pyo3(signature = (uri = "localhost:7687", user = "neo4j", password = "neo4j"))]
    fn py_new(uri: &str, user: &str, password: &str) -> Result<Self> {
        let config = neo4rs::ConfigBuilder::new()
            .uri(uri)
            .user(user)
            .password(password)
            .build()?;
        Self::new(config)
    }

    fn add_session(&mut self, session: Session) -> Result<Neo4jSession> {
        self.add_neo4j_session(session)
    }
    fn get_sessions(&self) -> Result<Vec<Neo4jSession>> {
        self.get_neo4j_sessions()
    }

    fn __repr__(&self) -> String {
        "Neo4j()".to_string()
    }
}

impl Database for Neo4j {
    type Error = Error;

    fn add_session(
        &mut self,
        session: Session,
    ) -> Result<Box<dyn DatabaseSession<Error = Self::Error>>> {
        Ok(Box::new(self.add_neo4j_session(session)?))
    }

    fn get_sessions(&self) -> Result<Vec<Box<dyn DatabaseSession<Error = Self::Error>>>> {
        Ok(self
            .get_neo4j_sessions()?
            .into_iter()
            .map(|x| Box::new(x) as Box<dyn DatabaseSession<Error = Self::Error>>)
            .collect())
    }
}

impl Neo4j {
    pub fn add_neo4j_session(&mut self, session: Session) -> Result<Neo4jSession> {
        self.rt.block_on(async {
            let q = query(
                "
                MERGE (s:software { name: $software_name, version: $software_version, compile_time: $software_time })
                MERGE (r:run { name: $run_name, date: $run_date, host: $run_host })
                MERGE (r)-[:uses]->(s)
                RETURN id(s), id(r)
            ",
            )
                .param("software_name", session.software.name.as_str())
                .param("software_version", session.software.version.as_str())
                .param("software_time", session.software.compile_time.as_str())
                .param("run_name", session.run.date.to_string().as_str())
                .param("run_date", session.run.date.to_string().as_str())
                .param("run_host", session.run.host.as_str());
            let row = self
                .graph
                .execute(q)
                .await?
                .next()
                .await?
                .expect("Failure while adding session");
            let software_id = row.get("id(s)").expect("Failure while adding software");
            let run_id = row.get("id(r)").expect("Failure while adding run");

            Ok(Neo4jSession {
                session,
                rt: self.rt.clone(),
                graph: self.graph.clone(),
                run_id,
                software_id,
            })
        })
    }

    pub fn get_neo4j_sessions(&self) -> Result<Vec<Neo4jSession>> {
        self.rt.block_on(async {
            let mut res: Vec<_> = Vec::new();
            let mut rows = self
                .graph
                .execute(query("MATCH (r:run)-[:uses]->(s:software) RETURN r, s"))
                .await?;

            while let Some(row) = rows.next().await? {
                let run_node: Node = row.get("r").expect("Run node not found");
                let software_node: Node = row.get("s").expect("Software node not found");
                let run = Run::new(
                    run_node
                        .get::<String>("date")
                        .ok_or(ErrorKind::GraphStructure(
                            "run does not contain date".to_string(),
                        ))?,
                    run_node
                        .get::<String>("name")
                        .ok_or(ErrorKind::GraphStructure(
                            "run does not contain date".to_string(),
                        ))?,
                );
                let software = Software::new(
                    software_node
                        .get::<String>("name")
                        .ok_or(ErrorKind::GraphStructure(
                            "software does not contain name".to_string(),
                        ))?,
                    software_node
                        .get::<String>("version")
                        .ok_or(ErrorKind::GraphStructure(
                            "software does not contain version".to_string(),
                        ))?,
                    software_node.get::<String>("compile_time").ok_or(
                        ErrorKind::GraphStructure(
                            "software does not contain compile_time".to_string(),
                        ),
                    )?,
                );
                let session = Session::new(software, run);
                res.push(Neo4jSession {
                    session,
                    rt: self.rt.clone(),
                    graph: self.graph.clone(),
                    run_id: run_node.id(),
                    software_id: software_node.id(),
                })
            }
            Ok(res)
        })
    }
}

#[derive(Clone)]
#[cfg_attr(feature = "py", pyclass)]
/// Session representation in Neo4j backend
pub struct Neo4jSession {
    /// Session information
    session: Session,
    /// Async runtime
    rt: Arc<Runtime>,
    /// Neo4j connection
    graph: Arc<Graph>,
    /// ID of [Run](crate::Run) node
    run_id: i64,
    /// ID of [Software](crate::Software) node
    software_id: i64,
}

impl Debug for Neo4jSession {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{:?} (Run {} Software {})",
            self.session, self.run_id, self.software_id
        )
    }
}

// TODO writing
#[cfg(feature = "py")]
#[pymethods]
impl Neo4jSession {
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
            "Neo4jSession(software={}-{}, run={}, software_id={}, run_id={})",
            self.session.software.name,
            self.session.software.version,
            self.session.run.date,
            self.software_id,
            self.run_id
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

// TODO add char
#[derive(Debug, Clone)]
pub enum ParameterValue {
    Bool(bool),
    String(String),
    Int(i64),
    Float(f64),
    BoolSeq(Vec<bool>),
    StringSeq(Vec<String>),
    IntSeq(Vec<i64>),
    FloatSeq(Vec<f64>),
}

macro_rules! seq_conv {
    ($vec:ident, $var:path, $seqvar:ident, $dec:expr, $p:pat) => {{
        Some(ParameterValue::$seqvar(
            $vec.iter()
                .filter_map(|x| {
                    if let $var($p) = x {
                        Some($dec.clone())
                    } else {
                        None
                    }
                })
                .collect(),
        ))
    }};
}

impl ParameterValue {
    pub fn scalar(v: Value) -> Option<ParameterValue> {
        match v {
            Value::Bool(x) => Some(ParameterValue::Bool(x)),
            Value::String(x) => Some(ParameterValue::String(x)),
            Value::Char(x) => Some(ParameterValue::String(x.to_string())),
            Value::Int(x) => Some(ParameterValue::Int(x)),
            Value::Float(Float(x)) => Some(ParameterValue::Float(x)),
            _ => None,
        }
    }

    pub fn sequence(v: Vec<Value>) -> Option<ParameterValue> {
        if v.is_empty() {
            return None;
        }
        match &v[0] {
            Value::Bool(_) => seq_conv!(v, Value::Bool, BoolSeq, y, y),
            Value::String(_) => seq_conv!(v, Value::String, StringSeq, y, y),
            Value::Char(_) => seq_conv!(v, Value::String, StringSeq, y.to_string(), y),
            Value::Int(_) => seq_conv!(v, Value::Int, IntSeq, y, y),
            Value::Float(_) => seq_conv!(v, Value::Float, FloatSeq, y, Float(y)),
            _ => None,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Parameter {
    name: String,
    path: VecDeque<String>,
    value: Option<ParameterValue>,
}

fn flatten_single(
    res: &mut Vec<Parameter>,
    name: String,
    value: Value,
    mut path: VecDeque<String>,
) {
    match value {
        Value::Bool(_) | Value::String(_) | Value::Char(_) | Value::Int(_) | Value::Float(_) => res
            .push(Parameter {
                path,
                name,
                value: ParameterValue::scalar(value),
            }),
        Value::Seq(v) => res.push(Parameter {
            path,
            name,
            value: ParameterValue::sequence(v),
        }),
        Value::Map(m) => {
            let inner = flatten_map(&m);
            res.extend(inner.into_iter().map(|mut x| {
                x.path.push_front(name.clone());
                x
            }));
        }
        Value::Variant(inner_name, inner_v) => {
            path.push_front(name);
            flatten_single(res, inner_name.clone(), *inner_v, path);
        }
        Value::StructVariant(variant_name, m) => {
            res.push(Parameter {
                path,
                name: variant_name.clone(),
                value: None,
            });
            let inner = flatten_map(&m);
            res.extend(inner.into_iter().map(|mut x| {
                x.path.push_front(name.clone());
                x
            }));
        }
        Value::Unit => res.push(Parameter {
            path,
            name,
            value: None,
        }),
    }
}

fn flatten_map(metadata: &BTreeMap<String, Value>) -> Vec<Parameter> {
    let mut res = Vec::new();
    for (k, v) in metadata {
        let path = VecDeque::new();
        flatten_single(&mut res, k.clone(), v.clone(), path);
    }
    res
}

fn insert_path_to_map(map: &mut Map, mut path: VecDeque<String>, value: Value) {
    if let Some(head) = path.pop_front() {
        if path.is_empty() {
            map.insert(head, value);
        } else if let Value::Map(ref mut inner_map) =
            map.entry(head).or_insert_with(|| Value::Map(Map::new()))
        {
            insert_path_to_map(inner_map, path, value);
        }
    }
}

impl DatabaseSession for Neo4jSession {
    type Error = Error;

    fn session(&self) -> &Session {
        &self.session
    }

    fn add_dataset(&mut self, data: &Dataset) -> Result<()> {
        self.rt.block_on(async {
            let q = query(
                "
            MERGE (f:file { name: $file_name, hash: $file_hash })
            WITH f
            MATCH (s:software) WHERE id(s) = $software_id
            MATCH (r:run) WHERE id(r) = $run_id
            MERGE (f)-[:uses]->(s)
            MERGE (f)-[:part_of]->(r)

            RETURN id(f)
            ",
            )
            .param("file_name", data.id.to_string())
            .param("file_hash", hex::encode(&data.hash))
            .param("software_id", self.software_id)
            .param("run_id", self.run_id);
            let row = self
                .graph
                .execute(q)
                .await?
                .next()
                .await?
                .expect("Failure while adding file");
            let file_id: i64 = row.get("id(f)").expect("Failure while adding file");

            let parameters = flatten_map(&data.metadata);
            for mut p in parameters {
                p.path.push_back(p.name.clone());
                let q = match p.value {
                    Some(value) => {
                        let q2 = query(
                            "
                        MERGE (p:data { name: $name, path: $path, value: $value, type: $type })
                        WITH p
                        MATCH (f:file) WHERE id(f) = $file_id
                        MERGE (f)-[:param]->(p)",
                        )
                        .param("name", p.name)
                        .param("path", Vec::from(p.path))
                        .param("file_id", file_id);
                        match value {
                            ParameterValue::Bool(x) => q2.param("value", x).param("type", "bool"),
                            ParameterValue::String(x) => {
                                q2.param("value", x).param("type", "string")
                            }
                            ParameterValue::Int(x) => q2.param("value", x).param("type", "int"),
                            ParameterValue::Float(x) => q2.param("value", x).param("type", "float"),
                            ParameterValue::BoolSeq(x) => {
                                q2.param("value", x).param("type", "boolseq")
                            }
                            ParameterValue::StringSeq(x) => {
                                q2.param("value", x).param("type", "stringseq")
                            }
                            ParameterValue::IntSeq(x) => {
                                q2.param("value", x).param("type", "intseq")
                            }
                            ParameterValue::FloatSeq(x) => {
                                q2.param("value", x).param("type", "floatseq")
                            }
                        }
                    }
                    None => query(
                        "
                        MERGE (p:data { name: $name, path: $path })
                        WITH p
                        MATCH (f:file) WHERE id(f) = $file_id
                        MERGE (f)-[:param]->(p)",
                    )
                    .param("name", p.name)
                    .param("path", Vec::from(p.path))
                    .param("file_id", file_id),
                };
                self.graph.run(q).await?;
            }

            Result::<()>::Ok(())
        })
    }

    fn get_datasets(&self) -> Result<Vec<Dataset>> {
        self.rt.block_on(async {
            let mut res = Vec::new();
            let mut rows = self
                .graph
                .execute(query(
                    "
                MATCH (f:file)
                OPTIONAL MATCH (f)-[:param]->(d:data)
                RETURN f, collect(d)
            ",
                ))
                .await?;
            while let Some(row) = rows.next().await? {
                let file_node: Node = row.get("f").expect("Failure while deconstructing row");
                let param_nodes: Vec<Node> = row
                    .get("collect(d)")
                    .expect("Failure while deconstructing row");

                let file_hash: Vec<u8> = hex::decode(file_node.get::<String>("hash").ok_or(
                    ErrorKind::GraphStructure("File does not contain hash".to_string()),
                )?)
                .map_err(|e| ErrorKind::GraphStructure(e.to_string()))?;
                let file_name: String = file_node.get("name").ok_or(ErrorKind::GraphStructure(
                    "File does not contain name".to_string(),
                ))?;
                let mut metadata = Map::new();

                for node in param_nodes {
                    let path: VecDeque<String> = node
                        .get::<Vec<String>>("path")
                        .ok_or(ErrorKind::GraphStructure(
                            "Parameter does not contain path".to_string(),
                        ))?
                        .into();
                    match node.get::<String>("type") {
                        Some(type_name) => {
                            let value = match type_name.as_str() {
                                "bool" => Value::Bool(node.get("value").ok_or(
                                    ErrorKind::GraphStructure(
                                        "Parameter does not contain value".to_string(),
                                    ),
                                )?),
                                "string" => Value::String(node.get("value").ok_or(
                                    ErrorKind::GraphStructure(
                                        "Parameter does not contain value".to_string(),
                                    ),
                                )?),
                                "int" => Value::Int(node.get("value").ok_or(
                                    ErrorKind::GraphStructure(
                                        "Parameter does not contain value".to_string(),
                                    ),
                                )?),
                                "float" => Value::Float(Float(node.get("value").ok_or(
                                    ErrorKind::GraphStructure(
                                        "Parameter does not contain value".to_string(),
                                    ),
                                )?)),
                                "boolseq" => Value::Seq(
                                    node.get::<Vec<bool>>("value")
                                        .ok_or(ErrorKind::GraphStructure(
                                            "Parameter does not contain value".to_string(),
                                        ))?
                                        .into_iter()
                                        .map(Value::Bool)
                                        .collect(),
                                ),
                                "stringseq" => Value::Seq(
                                    node.get::<Vec<String>>("value")
                                        .ok_or(ErrorKind::GraphStructure(
                                            "Parameter does not contain value".to_string(),
                                        ))?
                                        .into_iter()
                                        .map(Value::String)
                                        .collect(),
                                ),
                                "intseq" => Value::Seq(
                                    node.get::<Vec<i64>>("value")
                                        .ok_or(ErrorKind::GraphStructure(
                                            "Parameter does not contain value".to_string(),
                                        ))?
                                        .into_iter()
                                        .map(Value::Int)
                                        .collect(),
                                ),
                                "floatseq" => Value::Seq(
                                    node.get::<Vec<f64>>("value")
                                        .ok_or(ErrorKind::GraphStructure(
                                            "Parameter does not contain value".to_string(),
                                        ))?
                                        .into_iter()
                                        .map(|x| Value::Float(Float(x)))
                                        .collect(),
                                ),
                                _ => unreachable!(),
                            };
                            insert_path_to_map(&mut metadata, path, value);
                        }
                        None => insert_path_to_map(&mut metadata, path, Value::Unit),
                    }
                }

                res.push(Dataset::from_hash(
                    file_hash,
                    metadata,
                    Some(Uuid::parse_str(&file_name).map_err(|e| {
                        ErrorKind::GraphStructure(format!("Invalid UUID string: {e}"))
                    })?),
                )?);
            }

            Ok(res)
        })
    }
}
