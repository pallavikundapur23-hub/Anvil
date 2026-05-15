from flask import Flask, jsonify, request
from database import tasks

app = Flask(__name__)

# GET all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# ADD task
@app.route("/tasks", methods=["POST"])
def add_task():

    data = request.get_json()

    # BUG 1
    # wrong key name "task" instead of "title"

    new_task = {
        "id": len(tasks) + 1,
        "title": data["task"]
    }

    tasks.append(new_task)

    return jsonify(new_task), 201


# DELETE task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    # BUG 2
    # typo variable name "tasls"

    global tasls

    tasks = [t for t in tasks if t["id"] != task_id]

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True)