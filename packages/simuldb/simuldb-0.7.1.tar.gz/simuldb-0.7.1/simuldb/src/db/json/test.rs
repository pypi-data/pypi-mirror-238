use std::{
    env::{self, temp_dir},
    fs::remove_dir_all,
};

use arbitrary::Unstructured;
use log::*;
use test_log::test;
use uuid::Uuid;

use crate::db::{json::Json, testutils::round_trip};

trace::init_depth_var!();

fn get_db(u: Uuid) -> Json {
    let mut folder = env::temp_dir();
    folder.push("simuldb");
    folder.push(format!("{u}"));
    info!("Using path {}", folder.display());
    Json::new(folder)
}

fn json_round_trip(u: &mut Unstructured<'_>) -> arbitrary::Result<()> {
    round_trip(u, get_db)
}

#[test]
fn test_round_trip() {
    arbtest::builder().budget_ms(10_000).run(json_round_trip);
    let mut path = temp_dir();
    path.push("simuldb");
    remove_dir_all(path).expect("Failed to remove test directory");
}
