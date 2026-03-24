use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

pub type TodoList = HashMap<String, Todo>;
pub type SharedTodoList = Arc<RwLock<TodoList>>;

#[derive(Serialize, Deserialize, Clone)]
pub struct NewTodo {
    task: String,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Todo {
    task: String,
    #[serde(default)]
    pub done: bool,
}

impl Todo {
    pub fn new(task: String) -> Self {
        Self { task, done: false }
    }
}

impl From<NewTodo> for Todo {
    fn from(item: NewTodo) -> Self {
        Self {
            task: item.task,
            done: false,
        }
    }
}
