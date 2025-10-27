# Task API - A simple web service for managing tasks.

from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []
# ВИПРАВЛЕНО: Pylint вимагає UPPER_CASE для глобальних констант
TASK_ID_COUNTER = 1

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    """
    Handle GET (read all tasks) and POST (create new task) requests.
    """
    global TASK_ID_COUNTER # Змінено з task_id_counter

    if request.method == 'POST':
        if not request.json or 'title' not in request.json:
            return jsonify({"error": "Missing title"}), 400

        new_task = {
            'id': TASK_ID_COUNTER, # Змінено з task_id_counter
            'title': request.json['title'],
            'done': request.json.get('done', False)
        }
        tasks.append(new_task)
        TASK_ID_COUNTER += 1 # Змінено з task_id_counter
        return jsonify(new_task), 201

    return jsonify(tasks), 200

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update an existing task (by ID) using PUT request.
    """
    task = None
    for t in tasks:
        if t['id'] == task_id:
            task = t
            break

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    if not request.json:
        return jsonify({"error": "No data provided"}), 400

    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])

    return jsonify(task), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
