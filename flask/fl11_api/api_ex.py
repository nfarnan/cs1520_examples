from flask import Flask, request
from werkzeug.exceptions import abort

app = Flask(__name__)

TODOS = {
    "todo1": {"task": "build an API", "done": True},
    "todo2": {"task": "?????", "done": False},
    "todo3": {"task": "profit!", "done": False},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404)


# RESTful access to the list of todos
@app.route("/todos", methods=["GET"])
def list_get():
    # Flask automatically jsonify's dictionaries
    return TODOS


@app.route("/todos", methods=["POST"])
def list_post():
    # Get json request data
    req_data = request.get_json()

    # Calculate next available id value
    todo_id = int(max(TODOS.keys()).lstrip("todo")) + 1
    todo_id = f"todo{todo_id}"

    # Add todo item
    TODOS[todo_id] = {"task": req_data["task"], "done": False}

    # If returning a tuple, second arg can be a response code
    return {todo_id: TODOS[todo_id]}, 201


# RESTful access to individual todo resources
@app.route("/todos/<todo_id>", methods=["GET"])
def single_get(todo_id=None):
    # Check that the requested resource actually exists
    abort_if_todo_doesnt_exist(todo_id)

    return TODOS[todo_id]


@app.route("/todos/<todo_id>", methods=["DELETE"])
def single_delete(todo_id=None):
    abort_if_todo_doesnt_exist(todo_id)

    del TODOS[todo_id]

    return "", 204


@app.route("/todos/<todo_id>", methods=["PUT"])
def single_put(todo_id=None):
    req_data = request.get_json()

    if not req_data or "task" not in req_data:
        abort(400)

    new_todo = {"task": req_data["task"], "done": False}

    if "done" in req_data and req_data["done"]:
        new_todo["done"] = True

    # Report appropriate status code
    if todo_id in TODOS:
        # Successful update
        status_code = 200
    else:
        # Created new resource
        status_code = 201

    TODOS[todo_id] = new_todo

    return TODOS[todo_id], status_code


# RPC function to keep track of todos
@app.route("/count", methods=["POST"])
def counter():
    # Looking for "type" argument in request to be either "done" or "not_done"
    # If neither are found, return the count of all todos
    req_data = request.get_json()
    if req_data and "type" in req_data:
        if req_data["type"] == "done":
            return {"count": len([tid for tid, todo in TODOS.items() if todo["done"]])}
        elif req_data["type"] == "not_done":
            return {
                "count": len([tid for tid, todo in TODOS.items() if not todo["done"]])
            }

    return {"count": len(TODOS)}


# RPC function to mark items as done
@app.route("/mark", methods=["POST"])
def marker():
    # Looking for two arguments:
    # "id": the todo id to update
    # "status": either true or false for "done"/"not_done"
    req_data = request.get_json()
    if not req_data or "id" not in req_data or "status" not in req_data:
        abort(400)

    todo_id = req_data["id"]
    abort_if_todo_doesnt_exist(todo_id)

    if req_data["status"]:
        TODOS[todo_id]["done"] = True
    else:
        TODOS[todo_id]["done"] = False

    return {todo_id: TODOS[todo_id]}, 200
