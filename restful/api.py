#!/usr/bin/python

from flask import Flask, request
from flask_restful import reqparse, abort, Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


todos = {
	'todo1': {'task': 'build an API'},
	'todo2': {'task': '????'},
	'todo3': {'task': 'profit!'},
}

def abort_if_todo_doesnt_exist(todo_id):
	if todo_id not in todos:
		abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


class Todo(Resource):
	# curl -X GET http://localhost:5000/todos/todo2
	def get(self, todo_id):
		abort_if_todo_doesnt_exist(todo_id)
		return todos[todo_id]

	# curl -X PUT -v http://localhost:5000/todos/todo3 -d "task= something diffrent"
	def put(self, todo_id):
		args = parser.parse_args()
		task = {'task': args['task']}
		todos[todo_id] = task
		return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
	# curl -X GET http://localhost:5000/todos
    def get(self):
        return todos

	# curl -X POST -v http://localhost:5000/todos -d "task= something new"
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(todos.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        todos[todo_id] = {'task': args['task']}
        return todos[todo_id], 201


api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(TodoList, '/todos')
api.add_resource(HelloWorld, '/', '/hello')

if __name__ == '__main__':
    app.run(debug=True)

