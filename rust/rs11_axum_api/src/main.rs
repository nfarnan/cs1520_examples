use axum::{
    http::{HeaderValue, Method},
    routing::{get, post},
    Router,
};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};
use tower_http::cors::CorsLayer;
use tower_http::trace::TraceLayer;

mod rpc;
mod todo;
mod todos;
mod util;

use util::Todo;

#[tokio::main]
async fn main() {
    // Init logging
    tracing_subscriber::fmt::init();

    // Setup "database"
    let mut todo1 = Todo::new(String::from("build an API"));
    todo1.done = true;
    let todo_list = HashMap::from([
        (String::from("todo1"), todo1),
        (String::from("todo2"), Todo::new(String::from("?????"))),
        (String::from("todo3"), Todo::new(String::from("profit!"))),
    ]);

    // Build app
    let app = Router::new()
        .route("/todos", get(todos::get).post(todos::post))
        .route(
            "/todos/{todo}",
            get(todo::get).put(todo::put).delete(todo::delete),
        )
        .route("/count", post(rpc::count))
        .route("/mark", post(rpc::mark))
        .with_state(Arc::new(RwLock::new(todo_list)))
        .layer(
            CorsLayer::new()
                .allow_origin("http://localhost:5173".parse::<HeaderValue>().unwrap())
                .allow_methods(vec![Method::GET, Method::POST])
                .allow_headers(vec![axum::http::header::CONTENT_TYPE]),
        )
        .layer(TraceLayer::new_for_http());

    // Bind to address/port and run
    let listener = tokio::net::TcpListener::bind("localhost:5000")
        .await
        .unwrap();
    tracing::debug!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}
