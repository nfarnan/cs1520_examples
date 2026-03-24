use crate::util::{SharedTodoList, TodoList};
use axum::{extract::State, http::StatusCode, Json};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

pub async fn count(
    State(todo_list): State<SharedTodoList>,
    Json(args): Json<HashMap<String, String>>,
) -> Json<Count> {
    if let Some(t) = args.get("type") {
        if t == "done" || t == "not_done" {
            let t = t == "done";
            return Json(Count::new(
                todo_list
                    .read()
                    .unwrap()
                    .values()
                    .filter(|x| x.done == t)
                    .count(),
            ));
        }
    }

    Json(Count::new(todo_list.read().unwrap().len()))
}

pub async fn mark(
    State(todo_list): State<SharedTodoList>,
    Json(to_mark): Json<ToMark>,
) -> Result<(StatusCode, Json<TodoList>), StatusCode> {
    let mut todo_list = todo_list.write().unwrap();
    let mut todo = todo_list
        .get_mut(&to_mark.id)
        .ok_or(StatusCode::NOT_FOUND)?;

    todo.done = to_mark.status;

    Ok((
        StatusCode::OK,
        Json(HashMap::from([(to_mark.id, todo.clone())])),
    ))
}

#[derive(Serialize)]
pub struct Count {
    count: usize,
}

impl Count {
    fn new(count: usize) -> Self {
        Self { count }
    }
}

#[derive(Deserialize)]
pub struct ToMark {
    id: String,
    status: bool,
}
