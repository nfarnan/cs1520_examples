#!/bin/bash

num=1

msg () {
  echo "#=== $num: $1 ==="
  ((num=num+1))
}

msg "GET all"
curlie $1/todos
msg "GET todo1"
curlie $1/todos/todo1
msg "GET (missing) todo4"
curlie $1/todos/todo4
msg "POST new todo"
curlie POST $1/todos task="rewrite in rust"
msg "GET all"
curlie $1/todos
msg "PUT new todo that's done"
curlie PUT $1/todos/todo5 task="...well start it at least" done:=true
msg "GET all"
curlie $1/todos
msg "PUT new todo that's not done"
curlie PUT $1/todos/todo6 task="impress students"
msg "GET all"
curlie $1/todos
msg "POST to /count"
curlie POST $1/count
msg "POST to /count with type=done"
curlie POST $1/count type=done
msg "POST to /count with type=not_done"
curlie POST $1/count type=not_done
msg "POST to /mark to set todo5 to not done"
curlie POST $1/mark id=todo5 status:=false
msg "GET all"
curlie $1/todos
msg "DELETE todo5"
curlie DELETE $1/todos/todo5
msg "GET all"
curlie $1/todos
msg "POST to /mark to set todo6 to done"
curlie POST $1/mark id=todo6 status:=true
msg "GET all"
curlie $1/todos
