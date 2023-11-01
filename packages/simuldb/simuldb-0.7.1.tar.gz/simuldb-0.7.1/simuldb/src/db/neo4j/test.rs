use arbitrary::Unstructured;
use log::info;
use neo4rs::{query, ConfigBuilder};
use test_log::test;
use uuid::Uuid;

use crate::db::{neo4j::Neo4j, testutils::round_trip};

fn get_db(_: Uuid) -> Neo4j {
    let user = std::env::var("SIMULDB_NEO4J_USER").unwrap_or("neo4j".to_string());
    let pass = std::env::var("SIMULDB_NEO4J_PASSWORD").unwrap_or("neo4j".to_string());
    let uri = std::env::var("SIMULDB_NEO4J_URI").unwrap_or("localhost:7687".to_string());
    info!("Connecting to {user}:{pass}@{uri}");
    Neo4j::new(
        ConfigBuilder::new()
            .user(&user)
            .password(&pass)
            .uri(&uri)
            .build()
            .expect("Invalid Neo4j configuration"),
    )
    .expect("Could not create Neo4j database")
}

#[test]
fn can_connect() {
    let neo4j = get_db(Uuid::new_v4());
    neo4j
        .run(query("SHOW USERS"))
        .expect("Failure to run query");
}

fn neo4j_round_trip(u: &mut Unstructured<'_>) -> arbitrary::Result<()> {
    round_trip(u, get_db)
}

#[test]
fn test_round_trip() {
    arbtest::builder().budget_ms(10_000).run(neo4j_round_trip);
}
