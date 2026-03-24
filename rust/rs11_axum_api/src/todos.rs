use crate::util::{NewTodo, SharedTodoList, TodoList};
use axum::{extract::State, http::StatusCode, Json};
use std::collections::HashMap;

pub async fn get(State(todo_list): State<SharedTodoList>) -> (StatusCode, Json<TodoList>) {
    (StatusCode::OK, Json(todo_list.read().unwrap().clone()))
}

pub async fn post(
    State(todo_list): State<SharedTodoList>,
    Json(body): Json<NewTodo>,
) -> (StatusCode, Json<TodoList>) {
    let new_id = todo_list
        .read()
        .unwrap()
        .keys()
        .max()
        .unwrap_or(&String::from("todo0"))
        .chars()
        .skip(4)
        .collect::<String>()
        .parse::<i32>()
        .unwrap()
        + 1;

    let new_id = format!("todo{new_id}");
    todo_list
        .write()
        .unwrap()
        .insert(new_id.clone(), body.clone().into());

    (
        StatusCode::CREATED,
        Json(HashMap::from([(new_id, body.into())])),
    )
}
