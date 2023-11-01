use std::{
    collections::{BTreeMap, BTreeSet, HashMap},
    error::Error,
    fmt::Debug,
};

use arbitrary::Unstructured;
use log::{debug, info};
use uuid::Uuid;

use crate::{
    db::{transfer, Database},
    Dataset, Session,
};

type Result<T> = std::result::Result<T, Box<dyn Error>>;

pub fn db_to_map<D>(x: &D) -> Result<BTreeMap<Session, BTreeSet<Dataset>>>
where
    D: Database,
    D::Error: Error + 'static,
{
    let mut map = BTreeMap::new();
    for session in x.get_sessions()? {
        map.insert(
            session.session().clone(),
            session.get_datasets()?.into_iter().collect(),
        );
    }
    Ok(map)
}

#[allow(clippy::type_complexity)]
pub fn db_equal<D>(
    a: &D,
    b: &D,
) -> Result<
    Option<(
        BTreeMap<Session, BTreeSet<Dataset>>,
        BTreeMap<Session, BTreeSet<Dataset>>,
    )>,
>
where
    D: Database,
    D::Error: 'static,
{
    let map_a = db_to_map(a)?;
    let map_b = db_to_map(b)?;
    let set_a: BTreeSet<_> = map_a
        .clone()
        .into_iter()
        .flat_map(|(session, set)| set.into_iter().map(move |x| (session.clone(), x)))
        .collect();
    let set_b: BTreeSet<_> = map_b
        .clone()
        .into_iter()
        .flat_map(|(session, set)| set.into_iter().map(move |x| (session.clone(), x)))
        .collect();
    debug!("{set_a:?} {set_b:?}");
    let res: Vec<_> = set_a
        .into_iter()
        .zip(set_b)
        .filter(|(a, b)| a != b)
        .collect();
    for (i, (a, b)) in res.iter().enumerate() {
        debug!("{i:6>}\n\t{a:?}\n\t{b:?}");
    }
    Ok(if res.is_empty() {
        None
    } else {
        Some((map_a, map_b))
    })
}

pub fn round_trip<F, D>(u: &mut Unstructured<'_>, mut f: F) -> arbitrary::Result<()>
where
    F: FnMut(Uuid) -> D,
    D: Database + Debug,
    D::Error: 'static,
{
    let data: HashMap<Session, BTreeSet<Dataset>> = u.arbitrary()?;

    debug!("Trying to save and load the following data: {:#?}", data);

    let uuid1 = Uuid::new_v4();

    // write data to db
    let mut db = f(uuid1);
    for (session, datasets) in &data {
        info!("Saving session {:?}", session);
        let mut sessiondb = db
            .add_session(session.clone())
            .expect("Failed to add session");
        for d in datasets.clone() {
            info!("Saving dataset {:?}", d);
            sessiondb.add_dataset(&d).expect("Failed to add dataset");
        }
    }

    // read data from_db
    info!("Loading db again");
    let new_db = f(uuid1);

    // compare dbs
    assert!(db_equal(&db, &new_db)
        .expect("Failed to compare databases")
        .is_none());

    // transfer to other db
    let mut transfer_db = f(Uuid::new_v4());
    transfer(&new_db, &mut transfer_db).expect("Failed to transfer contents");

    // compare dbs
    assert!(db_equal(&new_db, &transfer_db)
        .expect("Failed to compare databases")
        .is_none());

    Ok(())
}
