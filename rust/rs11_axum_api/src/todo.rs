use crate::util::{SharedTodoList, Todo};
use axum::{
    extract::{Path, State},
    http::StatusCode,
    Json,
};

pub async fn get(
    Path(todo_id): Path<String>,
    State(todo_list): State<SharedTodoList>,
) -> Result<(StatusCode, Json<Todo>), StatusCode> {
    let todo_list = todo_list.read().unwrap();
    let todo = todo_list.get(&todo_id).ok_or(StatusCode::NOT_FOUND)?;
    Ok((StatusCode::OK, Json(todo.clone())))
}

pub async fn delete(
    Path(todo_id): Path<String>,
    State(todo_list): State<SharedTodoList>,
) -> StatusCode {
    match todo_list.write().unwrap().remove(&todo_id) {
        Some(_) => StatusCode::NO_CONTENT,
        None => StatusCode::NOT_FOUND,
    }
}

pub async fn put(
    Path(todo_id): Path<String>,
    State(todo_list): State<SharedTodoList>,
    Json(body): Json<Todo>,
) -> (StatusCode, Json<Todo>) {
    match todo_list.write().unwrap().insert(todo_id, body.clone()) {
        Some(_) => (StatusCode::OK, Json(body)),
        None => (StatusCode::CREATED, Json(body)),
    }
}
