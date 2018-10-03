#!flask/bin/python
from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)

tasks = [
    {
        'id' : 1,
        'title' : u'Buy groceries',
        'description' : u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done' : False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


def send_error_not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)


def send_error_bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task' : task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_tasks(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return send_error_not_found()
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):

    task = [task for task in tasks if task['id'] == task_id]

    if len(task) == 0:
        return send_error_not_found()
    if not request.json:
        return send_error_bad_request()
    if 'title' in request.json and type(request.json['title']) is not str:
        return send_error_bad_request()
    if 'description' in request.json and type(request.json['description']) is not str:
        return send_error_bad_request()
    if 'done' in request.json and type(request.json['done'] is not bool):
        return send_error_bad_request()

    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    task = [task for task in tasks if task['id'] == task_id]

    if len(task) == 0:
        return send_error_not_found()

    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)